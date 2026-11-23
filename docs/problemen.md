# Als het niet werkt

## De app doet niets bij het slepen

- Controleer of je een `.rbtproject` of `.xlsx` sleept en geen snelkoppeling.
- Op Windows: sleept de app vanuit Verkenner, niet vanuit een uitgepakte
  zip-preview.
- Geen drag & drop mogelijk (bv. in een virtuele desktop)? Gebruik **Bestand
  kiezen…** — dat doet exact hetzelfde.

## `Geen sleutel gevonden`

`keys.txt` ontbreekt of staat niet naast de exe. Zie [Je sleutel](sleutels.md).

## `Geen van de N sleutels opent dit project`

De sleutels zijn geladen, maar geen enkele hoort bij dit bestand. De melding
toont de key-id van het project; vergelijk die met je sleutels of lees de dongle
van die installatie uit.

## `login 400` bij het uitlezen van de dongle

- De dongle zit niet in (of is niet herkend) — steek hem opnieuw in.
- **Ringbus Tool is nog open** en houdt de dongle vast. Sluit de app volledig af
  (ook het icoon in de systeembalk).
- De HASP-driver ontbreekt: Ringbus Tool moet op deze machine geïnstalleerd zijn.

## `HASP_TS_DETECTED`

Je werkt in een Remote Desktop-sessie. De dongle weigert dan. Gebruik een gewone
console-sessie of een geplande taak onder SYSTEM.

## `RingBus Tool ... niet gevonden` / `configuration-*.jar niet gevonden`

De vendor-bibliotheek zit niet meer in de exe (sinds 2.2.0) en moet uit je
RingBus Tool-installatie komen. Installeer de RingBus Tool, of zet
`RINGBUSTOOL_HOME` naar de installatiemap (de map met `ringbustool\modules`).

## `JRE te oud voor de meegeleverde classes`

De binary en de Java-classes passen niet bij elkaar — dat hoort niet in een
release. Nieuwste versie downloaden.

## `Dit Excel-bestand is niet door ZENiX gemaakt`

Het werkboek heeft geen `_zenix_base`-tabblad. Enkel werkboeken gebruiken die uit
de app komen (of die iemand anders met de app maakte).

## `Naam geweigerd: verboden teken(s)`

Zie de [tekenregels](bewerken.md#tekenregels-voor-namen). De wijziging wordt
overgeslagen, de rest gaat door.

## Het project opent niet in de Ringbus Tool

- Controleer of je het **aangepaste** bestand opent en niet een halve download.
- Open het origineel opnieuw en maak een nieuwe export; zo sluit je uit dat het
  aan de bewerking lag.
- Meld het met de foutmelding van de Ringbus Tool erbij.

## De app start traag (Windows)

Een onefile-exe pakt zichzelf uit in `%TEMP%`. Enkele seconden is normaal.
Schijfruimte of antivirus kan het rekken; zet de map eventueel op de uitzonderingenlijst.

## Iets stuk dat hier niet staat

Noteer: welk bestand, welke stap, de exacte melding. Met die drie kan het
gereproduceerd worden.
