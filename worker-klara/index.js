/* Klara – KI-Hilfe auf speicherklar.de. Eigener Cloudflare Worker, getrennt vom Bezahl-Worker (worker/).

   GET  /status                                  → { on, grund? }      Ist Klara gerade da? (grund: "aus" | "budget")
   POST /start                                   → { aufgabe, bits }   Rechenaufgabe gegen Bots (Proof of Work)
   POST /session { aufgabe, nonce }              → { token }           Lösung prüfen, Gesprächs-Token für 30 Minuten
   POST /chat    { token, verlauf, seite, werte } → text/event-stream  Antwort von Claude als Stream:
        data: {"t":"text","v":"…"} · {"t":"knopf","ziel":"rechner|pro|mail|seite","text":"…","url":"…"} · {"t":"ende"} · {"t":"fehler","grund":"…"}

   Schutz: nur Origins aus ALLOWED_ORIGINS, Rechenaufgabe vor jedem Gespräch, Token 30 Min., höchstens MAX_FRAGEN Fragen
   je Gespräch und 600 Zeichen je Frage, Rate-Limit je IP (Binding RL, 6/Minute) und MAX_PRO_TAG Fragen je IP und Tag (KV).
   Budget: Kosten jeder Antwort aus den Token-Angaben der API, Summe je Monat in KV "stat:JJJJ-MM". Ab BUDGET_USD ist Klara
   bis zum Monatsersten aus. Not-Aus: KV-Eintrag "cfg:aus" = "1" (Cloudflare → Workers KV → speicherklar-klara-STATS).

   Datenschutz: Gesprächsinhalte werden nicht gespeichert und nicht geloggt. In KV stehen nur Summen (Kosten, Anzahl Fragen,
   Themen-Kategorien, Knöpfe) und Tageszähler je IP-Hash (laufen nach 2 Tagen ab).

   Variablen (wrangler.toml): SITE, ALLOWED_ORIGINS, MODEL, MAX_TOKENS, BUDGET_USD, PREIS_*, MAX_FRAGEN, MAX_PRO_TAG, POW_BITS
   Geheimnis: ANTHROPIC_API_KEY (daraus wird auch der Schlüssel für die Signaturen abgeleitet) */

import { REGELN } from "./regeln.js";
import { WISSEN, POLITIK, PFADE } from "./wissen.js";

const enc = new TextEncoder();
export const THEMEN = ["eingaben", "ergebnis", "methodik", "speichergroesse", "pv-groesse", "wirtschaftlichkeit", "technik",
  "politik-eeg", "steuer-foerderung", "speicherklar-pro", "kauf-zugang", "beschwerde", "sonstiges", "fremdes-thema"];
const ZIELE = { rechner: "Rechner starten", pro: "Angebot prüfen", mail: "Frage an Manuel mailen", seite: "Seite öffnen" };
const TOKEN_MIN = 30;
const AUFGABE_MIN = 5;

// Werte aus dem Rechner, die das Widget mitschicken darf (alles andere wird ignoriert)
export const WERTE = {
  region: "Region (erste Ziffer der PLZ)", ausrichtung: "Ausrichtung", neigung: "Dachneigung", pv: "PV-Leistung",
  verbrauch: "Stromverbrauch pro Jahr", waermepumpe: "Wärmepumpe pro Jahr", eauto: "E-Auto pro Jahr", laden: "E-Auto lädt",
  speicher: "Speichergröße (nutzbar)", speicherpreis: "Speicherpreis inkl. Einbau", lebensdauer: "Lebensdauer", strompreis: "Strompreis",
  eeg: "Einspeiseregeln", einspeisung: "Einspeisevergütung",
  urteil: "Urteil", ersparnis: "Ersparnis pro Jahr", amortisation: "Amortisation", kosten: "Anschaffung", bilanz: "Bilanz nach Lebensdauer",
  autarkie: "Autarkie ohne/mit Speicher", beste: "Welche Größe rechnet sich am besten",
};

