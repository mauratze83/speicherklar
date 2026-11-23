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

Alle zehn Regionen mit Tabelle und deine PLZ zum Nachschauen: https://speicherklar.de/ratgeber/stromspeicher-region.html?von=facebook

### Alt-Text Cover

Grafik im Speicherklar-Stil auf hellgrauem Grund: Überschrift „Ein Haus. Drei Orte.“, darunter „Ich hab mein Beispielhaus aus dem Ruhrgebiet nach Oberbayern und Schleswig-Holstein verschoben.“

### Prüfung

- Alle Zahlen live mit src/sim.js (main) gerechnet, Strompreis 33 ct und Einspeisung 7,70 ct = Standardwerte im Rechner. make.py bricht ab, falls die beste Größe in den drei Regionen nicht mehr gleich ist.
- Erzeugung und Füllstand (Slides 5 und 6) aus dayProfile, Durchschnittstag des Monats, 6-kWh-Speicher.
- Caption-Prüfer (caption_de.py, detect_de.py) liefen nicht. Manuell geprüft: keine Geviertstriche, eine Bitte, 5 Hashtags, kein Link in der Caption, ich-Form mit Umgangssprache (hab's, gibt's, sind's), kurze und lange Sätze gemischt.

## Karussell: post11-norden (8 Slides, Titel: Bernstein)

Vorschlag zum Veröffentlichen: Freitag, 27.11.2026, 18:30 Uhr.
Hinweis: In der App im Zuschnitt-Schritt auf das Rahmen-Symbol tippen und „Original“ bzw. 4:5 wählen, sonst schneidet Instagram auf ein Quadrat zu.
Profil-Haus „Haus Schleswig-Holstein“ aus dem Faktenblatt (Paar, 8 kWp Ost-West, 3.000 kWh). Nicht das umgezogene Standard-Haus aus post9 (das hat 6 kWh). Entscheidung 3 aus dem Umsatz-Review vom 22.11.2026.

### Caption

Lohnt sich ein Stromspeicher im Norden? Ja. Bei diesem Haus in Schleswig-Holstein reichen aber 3 kWh.

Ich hab mein Beispielhaus aus dem Norden durchgerechnet: ein Paar, 3.000 kWh Verbrauch im Jahr, 8 kWp aufs Ost-West-Dach. Mit 3 kWh Speicher steht nach 15 Jahren ein Plus von 1.262 €. Bezahlt hat er sich nach 8,1 Jahren.

Größer wird's nicht besser. 6 kWh bringen noch 568 €. Ab 8 kWh rutscht die Rechnung ins Minus, mit 10 kWh sind's −1.254 €. Klar, die Autarkie steigt dann von 65 auf 74 %. Nur kosten diese 9 Punkte 3.500 € mehr, und die holt der Speicher nicht wieder rein.

Liegt das am Norden? Kaum. Dasselbe Haus im Ruhrgebiet hätte auch 3 kWh als beste Größe. Ein Paar braucht abends einfach weniger Strom.

Dein Haus mit deinem Verbrauch rechnest du im kostenlosen Rechner auf speicherklar.de, ohne Anmeldung. Link in der Bio.

Beispiel: Region Schleswig-Holstein/Bremen/Niedersachsen-Nord, 8 kWp Ost-West (je 4 kWp, 35°), 3.000 kWh/Jahr, Speicher 500 €/kWh, Strom 33 ct, Einspeisung 7,70 ct, 15 Jahre, ohne Zinsen und Alterung. Gerechnet mit dem Speicherklar-Rechner, Modellstand 14.11.2026.

#stromspeicher #photovoltaik #pvanlage #solaranlage #schleswigholstein

### Facebook-Kommentar (als ersten Kommentar unter den Facebook-Beitrag)

Alle zehn Regionen im Vergleich und warum die Speichergröße am Verbrauch hängt: https://speicherklar.de/ratgeber/stromspeicher-region.html?von=facebook

### Alt-Text Cover

Grafik im Speicherklar-Stil auf bernsteinfarbenem Grund: Überschrift „Speicher im Norden? Lohnt sich. Aber klein.“, darunter „Ein Haus in Schleswig-Holstein, Ost-West-Dach, 3.000 kWh. Ich hab’s durchgerechnet.“

### Prüfung

- Alle Zahlen live mit src/sim.js (main, Stand 23.11.2026) gerechnet, Strompreis 33 ct und Einspeisung 7,70 ct = Standardwerte im Rechner; stimmen mit dem Faktenblatt (16.11.2026) überein. make.py bricht ab, wenn die beste Größe nicht mehr 3 kWh ist.
- Titelbild Bernstein: erster neuer Beitrag nach post9 (24.11., Hell). Falls die Reels dieser Woche vor Freitag erscheinen, die Farbfolge nach Termin neu vergeben.
- Caption-Prüfer (caption_de.py, detect_de.py) liefen nicht. Manuell geprüft: keine Geviertstriche, eine Bitte, 5 Hashtags, kein Link in der Caption, ich-Form mit Umgangssprache (hab, wird's, sind's), kurze und lange Sätze gemischt.
