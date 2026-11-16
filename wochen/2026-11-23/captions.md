# Woche 2026-11-23

## Karussell: post9-drei-orte (10 Slides)

Vorschlag zum Veröffentlichen: Dienstag, 24.11.2026, 18:30 Uhr.
Hinweis: In der App im Zuschnitt-Schritt auf das Rahmen-Symbol tippen und „Original“ bzw. 4:5 wählen, sonst schneidet Instagram auf ein Quadrat zu.
Standard-Haus aus dem Ruhrgebiet, nur die Region getauscht. Nicht die Profil-Häuser „Haus Oberbayern“ / „Haus Schleswig-Holstein“ aus dem Faktenblatt (die kommen in eigenen Posts).

### Caption

Ein Haus, drei Orte: Ich hab mein Beispielhaus nach Oberbayern und Schleswig-Holstein verschoben. Der beste Stromspeicher bleibt überall 6 kWh groß.

Es ist das bekannte Haus aus dem Ruhrgebiet: 9 kWp aufs Süddach, 4.500 kWh Verbrauch. Dach, Verbrauch und Preise bleiben gleich, nur der Ort wechselt. Klar, im Süden gibt's mehr Sonne. Rund 15 % mehr als im Norden. Nur kommt die fast komplett im Winter dazu. Im Juni erzeugen alle drei Häuser praktisch gleich viel.

Und der Speicher? Im Sommer wird er überall voll, im Dezember nirgends. Deshalb bleibt die passende Speichergröße gleich.

Was der Ort ändert, ist das Plus: nach 15 Jahren 3.380 € in Oberbayern, 2.668 € in Schleswig-Holstein. Die Größe richtet sich nach deinem Verbrauch. Bei 3.000 kWh im Jahr sind's im Ruhrgebiet 4 kWh, bei 6.000 kWh 8 kWh.

Deine Region wählst du im kostenlosen Rechner auf speicherklar.de, ohne Anmeldung. Link in der Bio.

Beispiel: 9 kWp Süd, 35°, 4.500 kWh/Jahr, Speicher 500 €/kWh, Strom 33 ct, Einspeisung 7,70 ct, 15 Jahre, ohne Zinsen und Alterung. Regionen im Rechner: München/Oberbayern, Ruhrgebiet/Westfalen, Schleswig-Holstein/Niedersachsen-Nord. Gerechnet mit dem Speicherklar-Rechner, Modellstand 14.11.2026.

#stromspeicher #photovoltaik #pvanlage #solaranlage #speichergroesse

### Facebook-Kommentar (als ersten Kommentar unter den Facebook-Beitrag)

Rechne dein Haus mit deiner Region selbst durch, kostenlos und ohne Anmeldung: https://speicherklar.de/?von=facebook

### Alt-Text Cover

Grafik im Speicherklar-Stil auf hellgrauem Grund: Überschrift „Ein Haus. Drei Orte.“, darunter „Ich hab mein Beispielhaus aus dem Ruhrgebiet nach Oberbayern und Schleswig-Holstein verschoben.“

### Prüfung

- Alle Zahlen live mit src/sim.js (main) gerechnet, Strompreis 33 ct und Einspeisung 7,70 ct = Standardwerte im Rechner. make.py bricht ab, falls die beste Größe in den drei Regionen nicht mehr gleich ist.
- Erzeugung und Füllstand (Slides 5 und 6) aus dayProfile, Durchschnittstag des Monats, 6-kWh-Speicher.
- Caption-Prüfer (caption_de.py, detect_de.py) liefen nicht. Manuell geprüft: keine Geviertstriche, eine Bitte, 5 Hashtags, kein Link in der Caption, ich-Form mit Umgangssprache (hab's, gibt's, sind's), kurze und lange Sätze gemischt.
