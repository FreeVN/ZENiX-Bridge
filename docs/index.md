# ZENiX Bridge — handleiding

!!! info "Versie"
    Deze handleiding hoort bij **ZENiX Bridge 2.3.0**. De exe staat op de
    [releases-pagina](https://github.com/FreeVN/ZENiX-Bridge/releases); de
    broncode staat in de privé-repo `FreeVN/zenix-ringbus-tool`.

ZENiX Bridge is een **tweerichtingsconverter** voor ZENiX-projectbestanden
(Rf-Technologies brandkleppen). Je sleept een `.rbtproject` op de app en krijgt
een overzichtelijk Excel-bestand; je bewerkt dat en sleept het terug. Klaar.

Geen Ringbus Tool-UI meer nodig om honderd kleppen te hernoemen, zones toe te
wijzen of adressen na te lopen.

```
Project.rbtproject          ──sleep──▶   Project - elementen.xlsx
Project - elementen.xlsx    ──sleep──▶   Project - elementen - aangepast.rbtproject
```

## Waarom

De Ringbus Tool is gemaakt om te configureren, niet om te bulk-editen. Alles wat
je doet — een naam, een zone, een adres — gaat door een formulier per element.
Bij een project met zestig of drieduizend elementen is dat werk dat je in Excel
in één middag doet.

ZENiX Bridge schrijft **enkel de verschillen** terug. De rest van het project
blijft byte-voor-byte wat het was: geen nieuwe ids, geen herschikte ringen, geen
verrassingen bij het openen.

## Voor wie

Voor de technieker en de commissingenieur die het project in de Ringbus Tool
aanmaken en daarna willen opschonen of uitbreiden. Je hoeft geen Python of Java
te kennen: de app is één bestand.

!!! warning "Reken op de Ringbus Tool als waarheid"
    ZENiX Bridge doet geen buscommunicatie, scant geen ringen en maakt geen
    elementen aan. Het bewerkt het **projectbestand**. Na het terugschrijven
    open je het in de Ringbus Tool ter controle — dat blijft de norm.

## De twee richtingen

| Je hebt | Je wil | Waar te beginnen |
|---|---|---|
| Een bestaand `.rbtproject` | Een overzicht in Excel | [Naar Excel](naar-excel.md) |
| Een bewerkt Excel-bestand | Terug een geldig project | [Terug naar een project](terug-naar-project.md) |

Eerst de app aan de praat krijgen? [Installeren](installatie.md) en
[je sleutel](sleutels.md).

## Wat je nodig hebt

- Windows 10/11 (x64) met de **RingBus Tool** geïnstalleerd — de app haalt de
  vendor-bibliotheek daaruit. Linux en Docker worden niet meer gemaakt.
- De **projectsleutel** van het project — zonder sleutel opent niets. Hoe je die
  regelt, staat in [Je sleutel](sleutels.md).
- Voor het uitlezen van een dongle: een geïnstalleerde Ringbus Tool en de dongle
  in een USB-poort.

## Eerlijk over de grenzen

- **Ringen en elementen toevoegen** doe je in de Ringbus Tool, niet in het blad.
- **Function blocks** zijn zichtbaar maar niet bewerkbaar.
- **Een project van een andere installatie** opent alleen met de sleutel van die
  installatie. De app zegt dan welke key-id ontbreekt.
