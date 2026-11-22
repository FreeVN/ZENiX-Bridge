# Excel bewerken

Alles wat je in de witte cellen zet, wordt bij het terugschrijven overgenomen.
De grijze cellen niet.

## Kolommen in `Elementen`

| Kolom | Betekenis | Opmerking |
|---|---|---|
| `Naam` | vrije naam van het element | zie tekenregels |
| `Ring` | ring waartoe het element hoort | keuzelijst |
| `Unit` | positie van de unit op de bus | getal |
| `Adres` | punt op de unit | getal |
| `Type` | soort punt (`fire`, `smoke`, `di`, `do`, …) | keuzelijst |
| `Device type` | hardwaretype | keuzelijst |
| `Beschrijving` | vrije tekst | geen `< > , ? *` |
| `Alarmfunctie` | AND/OR-combinatie | tekst |
| `Normaal open` | contactrust | `WAAR`/`ONWAAR` |
| `Inverteren` | logica omkeren | `WAAR`/`ONWAAR` |
| `Veilig` | veiligheidsstand (FIO) | tekst |

## Tekenregels voor namen

De Ringbus Tool weigert namen met onderstaande tekens, en de app doet hetzelfde.
Zo krijg je nooit een project terug dat de tool niet meer opent.

```
( ) . , ! | & < > ? * + / \ = " % $ # : ; ^ ' [ ] { }   spatie   -
en de streepjes ‐ ‑ – — ―
```

Een **underscore** `_` mag wel. Namen moeten uniek en niet leeg zijn.

!!! example "Goed en fout"
    | Invoer | Resultaat |
    |---|---|
    | `klep_01_glv` | ok |
    | `Klep 1` | geweigerd (spatie) |
    | `klep-01` | geweigerd (koppelteken) |
    | `klep.01` | geweigerd (punt) |
    | `brand,gang` | geweigerd (komma) |

De celweigering is een controle, geen automatische correctie: pas de naam aan.

## Zones toewijzen

In **Zone-lidmaatschap** vink je per element per zone aan. De kolommen komen uit
het tabblad `Zones`; je hoeft niets te verschuiven of te verplaatsen.

## Een zone toevoegen

Zet onderaan `Zones` een rij met een **lege Id** en een naam. De kolom verschijnt
vanzelf in de matrix. De id kent de app toe bij het terugschrijven.

## Wat je beter niet doet

- **Rijen invoegen of verwijderen** in `Elementen`: de matrix is positiegebonden.
  Nieuwe elementen maak je aan in de Ringbus Tool, daarna maak je een nieuwe
  export.
- **Ringen toevoegen**: dat doet de Ringbus Tool.
- **`Index in ring` aanpassen**: wordt bij openen herberekend.

## Klaar? Terug naar een project

Bewaar het bestand en ga naar [Terug naar een project](terug-naar-project.md).
