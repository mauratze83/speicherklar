/* Einstellungen für Verkauf und Freischaltung von Speicherklar Pro.
   Bezahlung über Stripe Managed Payments (Stripe ist Merchant of Record), Freischaltung über den Cloudflare Worker in worker/.
   Solange api leer ist, zeigt die Seite "Kauf startet bald" und verkauft nichts. Preise selbst stehen in Stripe und worker/wrangler.toml. */
var PRO_CONFIG = {
  api: "https://speicherklar-pro.speicherklar.workers.dev",                    // Adresse des Workers, z. B. "https://speicherklar-pro.<name>.workers.dev"
  price: 49,                  // Einführungspreis in € (nur Anzeige, muss zur Stripe-Preis-ID PRICE_INTRO passen)
  regularPrice: 89,           // Normalpreis in € (Anzeige, passend zu PRICE_REGULAR)
  introUntil: "2027-01-31",             // letzter Tag des Einführungspreises, z. B. "2027-02-28" (gleich wie INTRO_UNTIL im Worker)
  publicFrom: "2026-12-01",             // ab diesem Tag kann jeder kaufen; vorher nur mit ?vorab=1 (intern zum Testen)
  accessDays: 90                        // Laufzeit ab der ersten Freischaltung (Anzeige; gleich wie ACCESS_DAYS im Worker)
};
