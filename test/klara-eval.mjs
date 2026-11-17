// Prüft Klara gegen die echte Claude API mit den Fällen aus test/klara-faelle.json.
// Aufruf: ANTHROPIC_API_KEY=… node test/klara-eval.mjs   (kostet ein paar Cent; Antworten von Hand lesen!)
import fs from "node:fs";
import { system, kontext, TOOLS } from "../worker-klara/index.js";
const key = process.env.ANTHROPIC_API_KEY;
if (!key) { console.log("ANTHROPIC_API_KEY fehlt"); process.exit(1); }
const faelle = JSON.parse(fs.readFileSync(new URL("./klara-faelle.json", import.meta.url)));
const heute = new Date().toISOString().slice(0, 10);
let fehler = 0, usd = 0;
for (const f of faelle) {
  const r = await fetch("https://api.anthropic.com/v1/messages", { method: "POST",
    headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model: process.env.MODEL || "claude-haiku-5-5", max_tokens: 600, thinking: { type: "disabled" }, tools: TOOLS,
      system: [{ type: "text", text: system(heute), cache_control: { type: "ephemeral" } }, { type: "text", text: kontext(heute, "/", null) }],
      messages: [{ role: "user", content: f.frage }] }) });
  const d = await r.json();
  if (!r.ok) { console.log("API-Fehler", r.status, d); process.exit(1); }
  const text = d.content.filter((c) => c.type === "text").map((c) => c.text).join("");
  const knopf = d.content.find((c) => c.type === "tool_use" && c.name === "verweis")?.input?.ziel || null;
  const u = d.usage; usd += ((u.input_tokens || 0) * 0.1 + (u.cache_creation_input_tokens || 0) * 0.125 + (u.cache_read_input_tokens || 0) * 0.01 + (u.output_tokens || 0) * 0.5) / 1e6;
  const probleme = [];
  for (const m of f.muss || []) if (!new RegExp(m, "i").test(text)) probleme.push("fehlt: " + m);
  for (const m of f.darf_nicht || []) if (new RegExp(m, "im").test(text)) probleme.push("enthält: " + m);
  if (f.knopf && knopf !== f.knopf) probleme.push(`Knopf ${knopf} statt ${f.knopf}`);
  if (/—/.test(text)) probleme.push("Geviertstrich");
  if (text.split(/\s+/).length > 160) probleme.push("zu lang");
  fehler += probleme.length ? 1 : 0;
  console.log(`\n${probleme.length ? "✗" : "✓"} ${f.frage}\n  Knopf: ${knopf}\n  ${text.replace(/\n/g, "\n  ")}` + (probleme.length ? `\n  PROBLEME: ${probleme.join("; ")}` : ""));
}
console.log(`\n${faelle.length - fehler}/${faelle.length} ohne Auffälligkeit, Kosten rund ${usd.toFixed(4)} $`);
process.exit(fehler ? 1 : 0);
