# Naar Excel

Sleep een `.rbtproject` op de app, of:

```bat
ZENiXBridge.exe to-xlsx project.rbtproject
```

Je krijgt `project - elementen.xlsx` naast het bronbestand. Het origineel wordt
nooit aangepast.

## Wat er in het werkboek zit

| Tabblad | Inhoud |
|---|---|
| **Info** | titelblok, projectcijfers, legende, uitleg per kolom |
| **Ringen** | ringen met IP, CPU-type en BACnet-gegevens (alleen-lezen) |
| **Zones** | zones met id, naam, beschrijving en aantal elementen |
| **Elementen** | het werkblad: één rij per element |
| **Zone-lidmaatschap** | matrix met checkboxes: welk element hoort bij welke zone |

## Vaste en vrije kolommen

De opmaak vertelt je wat je mag aanpassen:

- **Rode kop** = invulbaar.
- **Donkere kop met 🔒** = vast: identificatie of formule.
- Grijze cellen horen bij een vaste kolom.

Vast in `Elementen`: `Origineel`, `Unit-ID`, `Index in ring`, `Zones`,
`FB master`, `FB conditioneel`.
Vast in de matrix: `Origineel` en `Unit-ID`.

!!! tip "Waarom staat `Origineel` vast?"
    Dat is de koppelsleutel met het project. Wil je een element een andere naam
    geven, wijzig dan `Naam` — niet `Origineel`. Anders weet de app bij het
    terugschrijven niet meer over welk element het gaat.

## Het bestand is zelfstandig

Het werkboek bevat een verborgen tabblad `_zenix_base` met de originele container
(en de key-id). Daardoor heb je het bronbestand niet meer nodig om terug te
converteren: je kan het Excel-bestand doorsturen, op een andere pc bewerken en
daar terugzetten.

!!! note "Grootte"
    Dat verborgen tabblad groeit mee met het project (base64). Voor normale
    projecten is dat enkele tientallen kilobytes tot een paar megabyte.

## Werken in Google Sheets?

Dat kan: het werkboek uploaden, bewerken, terug downloaden als `.xlsx` en op de
app slepen. De formules in de kolomkoppen en de zone-telling werken daar ook; de
checkboxes worden `WAAR/ONWAAR`.
