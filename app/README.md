# ZENiX Ringbus Toolchain — app-bron

Deze map bevat de bron van beide tools: **ZENiX Bridge** (`zenix_app.py`,
`zenix_cli.py`) en de **ZENiX Ringbus Editor** (`web/`).

- **Volledige handleiding:** [../docs/HANDLEIDING.md](../docs/HANDLEIDING.md)
- **Overzicht en downloads:** [../README.md](../README.md)

```
app/
  zenix_app.py   GUI (tkinter + tkinterdnd2, FlexPoll-huisstijl)
  zenix_cli.py   CLI: to-xlsx | to-project | keys | read-key | selftest
  core.py        crypto, zip, Java-aanroep, sleutelbeheer
  xlsx_build.py  Excel opbouwen (gedeeld met de Google Sheets-variant)
  diff_edits.py  vergelijking bewerkte rijen vs. basis
  java/          ZenixTool.java (dump/apply), ZenixKey.java (dongle)
  lib/           jaxb-api.jar (meegebundeld, JAXB 2.3.1); configuration*.jar
                 lokaal neerzetten om te ontwikkelen (nooit committen)
  build/         gecompileerde classes (Java 17, classversie 61)
  assets/        Montserrat (OFL)
```

## Lokaal testen

```bash
python3 -m venv .venv && .venv/bin/pip install cryptography openpyxl
.venv/bin/python app/zenix_cli.py selftest
.venv/bin/python app/zenix_cli.py to-xlsx samples/Duizendpoot/Duizendpoot.rbtproject /tmp/x.xlsx
```

De vendor-jar (`configuration*.jar`) komt uit je RingBus Tool-installatie of uit
`RINGBUSTOOL_HOME`. `app/lib/jaxb-api.jar` zit in de repo en wordt door
PyInstaller meegebundeld via `--add-data "app/lib;app/lib"`.
