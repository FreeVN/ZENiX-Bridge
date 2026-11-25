# app/lib — vendor- en runtime-bibliotheek

De RingBus Tool van Rf-Technologies levert `configuration-*.jar`. Dat bestand is
auteursrechtelijk beschermd: het zit **niet** in deze repo en **niet** in de exe.

`jaxb-api.jar` is anders: ZENiX Bridge bundelt sinds 2.4.0 zelf een samengevoegde
JAXB 2.3.1 (API + implementatie + core + activation) en die zit **wel** in deze
map en in de exe. Daardoor werkt de app ook op een JRE zonder losse JAXB-modules.

## Ondersteunde RingBus Tool-indelingen

| RingBus Tool | Locatie van de vendor-jar | Java |
|---|---|---|
| 1.4.x | `modules/ext/configuration.jar` | 8 |
| nieuwer | `modules/lib/configuration-<versie>.jar` | 8/17 |

Per modules-map zoekt de app in deze volgorde:

1. `lib/configuration-*.jar` (gesorteerd — de eerste wint);
2. `lib/configuration.jar`;
3. `ext/configuration-*.jar` (gesorteerd);
4. `ext/configuration.jar`;
5. `configuration*.jar` direct in `modules/`.

`RINGBUSTOOL_HOME` mag naar de installatiemap, naar de `ringbustool`-map zelf of
naar de `modules`-map wijzen. Daarna volgen de standaardinstallatiepaden en pas
als laatste deze map (`app/lib/`) als ontwikkel-fallback.

## Git

`app/lib/*.jar` staat in `.gitignore`, met één uitzondering:
`!app/lib/jaxb-api.jar`. Alleen de meegebundelde JAXB-jar is versiebeheerd; zet
hier lokaal eventueel een `configuration*.jar` neer om te ontwikkelen, maar
commit die nooit.
