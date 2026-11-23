# ZENiX Bridge — handleiding

De handleiding van [ZENiX Bridge](https://github.com/FreeVN/zenix-ringbus-tool):
een tweerichtingsconverter tussen ZENiX-projectbestanden (`.rbtproject`) en Excel.

**Lezen kan hier: <https://freevn.github.io/ZENiX-Bridge/>**

## Lokaal bekijken

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-docs.txt
.venv/bin/mkdocs serve
```

Deze repo bevat **enkel documentatie**. De app zelf staat in de privé-repo
[FreeVN/zenix-ringbus-tool](https://github.com/FreeVN/zenix-ringbus-tool).

> **Niet hetzelfde als de Ringbus Editor.** In diezelfde code-repo zit ook de
> **ZENiX Ringbus Editor**: een web-UI die het project rechtstreeks in de browser
> bewerkt (elementen, zones, ringen, alarmen, controlematrix). Dat is een **ander**
> product, met eigen docs (`docs/RINGBUS-EDITOR.md`) en eigen tags (`editor-v*`).
> De Bridge gebruikt `bridge-v*`.
