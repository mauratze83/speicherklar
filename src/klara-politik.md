# Klara: Politik und Förderung

<!--
Wissensdatei für Klara, die KI-Hilfe auf speicherklar.de. Klara beantwortet Fragen zu Politik, Steuern und
Förderung NUR aus dieser Datei und nennt dabei immer Stand und Quelle.

Format je Eintrag:
## Thema
- Stand: JJJJ-MM-TT        (Tag, an dem der Eintrag gegen die Quelle geprüft wurde)
- Status: geltendes Recht | beschlossen | geplant | in Verhandlung | nicht geprüft
- Quelle: Name, https://…  (Primärquelle bevorzugt; Presse mit Datum)
- Prüfen bis: JJJJ-MM-TT   (danach nimmt der Worker den Eintrag von selbst heraus)
Danach 2–4 Sätze Inhalt. Keine Zahlen, die nicht in der Quelle stehen.

Pflege: geplante Aufgabe „Klara Politik-Check“ schlägt Änderungen vor (claude/klara-politik-vorschlag.md im Projekt),
Manuel gibt frei. Danach build.py laufen lassen und pushen. Abgelaufene Einträge meldet build.py als WARNUNG.
-->

## Einspeisevergütung heute (EEG 2023)
- Stand: 2026-11-17
- Status: geltendes Recht
- Quelle: Bundesnetzagentur, https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/ErneuerbareEnergien/EEG_Foerderung/start.html
- Prüfen bis: 2026-12-31

Für neue PV-Anlagen auf Gebäuden mit Inbetriebnahme vom 01.08.2026 bis 31.01.2027 gelten bei Teileinspeisung (Überschuss) 7,70 ct/kWh für den Anteil bis 10 kWp und 6,66 ct/kWh für den Anteil über 10 bis 40 kWp, bei Volleinspeisung bis 10 kWp 12,22 ct/kWh. Der Satz gilt 20 Jahre plus den Rest des Jahres der Inbetriebnahme. Maßgeblich ist der Tag der Inbetriebnahme. Die Sätze sinken für neue Anlagen halbjährlich zum 1. Februar und 1. August um 1 %. Der Rechner nimmt 7,70 ct als Startwert.

## EEG-Reform 2027 (Entwurf)
- Stand: 2026-11-17
- Status: in Verhandlung, nicht beschlossen
- Quelle: Bundeswirtschaftsministerium, Pressemitteilung 29.07.2026, https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Pressemitteilungen/2026/07/20260729-eeg-novelle-und-netzanschlusspaket.html; Bundestag erste Lesung 24.09.2026 (pv magazine, 02.10.2026); Verhandlungsstand laut Reuters und ZfK, 14.–15.11.2026
- Prüfen bis: 2026-11-24

Das Bundeskabinett hat am 29.07.2026 einen Entwurf beschlossen: Neue Anlagen unter 25 kW sollten ab 2027 nach einer Übergangszahlung keine feste Einspeisevergütung mehr bekommen und höchstens 50 % ihrer Leistung einspeisen dürfen. Der Bundestag hat den Entwurf am 24.09.2026 zum ersten Mal beraten. Mitte November 2026 berichten Reuters und ZfK, dass Union und SPD die feste Vergütung für neue Anlagen bis 25 kW doch behalten und die 50-%-Grenze erst über 25 kW anwenden wollen; die Union knüpft die Einigung an das Netzpaket. Beschlossen ist das nicht, Bundestag und Bundesrat müssen noch abstimmen. Anlagen, die bis 31.12.2026 in Betrieb gehen, betrifft der Entwurf nicht. Der Schalter „EEG-Reform 2027“ im Rechner zeigt den Kabinettsentwurf (keine Vergütung, höchstens 50 % Einspeisung).

## Solarspitzengesetz
- Stand: 2026-11-17
- Status: geltendes Recht (seit 25.02.2025)
- Quelle: Verbraucherzentrale Hamburg, „Solarspitzen und Fördergelder: Neue Regeln für Photovoltaikanlagen“, https://www.vzhh.de/themen/bauen-immobilien-energie/erneuerbare-energien/solarspitzen-foerdergelder-neue-regeln-fuer-photovoltaikanlagen
- Prüfen bis: 2027-02-28

Für PV-Anlagen über 2 kWp, die ab dem 25.02.2025 in Betrieb gehen, gibt es keine Einspeisevergütung in Zeiten negativer Börsenstrompreise; die Förderdauer verlängert sich dafür. Solange kein intelligentes Messsystem mit Steuerbox eingebaut ist, darf die Anlage höchstens 60 % ihrer Leistung ins Netz einspeisen (Leistung, nicht Menge). Ein Speicher kann Strom aus diesen Zeiten auffangen. Der Rechner bildet im Modus „EEG heute“ weder die 60-%-Grenze noch die Stunden mit negativen Preisen ab.

