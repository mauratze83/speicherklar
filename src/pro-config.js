/* Einstellungen für Verkauf und Freischaltung von Speicherklar Pro.
   Solange organizationId oder checkoutUrl leer sind, zeigt die Seite "Kauf startet bald" und verkauft nichts. */
var PRO_CONFIG = {
  provider: "polar",          // Lizenzprüfung über Polar (Merchant of Record)
  sandbox: true,              // true = Polar-Testumgebung (sandbox.polar.sh), vor dem Start auf false
  organizationId: "",         // Polar: Settings → Organization ID
  benefitId: "",              // Polar: Benefits → License Keys → ID (optional, prüft, dass der Schlüssel zu Pro gehört)
  checkoutUrl: "",            // Polar: Checkout-Link des Produkts
  price: 49,                  // aktueller Preis in €
  regularPrice: 89,           // Preis nach der Einführung
  introUntil: "",             // letzter Tag des Einführungspreises, z. B. "2027-02-28"
  publicFrom: ""              // ab diesem Tag kann jeder kaufen; vorher nur mit Vorab-Link (?vorab=1) aus der Warteliste-Mail
};
