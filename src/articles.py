"""Ratgeber-Artikel für speicherklar.de. Jeder Artikel: slug, Titel, Beschreibung, Datum, HTML-Inhalt."""

STAND = "November 2026"
BEISPIEL = ("Alle Beispiele: Standort Ruhrgebiet (PLZ 4…), Dachneigung 35°, Speicherpreis 500 €/kWh inkl. Einbau, "
            "Strompreis 33 ct/kWh, Einspeisevergütung 7,70 ct/kWh, 15 Jahre Lebensdauer, wenn nicht anders angegeben. "
            "Gerechnet mit dem Speicherklar-Rechner: Jahressimulation in 5-Minuten-Schritten mit Sonnendaten aus PVGIS 2014–2023 und dem Wetterverlauf eines echten Jahres (2020).")

# Standardwerte für die automatischen Grafiken (gleich wie BEISPIEL). Jede Grafik ändert nur, was sie in "p" angibt.
CHART_BASE = {"region": "4", "roofs": [{"kwp": 9, "tilt": 35, "aspect": 0}], "cons": 4500, "ev": 0, "evTime": "eve",
              "bat": 6, "bprice": 500, "life": 15, "price": 33, "feed": 7.7, "feedLimit": 0}

ARTICLES = [
{
"slug": "stromspeicher-rechner-test-echte-daten",
"kennzahl": {"v": "1–2 Punkte", "t": "trifft der Rechner die Autarkie echter Häuser mit Speicher"},
"related": ["stromspeicher-groesse-berechnen", "ost-west-dach-speicher", "pv-angebot-pruefen"],
"bars": {"title": "Was der 10-kWh-Speicher an meiner Anlage im Jahr spart", "caption": "Netzstrom, den der Speicher ersetzt. Gemessen gegen drei Stände des Rechners.", "unit": "kWh",
         "rows": [["Gemessen", 1860], ["Rechner vorher", 2819, "Wärmepumpe mit Haushaltsspitzen"], ["Nach erster Korrektur", 1146, "Wetter zu wechselhaft"], ["Rechner heute", 1735]], "best": "Rechner heute", "mark": "Gemessen"},
"title": "Wie genau ist ein Stromspeicher-Rechner? Mein Test mit echten Messdaten",
"seo_title": "Stromspeicher-Rechner im Test mit Messdaten",
"h1": "Wie genau ist ein Stromspeicher-Rechner? Mein Test mit echten Messdaten",
"desc": "Ich habe meinen Rechner gegen fünf Jahre Messwerte meiner PV-Anlage und 30 gemessene Häuser geprüft. Ergebnis: auf 1–2 Punkte genau, nach zwei Korrekturen.",
"date": "2026-11-14",
"lead": "Mit Speicher trifft der Speicherklar-Rechner die Autarkie echter Häuser heute auf 1–2 Prozentpunkte. Auf dem Weg dahin habe ich zwei Fehler gefunden, die ich hier offen zeige, mit allen Zahlen.",
"body": """
<p>Jeder Rechner ist ein Modell. Ob er stimmt, sieht man erst, wenn man ihn gegen echte Messwerte hält. Genau das habe ich gemacht, mit meiner eigenen PV-Anlage und mit einem öffentlichen Datensatz von 30 Einfamilienhäusern. Hier steht, wie ich vorgegangen bin, was herauskam und was ich deshalb am Rechner geändert habe.</p>

<h2>Das Setup: meine Anlage</h2>
<ul>
<li><b>PV-Anlage:</b> 34 Module mit je 380 Wp, also 12,92 kWp, auf einem Ost-West-Dach mit 45° Neigung in Krefeld. 14 Module zeigen nach Osten (5,32 kWp), 20 nach Westen (7,60 kWp).</li>
<li><b>Speicher:</b> 10 kWh nutzbar.</li>
<li><b>Verbrauch:</b> ein einziger Zähler für Haushalt, Erdwärmepumpe, Pool mit eigener Wärmepumpe und E-Auto. Das macht rund 19.000 kWh im Jahr, gut viermal so viel wie das Standard-Beispiel im Rechner.</li>
<li><b>Verschattung:</b> Bäume nehmen der Anlage morgens und vor allem abends Licht.</li>
<li><b>Daten:</b> der Export meines Speichers mit 5-Minuten-Werten für Erzeugung, Verbrauch, Netz und Speicher, rund 1.800 Tage seit Oktober 2021.</li>
</ul>
<p>Für den Test habe ich das letzte volle Jahr genommen, den 26.10.2025 bis 25.10.2026. An 336 Tagen sind die Daten lückenlos. Die Energiebilanz geht auf: Erzeugung, Netzbezug und Entladen ergeben genau Verbrauch, Einspeisung und Laden.</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Gemessen an 336 Tagen</th><th>Wert</th></tr></thead>
<tbody>
<tr><td>Erzeugung</td><td class="num">9.405 kWh</td></tr>
<tr><td>Verbrauch</td><td class="num">17.610 kWh</td></tr>
<tr><td>Netzbezug</td><td class="num">9.493 kWh</td></tr>
<tr><td>Einspeisung</td><td class="num">1.149 kWh</td></tr>
<tr class="hl"><td>Autarkie</td><td class="num">46,1 %</td></tr>
<tr><td>Eigenverbrauch der Erzeugung</td><td class="num">87,8 %</td></tr>
</tbody></table></div>
<p>Mein Haus ist kein typischer Fall. Gerade deshalb ist es ein guter Test: Wo ein Rechner nur für den Durchschnitt passt, fällt es hier auf.</p>

<h2>Test 1: Rechnet der Speicher richtig?</h2>
<p>Zuerst habe ich nur das Speichermodell geprüft. Dafür bekommt es meine echte Erzeugung und meinen echten Verbrauch in 5-Minuten-Schritten. Es muss dann nur noch entscheiden, wann der Speicher lädt und entlädt.</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>336 Tage</th><th>Gemessen</th><th>Rechner</th></tr></thead>
<tbody>
<tr class="hl"><td>Netzbezug</td><td class="num">9.493 kWh</td><td class="num">9.716 kWh</td></tr>
<tr><td>Einspeisung</td><td class="num">1.149 kWh</td><td class="num">1.052 kWh</td></tr>
<tr><td>Autarkie</td><td class="num">46,1 %</td><td class="num">44,8 %</td></tr>
</tbody></table></div>
<p>Der Netzbezug liegt 2,3 % daneben, und zwar in die vorsichtige Richtung. Mein Speicher ist dabei anders gebaut als der im Rechner: Er verliert weniger (94 % statt 88 % Wirkungsgrad je Zyklus), lädt aber langsamer (rund 2,5 statt 5 kW). Beides gleicht sich fast aus. Der Speicher-Teil stimmt also.</p>

<h2>Test 2: Stimmt der Ertrag?</h2>
<p>Für meine Anlage rechnet Speicherklar mit 9.764 kWh im Jahr. Gemessen habe ich in den vier vollen Jahren:</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Jahr</th><th>Erzeugung gemessen</th></tr></thead>
<tbody>
<tr><td>2022</td><td class="num">10.334 kWh</td></tr>
<tr><td>2023</td><td class="num">10.034 kWh</td></tr>
<tr><td>2024</td><td class="num">9.027 kWh</td></tr>
<tr><td>2025</td><td class="num">9.993 kWh</td></tr>
</tbody></table></div>
<p>Der Rechner liegt mitten in dieser Spanne. 2024 war ein schwaches Sonnenjahr, der Rechner nimmt ein Mittel aus zehn Jahren. Im Tagesverlauf sieht man die Bäume: Im Juni liefert meine Anlage zwischen 19 und 21 Uhr nur 3,7 % ihres Tagesertrags, der Rechner erwartet 8,1 %. Dafür ist es mittags etwas mehr. Verschattung kennt der Rechner nicht, das steht auch in den Annahmen.</p>

<h2>Test 3: Die ganze Rechnung, und zwei Fehler</h2>
<p>Dann der eigentliche Test: Der Rechner bekommt nur, was du auch eingibst, also Anlage, Speicher und Verbrauch. Profil und Wetter erzeugt er selbst. Die Frage ist, wie viel Netzstrom der Speicher im Jahr ersetzt. Gemessen sind es bei mir 1.860 kWh.</p>
<!--BARS-->
<p><b>Fehler 1, die Wärmepumpe.</b> Der Rechner hat den ganzen Verbrauch mit den kurzen Spitzen eines Haushalts gerechnet: Wasserkocher an, Herd an, dann wieder fast nichts. Im Rechner lagen 62 % aller 5-Minuten-Werte unter dem halben Mittel ihrer Stunde, in meinem Haus sind es 12 %. Wärmepumpe und Pool laufen lange und gleichmäßig. Mein Haus braucht dadurch viel mehr Solarstrom direkt, und der Speicher hat weniger zu tun. Der alte Rechner zeigte 2.819 kWh, also die Hälfte zu viel.</p>
<p>Seit dem 14.11.2026 trägst du die Wärmepumpe im Rechner getrennt ein. Sie läuft dort ohne Spitzen, und wie sie sich auf Monate und Stunden verteilt, habe ich an echten Häusern abgelesen (unten mehr). Das E-Auto behält die Spitzen, weil eine Wallbox mehr Leistung zieht, als ein Speicher abgibt.</p>
<p><b>Fehler 2, das Wetter.</b> Danach lag der Rechner plötzlich zu niedrig, bei 1.146 kWh. Der Grund: Er hat jeden Tag einzeln ausgewürfelt, und im Sommer viel zu wechselhaft. Ich habe die Stundenwerte von PVGIS für alle zehn Regionen des Rechners nachgeprüft, 2014 bis 2023. Die trübsten 5 % der Julitage bringen dort 41 % eines durchschnittlichen Tages. Im Rechner waren es 11 %. Dafür fehlten Wolken mitten am Tag. Bei normalen Haushalten hob sich das zufällig auf, bei meinem großen Verbrauch nicht: An ganz trüben Tagen wird der Speicher nicht voll, an sehr sonnigen Tagen läuft er über.</p>
<p>Jetzt nimmt der Rechner den Wechsel von Sonne und Wolken Stunde für Stunde aus einem echten Jahr (2020), umgerechnet auf die Monatssummen deines Gebiets. Mit jedem der zehn Jahre bleibt die beste Größe im Standard-Beispiel bei 6 kWh, ich habe 2020 genommen, weil es in der Mitte liegt. Ergebnis für mein Haus: 1.735 kWh, gemessen 1.860 kWh.</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Mein Haus, 10 kWh</th><th>Autarkie ohne Speicher</th><th>mit Speicher</th></tr></thead>
<tbody>
<tr><td>Gemessen</td><td class="num">35,3 %</td><td class="num">45,0 %</td></tr>
<tr><td>Rechner vorher</td><td class="num">22,4 %</td><td class="num">37,2 %</td></tr>
<tr class="hl"><td>Rechner heute</td><td class="num">33,1 %</td><td class="num">42,1 %</td></tr>
</tbody></table></div>
<p class="note">Gemessen: ein volles Jahr, 29 Lückentage aus dem Vorjahr ergänzt; „ohne Speicher“ gerechnet aus den gemessenen 5-Minuten-Werten. Im Rechner: 4.500 kWh als Haushaltsstrom angenommen, der Rest als gleichmäßiger Verbrauch nach meinen echten Monatswerten. Die Lücke bei der Autarkie kommt vor allem vom Ertrag: Mit dem Wetterjahr rechnet der Rechner etwas weniger, als meine Anlage im Prüfjahr erzeugt hat.</p>

<h2>Gegenprobe an 30 fremden Häusern</h2>
<p>Ein Haus kann Zufall sein. Deshalb habe ich den Rechner zusätzlich an einem öffentlichen Datensatz geprüft. Das Institut für Solarenergieforschung Hameln hat bei rund 40 Einfamilienhäusern Haushaltsstrom und Wärmepumpe getrennt gemessen, minutengenau (Datensatz WPuQ, frei verfügbar). 30 Häuser haben ein lückenloses Jahr 2019. Ich habe ihren echten Verbrauch mit dem echten Wetter 2019 am Ort durchgerechnet und mit dem verglichen, was der Rechner nur aus dem Jahresverbrauch macht. Die Anlagen sind wie im Standard-Beispiel bemessen, 9 kWp je 4.500 kWh Haushaltsstrom.</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Autarkie, Speicher je 4.500 kWh</th><th>ohne</th><th>4 kWh</th><th>6 kWh</th><th>8 kWh</th><th>10 kWh</th></tr></thead>
<tbody>
<tr><td>30 Häuser gemessen</td><td class="num">39 %</td><td class="num">61 %</td><td class="num">69 %</td><td class="num">74 %</td><td class="num">76 %</td></tr>
<tr class="hl"><td>Rechner</td><td class="num">35 %</td><td class="num">62 %</td><td class="num">70 %</td><td class="num">75 %</td><td class="num">77 %</td></tr>
<tr><td>dieselben Häuser mit Wärmepumpe</td><td class="num">25 %</td><td class="num">35 %</td><td class="num">39 %</td><td class="num">42 %</td><td class="num">45 %</td></tr>
<tr><td>Rechner mit Wärmepumpe</td><td class="num">30 %</td><td class="num">39 %</td><td class="num">43 %</td><td class="num">46 %</td><td class="num">48 %</td></tr>
</tbody></table></div>
<p>Mit Speicher liegt der Rechner auf 1–2 Punkte genau. Ohne Speicher rechnet er etwas zu wenig Eigenverbrauch, das macht den Speicher eher einen Hauch zu gut. Mit Wärmepumpe liegt die Autarkie rund 4 Punkte zu hoch. Was der Speicher beiträgt, trifft er aber: 19 Punkte im Rechner, 20 Punkte gemessen. Für die Frage nach der Speichergröße zählt genau dieser Zugewinn.</p>

<h2>Was sich für dich ändert</h2>
<p>Für einen Haushalt ohne Wärmepumpe fast nichts. Im Standard-Beispiel (9 kWp Süd, 4.500 kWh) bleibt 6 kWh die beste Größe, die Bilanz nach 15 Jahren liegt bei 2.899 € statt vorher 2.758 €. Alle Artikel habe ich neu gerechnet. Eine Aussage hat sich dabei gedreht: Bei einem Ost-West-Dach rechnen sich jetzt 5 statt 4 kWh. Den Artikel <a href="ost-west-dach-speicher.html">Ost-West-Dach</a> habe ich angepasst.</p>
<p>Mit Wärmepumpe trag ihren Stromverbrauch im Rechner getrennt ein, statt ihn zum Haushalt zu zählen. Sonst rechnet der Speicher sich zu gut.</p>

<h2>Wann der Rechner eher danebenliegt</h2>
<ul>
<li>Deine Anlage ist verschattet, durch Bäume, Gauben oder Nachbarhäuser.</li>
<li>Dein Speicher lädt deutlich langsamer als mit der halben Kapazität pro Stunde. Gib die Leistung im Angebots-Check an, wenn du sie kennst.</li>
<li>Du lädst ein E-Auto gezielt mit Überschuss oder hast einen dynamischen Stromtarif. Beides bildet der Rechner nicht ab.</li>
<li>Du hast viele große Verbraucher, die gleichmäßig laufen, aber keine Heizungs-Wärmepumpen sind, etwa eine Pool-Wärmepumpe im Sommer.</li>
</ul>
<p>Alle Annahmen und der Rechenweg stehen auf der <a href="../methodik.html#eigene-anlage">Methodik-Seite</a>. Der Code liegt offen auf GitHub, jede Änderung ist dort mit Datum nachzulesen.</p>
""",
"faq": [
 ("Wie genau ist der Speicherklar-Rechner?", "Mit Speicher trifft er die Autarkie von 30 gemessenen Einfamilienhäusern auf 1–2 Prozentpunkte. Mit Wärmepumpe liegt die Autarkie rund 4 Punkte zu hoch, den Zugewinn durch den Speicher trifft er."),
 ("Warum weicht meine echte Autarkie vom Rechner ab?", "Die häufigsten Gründe sind Verschattung, ein Speicher mit wenig Ladeleistung, große gleichmäßige Verbraucher wie Wärmepumpe oder Pool und das Wetter des einzelnen Jahres. Der Rechner nimmt ein mittleres Jahr."),
 ("Welche Daten hast du für den Test genutzt?", "Die 5-Minuten-Messwerte meines eigenen Speichers von 2021 bis 2026 und den öffentlichen Datensatz WPuQ des Instituts für Solarenergieforschung Hameln mit Minutenwerten von 30 Häusern aus dem Jahr 2019."),
],
},
{
"slug": "stromsteuer-stromspeicher",
"kennzahl": {"v": "2,32 ct", "t": "pro kWh wird Strom billiger, wenn die Senkung der Stromsteuer voll ankommt"},
"chart": {"kind": "sweep", "title": "Gewinn nach 15 Jahren: ohne Senkung und mit dauerhafter Senkung", "caption": "9 kWp Süd, 35°, 4.500 kWh Verbrauch, Speicher 500 €/kWh, Einspeisung 7,7 ct, 15 Jahre. Strom 33 ct ohne Senkung, 30,68 ct mit Senkung aufs EU-Minimum.",
  "series": [{"label": "ohne Senkung (33 ct)", "p": {}}, {"label": "Senkung dauerhaft (30,68 ct)", "p": {"price": 30.68}}]},
"title": "Stromsteuer sinkt 2027: Was heißt das für deinen Stromspeicher?",
"seo_title": "Stromsteuer sinkt 2027: Folgen für Speicher",
"h1": "Stromsteuer sinkt 2027: Was heißt das für deinen Stromspeicher?",
"desc": "Die Koalition will die Stromsteuer 2027 für alle aufs EU-Minimum senken. Strom wird 2,32 ct billiger. Die beste Speichergröße bleibt gleich.",
"date": "2026-11-13",
"updated": "2026-11-18",
"lead": "Kurze Antwort: Für deine Planung ändert sich fast nichts. Die beste Speichergröße bleibt gleich. Der Speicher bezahlt sich etwas später, weil Netzstrom billiger wird: im Beispiel nach 7,7 statt 7,6 Jahren, wenn die Senkung nur 2027 gilt, nach 8,5 Jahren, wenn sie bleibt.",
"body": """
<p>Am 13.11. sah es so aus, als käme die Senkung für Haushalte vorerst nicht. So stand es auch hier. Das ist überholt: In der Nacht zum 18.11. haben sich Union und SPD doch geeinigt. Ich hab neu sortiert, was das für einen Stromspeicher heißt. Beispiel wie immer: 9 kWp auf einem Süddach im Ruhrgebiet, 4.500 kWh Verbrauch im Jahr.</p>

<h2>Was beschlossen ist (Stand 18.11.2026)</h2>
<p>Die Stromsteuer beträgt laut § 3 Stromsteuergesetz 20,50 € je Megawattstunde, also 2,05 ct je kWh. Darauf kommen 19 % Umsatzsteuer. Das EU-Minimum für Haushalte liegt bei 0,1 ct je kWh (Energiesteuerrichtlinie 2003/96/EG).</p>
<p>Der Koalitionsausschuss hat sich darauf geeinigt, die Stromsteuer für alle Verbraucher aufs EU-Minimum zu senken. Finanziert ist das bisher nur für 2027. Eine dauerhafte Senkung ist laut Ergebnispapier beabsichtigt (t-online und ZDFheute, 18.11.2026).</p>
<p><b>Gesetz ist das noch nicht.</b> Der Bundestag soll den Haushalt 2027 am 27.11. beschließen, außerdem muss das Stromsteuergesetz geändert werden. Ich aktualisiere den Artikel, sobald das durch ist.</p>

<h2>Um wie viel wird Strom billiger?</h2>
<p>Die Senkung von 2,05 auf 0,1 ct macht 1,95 ct netto. Mit der Umsatzsteuer, die darauf wegfällt, sind es 2,32 ct je kWh. Aus 33 ct im Beispiel werden also 30,68 ct, wenn dein Versorger die Senkung voll weitergibt.</p>
<p>Wie viel das im Jahr ausmacht, hängt davon ab, wie viel Strom du noch aus dem Netz kaufst:</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Haushalt mit 4.500 kWh</th><th>Strom aus dem Netz</th><th>Ersparnis durch Senkung/Jahr</th></tr></thead>
<tbody>
<tr><td>ohne PV-Anlage</td><td class="num">4.500 kWh</td><td class="num">104 €</td></tr>
<tr><td>9 kWp, ohne Speicher</td><td class="num">2.887 kWh</td><td class="num">67 €</td></tr>
<tr class="hl"><td>9 kWp, 6 kWh Speicher</td><td class="num">1.190 kWh</td><td class="num">28 €</td></tr>
</tbody></table></div>
<p>Mit PV-Anlage und Speicher hast du von der Senkung also am wenigsten. Du kaufst einfach kaum noch Netzstrom.</p>

<h2>Was das für den Speicher heißt</h2>
<p>Ein Speicher spart Geld, weil er Netzstrom ersetzt. Je billiger der Netzstrom, desto weniger ist jede gespeicherte kWh wert. Mit der Senkung verliert der Speicher also etwas. Wie viel, hängt daran, ob sie nur 2027 gilt oder bleibt:</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>6-kWh-Speicher</th><th>bezahlt nach</th><th>Bilanz 15 J.</th></tr></thead>
<tbody>
<tr><td>ohne Senkung (33 ct)</td><td class="num">7,6 J.</td><td class="num">+2.899 €</td></tr>
<tr class="hl"><td>Senkung nur 2027, danach 33 ct</td><td class="num">7,7 J.</td><td class="num">+2.860 €</td></tr>
<tr><td>Senkung dauerhaft (30,68 ct)</td><td class="num">8,5 J.</td><td class="num">+2.308 €</td></tr>
</tbody></table></div>
<p>Und so sieht es für alle Größen aus, wenn die Senkung dauerhaft bleibt. In jeder Zelle oben: ohne Senkung. Unten: Senkung dauerhaft.</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Speicher</th><th>Ersparnis pro Jahr</th><th>bezahlt nach</th><th>Bilanz 15 J.</th></tr></thead>
<tbody>
<tr><td>4 kWh</td><td class="num">304 €<br>273 €</td><td class="num">6,6 J.<br>7,3 J.</td><td class="num">+2.556 €<br>+2.094 €</td></tr>
<tr class="hl"><td>6 kWh</td><td class="num">393 €<br>354 €</td><td class="num">7,6 J.<br>8,5 J.</td><td class="num">+2.899 €<br>+2.308 €</td></tr>
<tr><td>8 kWh</td><td class="num">443 €<br>399 €</td><td class="num">9,0 J.<br>10,0 J.</td><td class="num">+2.646 €<br>+1.984 €</td></tr>
<tr><td>10 kWh</td><td class="num">470 €<br>423 €</td><td class="num">10,6 J.<br>11,8 J.</td><td class="num">+2.053 €<br>+1.352 €</td></tr>
</tbody></table></div>
<p>Die beste Größe ist in allen Fällen 6 kWh. Der Unterschied liegt bei knapp 40 € Ersparnis im Jahr. Wer gerade eine PV-Anlage plant, muss wegen der Stromsteuer also nicht umplanen. Ein Speicher lohnt sich im Beispiel auch mit Senkung.</p>
<p>Mit E-Auto sieht es ähnlich aus. Lädt es 2.500 kWh im Jahr abends zu Hause, sind mit und ohne Senkung 10 kWh die beste Größe. Der 10-kWh-Speicher bezahlt sich dann in 7,9 Jahren ohne und in 8,8 Jahren mit dauerhafter Senkung.</p>

<h2>Wann du anders rechnen solltest</h2>
<ul>
<li>Dein Versorger senkt den Preis. Dann trag im Rechner deinen neuen Arbeitspreis ein. Ob die Senkung voll weitergegeben wird, ist offen; die Rechnung geht davon aus.</li>
<li>Dein Strompreis liegt deutlich über oder unter 33 ct. Dann zählt dein eigener Preis mehr als die Steuer.</li>
<li>Du hast eine Wärmepumpe. Dann trag ihren Strom im Rechner getrennt ein, sie verschiebt die beste Größe.</li>
<li>Du hast einen dynamischen Tarif. Den bildet der Rechner nicht ab, er rechnet mit festem Strompreis.</li>
</ul>
<p>„Senkung nur 2027“ heißt in der Rechnung: ein Jahr mit 30,68 ct, danach 14 Jahre mit 33 ct. Weitere Preisänderungen rechne ich nicht ein.</p>
""",
"faq": [
 ("Wie hoch ist die Stromsteuer für Haushalte?", "Heute 2,05 ct je kWh laut § 3 Stromsteuergesetz, plus 19 % Umsatzsteuer. Das sind rund 2,44 ct je kWh auf deiner Rechnung. Das EU-Minimum liegt bei 0,1 ct."),
 ("Wird die Stromsteuer 2027 gesenkt?", "Die Koalition hat sich am 18.11.2026 darauf geeinigt, sie 2027 für alle aufs EU-Minimum zu senken. Finanziert ist bisher nur 2027. Endgültig ist das erst, wenn Bundestag und Stromsteuergesetz mitziehen; der Haushalt soll am 27.11. beschlossen werden."),
 ("Lohnt sich ein Stromspeicher trotzdem?", "Ja. Im Beispiel bezahlt sich ein 6-kWh-Speicher in 7,7 Jahren, wenn die Senkung nur 2027 gilt, und in 8,5 Jahren, wenn sie bleibt. Ohne Senkung wären es 7,6 Jahre. Die beste Größe bleibt gleich."),
],
},
{
"slug": "stromspeicher-lohnt-sich-2027",
"kennzahl": {"v": "+2.899 €", "t": "Gewinn nach 15 Jahren mit 6 kWh, heute gerechnet"},
"chart": {"kind": "sweep", "title": "Gewinn nach 15 Jahren je Speichergröße", "caption": "9 kWp Süd, 4.500 kWh Verbrauch, Speicher 500 €/kWh, Strom 33 ct/kWh. Der Punkt markiert die wirtschaftlichste Größe.",
  "series": [{"label": "EEG heute (7,7 ct Einspeisung)", "p": {}}, {"label": "EEG-Reform (keine Vergütung, max. 50 % Einspeisung)", "p": {"feed": 0, "feedLimit": 0.5}}]},
"title": "Lohnt sich ein Stromspeicher 2027?",
"h1": "Lohnt sich ein Stromspeicher 2027?",
"desc": "Mit Zahlen statt Prospekt: Wann sich ein Stromspeicher für eine neue PV-Anlage rechnet, was die EEG-Reform ändert und welche Größe am meisten bringt.",
"date": "2026-11-09",
"updated": "2026-11-16",
"lead": "Kurze Antwort: Bei den heutigen Preisen meistens ja, wenn der Speicher nicht zu groß ist. Sollte die geplante EEG-Reform kommen, rechnet er sich sogar deutlich schneller.",
"body": """
<p>Ob sich ein Speicher lohnt, hängt an vier Zahlen: was er kostet, was dein Netzstrom kostet, was du für eingespeisten Strom bekommst und wie viel Solarstrom er dir zusätzlich nutzbar macht. Ich habe das für ein typisches Einfamilienhaus durchgerechnet: 9 kWp auf einem Süddach, 4.500 kWh Verbrauch im Jahr.</p>

<h2>Das Ergebnis mit den heutigen Regeln</h2>
<p>Ohne Speicher deckt die Anlage 36 % des Verbrauchs. Mit Speicher steigt das deutlich, aber jede weitere Kilowattstunde Kapazität bringt weniger als die vorherige.</p>
<div class="tablewrap"><table>
<thead><tr><th>Speicher</th><th>Autarkie</th><th>Ersparnis/Jahr</th><th>Amortisation</th><th>Bilanz nach 15 Jahren</th></tr></thead>
<tbody>
<tr><td>ohne</td><td class="num">36 %</td><td class="num">–</td><td class="num">–</td><td class="num">–</td></tr>
<tr><td>4 kWh</td><td class="num">65 %</td><td class="num">304 €</td><td class="num">6,6 Jahre</td><td class="num">+2.556 €</td></tr>
<tr class="hl"><td>6 kWh</td><td class="num">74 %</td><td class="num">393 €</td><td class="num">7,6 Jahre</td><td class="num">+2.899 €</td></tr>
<tr><td>8 kWh</td><td class="num">78 %</td><td class="num">443 €</td><td class="num">9,0 Jahre</td><td class="num">+2.646 €</td></tr>
<tr><td>10 kWh</td><td class="num">81 %</td><td class="num">470 €</td><td class="num">10,6 Jahre</td><td class="num">+2.053 €</td></tr>
<tr><td>15 kWh</td><td class="num">84 %</td><td class="num">504 €</td><td class="num">14,9 Jahre</td><td class="num">+55 €</td></tr>
</tbody></table></div>
<p>Am meisten bleibt bei 6 kWh übrig. Ein 15-kWh-Speicher macht das Haus kaum unabhängiger als einer mit 8 kWh, kostet aber fast doppelt so viel. Er braucht fast die vollen 15 Jahre, bis er seine Kosten wieder reingeholt hat. Übrig bleibt praktisch nichts.</p>

<h2>Was die EEG-Reform ändern würde</h2>
<p>Das Bundeskabinett hat am 29. Juli 2026 einen Entwurf für ein neues EEG beschlossen. Für neue kleine Dachanlagen soll die feste Einspeisevergütung nach einer Übergangszeit wegfallen. Außerdem darf nur noch höchstens die Hälfte der Anlagenleistung ins Netz. Bundestag und Bundesrat müssen noch zustimmen. Stand 16. November 2026: Beschlossen ist noch nichts. Union und SPD wollen die feste Einspeisevergütung für neue Anlagen bis 25 kW nun doch behalten (Reuters, 14.11.2026). Ob die 50-%-Grenze bleibt, ist offen. Wann der Bundestag abstimmt, steht noch nicht fest. Der Rechner zeigt die Reform deshalb weiter so, wie das Kabinett sie geplant hat.</p>
<p>Für den Speicher ist das eine gute Nachricht. Jede Kilowattstunde, die du selbst nutzt, spart weiter 33 ct. Eine eingespeiste bringt dann nichts mehr. Und Strom, der wegen der 50-%-Grenze gar nicht ins Netz darf, geht verloren, wenn ihn kein Speicher auffängt. Im Beispielhaus wären das rund 560 kWh im Jahr.</p>
<div class="tablewrap"><table>
<thead><tr><th>Szenario</th><th>Beste Größe</th><th>Ersparnis/Jahr</th><th>Amortisation</th><th>Bilanz nach 15 Jahren</th></tr></thead>
<tbody>
<tr><td>EEG heute</td><td class="num">6 kWh</td><td class="num">393 €</td><td class="num">7,6 Jahre</td><td class="num">+2.899 €</td></tr>
<tr><td>EEG-Reform</td><td class="num">7 kWh</td><td class="num">598 €</td><td class="num">5,9 Jahre</td><td class="num">+5.467 €</td></tr>
</tbody></table></div>

<h2>Was am stärksten zählt: der Speicherpreis</h2>
<p>Die Verbraucherzentrale nennt für 2026 eine Spanne von etwa 300 bis 700 € pro kWh inklusive Einbau. Das macht einen größeren Unterschied als fast alles andere:</p>
<ul>
<li><b>350 €/kWh:</b> beste Größe 7 kWh, bezahlt nach 5,8 Jahren</li>
<li><b>500 €/kWh:</b> beste Größe 6 kWh, bezahlt nach 7,6 Jahren</li>
<li><b>700 €/kWh:</b> beste Größe 5 kWh, bezahlt nach 9,9 Jahren</li>
</ul>
<p>Hol dir deshalb mindestens zwei Angebote und rechne den Preis pro kWh nutzbarer Kapazität aus. Wird der Speicher mit der PV-Anlage zusammen gekauft, ist er meist günstiger als beim Nachrüsten.</p>

<h2>Wann sich ein Speicher eher nicht lohnt</h2>
<ul>
<li>Der Verbrauch ist klein. Bei 3.000 kWh im Jahr rechnen sich nur 4 kWh, ein 8-kWh-Speicher braucht gut 12 Jahre.</li>
<li>Der Angebotspreis liegt deutlich über 700 €/kWh.</li>
<li>Du bist tagsüber zu Hause und verbrauchst den Solarstrom ohnehin direkt.</li>
</ul>

<h2>Und das E-Auto?</h2>
<p>Ein E-Auto mit 2.500 kWh im Jahr verschiebt die Rechnung. Lädt es meist abends, nutzt es den Speicher kräftig: Dann darf er größer sein, bis etwa 10 kWh. Lädt es tagsüber direkt vom Dach, reichen 7 kWh. Bevor du einen großen Speicher fürs Auto kaufst, prüf also, ob es nicht einfach tagsüber laden kann.</p>
""",
"faq": [
 ("Wie lange hält ein Stromspeicher?", "Hersteller geben meist 10 Jahre Garantie und 6.000 und mehr Ladezyklen an. Ich rechne mit 15 Jahren Nutzung."),
 ("Gibt es eine Förderung für Stromspeicher?", "Einen bundesweiten Zuschuss gibt es 2026 nicht. Auf Speicher mit einer PV-Anlage fällt aber keine Umsatzsteuer an, und manche Länder und Kommunen haben eigene Förderprogramme."),
 ("Wie groß sollte mein Speicher sein?", "Als grobe Regel rechnen sich etwa 1 bis 1,5 kWh Speicher je 1.000 kWh Jahresverbrauch. Genauer geht es mit dem Rechner, weil Ausrichtung, Verbrauch und Preise viel ausmachen."),
],
},
{
"slug": "speichergroesse-4500-kwh",
"kennzahl": {"v": "5–7 kWh", "t": "rechnen sich bei Süddach am besten"},
"chart": {"kind": "day", "title": "Ein Durchschnittstag mit 6 kWh Speicher", "caption": "9 kWp Süd, 4.500 kWh Verbrauch. Alles unter der schwarzen Linie versorgt das Haus, darüber geht der Überschuss in den Speicher oder ins Netz.",
  "p": {}, "cap": 6, "months": [5, 11]},
"title": "Welche Speichergröße bei 4.500 kWh Verbrauch?",
"h1": "Welche Speichergröße bei 4.500 kWh Verbrauch?",
"desc": "Bei 4.500 kWh Jahresverbrauch rechnet sich meist ein Speicher mit 5 bis 7 kWh. Die Zahlen für 6, 9 und 12 kWp und warum größer nicht besser ist.",
"date": "2026-11-09",
"updated": "2026-11-14",
"lead": "Bei 4.500 kWh Jahresverbrauch und einem Süddach rechnet sich meist ein Speicher mit 5 bis 7 kWh nutzbarer Kapazität. Mehr macht dich kaum unabhängiger, nur die Rechnung schlechter.",
"body": """
<p>4.500 kWh im Jahr ist typisch für eine Familie mit zwei Kindern ohne Wärmepumpe und ohne E-Auto. Viele Angebote kommen in diesem Fall mit 10 kWh Speicher oder mehr. Ich habe nachgerechnet, ab welcher Größe sich das nicht mehr lohnt.</p>

<h2>Die beste Größe je Anlagengröße</h2>
<div class="tablewrap"><table>
<thead><tr><th>PV-Anlage (Süd)</th><th>Beste Speichergröße</th><th>Amortisation</th><th>Autarkie mit Speicher</th><th>Zum Vergleich: 8 kWh</th></tr></thead>
<tbody>
<tr><td>6 kWp</td><td class="num">6 kWh</td><td class="num">8,1 Jahre</td><td class="num">67 %</td><td class="num">9,7 Jahre</td></tr>
<tr class="hl"><td>9 kWp</td><td class="num">6 kWh</td><td class="num">7,6 Jahre</td><td class="num">74 %</td><td class="num">9,0 Jahre</td></tr>
<tr><td>12 kWp</td><td class="num">6 kWh</td><td class="num">7,4 Jahre</td><td class="num">77 %</td><td class="num">8,7 Jahre</td></tr>
</tbody></table></div>
<p>Auffällig: Ob 6, 9 oder 12 kWp, die beste Speichergröße bleibt 6 kWh. Ab 9 kWp ist im Sommer ohnehin mehr Strom da, als das Haus abends und nachts verbraucht. Der Engpass ist der Verbrauch in der Nacht, nicht die Erzeugung.</p>

<h2>Warum ein großer Speicher im Winter nicht hilft</h2>
<p>Mit 8 kWh Speicher deckt das Beispielhaus im Juni seinen Verbrauch fast ganz selbst, im Dezember nur 38 %. Im Dezember erzeugt die Anlage rund 240 kWh, das Haus braucht 450 kWh. Was nicht erzeugt wird, kann auch kein Speicher speichern. Ein größerer Speicher macht nur im Sommer zusätzlichen Überschuss nutzbar, und davon gibt es dann schon genug.</p>

<h2>Die Faustregel</h2>
<p>Rund 1 bis 1,5 kWh Speicher je 1.000 kWh Jahresverbrauch. Bei 4.500 kWh sind das 4,5 bis 7 kWh. Meine Simulation landet genau in diesem Bereich.</p>
<p>Etwas größer darf es sein, wenn</p>
<ul>
<li>ein E-Auto meist abends oder nachts lädt,</li>
<li>die geplante EEG-Reform kommt (dann 7 statt 6 kWh),</li>
<li>du den Speicher deutlich günstiger als 500 €/kWh bekommst.</li>
</ul>
<p>Kleiner reicht, wenn dein Dach nach Osten und Westen zeigt oder du tagsüber viel zu Hause bist.</p>

<h2>Und bei anderem Verbrauch?</h2>
<ul>
<li><b>3.000 kWh:</b> beste Größe 4 kWh</li>
<li><b>4.500 kWh:</b> beste Größe 6 kWh</li>
<li><b>6.000 kWh:</b> beste Größe 8 kWh</li>
</ul>
<p>(jeweils 9 kWp Süd)</p>
""",
"faq": [
 ("Brutto oder netto: Welche Speichergröße ist gemeint?", "Ich rechne immer mit der nutzbaren Kapazität. Manche Angebote nennen die Bruttokapazität, die 5 bis 10 % höher liegt. Frag im Zweifel nach."),
 ("Kann ich den Speicher später erweitern?", "Viele Systeme sind modular und lassen sich um weitere Batteriemodule ergänzen. Das ist ein guter Weg, mit 5 bis 6 kWh zu starten und erst bei E-Auto oder Wärmepumpe zu erweitern."),
],
},
{
"slug": "ost-west-dach-speicher",
"kennzahl": {"v": "5 kWh", "t": "reichen bei Ost-West, bei Süd sind es 6"},
"chart": {"kind": "sweep", "title": "Gewinn nach 15 Jahren: Süd gegen Ost-West", "caption": "Je 9 kWp, 35° Neigung, 4.500 kWh Verbrauch, Speicher 500 €/kWh, Strom 33 ct/kWh, Einspeisung 7,7 ct.",
  "series": [{"label": "Süd", "p": {}}, {"label": "Ost-West", "p": {"roofs": [{"kwp": 4.5, "tilt": 35, "aspect": -90}, {"kwp": 4.5, "tilt": 35, "aspect": 90}]}}]},
"title": "Ost-West-Dach: Braucht es einen Speicher?",
"h1": "Ost-West-Dach: Braucht es einen Speicher?",
"desc": "Eine Ost-West-Anlage liefert morgens und abends Strom. Deshalb reicht meist ein kleinerer Speicher als bei Süd. Die Zahlen im Vergleich.",
"date": "2026-11-09",
"updated": "2026-11-14",
"lead": "Ja, aber einen kleineren. Bei einer Ost-West-Anlage rechnet sich meist ein Speicher mit etwa 5 kWh, bei einem Süddach mit gleicher Leistung eher 6 kWh.",
"body": """
<p>Ost-West-Dächer gelten oft als zweite Wahl. Für den Eigenverbrauch sind sie aber besser als ihr Ruf: Sie liefern morgens und am späten Nachmittag Strom, also dann, wenn im Haus Kaffeemaschine, Herd und Waschmaschine laufen.</p>

<h2>Süd gegen Ost-West im Vergleich</h2>
<p>Beide Anlagen haben 9 kWp, 35° Neigung, das Haus verbraucht 4.500 kWh. Bei Ost-West ist die Leistung je zur Hälfte auf beide Dachseiten verteilt.</p>
<div class="tablewrap"><table>
<thead><tr><th></th><th>Süd</th><th>Ost-West</th></tr></thead>
<tbody>
<tr><td>Erzeugung pro Jahr</td><td class="num">9.040 kWh</td><td class="num">7.000 kWh</td></tr>
<tr><td>Solarstrom, der ohne Speicher im Haus bleibt</td><td class="num">18 %</td><td class="num">23 %</td></tr>
<tr><td>Wirtschaftlichste Speichergröße</td><td class="num">6 kWh</td><td class="num">5 kWh</td></tr>
<tr><td>Amortisation dieser Größe</td><td class="num">7,6 Jahre</td><td class="num">7,8 Jahre</td></tr>
<tr><td>Amortisation mit 8 kWh</td><td class="num">9,0 Jahre</td><td class="num">10,9 Jahre</td></tr>
</tbody></table></div>
<p>Ost-West erzeugt bei gleicher Leistung gut ein Fünftel weniger, verteilt den Strom aber gleichmäßiger über den Tag. Mittags bleibt weniger Überschuss übrig, der in einen Speicher gehen könnte. Deshalb lohnt sich ein großer Speicher hier noch weniger als bei Süd.</p>

<h2>Der teure Fehler</h2>
<p>Ein 8-kWh-Speicher an einer Ost-West-Anlage kostet 1.500 € mehr als einer mit 5 kWh, bringt pro Jahr aber nur rund 45 € zusätzlich. Nach 15 Jahren bleiben rund 800 € weniger übrig. Er braucht fast 11 Jahre, bis er sich bezahlt hat. Wenn dir ein Angebot für ein Ost-West-Dach einen großen Speicher vorschlägt, frag nach dem Grund.</p>

<h2>Mehr Fläche statt mehr Speicher</h2>
<p>Ein Ost-West-Dach bietet oft mehr Platz als eine einzelne Südseite. Bei 12 kWp Ost-West ist die beste Speichergröße immer noch 5 kWh, bei einer Amortisation von 7,4 Jahren. Statt mehr Speicher lohnt sich hier eher mehr Modulfläche.</p>

<h2>Mit der EEG-Reform</h2>
<p>Fällt die Einspeisevergütung weg, bleibt es bei Ost-West bei 5 kWh, der Speicher rechnet sich aber schneller: nach etwa 5,4 statt 7,8 Jahren. Die 50-%-Grenze trifft Ost-West kaum, weil die Anlage mittags nie ihre volle Leistung erreicht.</p>
""",
"faq": [
 ("Lohnt sich Ost-West überhaupt?", "Ja. Die Erzeugung ist etwas geringer, aber der Strom kommt zu Zeiten, in denen du ihn brauchst, und die Fläche ist oft größer. Für den Eigenverbrauch ist Ost-West oft eine sehr gute Wahl."),
 ("Brauche ich bei Ost-West zwei Wechselrichter?", "Meist nicht. Moderne Wechselrichter haben zwei getrennte Eingänge, einen für jede Dachseite."),
],
},
{
"slug": "stromspeicher-nachruesten",
"kennzahl": {"v": "unter 8 ct", "t": "Einspeisevergütung: Dann lohnt sich Nachrüsten meist"},
"chart": {"kind": "sweep", "title": "Nachrüsten: Gewinn nach 15 Jahren je Einspeisevergütung", "caption": "7 kWp Süd, 4.500 kWh Verbrauch, Speicher 700 €/kWh (Nachrüsten), Strom 33 ct/kWh.",
  "series": [{"label": "0 ct", "p": {"roofs": [{"kwp": 7, "tilt": 35, "aspect": 0}], "bprice": 700, "feed": 0}}, {"label": "7,7 ct", "p": {"roofs": [{"kwp": 7, "tilt": 35, "aspect": 0}], "bprice": 700, "feed": 7.7}}, {"label": "12 ct", "p": {"roofs": [{"kwp": 7, "tilt": 35, "aspect": 0}], "bprice": 700, "feed": 12}}, {"label": "20 ct", "p": {"roofs": [{"kwp": 7, "tilt": 35, "aspect": 0}], "bprice": 700, "feed": 20}}]},
"title": "Stromspeicher nachrüsten: Lohnt sich das?",
"h1": "Stromspeicher nachrüsten: Lohnt sich das?",
"desc": "Ob sich ein Speicher für deine bestehende PV-Anlage lohnt, entscheidet vor allem deine Einspeisevergütung. Ab etwa 12 ct wird es knapp, bei 20 ct nie.",
"date": "2026-11-09",
"updated": "2026-11-14",
"lead": "Kurze Antwort: Das hängt vor allem an deiner Einspeisevergütung. Bekommst du unter 8 ct pro kWh, lohnt sich ein kleiner Speicher meist. Bekommst du 20 ct oder mehr, lohnt er sich nicht.",
"body": """
<p>Du hast schon eine PV-Anlage und überlegst, einen Speicher dazuzukaufen? Dann ist die Rechnung anders als bei einer neuen Anlage. Der Speicher spart dir Netzstrom, aber jede Kilowattstunde, die er auffängt, speist du nicht mehr ein. Je mehr du fürs Einspeisen bekommst, desto weniger bleibt übrig.</p>
<p>Mein Beispiel: eine 7-kWp-Anlage auf einem Süddach, 4.500 kWh Verbrauch im Jahr, Strompreis 33 ct. Weil Nachrüsten oft teurer ist als der Kauf zusammen mit der Anlage, rechne ich hier mit 700 €/kWh statt 500 €/kWh.</p>

<h2>Deine Einspeisevergütung entscheidet</h2>
<div class="tablewrap"><table>
<thead><tr><th>Deine Vergütung</th><th>Beste Speichergröße</th><th>Ersparnis/Jahr</th><th>Amortisation</th><th>Bilanz nach 15 Jahren</th></tr></thead>
<tbody>
<tr class="hl"><td>0 ct (keine Vergütung mehr)</td><td class="num">6 kWh</td><td class="num">542 €</td><td class="num">7,8 Jahre</td><td class="num">+3.929 €</td></tr>
<tr><td>7,7 ct</td><td class="num">5 kWh</td><td class="num">344 €</td><td class="num">10,2 Jahre</td><td class="num">+1.657 €</td></tr>
<tr><td>12 ct</td><td class="num">4 kWh</td><td class="num">221 €</td><td class="num">12,7 Jahre</td><td class="num">+510 €</td></tr>
<tr><td>20 ct</td><td class="num">keine</td><td class="num">–</td><td class="num">–</td><td class="num">jede Größe im Minus</td></tr>
</tbody></table></div>
<p>Bei 20 ct Vergütung bringt selbst ein 5-kWh-Speicher nur rund 100 € im Jahr. Er bräuchte über 30 Jahre, bis er bezahlt ist. Der Grund: Jede gespeicherte Kilowattstunde spart dir 33 ct, kostet dich aber 20 ct Vergütung. Dazu kommen Verluste beim Laden und Entladen. Da bleibt kaum etwas.</p>
<p>Deine Vergütung steht auf der Jahresabrechnung deines Netzbetreibers. Sie hängt davon ab, wann deine Anlage in Betrieb ging.</p>

<h2>Wenn die feste Vergütung ausläuft</h2>
<p>Die EEG-Vergütung gibt es 20 Jahre lang, plus den Rest des Jahres, in dem die Anlage in Betrieb ging. Danach bekommst du für eingespeisten Strom deutlich weniger. Wie viel genau, hängt vom Marktwert und deinem Abnehmer ab. Ich rechne hier den ungünstigsten Fall mit 0 ct.</p>
<p>Dann sieht es ganz anders aus: Der Speicher rechnet sich in knapp 8 Jahren, auch bei 700 €/kWh. Wenn deine Anlage bald aus der Vergütung fällt, ist das der beste Zeitpunkt für einen Speicher. Prüf aber vorher, ob Module und Wechselrichter noch einige Jahre durchhalten.</p>

<h2>Was der Preis ausmacht</h2>
<p>Gleiche Anlage, Vergütung 7,7 ct. Nur der Speicherpreis ändert sich:</p>
<div class="tablewrap"><table>
<thead><tr><th>Preis inkl. Einbau</th><th>Beste Größe</th><th>Amortisation</th><th>Bilanz nach 15 Jahren</th><th>Zum Vergleich: 10 kWh</th></tr></thead>
<tbody>
<tr><td>500 €/kWh</td><td class="num">6 kWh</td><td class="num">7,9 Jahre</td><td class="num">+2.699 €</td><td class="num">11,1 Jahre</td></tr>
<tr class="hl"><td>700 €/kWh</td><td class="num">5 kWh</td><td class="num">10,2 Jahre</td><td class="num">+1.657 €</td><td class="num">15,6 Jahre</td></tr>
<tr><td>900 €/kWh</td><td class="num">4 kWh</td><td class="num">12,3 Jahre</td><td class="num">+807 €</td><td class="num">20,0 Jahre</td></tr>
</tbody></table></div>
<p>Beim Nachrüsten gilt noch mehr als beim Neukauf: lieber klein. Ein 10-kWh-Speicher holt seine Kosten ab 700 €/kWh in 15 Jahren nicht mehr rein.</p>

<h2>Wann sich Nachrüsten eher nicht lohnt</h2>
<ul>
<li>Du bekommst 12 ct oder mehr für eingespeisten Strom und die Vergütung läuft noch viele Jahre.</li>
<li>Deine Anlage speist voll ein. Ein Speicher hilft nur, wenn du den Strom selbst verbrauchst.</li>
<li>Die Anlage ist alt und der Wechselrichter muss bald ohnehin getauscht werden. Dann rechne beides zusammen und hol ein Angebot für das Gesamtpaket.</li>
</ul>

<h2>Was das Modell nicht abbildet</h2>
<p>Viele Nachrüst-Speicher haben einen eigenen Wechselrichter (AC-gekoppelt). Dabei wird der Strom öfter umgewandelt, das kostet etwas Wirkungsgrad. Der Rechner rechnet für alle Speicher mit 88 % je Zyklus. Er weiß auch nicht, wie lange deine Module und dein Wechselrichter noch halten. Die geplante EEG-Reform betrifft laut Entwurf neue Anlagen, nicht deine bestehende.</p>
""",
"faq": [
 ("Kann ich an jede PV-Anlage einen Speicher nachrüsten?", "Meist ja. Hat dein Wechselrichter keinen Anschluss für einen Speicher, gibt es Speicher mit eigenem Wechselrichter. Die schließt ein Elektriker am Hausnetz an."),
 ("Wo finde ich meine Einspeisevergütung?", "Auf der Jahresabrechnung deines Netzbetreibers. Dort steht der Satz in Cent pro Kilowattstunde. Gib ihn im Rechner unter Einspeisevergütung ein."),
 ("Lohnt sich ein Speicher nach 20 Jahren EEG?", "Oft ja. Ohne feste Vergütung ist jede selbst genutzte Kilowattstunde viel mehr wert als eine eingespeiste. Im Beispiel rechnet sich ein 5-kWh-Speicher dann in gut 7 Jahren, ein 6-kWh-Speicher in knapp 8."),
],
},
{
"slug": "pv-angebot-pruefen",
"kennzahl": {"v": "6 statt 10 kWh", "t": "Speichergröße, die im Beispiel am meisten bringt"},
"bars": {"title": "Bilanz nach 15 Jahren je Speichergröße", "caption": "Angebot: 10 kWh für 6.500 €. Am meisten bleibt bei 6 kWh übrig.",
         "rows": [["4 kWh", 858], ["5 kWh", 1105], ["6 kWh", 1219], ["7 kWh", 1180], ["8 kWh", 1056], ["10 kWh", 553, "Angebot"]], "best": "6 kWh", "mark": "10 kWh"},
"title": "PV-Angebot prüfen: Ist der Speicher zu groß?",
"h1": "PV-Angebot prüfen: Ist der Speicher zu groß?",
"desc": "Im Beispiel bringt ein 6-kWh-Speicher in 15 Jahren rund 670 € mehr als die angebotenen 10 kWh. So prüfst du dein PV-Angebot, bevor du unterschreibst.",
"date": "2026-11-10",
"updated": "2026-11-14",
"lead": "Oft ja. In meinem Beispielhaushalt mit 4.500 kWh Verbrauch steht ein 10-kWh-Speicher im Angebot, am meisten bringt aber einer mit 6 kWh. Der kleinere spart pro Jahr etwas weniger, kostet dafür deutlich weniger.",
"body": """
<p>Mein Beispiel: 9 kWp auf einem Süddach mit 35° Neigung im Ruhrgebiet, 4.500 kWh Verbrauch im Jahr, Strompreis 33 ct, Einspeisevergütung 7,70 ct. Im Angebot steht ein Speicher mit 10 kWh nutzbarer Kapazität und 5 kW Leistung. Der Aufpreis für den Speicher beträgt 6.500 €, also 650 €/kWh.</p>

<h2>Warum Angebote oft größer ausfallen</h2>
<p>Ein größerer Speicher fängt im Sommer mehr Strom ab. Das sieht im Prospekt gut aus. Im Winter wird er aber selten voll, weil die Anlage dann kaum Überschuss hat. Jede zusätzliche Kilowattstunde Speicher bringt deshalb weniger als die vorherige. Ab einer bestimmten Größe kostet sie mehr, als sie über die Jahre spart.</p>
<p>Das ist kein Vorwurf an den Installateur. Viele Systeme gibt es nur in festen Stufen, und manche Haushalte planen später ein E-Auto. Du solltest nur wissen, welche Größe für deinen Verbrauch reicht.</p>

<h2>Beispielrechnung: 10 kWh im Angebot</h2>
<!--BARS-->
<div class="tablewrap"><table>
<thead><tr><th>Speicher</th><th>Ersparnis/Jahr</th><th>Kosten</th><th>Bilanz nach 15 Jahren</th></tr></thead>
<tbody>
<tr><td>4 kWh</td><td class="num">309 €</td><td class="num">3.770 €</td><td class="num">+858 €</td></tr>
<tr><td>5 kWh</td><td class="num">355 €</td><td class="num">4.225 €</td><td class="num">+1.105 €</td></tr>
<tr class="hl"><td>6 kWh</td><td class="num">393 €</td><td class="num">4.680 €</td><td class="num">+1.219 €</td></tr>
<tr><td>7 kWh</td><td class="num">421 €</td><td class="num">5.135 €</td><td class="num">+1.180 €</td></tr>
<tr><td>8 kWh</td><td class="num">443 €</td><td class="num">5.590 €</td><td class="num">+1.056 €</td></tr>
<tr><td>10 kWh (Angebot)</td><td class="num">470 €</td><td class="num">6.500 €</td><td class="num">+553 €</td></tr>
</tbody></table></div>
<p>Die Kosten der kleineren Speicher habe ich aus dem Angebot heruntergerechnet. Dabei gilt: Rund 30 % des Preises sinken nicht mit der Größe, etwa Wechselrichter, Montage und Anschluss.</p>
<p>Der 10-kWh-Speicher spart nur 77 € pro Jahr mehr als der mit 6 kWh. Dafür kostet er 1.820 € mehr. Über 15 Jahre bleiben beim kleineren Speicher rund 670 € mehr übrig. Zwischen 5 und 7 kWh liegt die Bilanz eng beieinander. Diese Spanne passt zum Beispielhaushalt.</p>

<h2>Diese Angaben brauchst du aus dem Angebot</h2>
<ul>
<li><b>Nutzbare Kapazität</b>, nicht brutto. Brutto ist die Gesamtkapazität, nutzbar etwas weniger. Steht nur eine Zahl da, frag nach.</li>
<li><b>Aufpreis für den Speicher.</b> Steht oft als eigene Position. Fehlt er, frag nach dem Preis derselben Anlage ohne Speicher.</li>
<li><b>Lade- und Entladeleistung</b> in kW.</li>
<li><b>Dein Jahresverbrauch</b> von der letzten Stromrechnung, dazu E-Auto oder Wärmepumpe, wenn sie geplant sind.</li>
</ul>
<p>Mit diesen Werten ordnet der <a href="../pro/" data-umami-event="artikel-zu-pro" data-umami-event-artikel="pv-angebot-pruefen">Angebots-Check</a> dein Angebot kostenlos ein.</p>

<h2>Wann ein großer Speicher doch passt</h2>
<p>Mit einem E-Auto, das meist abends lädt, sieht es anders aus. Kommen im Beispiel 2.500 kWh fürs Auto dazu, passt das 10-kWh-Angebot. Lädt das Auto meist tagsüber direkt aus der Anlage, braucht es weniger Speicher.</p>
<p>Ein höherer Strompreis oder ein günstigerer Speicherpreis verschieben die passende Größe ebenfalls nach oben.</p>

<h2>Was du den Installateur fragen kannst</h2>
<ul>
<li>Gibt es dasselbe System mit 5 oder 6 kWh, und was kostet es dann?</li>
<li>Ist der Speicher modular, und was kostet später ein weiteres Modul?</li>
<li>Welche Garantie gibt es auf die Restkapazität?</li>
<li>Ist Notstrom oder Ersatzstrom enthalten, und was kostet er extra?</li>
</ul>

<h2>Was das Modell nicht abbildet</h2>
<p>Die Rechnung kennt keine Verschattung, keine Alterung des Speichers und keinen Notstrom. Eine Wärmepumpe trägst du im kostenlosen Rechner und im Angebots-Check getrennt ein.</p>
""",
"faq": [
 ("Wie groß sollte ein Speicher bei 4.500 kWh sein?", "Im Beispiel mit 9 kWp lohnen sich 5 bis 7 kWh am meisten. Mit E-Auto oder anderer Dachausrichtung kann es anders aussehen."),
 ("Ist ein zu großer Speicher schlimm?", "Er schadet nicht, kostet aber mehr, als er zusätzlich spart. Im Beispiel bleiben mit 10 statt 6 kWh rund 670 € weniger übrig."),
 ("Woran erkenne ich, ob das Angebot brutto oder nutzbar angibt?", "Am Datenblatt des Speichers. Dort stehen beide Werte. Im Angebot fehlt die Angabe oft."),
],
},
{
"slug": "stromspeicher-groesse-berechnen",
"kennzahl": {"v": "1 kWh", "t": "Speicher je 1.000 kWh Jahresverbrauch trifft meist die beste Größe"},
"chart": {"kind": "sweep", "title": "Gewinn nach 15 Jahren je Speichergröße und Verbrauch", "caption": "9 kWp Süd, 35°, Speicher 500 €/kWh, Strom 33 ct/kWh, Einspeisung 7,7 ct, 15 Jahre. Der Punkt markiert die wirtschaftlichste Größe.",
  "series": [{"label": "3.000 kWh Verbrauch", "p": {"cons": 3000}}, {"label": "4.500 kWh", "p": {}}, {"label": "6.000 kWh", "p": {"cons": 6000}}]},
"title": "Stromspeicher-Größe berechnen: Wie viel kWh brauche ich?",
"seo_title": "Stromspeicher-Größe berechnen: Wie viel kWh?",
"h1": "Stromspeicher-Größe berechnen: Wie viel kWh brauche ich?",
"desc": "Faustregel: 1 kWh Speicher je 1.000 kWh Verbrauch. Die Regel „1 kWh je kWp“ kostet bei großen Anlagen über 1.000 €. Tabelle für 3.000 bis 6.000 kWh.",
"date": "2026-11-12",
"updated": "2026-11-14",
"lead": "Rechne mit deinem Verbrauch, nicht mit der Anlagengröße. Rund 1 kWh nutzbarer Speicher je 1.000 kWh Jahresverbrauch liegt fast immer nah an der wirtschaftlichsten Größe. Die oft genannte Regel „1 kWh je kWp“ führt bei großen Anlagen zu Speichern, die sich kaum noch rechnen.",
"body": """
<p>Ob du Stromspeicher, Batteriespeicher, PV-Speicher oder Solarspeicher liest: Gemeint ist dasselbe, eine Batterie im Haus, die Solarstrom vom Mittag für den Abend aufhebt. Für ihre Größe kursieren drei Faustformeln. Ich habe alle drei gegen eine Jahressimulation in 5-Minuten-Schritten gerechnet.</p>

<h2>Drei Faustformeln im Test</h2>
<ul>
<li><b>1 kWh je 1.000 kWh Jahresverbrauch</b></li>
<li><b>1,5 kWh je 1.000 kWh Jahresverbrauch</b></li>
<li><b>1 kWh je kWp Anlagenleistung</b></li>
</ul>
<p>Für den typischen Haushalt mit 4.500 kWh und 9 kWp Süd ergibt sich:</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Regel</th><th>Speichergröße</th><th>Bilanz nach 15 Jahren</th></tr></thead>
<tbody>
<tr class="hl"><td>Simulation (beste Größe)</td><td class="num">6 kWh</td><td class="num">+2.899 €</td></tr>
<tr><td>1 kWh je 1.000 kWh</td><td class="num">5 kWh</td><td class="num">+2.830 €</td></tr>
<tr><td>1,5 kWh je 1.000 kWh</td><td class="num">7 kWh</td><td class="num">+2.815 €</td></tr>
<tr><td>1 kWh je kWp</td><td class="num">9 kWh</td><td class="num">+2.385 €</td></tr>
</tbody></table></div>
<p>Die beiden Verbrauchs-Regeln liegen nur rund 70 bis 85 € neben dem besten Wert. Die kWp-Regel verschenkt schon hier rund 510 €.</p>

<h2>Wo die kWp-Regel richtig teuer wird</h2>
<p>Je größer die Anlage im Verhältnis zum Verbrauch, desto weiter liegt „1 kWh je kWp“ daneben. Die Tabelle zeigt die Bilanz nach 15 Jahren für neun Kombinationen:</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Verbrauch, Anlage</th><th>Beste Größe</th><th>Regel 1 kWh je 1.000 kWh</th><th>Regel 1 kWh je kWp</th></tr></thead>
<tbody>
<tr><td>3.000 kWh<br>6 kWp</td><td class="num">4 kWh<br>+1.711 €</td><td class="num">3 kWh<br>+1.568 €</td><td class="num">6 kWh<br>+1.395 €</td></tr>
<tr><td>3.000 kWh<br>9 kWp</td><td class="num">4 kWh<br>+1.858 €</td><td class="num">3 kWh<br>+1.687 €</td><td class="num">9 kWh<br>+536 €</td></tr>
<tr><td>3.000 kWh<br>12 kWp</td><td class="num">5 kWh<br>+1.907 €</td><td class="num">3 kWh<br>+1.696 €</td><td class="num">12 kWh<br>−640 €</td></tr>
<tr><td>4.500 kWh<br>6 kWp</td><td class="num">6 kWh<br>+2.550 €</td><td class="num">5 kWh<br>+2.528 €</td><td class="num">6 kWh<br>+2.550 €</td></tr>
<tr class="hl"><td>4.500 kWh<br>9 kWp</td><td class="num">6 kWh<br>+2.899 €</td><td class="num">5 kWh<br>+2.830 €</td><td class="num">9 kWh<br>+2.385 €</td></tr>
<tr><td>4.500 kWh<br>12 kWp</td><td class="num">6 kWh<br>+3.050 €</td><td class="num">5 kWh<br>+2.960 €</td><td class="num">12 kWh<br>+1.533 €</td></tr>
<tr><td>6.000 kWh<br>6 kWp</td><td class="num">7 kWh<br>+3.179 €</td><td class="num">6 kWh<br>+3.109 €</td><td class="num">6 kWh<br>+3.109 €</td></tr>
<tr><td>6.000 kWh<br>9 kWp</td><td class="num">8 kWh<br>+3.787 €</td><td class="num">6 kWh<br>+3.634 €</td><td class="num">9 kWh<br>+3.680 €</td></tr>
<tr><td>6.000 kWh<br>12 kWp</td><td class="num">8 kWh<br>+4.085 €</td><td class="num">6 kWh<br>+3.865 €</td><td class="num">12 kWh<br>+3.294 €</td></tr>
</tbody></table></div>
<p>Die Verbrauchs-Regel liegt höchstens rund 220 € neben dem besten Wert. Die kWp-Regel kostet bei 4.500 kWh und 12 kWp rund 1.520 €. Bei 3.000 kWh und 12 kWp holt der 12-kWh-Speicher seine Kosten in 15 Jahren gar nicht rein.</p>

<h2>Warum die Anlagengröße kaum zählt</h2>
<p>Ein Speicher lohnt sich nur mit dem Strom, den du abends und nachts verbrauchst. Der hängt an deinem Haushalt, nicht am Dach. Im Sommer liefert schon eine mittelgroße Anlage mehr, als das Haus abends und nachts braucht. Eine größere Anlage füllt den Speicher nur früher am Tag, und im Winter reicht der Strom vom Dach trotzdem nicht. Bei 4.500 kWh Verbrauch ist die beste Größe deshalb mit 9 kWp und mit 12 kWp dieselbe: 6 kWh.</p>

<h2>Warum größer trotzdem verlockend aussieht</h2>
<p>Mit 10 statt 6 kWh steigt die Autarkie im Beispiel von 74 auf 81 %. Das klingt nach viel. In Euro sind es 77 € Ersparnis mehr pro Jahr, dafür kostet der Speicher 2.000 € mehr. Nach 15 Jahren bleiben mit 10 kWh rund 850 € weniger übrig als mit 6 kWh. Wer ein Angebot mit großem Speicher hat, findet die Rechnung dazu unter <a href="pv-angebot-pruefen.html">PV-Angebot prüfen</a>.</p>

<h2>Wann die Faustformel nicht passt</h2>
<ul>
<li><b>E-Auto, das abends lädt:</b> Mit 2.500 kWh fürs Auto zusätzlich lohnen sich im Beispiel 10 kWh. Lädt das Auto meist tagsüber, sind es 7 kWh.</li>
<li><b>Ost-West-Dach:</b> Die Anlage liefert morgens und abends selbst Strom, im Beispiel reichen 5 kWh. Mehr dazu im Artikel <a href="ost-west-dach-speicher.html">Ost-West-Dach</a>.</li>
<li><b>Speicherpreis:</b> Bei 400 €/kWh lohnen sich 7 kWh, bei 700 €/kWh nur 5 kWh.</li>
<li><b>Wärmepumpe:</b> Ihr Verbrauch fällt vor allem im Winter an, wenn die Anlage wenig liefert. Mit 3.500 kWh Wärmepumpe zusätzlich lohnen sich im Beispiel 7 kWh statt 6, es bleibt aber weniger übrig: 2.534 € statt 2.899 €. Trag sie im Rechner getrennt ein, statt sie in die Faustformel zu rechnen.</li>
</ul>
<p>Was das Modell außerdem nicht abbildet: Notstrom, Verschattung, Alterung des Speichers und dynamische Stromtarife.</p>
""",
"faq": [
 ("Wie viel kWh Speicher brauche ich bei 10 kWp?", "Das hängt vom Verbrauch ab, nicht von den 10 kWp. Im Beispiel mit Süddach: 4 kWh bei 3.000 kWh, 6 kWh bei 4.500 kWh und 8 kWh bei 6.000 kWh Jahresverbrauch."),
 ("Gilt die Faustformel für brutto oder nutzbare Kapazität?", "Für die nutzbare Kapazität. Die Bruttokapazität im Datenblatt liegt meist etwas höher. Steht im Angebot nur eine Zahl, frag nach."),
 ("Ist ein etwas zu großer Speicher schlimm?", "Im Standard-Beispiel (4.500 kWh, 9 kWp) kostet 1 kWh mehr oder weniger rund 70 bis 85 €. Teuer wird es erst, wenn der Speicher deutlich größer ist, als der Verbrauch am Abend und in der Nacht hergibt."),
],
},
{
"slug": "stromspeicher-preis-pro-kwh",
"kennzahl": {"v": "rund 700 €", "t": "je kWh: ab da bringt ein 10-kWh-Speicher im Beispiel nach 15 Jahren nichts mehr"},
"related": ["pv-angebot-pruefen", "stromspeicher-groesse-berechnen", "stromspeicher-lohnt-sich-2027"],
"chart": {"kind": "sweep", "title": "Gewinn nach 15 Jahren je Speichergröße und Speicherpreis", "caption": "9 kWp Süd, 35°, 4.500 kWh, Strom 33 ct/kWh, Einspeisung 7,7 ct, 15 Jahre. Der Punkt markiert die wirtschaftlichste Größe.",
  "series": [{"label": "400 €/kWh", "p": {"bprice": 400}}, {"label": "500 €/kWh", "p": {}}, {"label": "700 €/kWh", "p": {"bprice": 700}}]},
"title": "Was darf ein Stromspeicher pro kWh kosten?",
"h1": "Was darf ein Stromspeicher pro kWh kosten?",
"desc": "Im Beispiel bringt ein 10-kWh-Speicher ab rund 700 € je kWh nach 15 Jahren nichts mehr. Je teurer der Speicher, desto kleiner sollte er sein.",
"date": "2026-11-16",
"lead": "Das hängt an der Größe. Im Beispielhaushalt mit 4.500 kWh macht sich ein 6-kWh-Speicher bis rund 980 € je kWh gerade noch bezahlt, ein 10-kWh-Speicher nur bis rund 700 €. Je teurer die Kilowattstunde Speicher, desto kleiner ist die Größe, bei der am meisten übrig bleibt.",
"body": """
<p>Mein Beispiel: 9 kWp auf einem Süddach mit 35° Neigung im Ruhrgebiet, 4.500 kWh Verbrauch im Jahr, Strompreis 33 ct, Einspeisevergütung 7,70 ct, 15 Jahre Lebensdauer. Ich hab's mit dem Speicherklar-Rechner durchgerechnet und nur den Speicherpreis verändert. Gemeint ist immer der Preis je kWh <b>nutzbarer</b> Kapazität, inklusive Einbau.</p>

<h2>Speicherpreis und beste Größe</h2>
<p>Was ein Stromspeicher einer bestimmten Größe im Jahr spart, hängt nicht von seinem Preis ab. Das gilt für jeden Batteriespeicher, PV-Speicher oder Solarspeicher. Der Preis entscheidet nur, bei welcher Größe nach 15 Jahren am meisten übrig bleibt:</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Preis je kWh</th><th>Beste Größe</th><th>Bezahlt nach</th><th>Bilanz nach 15 Jahren</th></tr></thead>
<tbody>
<tr><td>300 €</td><td class="num">8 kWh</td><td class="num">5,4 Jahren</td><td class="num">+4.246 €</td></tr>
<tr><td>400 €</td><td class="num">7 kWh</td><td class="num">6,7 Jahren</td><td class="num">+3.515 €</td></tr>
<tr class="hl"><td>500 €</td><td class="num">6 kWh</td><td class="num">7,6 Jahren</td><td class="num">+2.899 €</td></tr>
<tr><td>600 €</td><td class="num">5 kWh</td><td class="num">8,4 Jahren</td><td class="num">+2.330 €</td></tr>
<tr><td>700 €</td><td class="num">5 kWh</td><td class="num">9,9 Jahren</td><td class="num">+1.830 €</td></tr>
<tr><td>800 €</td><td class="num">4 kWh</td><td class="num">10,5 Jahren</td><td class="num">+1.356 €</td></tr>
<tr><td>1.000 €</td><td class="num">3 kWh</td><td class="num">12,6 Jahren</td><td class="num">+558 €</td></tr>
</tbody></table></div>
<p>Ein teurer Speicher ist also nicht gleich ein Fehlkauf. Du solltest dann nur kleiner kaufen. Bei 700 € je kWh bringen 5 kWh nach 15 Jahren noch rund 1.830 €, ein 10-kWh-Speicher zum selben Preis kommt gerade auf +53 €.</p>

<h2>Bis zu welchem Preis rechnet sich welche Größe?</h2>
<p>Jede Größe hat einen Höchstpreis. Darüber holt der Speicher seine Kosten in 15 Jahren nicht mehr herein. Ohne Zinsen, mit gleichbleibendem Strompreis:</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Speicher</th><th>Ersparnis pro Jahr</th><th>Höchstpreis je kWh</th></tr></thead>
<tbody>
<tr><td>4 kWh</td><td class="num">304 €</td><td class="num">1.139 €</td></tr>
<tr><td>5 kWh</td><td class="num">355 €</td><td class="num">1.066 €</td></tr>
<tr class="hl"><td>6 kWh</td><td class="num">393 €</td><td class="num">983 €</td></tr>
<tr><td>7 kWh</td><td class="num">421 €</td><td class="num">902 €</td></tr>
<tr><td>8 kWh</td><td class="num">443 €</td><td class="num">831 €</td></tr>
<tr><td>10 kWh</td><td class="num">470 €</td><td class="num">705 €</td></tr>
<tr><td>12 kWh</td><td class="num">487 €</td><td class="num">609 €</td></tr>
</tbody></table></div>
<p>Der Höchstpreis heißt: Bilanz genau null nach 15 Jahren. Willst du am Ende etwas übrig haben, musst du deutlich darunter bleiben. Für einen 10-kWh-Speicher liegt die Grenze bei rund 700 €, für 12 kWh schon bei rund 610 €.</p>
<p>Warum große Speicher so schnell an die Grenze kommen, siehst du an den Zyklen. Jede zusätzliche kWh wird seltener voll. Der 6-kWh-Speicher macht im Beispiel rund 283 volle Zyklen im Jahr, der mit 10 kWh nur rund 201. Eine Kilowattstunde aus dem Speicher ist dabei rund 23 ct wert, nicht 33 ct. Ohne Speicher hättest du den Strom für 7,70 ct eingespeist, und ein Teil geht beim Laden und Entladen verloren.</p>

<h2>Wenn der Speicher nur 10 Jahre hält</h2>
<p>Die Verbraucherzentrale Rheinland-Pfalz nennt für Batteriespeicher eine Lebensdauer zwischen 10 und 15 Jahren (<a href="https://verbraucherzentrale-rlp.de/node/92408" rel="noopener">Faktencheck „Die richtige Speichergröße“</a>, Stand 01/2024). Mit 10 statt 15 Jahren sieht die Rechnung so aus:</p>
<ul>
<li>Bei 500 € je kWh lohnen sich 5 kWh am meisten, mit +1.053 €. Der 10-kWh-Speicher landet bei −298 €.</li>
<li>Bei 700 € je kWh bleiben mit 6 kWh −267 €. Am meisten bringen dann 3 kWh, mit +272 €.</li>
</ul>
<p>Wie lange dein Speicher hält, weiß vorher keiner. Ich auch nicht. Die Garantie im Datenblatt gibt einen Anhaltspunkt. Je kürzer du rechnest, desto stärker zählt ein niedriger Preis je kWh.</p>

<h2>So rechnest du den Preis je kWh aus deinem Angebot</h2>
<p>Teile den Aufpreis für den Speicher durch die nutzbare Kapazität. Ein Beispiel: 6.500 € für 10 kWh nutzbar sind 650 € je kWh. Mehr braucht's dafür nicht. Steht der Speicher nicht als eigene Position im Angebot, frag nach dem Preis derselben Anlage ohne Speicher.</p>
<p>Kleine Speicher sind je kWh meist teurer, weil Wechselrichter, Montage und Anschluss nicht mit der Größe sinken. Der kostenlose Rechner nimmt einen festen Preis je kWh an. Für ein echtes Angebot ordnet der <a href="../pro/" data-umami-event="artikel-zu-pro" data-umami-event-artikel="stromspeicher-preis-pro-kwh">Angebots-Check</a> den Preis je kWh kostenlos ein, als Ampel: grün, gelb oder rot. Dazu bewertet er die Speichergröße, die Größe der PV-Anlage und deren Preis je kWp. Der Bericht von Speicherklar Pro zeigt dann, welche PV-Anlage und welcher Speicher am besten zusammenpassen. Wie das an einem Angebot mit 10 kWh aussieht, steht unter <a href="pv-angebot-pruefen.html">PV-Angebot prüfen</a>.</p>

<h2>Wann sich ein Speicher eher nicht rechnet</h2>
<ul>
<li><b>Großer Speicher zum hohen Preis:</b> Im Beispiel bringen 10 kWh ab rund 700 € je kWh nach 15 Jahren nichts mehr, 12 kWh schon ab rund 610 €.</li>
<li><b>Sehr hoher Preis je kWh:</b> Bei 1.000 € je kWh bleiben selbst mit der besten Größe (3 kWh) nach 15 Jahren nur rund 560 €.</li>
<li><b>Kurze Lebensdauer:</b> Hält der Speicher nur 10 Jahre, rutscht ein 6-kWh-Speicher bei 700 € je kWh ins Minus.</li>
<li><b>Kleiner Verbrauch:</b> Bei 3.000 statt 4.500 kWh im Jahr sinkt der Höchstpreis für 6 kWh von rund 980 € auf rund 770 € je kWh, für 10 kWh auf rund 510 €.</li>
</ul>
<p>Was das Modell nicht abbildet: Alterung des Speichers, Notstrom, Verschattung, dynamische Stromtarife, Zinsen und steigende Strompreise. Eine Wärmepumpe trägst du im Rechner getrennt ein. Mit Wärmepumpe rechnet er die Autarkie rund 4 Punkte zu hoch, den Zugewinn durch den Speicher trifft er.</p>
""",
"faq": [
 ("Ab welchem Preis pro kWh lohnt sich ein Stromspeicher nicht mehr?", "Das hängt von der Größe ab. Im Beispiel mit 4.500 kWh und 9 kWp kommt ein 6-kWh-Speicher bis rund 980 € je kWh in 15 Jahren auf null, ein 10-kWh-Speicher nur bis rund 700 €. Ohne Zinsen und Alterung."),
 ("Lohnt sich ein größerer Speicher, wenn er je kWh günstiger ist?", "Nur bei deutlichem Preisunterschied. Im Beispiel bringen 6 kWh zu 500 € je kWh +2.899 €. Ein 10-kWh-Speicher holt das erst ein, wenn er unter rund 415 € je kWh kostet."),
 ("Zählt beim Preis je kWh die Brutto- oder die nutzbare Kapazität?", "Rechne mit der nutzbaren Kapazität. Sie steht im Datenblatt und liegt etwas unter der Bruttokapazität. Mit brutto gerechnet sieht der Speicher günstiger aus, als er ist."),
],
},
{
"slug": "stromspeicher-region",
"kennzahl": {"v": "6 kWh", "t": "beste Speichergröße im Beispielhaus, in allen zehn Regionen des Rechners"},
"related": ["stromspeicher-groesse-berechnen", "ost-west-dach-speicher", "speichergroesse-4500-kwh"],
"chart": {"kind": "sweep", "title": "Gewinn nach 15 Jahren je Speichergröße: gleiches Haus, drei Regionen", "caption": "9 kWp Süd, 35°, 4.500 kWh, Speicher 500 €/kWh, Strom 33 ct/kWh, Einspeisung 7,7 ct, 15 Jahre. Der Punkt markiert die wirtschaftlichste Größe.",
  "series": [{"label": "Oberbayern (PLZ 8)", "p": {"region": "8"}}, {"label": "Ruhrgebiet (PLZ 4)", "p": {}}, {"label": "Schleswig-Holstein (PLZ 2)", "p": {"region": "2"}}]},
"title": "Stromspeicher im Süden oder Norden: Was ändert die Region?",
"seo_title": "Stromspeicher: Was ändert die Region?",
"h1": "Stromspeicher im Süden oder Norden: Was ändert die Region?",
"desc": "Im Süden gibt's mehr Sonne, die beste Speichergröße bleibt aber gleich: im Beispielhaus überall 6 kWh. Die Region ändert nur, wie viel übrig bleibt.",
"date": "2026-11-19",
"lead": "Weniger, als du denkst. Ich hab dasselbe Haus durch alle zehn Regionen des Rechners geschickt: Die beste Speichergröße ist überall 6 kWh. Die Region verschiebt nur, wie viel nach 15 Jahren übrig bleibt, im Beispiel zwischen rund 2.670 € und 3.380 €.",
"body": """
<p>Das Beispiel ist mein Standard-Haus: 9 kWp auf einem Süddach mit 35° Neigung, 4.500 kWh Verbrauch im Jahr, Speicher 500 € je kWh nutzbar inklusive Einbau, Strompreis 33 ct, Einspeisevergütung 7,70 ct, 15 Jahre. Ich hab nichts daran verändert außer dem Ort. Der Rechner ordnet deinen Ort über die erste Ziffer der Postleitzahl einer von zehn Regionen zu, mit Sonnendaten aus PVGIS.</p>

<h2>Alle zehn Regionen im Vergleich</h2>
<p>Gleiches Haus, gleicher Stromspeicher, nur die Postleitzahl ändert sich. Die beste Größe ist in allen zehn Regionen 6 kWh.</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Region</th><th>Ertrag<br>je kWp</th><th>Plus nach 15 J.<br>bezahlt nach</th></tr></thead>
<tbody>
<tr><td>PLZ 0: Sachsen, Thüringen-Ost, Sachsen-Anhalt-Süd</td><td class="num">1.064 kWh</td><td class="num">+2.918 €<br>7,6 J.</td></tr>
<tr><td>PLZ 1: Berlin, Brandenburg, Mecklenburg-Vorpommern</td><td class="num">1.010 kWh</td><td class="num">+2.726 €<br>7,9 J.</td></tr>
<tr><td>PLZ 2: Schleswig-Holstein, Bremen, Niedersachsen-Nord</td><td class="num">969 kWh</td><td class="num">+2.668 €<br>7,9 J.</td></tr>
<tr><td>PLZ 3: Hannover, Braunschweig, Magdeburg, Kassel</td><td class="num">992 kWh</td><td class="num">+2.732 €<br>7,9 J.</td></tr>
<tr class="hl"><td>PLZ 4: Ruhrgebiet, Niederrhein, Münsterland, Westfalen</td><td class="num">1.004 kWh</td><td class="num">+2.899 €<br>7,6 J.</td></tr>
<tr><td>PLZ 5: Köln, Bonn, Aachen, Koblenz, Trier</td><td class="num">1.013 kWh</td><td class="num">+2.932 €<br>7,6 J.</td></tr>
<tr><td>PLZ 6: Rhein-Main, Pfalz, Saarland, Mannheim</td><td class="num">1.095 kWh</td><td class="num">+2.947 €<br>7,6 J.</td></tr>
<tr><td>PLZ 7: Stuttgart, Baden, Bodensee</td><td class="num">1.121 kWh</td><td class="num">+3.283 €<br>7,2 J.</td></tr>
<tr><td>PLZ 8: München, Augsburg, Allgäu, Oberbayern</td><td class="num">1.115 kWh</td><td class="num">+3.380 €<br>7,1 J.</td></tr>
<tr><td>PLZ 9: Nürnberg, Würzburg, Franken, Thüringen-Süd</td><td class="num">1.061 kWh</td><td class="num">+2.944 €<br>7,6 J.</td></tr>
</tbody></table></div>
<p>Zwischen dem besten und dem schwächsten Ort liegen beim Ertrag rund 16 %. Beim Plus durch den Speicher sind es 712 € in 15 Jahren. Die beste Größe bleibt überall dieselbe.</p>

<h2>Warum die Größe gleich bleibt</h2>
<p>Die Mehr-Sonne im Süden kommt fast nur im Winter dazu. Im Sommer erzeugen alle Regionen ähnlich viel. Ein Durchschnittstag mit dem Beispielhaus:</p>
<div class="tablewrap"><table class="fit">
<thead><tr><th>Region</th><th>Juni<br>kWh am Tag</th><th>Dezember<br>kWh am Tag</th><th>Speicher voll<br>Juni / Dezember</th></tr></thead>
<tbody>
<tr><td>Oberbayern (PLZ 8)</td><td class="num">39,3</td><td class="num">12,5</td><td class="num">99 % / 65 %</td></tr>
<tr><td>Rhein-Main (PLZ 6)</td><td class="num">40,8</td><td class="num">7,7</td><td class="num">99 % / 38 %</td></tr>
<tr class="hl"><td>Ruhrgebiet (PLZ 4)</td><td class="num">37,7</td><td class="num">7,8</td><td class="num">98 % / 39 %</td></tr>
<tr><td>Schleswig-Holstein (PLZ 2)</td><td class="num">38,5</td><td class="num">6,0</td><td class="num">99 % / 33 %</td></tr>
</tbody></table></div>
<p>„Speicher voll“ heißt: so weit ist der 6-kWh-Speicher am Nachmittag eines Durchschnittstags geladen. Im Juni wird er überall voll. Mehr Sonne bringt dann nichts mehr, der Rest geht ins Netz. Im Dezember wird er nirgends voll, auch nicht in Oberbayern. Wie groß der Speicher sein sollte, entscheidet deshalb dein Verbrauch am Abend und in der Nacht. Und der hängt nicht an der Postleitzahl.</p>

<h2>Mehr Sonne heißt nicht automatisch mehr Plus</h2>
<p>Rhein-Main erzeugt im Jahr fast so viel wie Oberbayern, 1.095 statt 1.115 kWh je kWp. Beim Speicher bleiben dort aber nur +2.947 €, kaum mehr als im Ruhrgebiet. Der Grund steht in der Tabelle oben: Die Extra-Sonne kommt in Rhein-Main im Sommer, wenn der Speicher eh voll ist. In Oberbayern und am Bodensee scheint sie auch im Winter öfter. Dann füllt sie den Speicher an Tagen, an denen er sonst halb leer bliebe.</p>
<p>Für die PV-Anlage selbst zählt jede kWh. Für den Batteriespeicher zählt vor allem die Sonne von Oktober bis Februar.</p>

<h2>Was die Größe wirklich verschiebt</h2>
<p>Statt der Region solltest du dir drei andere Dinge ansehen. Mit dem Beispielhaus gerechnet:</p>
<ul>
<li><b>Verbrauch:</b> Bei 3.000 kWh im Jahr ist die beste Größe 4 kWh, im Süden (PLZ 7 und 8) 5 kWh. Bei 6.000 kWh sind es 8 kWh, im Norden und Osten (PLZ 1, 2, 3) 7 kWh.</li>
<li><b>Dach:</b> Ein Ost-West-Dach mit gleicher Leistung braucht 5 statt 6 kWh, in Schleswig-Holstein 4 kWh. Mehr dazu unter <a href="ost-west-dach-speicher.html">Ost-West-Dach</a>.</li>
<li><b>Speicherpreis:</b> Je teurer die kWh, desto kleiner die beste Größe. Siehe <a href="stromspeicher-preis-pro-kwh.html">Was darf ein Stromspeicher pro kWh kosten?</a></li>
</ul>
<p>Wie du die Größe für deinen Verbrauch abschätzt, steht unter <a href="stromspeicher-groesse-berechnen.html">Stromspeicher-Größe berechnen</a>.</p>

<h2>Wann sich ein Speicher eher nicht rechnet</h2>
<ul>
<li><b>Zu groß im Norden:</b> Ein 10-kWh-Speicher bringt in Schleswig-Holstein nach 15 Jahren +1.747 €, also 921 € weniger als 6 kWh. In Oberbayern sind es mit 10 kWh +2.697 €.</li>
<li><b>Kleiner Verbrauch:</b> Wer wenig Strom braucht, profitiert überall weniger. Das gilt im Süden genauso wie im Norden.</li>
<li><b>Teurer Speicher:</b> Die Region gleicht einen hohen Preis je kWh nicht aus. Rund 700 € Unterschied zwischen Nord und Süd sind schnell weg, wenn der Speicher 2 kWh zu groß ist oder deutlich mehr als 500 € je kWh kostet.</li>
</ul>
<p>Was das Modell nicht abbildet: Verschattung, Alterung des Speichers, Notstrom, dynamische Stromtarife, Zinsen und steigende Strompreise. Der Rechner nimmt für alle Regionen den Stunden-Verlauf eines echten Wetterjahres (2020) und bringt ihn auf die Monatssummen der Region aus PVGIS. Wie oft im Süden Sonne und Wolken innerhalb eines Monats wechseln, bildet er deshalb nur über die Monatssumme ab. Speicherklar Pro rechnet mit genaueren Sonnendaten je PLZ-Gebiet.</p>
""",
"faq": [
 ("Brauche ich in Süddeutschland einen größeren Stromspeicher?", "Nein. Im Beispielhaus mit 9 kWp und 4.500 kWh ist die beste Größe in allen zehn Regionen des Rechners 6 kWh. Die Mehr-Sonne im Süden kommt vor allem im Winter, wenn der Speicher ohnehin nicht voll wird."),
 ("Lohnt sich ein Stromspeicher in Norddeutschland?", "Im Beispiel ja. In Schleswig-Holstein und Niedersachsen-Nord (PLZ 2) bringen 6 kWh nach 15 Jahren +2.668 €, bezahlt nach 7,9 Jahren. Das sind 712 € weniger als in Oberbayern."),
 ("Wo lohnt sich ein Stromspeicher am meisten?", "Im Beispiel in Oberbayern und im Allgäu (PLZ 8) mit +3.380 € nach 15 Jahren, knapp vor Stuttgart, Baden und Bodensee (PLZ 7) mit +3.283 €. Dort scheint auch im Winter mehr Sonne, und die füllt den Speicher."),
],
},
]
