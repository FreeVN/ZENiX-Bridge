# Hoe het werkt

Kort genoeg om te begrijpen wat de app doet, diep genoeg om te weten waar de
grenzen zitten.

## Het bestandsformaat

Een `.rbtproject` is een zip, versleuteld met **AES-256-GCM**:

```
.rbtproject  =  AES-GCM( sleutel , zip )
zip          =  <naam>.rbproject        ← Java-serialized Configuration
                project.properties
                fb/…                    ← function blocks
```

De nonce is de sleutel zelf (32 bytes). Dat betekent dat het bestand **geen
sleutelmateriaal bevat**: zonder de projectsleutel is er niets te openen en niets
te raden. Het is geen wachtwoord op een zip; het is echte encryptie.

## De rolverdeling

| Laag | Doet |
|---|---|
| Python | sleutel beheren, decrypt/encrypt, zip in- en uitpakken, Excel bouwen en lezen, verschillen berekenen |
| Java | enkel de (de)serialisatie van de vendor-`Configuration` (`configuration-1.4.1.jar`) |

Daarom zit er een JRE in de binary: de vendor-classes zijn de enige betrouwbare
manier om het projectformaat te lezen en te schrijven.

## Waarom enkel de verschillen

Bij het terugschrijven vergelijkt de app elke rij met de basis uit `_zenix_base`.
Alleen gewijzigde velden worden aangepast. Ongewijzigde objecten blijven exact
hetzelfde object in de Java-structuur — geen nieuwe ids, geen herschikte ringen,
geen veranderde verwijzingen.

Dat is ook de reden dat `Origineel` vast staat: het is de naam waarmee de rij aan
het object gekoppeld wordt.

## Wat de app niet aanraakt

- Buscommunicatie, scannen, firmware, BACnet-configuratie.
- Elementen of ringen toevoegen.
- Function blocks.

## De sleutel en de dongle

De projectsleutel staat in de HASP-dongle van de installatie (twee bestanden op
de dongle, 32-byte blokken). De app leest die via de **HASP-driver van de
Ringbus Tool-installatie** — die driver wordt niet meegeleverd.

Projecten van een andere installatie openen alleen met de sleutel van die
installatie, tenzij de vendor één globale sleutel gebruikt. Dat laatste is enkel
vast te stellen door een vreemd project te proberen.

## De build

- `jlink` bouwt een JRE 17 met enkel de nodige modules; die gaat mee in de binary.
- De Java-helper is voor **Java 17** gecompileerd (classversie 61).
- PyInstaller maakt één bestand per platform; GitHub Actions bouwt Windows en
  Linux, draait een zelftest en publiceert bij een tag de binaries + het
  Docker-image.

De zelftest roept de Java-helper echt aan. Een binary die alleen controleert of
`java` bestaat, kan stilletjes sterven op het eerste echte bestand — dat is
precies één keer gebeurd en daarna zo opgelost.