## Umsatzsteuer: Nullsteuersatz
- Stand: 2026-11-17
- Status: geltendes Recht (seit 01.01.2023)
- Quelle: § 12 Abs. 3 Umsatzsteuergesetz, https://www.gesetze-im-internet.de/ustg_1980/__12.html
- Prüfen bis: 2027-06-30

Auf Lieferung und Installation von Solarmodulen, wesentlichen Komponenten und Speichern an den Betreiber einer PV-Anlage auf oder in der Nähe von Wohngebäuden fallen 0 % Umsatzsteuer an. Die Voraussetzung gilt als erfüllt, wenn die Anlage laut Marktstammdatenregister höchstens 30 kW (peak) hat. Auf der Rechnung steht dann 0 % Umsatzsteuer, Netto ist gleich Brutto. Ob es im Einzelfall passt, klärt der Installateur oder ein Steuerberater.

## Einkommensteuer: Steuerbefreiung kleiner Anlagen
- Stand: 2026-11-17
- Status: geltendes Recht
- Quelle: § 3 Nr. 72 Einkommensteuergesetz, https://www.gesetze-im-internet.de/estg/__3.html
- Prüfen bis: 2027-06-30

Einnahmen aus PV-Anlagen auf, an oder in Gebäuden sind einkommensteuerfrei, wenn die Anlage laut Marktstammdatenregister höchstens 30 kW (peak) je Wohn- oder Gewerbeeinheit hat, insgesamt höchstens 100 kW (peak) je Person oder Gesellschaft. Die einheitliche 30-kW-Grenze gilt für Anlagen, die nach dem 31.12.2024 angeschafft, in Betrieb genommen oder erweitert wurden (Jahressteuergesetz 2024); davor galten für Mehrfamilienhäuser 15 kW (peak) je Einheit. Für Einzelfälle (Vermietung, mehrere Anlagen, Gewerbe) ist ein Steuerberater oder Lohnsteuerhilfeverein die richtige Stelle.

## Stromsteuer
- Stand: 2026-11-18
- Status: geltendes Recht 2,05 ct/kWh; Senkung für alle aufs EU-Minimum ab 2027 im Koalitionsausschuss beschlossen, Bundestag (Haushalt 2027 am 27.11.2026) und Änderung des Stromsteuergesetzes noch offen
- Quelle: § 3 Stromsteuergesetz; Koalitionsausschuss laut t-online und ZDFheute (18.11.2026), zusammengefasst im Artikel https://speicherklar.de/ratgeber/stromsteuer-stromspeicher.html
- Prüfen bis: 2026-11-28

Die Stromsteuer beträgt heute 2,05 ct je kWh, dazu kommt Umsatzsteuer. In der Nacht zum 18.11.2026 hat sich der Koalitionsausschuss von Union und SPD darauf geeinigt, sie für alle Verbraucher aufs EU-Minimum von 0,1 ct je kWh zu senken. Finanziert ist das bisher nur für 2027, eine dauerhafte Senkung ist beabsichtigt. Gesetz ist das noch nicht: Der Bundestag soll den Haushalt 2027 am 27.11.2026 beschließen, das Stromsteuergesetz muss geändert werden. Gibt der Versorger die Senkung voll weiter, wird Strom rund 2,32 ct je kWh billiger. Für die Planung eines Speichers ändert sich laut Speicherklar-Artikel wenig: Die beste Größe bleibt gleich, der Speicher bezahlt sich etwas später.

## KfW-Kredit
- Stand: 2026-11-17
- Status: geltendes Programm
- Quelle: KfW, Programm 270 „Erneuerbare Energien – Standard“, https://www.kfw.de/270
- Prüfen bis: 2027-03-31

Die KfW bietet mit Programm 270 einen Kredit für PV-Anlagen, mit dem auch Batteriespeicher finanziert werden können. Beantragt wird er über die eigene Bank vor dem Kauf. Einen bundesweiten Zuschuss nur für Stromspeicher gibt es nicht; das frühere KfW-Programm 442 kann nicht mehr beantragt werden. Konditionen ändern sich, deshalb immer direkt bei der KfW nachsehen.

## Landes- und Kommunalförderung
- Stand: 2026-11-17
- Status: nicht geprüft
- Quelle: keine geprüfte Quelle
- Prüfen bis: 2027-06-30

Zu Förderprogrammen der Länder, Städte und Stadtwerke hat Speicherklar keinen geprüften Stand, weil sie oft wechseln und schnell ausgeschöpft sind. Klara nennt keine einzelnen Programme, sondern verweist auf die Förderseite des eigenen Bundeslands, der Stadt oder des Stadtwerks und auf die Verbraucherzentrale.
