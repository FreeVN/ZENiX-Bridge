# Terug naar een project

Sleep het bewerkte `.xlsx` terug op de app, of:

```bat
ZENiXBridge.exe to-project "project - elementen.xlsx"
```

Je krijgt `… - aangepast.rbtproject`. Het bronbestand blijft ongemoeid.

## Wat er gebeurt

1. De app leest het verborgen tabblad `_zenix_base` en pakt de originele
   container uit.
2. Elke rij wordt vergeleken met de basis; **enkel de verschillen** blijven over.
3. Die verschillen worden in het project geschreven en het bestand wordt opnieuw
   verpakt en versleuteld.

Een onbewerkt werkboek levert dus **nul wijzigingen** en een identiek project —
een goede test voor je begint.

## Wat teruggeschreven wordt

| Veld | Terug |
|---|---|
| `Naam` | ja |
| `Ring` | ja |
| `Unit`, `Adres` | ja |
| `Type`, `Device type` | ja |
| `Beschrijving`, `Alarmfunctie` | ja |
| `Normaal open`, `Inverteren`, `Veilig` | ja |
| Zones (matrix) | ja |
| Nieuwe zones (lege Id) | ja, met nieuwe id |
| `Origineel`, `Unit-ID`, `Index in ring` | nee |
| `FB master`, `FB conditioneel` | nee |

## Altijd controleren

Open het resultaat in de Ringbus Tool. Daar zie je meteen of namen, adressen en
zones kloppen, en of de tool het project zonder klagen laadt. De tool blijft de
norm; de app doet geen buscommunicatie.

!!! tip "Bewaar je tussenstand"
    Het Excel-bestand is je werkdocument. Het bevat de originele container, dus
    je kan altijd opnieuw beginnen zonder het bronbestand te zoeken.

## Foutmeldingen

| Melding | Betekenis |
|---|---|
| `Dit Excel-bestand is niet door ZENiX gemaakt` | geen `_zenix_base`-tabblad |
| `De sleutel voor dit project (…) staat niet in keys.txt` | sleutel toevoegen |
| `Naam geweigerd: verboden teken(s)` | zie [tekenregels](bewerken.md#tekenregels-voor-namen) |
| `n rij(en) niet herkend` | `Origineel` gewijzigd of rij verschoven |
