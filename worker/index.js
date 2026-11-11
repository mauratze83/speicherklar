/* Speicherklar Pro – Kauf und Freischaltung über Stripe (Managed Payments, Stripe ist Merchant of Record).
   Läuft als Cloudflare Worker. Der Lizenzschlüssel enthält die Stripe-Checkout-ID und eine Signatur.

   POST /checkout  {}                  → { url }            Bezahlseite (Einführungs- oder Normalpreis nach Datum)
   POST /verify    { session, device } → { key, email }     nach dem Kauf: bezahlt? Schlüssel ausgeben, Gerät eintragen, Mail auslösen
   POST /validate  { key, device }     → { ok, email, until } Schlüssel prüfen: Signatur, bezahlt, nicht erstattet, nicht gesperrt, nicht abgelaufen, Gerätelimit
   POST /recover   { email }           → { ok }             Schlüssel noch einmal per Mail an diese Adresse (Antwort verrät nichts)

   Laufzeit: ACCESS_DAYS Tage ab der ersten Freischaltung (activatedAt, gesetzt beim ersten /verify oder /validate).
   Danach antwortet /validate mit 410 { error: "expired", until }. Der PDF-Bericht des Käufers bleibt davon unberührt.

   KV LICENSES:  "lic:<checkout-id>" → { devices: [..], email: "m•••@gmx.de", mailed: true, blocked: false,
                                         activatedAt: "2026-12-03T10:00:00.000Z", until: "2027-06-30" (optional) }
                 "rec:<email>:<tag>" → Zähler gegen Missbrauch von /recover
   Sperren: im Cloudflare-Dashboard unter Workers KV den Eintrag lic:<checkout-id> öffnen und "blocked": true setzen.
   Verlängern: dort "until": "JJJJ-MM-TT" setzen (letzter gültiger Tag); das ersetzt das berechnete Ende.

   Variablen (wrangler.toml): SITE, ALLOWED_ORIGINS, PRICE_INTRO, PRICE_REGULAR, INTRO_UNTIL, STRIPE_VERSION, MAX_DEVICES, ACCESS_DAYS, ML_GROUP_BUYERS, ML_GROUP_RESEND
   Geheimnisse: STRIPE_SECRET_KEY, LICENSE_SECRET, MAILERLITE_API_KEY (ohne diesen wird keine Mail verschickt) */

const enc = new TextEncoder();

function cors(req, env) {
  const origin = req.headers.get("Origin") || "";
  const allowed = (env.ALLOWED_ORIGINS || env.SITE).split(",").map((s) => s.trim());
  return {
    "Access-Control-Allow-Origin": allowed.includes(origin) ? origin : allowed[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}
const json = (req, env, body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...cors(req, env) } });

async function stripe(env, method, path, params) {
  const headers = { Authorization: `Bearer ${env.STRIPE_SECRET_KEY}` };
  if (env.STRIPE_VERSION) headers["Stripe-Version"] = env.STRIPE_VERSION;
  let url = `https://api.stripe.com/v1/${path}`, body;
  if (params) {
    const form = new URLSearchParams(params).toString();
    if (method === "GET") url += `?${form}`;
    else { body = form; headers["Content-Type"] = "application/x-www-form-urlencoded"; }
  }
  const r = await fetch(url, { method, headers, body });
  const data = await r.json();
  if (!r.ok) throw Object.assign(new Error(data.error?.message || `Stripe ${r.status}`), { status: r.status });
  return data;
}

