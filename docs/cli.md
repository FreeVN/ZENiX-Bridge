# Command line & Docker

De Linux-binary, de Pi-installatie en het Docker-image gebruiken dezelfde CLI.

## Commando's

```
ZENiXBridge-linux to-xlsx    <project.rbtproject> [out.xlsx]
ZENiXBridge-linux to-project <werkboek.xlsx>      [out.rbtproject]
ZENiXBridge-linux keys                  # geladen sleutels + key-ids
ZENiXBridge-linux read-key [project]    # sleutel(s) uit de dongle
ZENiXBridge-linux selftest              # JRE, jars en classes controleren
```

Elk commando print JSON, zodat je het in scripts kan opvangen:

```json
{"project": "Duizendpoot", "elements": 23, "zones": 2, "rings": 1,
 "out": "/data/Duizendpoot - elementen.xlsx"}
```

## Voorbeeld: in bulk omzetten

```bash
for f in projecten/*.rbtproject; do
  ZENiXBridge-linux to-xlsx "$f" "${f%.rbtproject} - elementen.xlsx"
done
```

## Docker

```bash
docker run --rm -v "$PWD:/data" -e ZENIX_KEY=<hex> \
  ghcr.io/freevn/zenix-bridge to-xlsx /data/project.rbtproject /data/project.xlsx
```

- Werkmap is `/data`; mount daar je projecten.
- Sleutel meegeven met `-e ZENIX_KEY=<hex>` of met een mount:
  `-v "$PWD/keys.txt:/opt/zenix/keys.txt:ro"`.
- Image: `ghcr.io/freevn/zenix-bridge:latest` (ook per versie, bv. `:v2.0.0`).

## In een cron of systemd-timer

```bash
ZENIX_KEY=$(cat /etc/zenix/key) /usr/local/bin/zenix to-xlsx /srv/project.rbtproject /srv/export/project.xlsx
```

De CLI geeft exitcode 0 bij succes en 1 bij een fout, met de reden op stderr.