export const TOOLS = [
  { name: "verweis", description: "Zeigt unter der Antwort einen Knopf. Höchstens einmal pro Antwort, nach dem Text.",
    input_schema: { type: "object", properties: {
      ziel: { type: "string", enum: Object.keys(ZIELE) },
      pfad: { type: "string", description: "Nur bei ziel seite: Pfad genau wie in der Liste der Seiten, z. B. methodik.html" },
      text: { type: "string", description: "Knopftext, höchstens 4 Wörter" } }, required: ["ziel"] } },
  { name: "thema", description: "Anonyme Statistik: Kategorie der letzten Nutzerfrage. Bei jeder Antwort genau einmal, nach dem Text.",
    input_schema: { type: "object", properties: { kategorie: { type: "string", enum: THEMEN } }, required: ["kategorie"] } },
];

// ---------- Hilfen ----------
function cors(req, env) {
  const origin = req.headers.get("Origin") || "";
  const allowed = (env.ALLOWED_ORIGINS || env.SITE).split(",").map((s) => s.trim());
  return { "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0], "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type", "Access-Control-Max-Age": "86400", Vary: "Origin" };
}
const json = (req, env, body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...cors(req, env) } });
const b64u = (bytes) => btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const b64uText = (s) => b64u(enc.encode(s));
const unb64u = (s) => new TextDecoder().decode(Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0)));
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
const sha256 = async (s) => crypto.subtle.digest("SHA-256", enc.encode(s));

