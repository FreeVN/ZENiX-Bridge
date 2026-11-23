# Installeren

De app is één bestand per platform. Er is geen installatieprogramma en geen Java
op je systeem nodig: de JRE zit in de binary.

!!! warning "RingBus Tool moet geïnstalleerd zijn"
    Vanaf **2.2.0** zit de vendor-bibliotheek (`configuration-*.jar`,
    `jaxb-api.jar`) **niet meer** in de binary — die wordt uit je RingBus
    Tool-installatie geladen. Staat de RingBus Tool niet in het standaardpad,
    zet dan `RINGBUSTOOL_HOME` naar de installatiemap (de map die
    `ringbustool/modules` bevat). Zonder die bibliotheek kan de app geen project
    openen; ze zegt dat dan ook duidelijk.

## Windows 10/11 (x64)

1. Download `ZENiXBridge.exe` van de [releases-pagina](https://github.com/FreeVN/ZENiX-Bridge/releases).
2. Maak een map, bijvoorbeeld `C:\Tools\ZENiX Bridge\`, en zet de exe erin.
3. Zet `keys.txt` in dezelfde map — zie [Je sleutel](sleutels.md).
4. Dubbelklikken.

!!! tip "Eerste start"
    De eerste start duurt enkele seconden: een onefile-app pakt zichzelf uit in
    `%TEMP%`. Daarna gaat het snel. Windows SmartScreen kan waarschuwen omdat de
    exe niet ondertekend is: *Meer informatie → Toch uitvoeren*.

## Linux, Pi of een server

Er is **geen kant-en-klare Linux-binary en geen Docker-image**: de RingBus Tool
draait enkel op Windows, en zonder die installatie heb je de vendor-bibliotheek
niet. De CLI bestaat wel nog en draait overal waar Python en Java staan:

```bash
apt-get install -y default-jre-headless
python3 -m venv /opt/zenix/venv
/opt/zenix/venv/bin/pip install cryptography openpyxl
# zet de map app/ van de repo in /opt/zenix/app
printf '#!/bin/sh\nexec /opt/zenix/venv/bin/python /opt/zenix/app/zenix_cli.py "$@"\n' \
  > /usr/local/bin/zenix && chmod +x /usr/local/bin/zenix
zenix selftest
```

Zie [Command line](cli.md) voor de commando's.

## Controleren of alles werkt

```bash
zenix selftest          # Linux/server, uit de bron
ZENiXBridge.exe --selftest   # Windows
```

```json
{"java": ".../jre/bin/java", "jars": [["configuration-1.4.1.jar", true],
 ["jaxb-api.jar", true]], "keys": 1, "java_check": [true, "ok"]}
```

`java_check` doet een echte aanroep van de Java-helper: zo weet je dat de
meegeleverde JRE de classes kan laden, niet alleen dat `java` bestaat.

## Updaten

Nieuwe versie downloaden en de oude exe vervangen. `keys.txt` blijft staan — die
staat ernaast, niet erin.
