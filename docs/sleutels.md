# Je sleutel

Een `.rbtproject` is versleuteld met een **projectsleutel** van 32 bytes
(64 hex-tekens). Zonder sleutel opent niets — dat is geen instelling van deze
app, dat is het formaat. De app bewaart de sleutel niet in het project en niet in
de exe.

## Drie manieren om de sleutel te regelen

### 1. In `keys.txt` naast de app

```
# commentaar mag, met #
0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

Eén sleutel per lijn. Meerdere mogen: de app probeert ze allemaal en gebruikt de
eerste die het bestand opent. Handig als je projecten van verschillende
installaties of klanten hebt.

### 2. Invoeren in de app

Knop **Sleutel invoeren…** → plak de hex-sleutel. De app controleert de lengte en
zet hem in `keys.txt`.

### 3. Uitlezen uit de dongle

Knop **Sleutel inlezen (dongle)** leest de sleutel uit de aangesloten HASP-dongle.

Voorwaarden:

- Ringbus Tool is geïnstalleerd op deze machine — de app gebruikt **de driver van
  die installatie**, die wordt niet meegeleverd.
- De dongle zit in een USB-poort.
- **Ringbus Tool is afgesloten.** Anders is de dongle bezet en krijg je
  `login 400`.

!!! warning "Niet via RDP"
    In een Remote Desktop-sessie weigert de dongle (`HASP_TS_DETECTED`). Gebruik
    een gewone console-sessie, of een geplande taak onder SYSTEM.

## Welke sleutel hoort bij dit bestand?

Elk Excel-bestand dat de app maakt, bevat een **key-id**: de eerste 12 tekens van
de SHA-256 van de sleutel. Ontbreekt de juiste sleutel, dan zegt de app:

```
De sleutel voor dit project (48fbea6cfc9d…) staat niet in keys.txt.
```

Vergelijk die id met de sleutels die je hebt, of lees de dongle van de
betreffende installatie uit.

## Waarom niet in de exe?

Een sleutel in een binary is geen geheim: iedereen die de exe heeft, kan hem
uithalen, en hij komt ook in de git-historiek terecht. `keys.txt` ernaast is
even gebruiksvriendelijk en veel properder. Wil je de sleutel niet intypen op een
nieuwe machine: kopieer `keys.txt` mee.

## Sleutels beheren

```bash
ZENiXBridge-linux keys          # aantal sleutels + key-ids
ZENiXBridge-linux read-key      # dongle uitlezen en toevoegen
```