let _key, _keySrc;
async function hmacKey(env) {
  if (_key && _keySrc === env.ANTHROPIC_API_KEY) return _key;
  const raw = await sha256("klara-signatur:" + (env.ANTHROPIC_API_KEY || "ohne-schluessel"));
  _key = await crypto.subtle.importKey("raw", raw, { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
  _keySrc = env.ANTHROPIC_API_KEY;
  return _key;
}
async function sign(env, text) {
  return b64u(new Uint8Array(await crypto.subtle.sign("HMAC", await hmacKey(env), enc.encode(text))).slice(0, 16));
}
async function signed(env, obj) {
  const body = b64uText(JSON.stringify(obj));
  return `${body}.${await sign(env, body)}`;
}
export async function unsign(env, s) {
  if (typeof s !== "string" || s.length > 400) return null;
  const [body, sig] = s.split(".");
  if (!body || !sig || sig !== (await sign(env, body))) return null;
  try { return JSON.parse(unb64u(body)); } catch { return null; }
}
// Anzahl führender Null-Bits eines Hashes
export function nullBits(buf) {
  let n = 0;
  for (const b of new Uint8Array(buf)) { if (b === 0) { n += 8; continue; } n += Math.clz32(b) - 24; break; }
  return n;
}
const monat = (d = new Date()) => d.toISOString().slice(0, 7);
const tag = (d = new Date()) => d.toISOString().slice(0, 10);
const zahl = (v, d) => (Number.isFinite(+v) && v !== "" ? +v : d);

export function kosten(env, u) {
  return ((u.in || 0) * zahl(env.PREIS_IN, 0.1) + (u.cw || 0) * zahl(env.PREIS_CACHE_SCHREIBEN, 0.125) +
    (u.cr || 0) * zahl(env.PREIS_CACHE_LESEN, 0.01) + (u.out || 0) * zahl(env.PREIS_OUT, 0.5)) / 1e6;
}

async function stat(env) {
  if (!env.STATS) return { usd: 0 };
  return (await env.STATS.get("stat:" + monat(), "json")) || { usd: 0 };
}
async function zustand(env) {
  if (env.STATS && (await env.STATS.get("cfg:aus")) === "1") return { on: false, grund: "aus" };
  if (!env.ANTHROPIC_API_KEY) return { on: false, grund: "aus" };
  const s = await stat(env);
  if (s.usd >= zahl(env.BUDGET_USD, 10)) return { on: false, grund: "budget" };
  return { on: true };
}

async function zaehlen(env, usage, thema, knoepfe) {
  if (!env.STATS) return;
  try {
    const key = "stat:" + monat();
    const s = (await env.STATS.get(key, "json")) || { usd: 0 };
    s.usd = Math.round(((s.usd || 0) + kosten(env, usage)) * 1e6) / 1e6;
    s.fragen = (s.fragen || 0) + 1;
    s.tokens = s.tokens || { in: 0, cw: 0, cr: 0, out: 0 };
    for (const k of ["in", "cw", "cr", "out"]) s.tokens[k] += usage[k] || 0;
    s.themen = s.themen || {};
    if (thema) s.themen[thema] = (s.themen[thema] || 0) + 1;
    s.knoepfe = s.knoepfe || {};
    for (const k of knoepfe) s.knoepfe[k.ziel] = (s.knoepfe[k.ziel] || 0) + 1;
    await env.STATS.put(key, JSON.stringify(s), { expirationTtl: 400 * 86400 });
  } catch (e) { console.log("Statistik nicht gespeichert"); }
}

function sauber(v, max) {
  return String(v ?? "").replace(/[\u0000-\u001f<>`]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);
}

export function kontext(heute, seite, werte) {
  const d = heute.split("-").reverse().join(".");
  let k = `# Gerade\nHeute ist der ${d}. Der Nutzer ist auf der Seite ${sauber(seite, 100) || "/"} von speicherklar.de.`;
  if (werte && typeof werte === "object") {
    const z = Object.keys(WERTE).filter((key) => werte[key] !== undefined && werte[key] !== "").map((key) => `- ${WERTE[key]}: ${sauber(werte[key], 200)}`);
    if (z.length) k += "\nAktuelle Werte und Ergebnisse im Rechner auf dieser Seite (vom Rechner selbst angezeigt, nur wiedergeben und erklären, nicht neu rechnen):\n" + z.join("\n");
  }
  return k;
}

export function system(heute) {
  const pol = POLITIK.filter((e) => e.pruefenBis >= heute);
  const polText = pol.length
    ? pol.map((e) => `## ${e.thema}\nStand: ${e.stand}\nStatus: ${e.status}\nQuelle: ${e.quelle}\n${e.text}`).join("\n\n")
    : "(Zurzeit keine geprüften Einträge. Sag bei Politik-Fragen, dass du keinen geprüften Stand hast.)";
  const seiten = PFADE.map((p) => "- " + (p === "" ? "/ (Startseite)" : p)).join("\n");
  return `${REGELN}\n# Politik und Förderung\n${polText}\n\n# Seiten, auf die du mit verweis (ziel seite) zeigen kannst\n${seiten}\n\n# Dein Wissen (aus der Website, Stand der letzten Veröffentlichung)\n${WISSEN}`;
}

export function knopf(env, a) {
  if (!a || !ZIELE[a.ziel]) return null;
  const text = sauber(a.text, 40) || ZIELE[a.ziel];
  const site = (env.SITE || "https://speicherklar.de").replace(/\/$/, "") + "/";
  if (a.ziel === "rechner") return { ziel: "rechner", text, url: site + "#rechner" };
  if (a.ziel === "pro") return { ziel: "pro", text, url: site + "pro/" };
  if (a.ziel === "mail") return { ziel: "mail", text };
  const p = String(a.pfad || "").replace(/^https?:\/\/(www\.)?speicherklar\.de\//, "").replace(/^\//, "");
  if (!PFADE.includes(p)) return null;
  return { ziel: "seite", text, url: site + p };
}

export function pruefeVerlauf(env, verlauf) {
  if (!Array.isArray(verlauf) || verlauf.length < 1 || verlauf.length > 2 * zahl(env.MAX_FRAGEN, 10)) return "verlauf";
  const msgs = [];
  for (const m of verlauf) {
    if (!m || (m.rolle !== "ich" && m.rolle !== "klara") || typeof m.text !== "string") return "verlauf";
    const t = m.text.trim();
    if (!t) return "verlauf";
    if (m.rolle === "ich" && t.length > 600) return "lang";
    msgs.push({ role: m.rolle === "ich" ? "user" : "assistant", content: t.slice(0, 3000) });
  }
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  if (!msgs.length || msgs[msgs.length - 1].role !== "user") return "verlauf";
  for (let i = 1; i < msgs.length; i++) if (msgs[i].role === msgs[i - 1].role) return "verlauf";
  if (msgs.filter((m) => m.role === "user").length > zahl(env.MAX_FRAGEN, 10)) return "genug";
  return msgs;
}

// ---------- Endpunkte ----------
async function start(req, env) {
  const aufgabe = await signed(env, { ts: Date.now(), r: b64u(crypto.getRandomValues(new Uint8Array(9))) });
  return json(req, env, { aufgabe, bits: zahl(env.POW_BITS, 16) });
}

async function session(req, env, body) {
  const a = await unsign(env, body.aufgabe);
  if (!a || Date.now() - a.ts > AUFGABE_MIN * 60000) return json(req, env, { error: "aufgabe" }, 400);
  const nonce = String(body.nonce ?? "").slice(0, 20);
  if (nullBits(await sha256(body.aufgabe + ":" + nonce)) < zahl(env.POW_BITS, 16)) return json(req, env, { error: "aufgabe" }, 400);
  const token = await signed(env, { sid: b64u(crypto.getRandomValues(new Uint8Array(9))), exp: Date.now() + TOKEN_MIN * 60000 });
  return json(req, env, { token });
}

async function grenzen(req, env) {
  const ip = req.headers.get("CF-Connecting-IP") || "unbekannt";
  const ipHash = (await sign(env, "ip|" + tag() + "|" + ip)).slice(0, 16);
  if (env.RL) {
    const { success } = await env.RL.limit({ key: ipHash });
    if (!success) return "minute";
  }
  if (env.STATS) {
    const key = `ip:${ipHash}:${tag()}`;
    const n = +(await env.STATS.get(key)) || 0;
    if (n >= zahl(env.MAX_PRO_TAG, 40)) return "tag";
    await env.STATS.put(key, String(n + 1), { expirationTtl: 2 * 86400 });
  }
  return null;
}

async function chat(req, env, ctx, body) {
  const t = await unsign(env, body.token);
  if (!t || !t.exp || Date.now() > t.exp) return json(req, env, { error: "token" }, 401);
  const z = await zustand(env);
  if (!z.on) return json(req, env, { error: "pause", grund: z.grund }, 503);
  const msgs = pruefeVerlauf(env, body.verlauf);
  if (typeof msgs === "string") return json(req, env, { error: msgs }, 400);
  const g = await grenzen(req, env);
  if (g) return json(req, env, { error: "langsam", grund: g }, 429);

  const heute = tag();
  const payload = {
    model: env.MODEL || "claude-haiku-5-5",
    max_tokens: zahl(env.MAX_TOKENS, 600),
    // Haiku 5.5 denkt sonst standardmäßig nach; das zählt gegen max_tokens und schneidet Antworten ab
    thinking: { type: "disabled" },
    stream: true,
    system: [
      { type: "text", text: system(heute), cache_control: { type: "ephemeral" } },
      { type: "text", text: kontext(heute, body.seite, body.werte) },
    ],
    tools: TOOLS,
    tool_choice: { type: "auto" },
    messages: msgs,
  };

  const { readable, writable } = new TransformStream();
  const w = writable.getWriter();
  const send = (o) => w.write(enc.encode(`data: ${JSON.stringify(o)}\n\n`));
  ctx.waitUntil((async () => {
    const usage = { in: 0, cw: 0, cr: 0, out: 0 };
    const tools = {};
    let thema = null, stop = null;
    const knoepfe = [];
    try {
      const r = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!r.ok) {
        console.log("Claude API", r.status);
        await send({ t: "fehler", grund: r.status === 429 || r.status === 529 ? "voll" : "api" });
        return;
      }
      const reader = r.body.pipeThrough(new TextDecoderStream()).getReader();
      let buf = "";
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += value;
        let i;
        while ((i = buf.indexOf("\n\n")) >= 0) {
          const ev = buf.slice(0, i);
          buf = buf.slice(i + 2);
          const line = ev.split("\n").find((l) => l.startsWith("data:"));
          if (!line) continue;
          let d;
          try { d = JSON.parse(line.slice(5)); } catch { continue; }
          if (d.type === "message_start" && d.message?.usage) {
            const u = d.message.usage;
            usage.in = u.input_tokens || 0; usage.cw = u.cache_creation_input_tokens || 0;
            usage.cr = u.cache_read_input_tokens || 0; usage.out = u.output_tokens || 0;
          } else if (d.type === "content_block_start" && d.content_block?.type === "tool_use") {
            tools[d.index] = { name: d.content_block.name, json: "" };
          } else if (d.type === "content_block_delta") {
            if (d.delta?.type === "text_delta") await send({ t: "text", v: d.delta.text });
            else if (d.delta?.type === "input_json_delta" && tools[d.index]) tools[d.index].json += d.delta.partial_json;
          } else if (d.type === "message_delta") {
            if (d.usage?.output_tokens != null) usage.out = d.usage.output_tokens;
            if (d.delta?.stop_reason) stop = d.delta.stop_reason;
          } else if (d.type === "error") {
            throw new Error("stream");
          }
        }
      }
      for (const tl of Object.values(tools)) {
        let a;
        try { a = JSON.parse(tl.json || "{}"); } catch { continue; }
        if (tl.name === "verweis" && !knoepfe.length) { const k = knopf(env, a); if (k) knoepfe.push(k); }
        if (tl.name === "thema" && THEMEN.includes(a.kategorie)) thema = a.kategorie;
      }
      for (const k of knoepfe) await send({ t: "knopf", ...k });
      if (stop === "max_tokens") console.log("Antwort bei max_tokens abgeschnitten");
      await send({ t: "ende", stop });
    } catch (e) {
      console.log("Antwort abgebrochen");
      try { await send({ t: "fehler", grund: "api" }); } catch {}
    } finally {
      try { await w.close(); } catch {}
      await zaehlen(env, usage, thema, knoepfe);
    }
  })());
  return new Response(readable, { headers: { "Content-Type": "text/event-stream; charset=utf-8", "Cache-Control": "no-store", ...cors(req, env) } });
}

export default {
  async fetch(req, env, ctx) {
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(req, env) });
    const allowed = (env.ALLOWED_ORIGINS || env.SITE).split(",").map((s) => s.trim());
    if (!allowed.includes(req.headers.get("Origin") || "")) return json(req, env, { error: "origin" }, 403);
    const path = new URL(req.url).pathname;
    try {
      if (req.method === "GET" && path === "/status") return json(req, env, await zustand(env));
      if (req.method !== "POST") return json(req, env, { error: "methode" }, 405);
      const len = +req.headers.get("Content-Length") || 0;
      if (len > 40000) return json(req, env, { error: "gross" }, 413);
      const text = await req.text();
      if (text.length > 40000) return json(req, env, { error: "gross" }, 413);
      let body = {};
      try { body = text ? JSON.parse(text) : {}; } catch { return json(req, env, { error: "json" }, 400); }
      if (path === "/start") return start(req, env);
      if (path === "/session") return session(req, env, body);
      if (path === "/chat") return chat(req, env, ctx, body);
      return json(req, env, { error: "unbekannt" }, 404);
    } catch (e) {
      console.log("Fehler", e && e.message);
      return json(req, env, { error: "server" }, 500);
    }
  },
};