async function sign(env, text) {
  const key = await crypto.subtle.importKey("raw", enc.encode(env.LICENSE_SECRET), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(text)));
  return btoa(String.fromCharCode(...mac.slice(0, 12))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
const makeKey = async (env, sessionId) => `SK.${sessionId}.${await sign(env, sessionId)}`;
// Freischlüssel (z. B. Familie und Freunde): gelten ohne Kauf, ohne Gerätelimit und ohne Ablauf.
// Im Repo steht nur der SHA-256-Hash (FREE_KEYS in wrangler.toml). Sperren: Hash dort löschen und pushen.
async function isFreeKey(env, key) {
  const list = String(env.FREE_KEYS || "").split(",").map((x) => x.trim()).filter(Boolean);
  if (!list.length || !key) return false;
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(String(key).trim()));
  const hex = [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
  return list.includes(hex);
}
async function parseKey(env, key) {
  const m = /^SK\.(cs_[A-Za-z0-9_]+)\.([A-Za-z0-9_-]{16})$/.exec(String(key || "").trim());
  if (!m) return null;
  return (await sign(env, m[1])) === m[2] ? m[1] : null;
}

// m•••@gmx.de: erkennbar für den Käufer, für andere nicht vollständig lesbar
function maskEmail(e) {
  const [u, d] = String(e || "").split("@");
  return u && d ? `${u[0]}•••@${d}` : "";
}
const validDevice = (d) => /^[A-Za-z0-9-]{8,64}$/.test(String(d || ""));

// Bezahlt und nicht erstattet? Liefert auch die Käufer-Adresse.
async function paidSession(env, id) {
  let s;
  try { s = await stripe(env, "GET", `checkout/sessions/${encodeURIComponent(id)}`, { "expand[]": "payment_intent.latest_charge" }); }
  catch (e) { if (e.status === 404) return { ok: false, reason: "unknown" }; throw e; }
  if (s.payment_status !== "paid") return { ok: false, reason: "unpaid" };
  const charge = s.payment_intent && s.payment_intent.latest_charge;
  if (charge && charge.refunded) return { ok: false, reason: "refunded" };
  return { ok: true, email: (s.customer_details && s.customer_details.email) || "" };
}

async function getLic(env, id) {
  if (!env.LICENSES) return { devices: [] };
  return (await env.LICENSES.get(`lic:${id}`, "json")) || { devices: [] };
}
const putLic = (env, id, lic) => env.LICENSES ? env.LICENSES.put(`lic:${id}`, JSON.stringify(lic)) : null;

// Gerät eintragen, solange das Limit nicht erreicht ist
function admit(env, lic, device) {
  const max = Number(env.MAX_DEVICES || 3);
  if (lic.blocked) return "blocked";
  if (!validDevice(device) || lic.devices.includes(device)) return "ok";
  if (lic.devices.length >= max) return "limit";
  lic.devices.push(device); lic.changed = true;
  return "ok";
}

// MailerLite: Käufer mit Schlüssel in eine Gruppe eintragen; die Automatisierung dort verschickt die Mail
async function mailKey(env, email, key, group) {
  if (!env.MAILERLITE_API_KEY || !group || !email) return false;
  const h = { Authorization: `Bearer ${env.MAILERLITE_API_KEY}`, "Content-Type": "application/json", Accept: "application/json" };
  const r = await fetch("https://connect.mailerlite.com/api/subscribers", { method: "POST", headers: h, body: JSON.stringify({ email, fields: { lizenz: key } }) });
  if (!r.ok) return false;
  const sub = (await r.json()).data;
  // Erst austragen, dann eintragen: so startet die Automatisierung auch beim zweiten Mal
  await fetch(`https://connect.mailerlite.com/api/subscribers/${sub.id}/groups/${group}`, { method: "DELETE", headers: h });
  const g = await fetch(`https://connect.mailerlite.com/api/subscribers/${sub.id}/groups/${group}`, { method: "POST", headers: h });
  return g.ok;
}

const today = () => new Date().toISOString().slice(0, 10);

// Laufzeit ab der ersten Freischaltung. Setzt activatedAt beim ersten Aufruf und liefert den letzten gültigen Tag (JJJJ-MM-TT).
function access(env, lic) {
  if (!lic.activatedAt) { lic.activatedAt = new Date().toISOString(); lic.changed = true; }
  if (lic.until) return lic.until;
  const days = Number(env.ACCESS_DAYS || 90);
  return new Date(Date.parse(lic.activatedAt) + (days - 1) * 86400000).toISOString().slice(0, 10);
}

export default {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(req, env) });
    if (req.method !== "POST") return json(req, env, { error: "Nur POST" }, 405);
    const path = new URL(req.url).pathname;
    let body = {};
    try { body = await req.json(); } catch (e) {}
    try {
      if (path === "/checkout") {
        const price = env.PRICE_INTRO && env.INTRO_UNTIL && today() <= env.INTRO_UNTIL ? env.PRICE_INTRO : env.PRICE_REGULAR;
        const s = await stripe(env, "POST", "checkout/sessions", {
          mode: "payment",
          "line_items[0][price]": price,
          "line_items[0][quantity]": "1",
          "managed_payments[enabled]": "true",
          locale: "de",
          success_url: `${env.SITE}/pro/?kauf={CHECKOUT_SESSION_ID}`,
          cancel_url: `${env.SITE}/pro/`,
        });
        return json(req, env, { url: s.url });
      }

      if (path === "/verify") {
        const id = String(body.session || "");
        if (!/^cs_[A-Za-z0-9_]+$/.test(id)) return json(req, env, { error: "Ungültige Kauf-ID" }, 400);
        const p = await paidSession(env, id);
        if (!p.ok) {
          const msg = { unknown: "Diesen Kauf finden wir nicht.", refunded: "Dieser Kauf wurde erstattet.", unpaid: "Die Zahlung ist noch nicht abgeschlossen." }[p.reason];
          return json(req, env, { error: msg }, p.reason === "unknown" ? 404 : 402);
        }
        const key = await makeKey(env, id), lic = await getLic(env, id);
        const st = admit(env, lic, body.device);
        const until = access(env, lic);
        if (!lic.email) { lic.email = maskEmail(p.email); lic.changed = true; }
        if (!lic.mailed && await mailKey(env, p.email, key, env.ML_GROUP_BUYERS)) { lic.mailed = true; lic.changed = true; }
        if (lic.changed) { delete lic.changed; await putLic(env, id, lic); }
        if (st === "blocked") return json(req, env, { error: "Dieser Schlüssel ist gesperrt." }, 410);
        if (today() > until) return json(req, env, { error: "Dieser Schlüssel ist abgelaufen.", until }, 410);
        return json(req, env, { key, email: lic.email, mailed: !!lic.mailed, limit: st === "limit", until });
      }

      if (path === "/validate") {
        if (await isFreeKey(env, body.key)) return json(req, env, { ok: true, email: "" });
        const id = await parseKey(env, body.key);
        if (!id) return json(req, env, { ok: false, error: "unknown" }, 404);
        const p = await paidSession(env, id);
        if (!p.ok) return json(req, env, { ok: false, error: p.reason }, p.reason === "unknown" ? 404 : 410);
        const lic = await getLic(env, id);
        const until = access(env, lic);
        // Abgelaufen: kein neues Gerät mehr eintragen
        const st = today() > until ? (lic.blocked ? "blocked" : "expired") : admit(env, lic, body.device);
        if (!lic.email) { lic.email = maskEmail(p.email); lic.changed = true; }
        if (lic.changed) { delete lic.changed; await putLic(env, id, lic); }
        if (st === "blocked") return json(req, env, { ok: false, error: "blocked" }, 410);
        if (st === "expired") return json(req, env, { ok: false, error: "expired", until }, 410);
        if (st === "limit") return json(req, env, { ok: false, error: "limit", max: Number(env.MAX_DEVICES || 3) }, 409);
        return json(req, env, { ok: true, email: lic.email, until });
      }

      if (path === "/recover") {
        const email = String(body.email || "").trim().toLowerCase();
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 200) return json(req, env, { error: "Bitte gib eine gültige E-Mail-Adresse ein." }, 400);
        // höchstens 3 Anfragen pro Adresse und Tag
        if (env.LICENSES) {
          const rk = `rec:${email}:${today()}`, n = Number((await env.LICENSES.get(rk)) || 0);
          if (n >= 3) return json(req, env, { ok: true });
          await env.LICENSES.put(rk, String(n + 1), { expirationTtl: 172800 });
        }
        const list = await stripe(env, "GET", "checkout/sessions", { "customer_details[email]": email, status: "complete", limit: "10" });
        const paid = (list.data || []).filter((s) => s.payment_status === "paid");
        if (paid.length) await mailKey(env, email, await makeKey(env, paid[0].id), env.ML_GROUP_RESEND || env.ML_GROUP_BUYERS);
        return json(req, env, { ok: true });
      }

      return json(req, env, { error: "Unbekannter Pfad" }, 404);
    } catch (e) {
      return json(req, env, { error: "Stripe nicht erreichbar", detail: e.message }, 502);
    }
  },
};
