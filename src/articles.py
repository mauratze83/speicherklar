"""Ratgeber-Artikel für speicherklar.de. Jeder Artikel: slug, Titel, Beschreibung, Datum, HTML-Inhalt."""

STAND = "November 2026"
BEISPIEL = ("Alle Beispiele: Standort Ruhrgebiet (PLZ 4…), Dachneigung 35°, Speicherpreis 500 €/kWh inkl. Einbau, "
            "Strompreis 32 ct/kWh, Einspeisevergütung 7,70 ct/kWh, 15 Jahre Lebensdauer, wenn nicht anders angegeben. "
            "Gerechnet mit dem Speicherklar-Rechner: Jahressimulation in 5-Minuten-Schritten mit Sonnendaten aus PVGIS 2014–2023.")

ARTICLES = [
{
"slug": "stromspeicher-lohnt-sich-2027",
"title": "Lohnt sich ein Stromspeicher 2027?",
"h1": "Lohnt sich ein Stromspeicher 2027?",
"desc": "Mit Zahlen statt Prospekt: Wann sich ein Stromspeicher für eine neue PV-Anlage rechnet, was die EEG-Reform ändert und welche Größe am meisten bringt.",
"date": "2026-11-08",
"lead": "Kurze Antwort: Bei den heutigen Preisen meistens ja, wenn der Speicher nicht zu groß ist. Sollte die geplante EEG-Reform kommen, rechnet er sich sogar deutlich schneller.",
"body": """
<p>Ob sich ein Speicher lohnt, hängt an vier Zahlen: was er kostet, was dein Netzstrom kostet, was du für eingespeisten Strom bekommst und wie viel Solarstrom er dir zusätzlich nutzbar macht. Wir haben das für ein typisches Einfamilienhaus durchgerechnet: 9 kWp auf einem Süddach, 4.500 kWh Verbrauch im Jahr.</p>

<h2>Das Ergebnis mit den heutigen Regeln</h2>
<p>Ohne Speicher deckt die Anlage 37 % des Verbrauchs. Mit Speicher steigt das deutlich, aber jede weitere Kilowattstunde Kapazität bringt weniger als die vorherige.</p>
<div class="tablewrap"><table>
<thead><tr><th>Speicher</th><th>Autarkie</th><th>Ersparnis/Jahr</th><th>Amortisation</th><th>Bilanz nach 15 Jahren</th></tr></thead>
<tbody>
<tr><td>ohne</td><td class="num">37 %</td><td class="num">–</td><td class="num">–</td><td class="num">–</td></tr>
<tr><td>4 kWh</td><td class="num">66 %</td><td class="num">284 €</td><td class="num">7,0 Jahre</td><td class="num">+2.259 €</td></tr>
<tr class="hl"><td>6 kWh</td><td class="num">74 %</td><td class="num">367 €</td><td class="num">8,2 Jahre</td><td class="num">+2.509 €</td></tr>
<tr><td>8 kWh</td><td class="num">79 %</td><td class="num">418 €</td><td class="num">9,6 Jahre</td><td class="num">+2.263 €</td></tr>
<tr><td>10 kWh</td><td class="num">81 %</td><td class="num">446 €</td><td class="num">11,2 Jahre</td><td class="num">+1.697 €</td></tr>
<tr><td>15 kWh</td><td class="num">85 %</td><td class="num">480 €</td><td class="num">15,6 Jahre</td><td class="num">−307 €</td></tr>
</tbody></table></div>
<p>Am meisten bleibt bei 6 kWh übrig. Ein 15-kWh-Speicher macht das Haus kaum unabhängiger als einer mit 8 kWh, kostet aber fast doppelt so viel. Er holt seine Kosten in 15 Jahren nicht wieder rein.</p>

<h2>Was die EEG-Reform ändern würde</h2>
<p>Das Bundeskabinett hat am 29. Juli 2026 einen Entwurf für ein neues EEG beschlossen. Für neue kleine Dachanlagen soll die feste Einspeisevergütung nach einer Übergangszeit wegfallen. Außerdem darf nur noch höchstens die Hälfte der Anlagenleistung ins Netz. Bundestag und Bundesrat müssen noch zustimmen, Änderungen sind möglich.</p>
<p>Für den Speicher ist das eine gute Nachricht. Jede Kilowattstunde, die du selbst nutzt, spart weiter 32 ct. Eine eingespeiste bringt dann nichts mehr. Und Strom, der wegen der 50-%-Grenze gar nicht ins Netz darf, geht verloren, wenn ihn kein Speicher auffängt. Im Beispielhaus wären das rund 880 kWh im Jahr.</p>
<div class="tablewrap"><table>
<thead><tr><th>Szenario</th><th>Beste Größe</th><th>Ersparnis/Jahr</th><th>Amortisation</th><th>Bilanz nach 15 Jahren</th></tr></thead>
<tbody>
<tr><td>EEG heute</td><td class="num">6 kWh</td><td class="num">367 €</td><td class="num">8,2 Jahre</td><td class="num">+2.509 €</td></tr>
<tr><td>EEG-Reform</td><td class="num">7 kWh</td><td class="num">570 €</td><td class="num">6,1 Jahre</td><td class="num">+5.044 €</td></tr>
</tbody></table></div>

<h2>Was am stärksten zählt: der Speicherpreis</h2>
<p>Die Verbraucherzentrale nennt für 2026 eine Spanne von etwa 300 bis 700 € pro kWh inklusive Einbau. Das macht einen größeren Unterschied als fast alles andere:</p>
<ul>
<li><b>350 €/kWh:</b> beste Größe 7 kWh, bezahlt nach 6,2 Jahren</li>
<li><b>500 €/kWh:</b> beste Größe 6 kWh, bezahlt nach 8,2 Jahren</li>
<li><b>700 €/kWh:</b> beste Größe 5 kWh, bezahlt nach 10,6 Jahren</li>
</ul>
<p>Hol dir deshalb mindestens zwei Angebote und rechne den Preis pro kWh nutzbarer Kapazität aus. Wird der Speicher mit der PV-Anlage zusammen gekauft, ist er meist günstiger als beim Nachrüsten.</p>

<h2>Wann sich ein Speicher eher nicht lohnt</h2>
<ul>
<li>Der Verbrauch ist klein. Bei 3.000 kWh im Jahr rechnen sich nur 4 kWh, ein 8-kWh-Speicher braucht fast 13 Jahre.</li>
<li>Der Angebotspreis liegt deutlich über 700 €/kWh.</li>
<li>Du bist tagsüber zu Hause und verbrauchst den Solarstrom ohnehin direkt.</li>
</ul>

<h2>Und das E-Auto?</h2>
<p>Ein E-Auto mit 2.500 kWh im Jahr verschiebt die Rechnung. Lädt es meist abends, nutzt es den Speicher kräftig: Dann darf er größer sein, bis etwa 10 kWh. Lädt es tagsüber direkt vom Dach, reichen 6 kWh. Bevor du einen großen Speicher fürs Auto kaufst, prüf also, ob es nicht einfach tagsüber laden kann.</p>
""",
"faq": [
 ("Wie lange hält ein Stromspeicher?", "Hersteller geben meist 10 Jahre Garantie und 6.000 und mehr Ladezyklen an. Wir rechnen mit 15 Jahren Nutzung."),
 ("Gibt es eine Förderung für Stromspeicher?", "Einen bundesweiten Zuschuss gibt es 2026 nicht. Auf Speicher mit einer PV-Anlage fällt aber keine Umsatzsteuer an, und manche Länder und Kommunen fördern eigene Programme."),
 ("Wie groß sollte mein Speicher sein?", "Als grobe Regel rechnen sich etwa 1 bis 1,5 kWh Speicher je 1.000 kWh Jahresverbrauch. Genauer geht es mit dem Rechner, weil Ausrichtung, Verbrauch und Preise viel ausmachen."),
],
},
{
"slug": "speichergroesse-4500-kwh",
"title": "Welche Speichergröße bei 4.500 kWh Verbrauch?",
"h1": "Welche Speichergröße bei 4.500 kWh Verbrauch?",
"desc": "Bei 4.500 kWh Jahresverbrauch rechnet sich meist ein Speicher mit 5 bis 7 kWh. Die Zahlen für 6, 9 und 12 kWp und warum größer nicht besser ist.",
"date": "2026-11-08",
"lead": "Bei 4.500 kWh Jahresverbrauch und einem Süddach rechnet sich meist ein Speicher mit 5 bis 7 kWh nutzbarer Kapazität. Mehr macht dich kaum unabhängiger, nur die Rechnung schlechter.",
"body": """
<p>4.500 kWh im Jahr ist typisch für eine Familie mit zwei Kindern ohne Wärmepumpe und ohne E-Auto. Viele Angebote kommen in diesem Fall mit 10 kWh Speicher oder mehr. Wir haben nachgerechnet, ab welcher Größe sich das nicht mehr lohnt.</p>

<h2>Die beste Größe je Anlagengröße</h2>
<div class="tablewrap"><table>
<thead><tr><th>PV-Anlage (Süd)</th><th>Beste Speichergröße</th><th>Amortisation</th><th>Autarkie mit Speicher</th><th>Zum Vergleich: 8 kWh</th></tr></thead>
<tbody>
<tr><td>6 kWp</td><td class="num">5 kWh</td><td class="num">8,3 Jahre</td><td class="num">63 %</td><td class="num">10,9 Jahre</td></tr>
<tr class="hl"><td>9 kWp</td><td class="num">6 kWh</td><td class="num">8,2 Jahre</td><td class="num">74 %</td><td class="num">9,6 Jahre</td></tr>
<tr><td>12 kWp</td><td class="num">6 kWh</td><td class="num">7,9 Jahre</td><td class="num">78 %</td><td class="num">9,2 Jahre</td></tr>
</tbody></table></div>
<p>Auffällig: Auch eine größere Anlage braucht keinen größeren Speicher. Ab 9 kWp ist im Sommer ohnehin mehr Strom da, als das Haus abends und nachts verbraucht. Der Engpass ist der Verbrauch in der Nacht, nicht die Erzeugung.</p>

<h2>Warum ein großer Speicher im Winter nicht hilft</h2>
<p>Mit 8 kWh Speicher deckt das Beispielhaus im Juni 99 % seines Verbrauchs selbst, im Dezember nur 47 %. Im Dezember erzeugt die Anlage rund 280 kWh, das Haus braucht 450 kWh. Was nicht erzeugt wird, kann auch kein Speicher speichern. Ein größerer Speicher macht nur im Sommer zusätzlichen Überschuss nutzbar, und davon gibt es dann schon genug.</p>

<h2>Die Faustregel</h2>
<p>Rund 1 bis 1,5 kWh Speicher je 1.000 kWh Jahresverbrauch. Bei 4.500 kWh sind das 4,5 bis 7 kWh. Unsere Simulation landet genau in diesem Bereich.</p>
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
<li><b>6.000 kWh:</b> beste Größe 7 kWh</li>
</ul>
<p>(jeweils 9 kWp Süd)</p>
""",
"faq": [
 ("Brutto oder netto: welche Speichergröße ist gemeint?", "Wir rechnen immer mit der nutzbaren Kapazität. Manche Angebote nennen die Bruttokapazität, die 5 bis 10 % höher liegt. Frag im Zweifel nach."),
 ("Kann ich den Speicher später erweitern?", "Viele Systeme sind modular und lassen sich um weitere Batteriemodule ergänzen. Das ist ein guter Weg, mit 5 bis 6 kWh zu starten und erst bei E-Auto oder Wärmepumpe zu erweitern."),
],
},
{
"slug": "ost-west-dach-speicher",
"title": "Ost-West-Dach: Braucht es einen Speicher?",
"h1": "Ost-West-Dach: Braucht es einen Speicher?",
"desc": "Eine Ost-West-Anlage liefert morgens und abends Strom. Deshalb reicht meist ein kleinerer Speicher als bei Süd. Die Zahlen im Vergleich.",
"date": "2026-11-08",
"lead": "Ja, aber einen kleineren. Bei einer Ost-West-Anlage rechnet sich meist ein Speicher mit etwa 4 kWh, bei einem Süddach mit gleicher Leistung eher 6 kWh.",
"body": """
<p>Ost-West-Dächer gelten oft als zweite Wahl. Für den Eigenverbrauch sind sie aber besser als ihr Ruf: Sie liefern morgens und am späten Nachmittag Strom, also dann, wenn im Haus Kaffeemaschine, Herd und Waschmaschine laufen.</p>

<h2>Süd gegen Ost-West im Vergleich</h2>
<p>Beide Anlagen haben 9 kWp, 35° Neigung, das Haus verbraucht 4.500 kWh. Bei Ost-West ist die Leistung je zur Hälfte auf beide Dachseiten verteilt.</p>
<div class="tablewrap"><table>
<thead><tr><th></th><th>Süd</th><th>Ost-West</th></tr></thead>
<tbody>
<tr><td>Erzeugung pro Jahr</td><td class="num">9.260 kWh</td><td class="num">7.270 kWh</td></tr>
<tr><td>Solarstrom, der ohne Speicher im Haus bleibt</td><td class="num">18 %</td><td class="num">22 %</td></tr>
<tr><td>Wirtschaftlichste Speichergröße</td><td class="num">6 kWh</td><td class="num">4 kWh</td></tr>
<tr><td>Amortisation dieser Größe</td><td class="num">8,2 Jahre</td><td class="num">8,3 Jahre</td></tr>
<tr><td>Amortisation mit 8 kWh</td><td class="num">9,6 Jahre</td><td class="num">12,9 Jahre</td></tr>
</tbody></table></div>
<p>Ost-West erzeugt bei gleicher Leistung rund ein Fünftel weniger, verteilt den Strom aber gleichmäßiger über den Tag. Mittags bleibt weniger Überschuss übrig, der in einen Speicher könnte. Deshalb lohnt sich ein großer Speicher hier noch weniger als bei Süd.</p>

<h2>Der teure Fehler</h2>
<p>Ein 8-kWh-Speicher an einer Ost-West-Anlage kostet 2.000 € mehr als einer mit 4 kWh, bringt pro Jahr aber nur rund 70 € zusätzlich. Er braucht fast 13 Jahre, bis er sich bezahlt hat. Wenn dir ein Angebot für ein Ost-West-Dach einen großen Speicher vorschlägt, frag nach dem Grund.</p>

<h2>Mehr Fläche statt mehr Speicher</h2>
<p>Ein Ost-West-Dach bietet oft mehr Platz als eine einzelne Südseite. Bei 12 kWp Ost-West ist die beste Speichergröße immer noch 4 kWh, und die Rechnung wird besser (Amortisation 7,6 Jahre). Statt mehr Speicher lohnt sich hier eher mehr Modulfläche.</p>

<h2>Mit der EEG-Reform</h2>
<p>Fällt die Einspeisevergütung weg, rechnet sich auch bei Ost-West ein etwas größerer Speicher: 5 statt 4 kWh, Amortisation nach etwa 6,4 statt 8,3 Jahren. Die 50-%-Grenze trifft Ost-West kaum, weil die Anlage mittags nie ihre volle Leistung erreicht.</p>
""",
"faq": [
 ("Lohnt sich Ost-West überhaupt?", "Ja. Die Erzeugung ist etwas geringer, aber der Strom kommt zu Zeiten, in denen du ihn brauchst, und die Fläche ist oft größer. Für den Eigenverbrauch ist Ost-West oft eine sehr gute Wahl."),
 ("Brauche ich bei Ost-West zwei Wechselrichter?", "Meist nicht. Moderne Wechselrichter haben zwei getrennte Eingänge, einen für jede Dachseite."),
],
},
]
