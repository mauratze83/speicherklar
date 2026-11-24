// Tests für die Bewertungen im Bezahl-Worker (worker/index.js) ohne echtes Stripe, KV und GitHub.
// Aufruf: node test/bewertungen.test.mjs
import assert from "node:assert/strict";
import W from "../worker/index.js";

const ORIGIN = "https://speicherklar.de";
function kv() {
  const m = new Map();
  return { m,
    async get(k, t) { const v = m.get(k); return v == null ? null : t === "json" ? JSON.parse(v) : v; },
    async put(k, v) { m.set(k, v); },
    async list({ prefix }) { return { keys: [...m.keys()].filter((k) => k.startsWith(prefix)).map((name) => ({ name })), list_complete: true }; } };
}
const env = (o = {}) => ({ SITE: ORIGIN, ALLOWED_ORIGINS: ORIGIN, LICENSE_SECRET: "geheim", STRIPE_SECRET_KEY: "sk_test", LICENSES: kv(),
  REVIEW_ADMIN_KEY: "admin-123", GH_DISPATCH_TOKEN: "gh-token", GH_REPO: "mauratze83/speicherklar", FREE_KEYS: "", ...o });
const req = (path, body, auth) => new Request("https://w.test" + path, { method: "POST", headers: { Origin: ORIGIN, "Content-Type": "application/json", ...(auth ? { Authorization: "Bearer " + auth } : {}) }, body: JSON.stringify(body || {}) });
const call = async (e, path, body, auth) => { const r = await W.fetch(req(path, body, auth), e); return { s: r.status, j: await r.json(), h: r.headers }; };

// Stripe und GitHub nachbauen
const SESS = { cs_paid: { payment_status: "paid", payment_intent: { latest_charge: { refunded: false } }, customer_details: { email: "a@b.de" } },
  cs_refund: { payment_status: "paid", payment_intent: { latest_charge: { refunded: true } }, customer_details: { email: "c@d.de" } } };
