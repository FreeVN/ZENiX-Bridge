# Command line

De Windows-exe heeft ook een CLI. Handig voor scripts en bulkwerk.

## Commando's

```bat
ZENiXBridge.exe to-xlsx    <project.rbtproject> [out.xlsx]
ZENiXBridge.exe to-project <werkboek.xlsx>      [out.rbtproject]
ZENiXBridge.exe keys                  :: geladen sleutels + key-ids
ZENiXBridge.exe read-key [project]    :: sleutel(s) uit de dongle
ZENiXBridge.exe selftest              :: JRE, jars en classes controleren
```

Elk commando print JSON, zodat je het in scripts kan opvangen:

```json
{"project": "Duizendpoot", "elements": 23, "zones": 2, "rings": 1,
 "out": "C:\\werk\\Duizendpoot - elementen.xlsx"}
```

## Voorbeeld: in bulk omzetten (PowerShell)

```powershell
Get-ChildItem projecten\*.rbtproject | ForEach-Object {
  .\ZENiXBridge.exe to-xlsx $_.FullName ($_.FullName -replace '\.rbtproject$',' - elementen.xlsx')
}
```

## In een geplande taak

```bat
set ZENIX_KEY=<hex>
"C:\Tools\ZENiX Bridge\ZENiXBridge.exe" to-xlsx "C:\werk\project.rbtproject" "C:\export\project.xlsx"
```

De CLI geeft exitcode 0 bij succes en 1 bij een fout, met de reden op stderr.

## Linux, Raspberry Pi en Docker

Die builds worden niet meer gemaakt. De RingBus Tool draait enkel op Windows, en
de app heeft de vendor-bibliotheek uit die installatie nodig. Gebruik de
Windows-exe.
