# ZENiX Bridge

Tweerichtingsconverter tussen ZENiX-projectbestanden (`.rbtproject`, Rf-Technologies
brandkleppen) en Excel: je sleept een project op de app, bewerkt het werkboek en
sleept het terug.

**Handleiding: <https://freevn.github.io/ZENiX-Bridge/>** ·
**Download: [releases](https://github.com/FreeVN/ZENiX-Bridge/releases)** (`ZENiXBridge.exe`)

Deze repo is **zelfstandig**: bron, handleiding, CI en releases staan hier samen.

> **Ander product:** de **ZENiX Ringbus Editor** (web-UI, bewerken in de browser)
> woont in <https://github.com/FreeVN/ZENiX-Editor> met een eigen exe
> (`ZENiXEditor.exe`). Niets daarvan hoort in deze repo.

## Wat zit waar

| Pad | Inhoud |
|---|---|
| `app/zenix_app.py` | tkinter-GUI met drag & drop |
| `app/zenix_cli.py` | CLI (`to-xlsx`, `to-project`, `keys`, `read-key`, `selftest`) |
| `app/xlsx_build.py` | Excel-werkboek bouwen (openpyxl) |
| `app/core.py` | container-crypto (AES-256-GCM) en vendor-jar-resolutie |
| `app/java/`, `app/build/` | Java-helper (Java 17) voor het vendor-formaat |
| `docs/` | de handleiding (MkDocs Material) |
| `tests/` | pytest-suite |

## Zelf draaien

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
ZENIX_KEY=<64 hex> .venv/bin/python app/zenix_cli.py to-xlsx project.rbtproject
```

De vendor-bibliotheek (`configuration-*.jar`, `jaxb-api.jar`) zit **niet** in deze
repo: die komt uit je RingBus Tool-installatie (of `RINGBUSTOOL_HOME`).

## Release bouwen

Tag `v*` (bv. `v2.3.1`) → `.github/workflows/build.yml` bouwt `ZENiXBridge.exe` op
een Windows-runner en zet hem als asset op de release. De zelftest draait enkel
wanneer de vendor-jar lokaal in `app/lib/` staat — in deze publieke repo dus niet.

## Licentie

MIT — zie [LICENSE](LICENSE).
