/* Speicherklar Pro – Kauf und Freischaltung über Stripe (Managed Payments, Stripe ist Merchant of Record).
   Läuft als Cloudflare Worker. Speichert nichts: Der Lizenzschlüssel enthält die Stripe-Checkout-ID und eine Signatur.

   POST /checkout  {}            → { url }   Bezahlseite von Stripe (Einführungs- oder Normalpreis nach Datum)
   POST /verify    { session }   → { key }   nach dem Kauf: bezahlt? dann Schlüssel ausgeben
   POST /validate  { key }       → { ok }    Schlüssel prüfen (Signatur, bezahlt, nicht erstattet)

   Variablen (wrangler.toml): SITE, ALLOWED_ORIGINS, PRICE_INTRO, PRICE_REGULAR, INTRO_UNTIL, STRIPE_VERSION
   Geheimnisse (wrangler secret / GitHub Actions): STRIPE_SECRET_KEY, LICENSE_SECRET */

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
async function parseKey(env, key) {
  const m = /^SK\.(cs_[A-Za-z0-9_]+)\.([A-Za-z0-9_-]{16})$/.exec(String(key || "").trim());
  if (!m) return null;
  return (await sign(env, m[1])) === m[2] ? m[1] : null;
}

// Bezahlt und nicht (vollständig) erstattet?
async function paidSession(env, id) {
  const s = await stripe(env, "GET", `checkout/sessions/${encodeURIComponent(id)}`, { "expand[]": "payment_intent.latest_charge" });
  if (s.payment_status !== "paid") return { ok: false, reason: "unpaid" };
  const charge = s.payment_intent && s.payment_intent.latest_charge;
  if (charge && charge.refunded) return { ok: false, reason: "refunded" };
  return { ok: true };
}

const today = () => new Date().toISOString().slice(0, 10);

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
        if (!p.ok) return json(req, env, { error: p.reason === "refunded" ? "Dieser Kauf wurde erstattet." : "Die Zahlung ist noch nicht abgeschlossen." }, 402);
        return json(req, env, { key: await makeKey(env, id) });
      }
      if (path === "/validate") {
        const id = await parseKey(env, body.key);
        if (!id) return json(req, env, { ok: false, error: "unknown" }, 404);
        const p = await paidSession(env, id);
        return json(req, env, p.ok ? { ok: true } : { ok: false, error: p.reason }, p.ok ? 200 : 410);
      }
      return json(req, env, { error: "Unbekannter Pfad" }, 404);
    } catch (e) {
      return json(req, env, { error: "Stripe nicht erreichbar", detail: e.message }, 502);
    }
  },
};