let dispatches = 0;
globalThis.fetch = async (url, init) => {
  url = String(url);
  if (url.startsWith("https://api.stripe.com/v1/checkout/sessions/")) {
    const id = decodeURIComponent(url.split("/sessions/")[1].split("?")[0]);
    return SESS[id] ? new Response(JSON.stringify(SESS[id]), { status: 200 }) : new Response(JSON.stringify({ error: { message: "nope" } }), { status: 404 });
  }
  if (url.includes("/actions/workflows/bewertungen.yml/dispatches")) {
    assert.equal(init.headers.Authorization, "Bearer gh-token"); assert.equal(JSON.parse(init.body).ref, "main");
    dispatches++; return new Response(null, { status: 204 });
  }
  throw new Error("unerwarteter Aufruf " + url);
};
// Schlüssel wie der Worker ihn baut (HMAC über die Checkout-ID)
async function key(id, secret = "geheim") {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const mac = new Uint8Array(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(id)));
  return `SK.${id}.` + btoa(String.fromCharCode(...mac.slice(0, 12))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
const GOOD = { stars: 5, text: "Der Bericht hat mir gezeigt, dass 6 kWh reichen.", name: "Petra", ok: true };
let n = 0; const ok = (t) => { n++; console.log("ok", t); };

const e = env(), K = await key("cs_paid");

// CORS erlaubt den Authorization-Kopf
{ const r = await W.fetch(new Request("https://w.test/admin/reviews", { method: "OPTIONS", headers: { Origin: ORIGIN } }), e);
  assert.match(r.headers.get("Access-Control-Allow-Headers"), /Authorization/); ok("CORS mit Authorization"); }

// Status: gültiger Kauf darf, falscher/erstatteter/Freischlüssel nicht
assert.deepEqual((await call(e, "/review/status", { key: K })).j, { can: true, done: false }); ok("Käufer darf bewerten");
assert.equal((await call(e, "/review/status", { key: "SK.cs_paid.AAAAAAAAAAAAAAAA" })).j.can, false); ok("falsche Signatur nicht");
assert.equal((await call(e, "/review/status", { key: await key("cs_refund") })).j.can, false); ok("erstatteter Kauf nicht");
{ const fe = env({ FREE_KEYS: "" }); assert.equal((await call(fe, "/review/status", { key: "familie-1" })).j.can, false); ok("Freischlüssel nicht"); }
{ const be = env(); await be.LICENSES.put("lic:cs_paid", JSON.stringify({ devices: [], blocked: true }));
  assert.equal((await call(be, "/review/status", { key: K })).j.can, false); ok("gesperrter Schlüssel nicht"); }

// Eingaben prüfen
for (const [b, frag] of [[{ ...GOOD, stars: 0 }, "Sterne"], [{ ...GOOD, stars: 4.5 }, "Sterne"], [{ ...GOOD, text: "kurz" }, "mindestens"],
  [{ ...GOOD, text: "x".repeat(1001) }, "höchstens"], [{ ...GOOD, name: "n".repeat(41) }, "Name"], [{ ...GOOD, text: "Super, schaut auf www.example.com vorbei!!" }, "Links"],
  [{ ...GOOD, name: "petra@mail.de" }, "Links"], [{ ...GOOD, ok: false }, "bestätige"]]) {
  const r = await call(e, "/review", { key: K, ...b }); assert.equal(r.s, 400); assert.match(r.j.error, new RegExp(frag));
}
ok("ungültige Bewertungen abgelehnt");
assert.equal((await call(e, "/review", { key: await key("cs_refund"), ...GOOD })).s, 403); ok("Nicht-Käufer 403");

// Speichern, einmal je Kauf
assert.equal((await call(e, "/review", { key: K, ...GOOD })).j.ok, true);
const saved = JSON.parse(e.LICENSES.m.get("rev:cs_paid"));
assert.equal(saved.status, "offen"); assert.match(saved.rid, /^[0-9a-f]{12}$/); assert.equal(saved.name, "Petra"); ok("Bewertung gespeichert, Status offen");
assert.equal((await call(e, "/review", { key: K, ...GOOD })).s, 409); ok("zweite Bewertung je Kauf abgelehnt");
assert.equal((await call(e, "/review/status", { key: K })).j.done, true); ok("Status meldet schon bewertet");

// Öffentlich nur freigegebene, ohne Kauf-ID
{ const r = (await call(e, "/reviews")).j; assert.deepEqual(r.reviews, []); assert.equal(r.offen, 1); ok("offene Bewertung nicht öffentlich, nur gezählt"); }

// Admin: ohne/falscher Schlüssel, ohne Secret
assert.equal((await call(e, "/admin/reviews")).s, 401);
assert.equal((await call(e, "/admin/reviews", {}, "falsch")).s, 401); ok("Admin ohne richtigen Schlüssel 401");
assert.equal((await call(env({ REVIEW_ADMIN_KEY: "" }), "/admin/reviews", {}, "admin-123")).s, 404); ok("ohne Secret 404");
{ const r = await call(e, "/admin/reviews", {}, "admin-123");
  assert.equal(r.j.reviews.length, 1); assert.equal(r.j.reviews[0].status, "offen"); assert.ok(!JSON.stringify(r.j).includes("cs_paid")); ok("Admin-Liste ohne Kauf-ID"); }

// Freigeben startet den Neubau, Ablehnen einer offenen nicht, Entfernen einer freigegebenen schon
assert.equal((await call(e, "/admin/review", { rid: saved.rid, status: "weg" }, "admin-123")).s, 400);
assert.equal((await call(e, "/admin/review", { rid: "000000000000", status: "frei" }, "admin-123")).s, 404); ok("ungültige Freigabe abgelehnt");
{ const r = await call(e, "/admin/review", { rid: saved.rid, status: "frei" }, "admin-123"); assert.deepEqual(r.j, { ok: true, build: true }); assert.equal(dispatches, 1); }
{ assert.equal((await call(e, "/reviews")).j.offen, 0); const pub = (await call(e, "/reviews")).j.reviews; assert.equal(pub.length, 1); assert.deepEqual(Object.keys(pub[0]).sort(), ["date", "name", "rid", "stars", "text"]);
  assert.ok(!JSON.parse(e.LICENSES.m.get("rev:cs_paid"))._k); ok("freigegeben: öffentlich, nur erlaubte Felder, Neubau gestartet"); }
{ const r = await call(e, "/admin/review", { rid: saved.rid, status: "ab" }, "admin-123"); assert.equal(r.j.build, true); assert.equal(dispatches, 2);
  assert.deepEqual((await call(e, "/reviews")).j.reviews, []); ok("wieder entfernt: Neubau, nicht mehr öffentlich"); }
{ const e2 = env(); await call(e2, "/review", { key: K, ...GOOD }); const rid = JSON.parse(e2.LICENSES.m.get("rev:cs_paid")).rid;
  const r = await call(e2, "/admin/review", { rid, status: "ab" }, "admin-123"); assert.equal(r.j.build, false); assert.equal(dispatches, 2); ok("offene ablehnen: kein Neubau"); }
{ const e3 = env({ GH_DISPATCH_TOKEN: "" }); await call(e3, "/review", { key: K, ...GOOD }); const rid = JSON.parse(e3.LICENSES.m.get("rev:cs_paid")).rid;
  const r = await call(e3, "/admin/review", { rid, status: "frei" }, "admin-123"); assert.deepEqual(r.j, { ok: true, build: false }); ok("ohne GitHub-Schlüssel: gespeichert, build false"); }

console.log(`\n${n} Prüfungen bestanden`);
