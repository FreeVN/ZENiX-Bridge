# Command line (uit de bron)

De CLI zit in `app/zenix_cli.py`. Er is geen kant-en-klare Linux-binary of
Docker-image meer: de RingBus Tool draait enkel op Windows. Op een server of Pi
draai je de CLI met Python uit de bron.

## Commando's

```
python3 app/zenix_cli.py to-xlsx    <project.rbtproject> [out.xlsx]
python3 app/zenix_cli.py to-project <werkboek.xlsx>      [out.rbtproject]
python3 app/zenix_cli.py keys                  # geladen sleutels + key-ids
python3 app/zenix_cli.py read-key [project]    # sleutel(s) uit de dongle
python3 app/zenix_cli.py selftest              # JRE, vendor-jars en classes
```

Op Windows doet `ZENiXBridge.exe --selftest` hetzelfde.

Elk commando print JSON, zodat je het in scripts kan opvangen:

```json
{"project": "Duizendpoot", "elements": 23, "zones": 2, "rings": 1,
 "out": "/data/Duizendpoot - elementen.xlsx"}
```

## Voorbeeld: in bulk omzetten

```bash
for f in projecten/*.rbtproject; do
  python3 app/zenix_cli.py to-xlsx "$f" "${f%.rbtproject} - elementen.xlsx"
done
```

## De vendor-bibliotheek

De CLI heeft `configuration-*.jar` nodig. Die komt uit je RingBus Tool-installatie
of uit de map waarnaar `RINGBUSTOOL_HOME` wijst (de map met
`ringbustool/modules`). Ontbreekt ze, dan stopt de CLI met een duidelijke melding.

## In een cron of systemd-timer

```bash
ZENIX_KEY=$(cat /etc/zenix/key) /usr/local/bin/zenix to-xlsx /srv/project.rbtproject /srv/export/project.xlsx
```

De CLI geeft exitcode 0 bij succes en 1 bij een fout, met de reden op stderr.
