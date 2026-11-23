# Installeren

De app is één bestand: `ZENiXBridge.exe`. Er is geen installatieprogramma en geen
Java op je systeem nodig — de JRE zit in de binary. Wat **niet** in de binary
zit, is de vendor-bibliotheek van de RingBus Tool: die haalt de app uit je
bestaande RingBus Tool-installatie.

## Vereiste: de RingBus Tool

Installeer eerst de **ZENiX RingBus Tool** (van Rf-Technologies) op dezelfde pc.
De app gebruikt daaruit:

- `configuration-1.4.1.jar` — de vendor-bibliotheek voor het projectformaat;
- de USB-dongle-route, als je die gebruikt.

Staat de RingBus Tool ergens anders dan in `Program Files`, zet dan de
omgevingsvariabele `RINGBUSTOOL_HOME` naar die map.

## Windows 10/11 (x64)

1. Download `ZENiXBridge.exe` van de [releases-pagina](https://github.com/FreeVN/ZENiX-Bridge/releases).
2. Maak een map, bijvoorbeeld `C:\Tools\ZENiX Bridge\`, en zet de exe erin.
3. Zet `keys.txt` in dezelfde map — zie [Je sleutel](sleutels.md).
4. Dubbelklikken.

!!! tip "Eerste start"
    De eerste start duurt enkele seconden: een onefile-app pakt zichzelf uit in
    `%TEMP%`. Daarna gaat het snel. Windows SmartScreen kan waarschuwen omdat de
    exe niet ondertekend is: *Meer informatie → Toch uitvoeren*.

!!! warning "RingBus Tool niet gevonden"
    Dan stopt de app met een duidelijke melding. Installeer de RingBus Tool, of
    zet `RINGBUSTOOL_HOME` naar de installatiemap. De app werkt niet zonder die
    bibliotheek.

## Controleren of alles werkt

Dubbelklik de exe en kies **zelftest**, of vanaf de command line:

```bat
ZENiXBridge.exe selftest
```

```json
{"java": "...\\jre\\bin\\java.exe", "jars": [["configuration-1.4.1.jar", true]],
 "keys": 1, "java_check": [true, "ok"]}
```

`java_check` doet een echte aanroep van de Java-helper: zo weet je dat de
meegeleverde JRE de classes kan laden, niet alleen dat `java` bestaat. Staat
`jars` leeg, dan is de RingBus Tool niet gevonden.

## Updaten

Nieuwe versie downloaden en de oude exe vervangen. `keys.txt` blijft staan — die
staat ernaast, niet erin.

## Linux, Raspberry Pi en Docker

Die builds worden niet meer gemaakt. De RingBus Tool van ZENiX draait enkel op
Windows, en de app is de schil errond. Gebruik de Windows-versie.
