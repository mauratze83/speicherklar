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

## Reels

Titelbild-Farben nach Termin: post9 (Di 24.11.) Hell → Reel A (Mi 25.11.) **Dunkel** → post11 (Fr 27.11., schon fertig) Bernstein → Reel B (So 29.11.) **Hell**. So stehen nie zwei gleiche Farben nebeneinander und jede Dreierreihe hat alle drei Farben (post11 war schon in Bernstein gebaut, deshalb Reel A Dunkel statt Bernstein).

### Reel A: reel4-passt-7-kwh (36 s, 1080×1350, Titel: Dunkel)

Vorschlag zum Veröffentlichen: Mittwoch, 25.11.2026, 18:30 Uhr.
Titelbild: `reel4-passt-7-kwh-titelbild.png`, beim Hochladen unter „Titelbild bearbeiten“ → „Aus Galerie hinzufügen“.
Entscheidung 2 aus dem Umsatz-Review vom 22.11.2026 (Angebots-Check mit einem Angebot, das passt). Taugt auch als Motiv für die zweite Anzeige.

#### Caption

7 kWh Stromspeicher im PV-Angebot? Bei dieser Familie passt das genau. Und das sag ich dir auch.

Ich hab ein Angebot durchgerechnet: Familie in Dortmund, 5.500 kWh im Jahr, 10 kWp aufs Süddach, 7 kWh Batteriespeicher, 17.000 € gesamt, davon 4.000 € für den Speicher.

Ergebnis: Mit genau 7 kWh bleiben nach 15 Jahren 3.146 € übrig. Mehr bringt keine andere Größe. Mit 10 kWh wären's 301 € weniger, mit 5 kWh 542 € weniger. Bezahlt hat sich der Speicher nach 8,4 Jahren.

Genau so prüft Speicherklar Pro dein Angebot. Erst kostenlos eine erste Einschätzung als Ampel: grün, gelb oder rot. Dann der Bericht, welche PV-Anlage und welcher Speicher am besten zusammenpassen. Zu groß, zu klein oder passend. Speicherklar Pro gibt's ab sofort für alle: 49 € bis 31.01.2027, danach 89 €, einmalig. Link in der Bio.

Beispiel: PLZ-Gebiet 44 (Dortmund, Bochum), 10 kWp Süd, 35°, 5.500 kWh/Jahr, Strom 33 ct, Einspeisung 7,70 ct, 15 Jahre, ohne Zinsen und Alterung. Angebot 7 kWh für 4.000 € (gesamt 17.000 €), andere Größen mit 30 % Fixanteil. Gerechnet mit Speicherklar Pro, Modellstand 14.11.2026.

#stromspeicher #photovoltaik #pvanlage #batteriespeicher #pvangebot

#### Facebook-Kommentar (als ersten Kommentar unter den Facebook-Beitrag)

Hier prüfst du dein eigenes Angebot, die erste Einschätzung ist kostenlos: https://speicherklar.de/pro/?von=facebook

### Reel B: reel5-pv-groesse-9-statt-15 (34 s, 1080×1350, Titel: Hell)

Vorschlag zum Veröffentlichen: Sonntag, 29.11.2026, 18:30 Uhr.
Titelbild: `reel5-pv-groesse-9-statt-15-titelbild.png`, beim Hochladen unter „Titelbild bearbeiten“ → „Aus Galerie hinzufügen“.
Zum Wochenartikel „Wie groß soll meine PV-Anlage sein?“ (23.11.2026). EEG-Stand 23.11.2026, Entwurf noch nicht beschlossen.

#### Caption

9 kWp im Angebot, aber Platz für 15? Mit heutiger Einspeisevergütung bringt die größere PV-Anlage rund 3.500 € mehr.

Ich hab mein Musterangebot durchgerechnet: Süddach mit Platz für 15 kWp, 4.500 kWh Verbrauch. Mit 14,5 statt 9 kWp bleiben nach allen Kosten 3.506 € mehr übrig. Gerüst, Zählerschrank und Anmeldung zahlst du nur einmal, jedes weitere kWp kostet deshalb rund 1.040 € statt 1.390 €.

Und der Stromspeicher? Wächst kaum mit, von 6 auf 7 kWh.

Aber: Das gilt mit der heutigen Vergütung. Käme die EEG-Reform so wie im Kabinettsentwurf vom 29.07.2026 (keine Vergütung, höchstens 50 % einspeisen), wären eher 4,5 bis 5,5 kWp richtig. Noch nicht beschlossen, Stand 23.11.2026. Beide Fälle mit Tabelle stehen im Ratgeber auf speicherklar.de. Link in der Bio.

Beispiel: PLZ-Gebiet 47 (Duisburg, Krefeld), Süddach 35°, Angebot 9 kWp und 10 kWh für 19.000 € (davon Speicher 6.500 €), Platz für 15 kWp, 4.500 kWh/Jahr, Strom 33 ct, Einspeisung 7,70 ct bis 10 kWp und 6,66 ct darüber. PV über 20 Jahre, bester Speicher über 15 Jahre, ohne Zinsen. Gerechnet mit Speicherklar Pro, Modellstand 14.11.2026.

#photovoltaik #pvanlage #stromspeicher #solaranlage #eeg

#### Facebook-Kommentar (als ersten Kommentar unter den Facebook-Beitrag)

Beide Fälle mit allen Zahlen, heute und nach dem EEG-Entwurf: https://speicherklar.de/ratgeber/pv-anlage-groesse.html?von=facebook

### Prüfung Reels

- Zahlen frisch mit src/pro.js (main, Commit 8a0496d) gerechnet, 23.11.2026. Strompreis 33 ct und Einspeisung 7,70 ct = Standardwerte im Rechner (src/body.html) und im Faktenblatt. Reel A: PRO.check verdict „passt“, beste Größe 7 kWh (+3.146 €), 8 kWh +3.125 €, 10 kWh +2.845 €, 5 kWh +2.604 €; Ampel alle vier grün (Speicherpreis 571 €/kWh, PV 1.300 €/kWp, beide üblich laut src/markt.js). Reel B: pvSize verdict „mehr“, 9 kWp +11.242 €, 14,5 kWp +14.748 € (Empfehlung), EEG-Entwurf beste 5,5 / Empfehlung 4,5 kWp, stimmt mit dem Artikel überein.
- Hinweis Reel A: In 7 von 8 Szenarien des Berichts bleibt es bei „passt“; nur mit späterem E-Auto wäre 7 kWh zu klein. Darum keine Aussage „passt immer“.
- MP4 per ffprobe 1080×1350, Schnitte gegen Sprechpausen (silencedetect) geprüft, Slides und Titelbilder angesehen: nichts abgeschnitten, Inhalt rechts bis x 930 und unten bis y 1080, keine Ersatzschrift.
- Caption-Prüfer (caption_de.py, detect_de.py) liefen nicht. Manuell geprüft: keine Geviertstriche, eine Bitte, 5 Hashtags, kein Link in der Caption, ich-Form mit Umgangssprache (hab, wär's, gibt's), kurze und lange Sätze gemischt, keine Rendite-Versprechen, kein Streichpreis.
