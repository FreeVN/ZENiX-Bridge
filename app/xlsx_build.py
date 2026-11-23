#!/usr/bin/env python3
"""ZENiX Excel-hulp: zet rijen (uit een dump of uit de Google Sheet) om naar .xlsx.

    xlsx_build.py <dump.json> <out.xlsx>     # uit een project-dump
    (voor de live sheet: gsheet_to_xlsx.py)

Opmaak identiek aan de Google Sheet: rode koppen = invulbaar, donkere koppen met
slotje = vast, grijze cellen = niet wijzigen.
"""
import json, sys, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

FONT = "Montserrat"
RED = "E4002B"
BLUE = "2271B1"
SLATE = "5C6B7A"
LOCK_BG = "DCE3EC"
LOCK_TXT = "5A6673"
BAND = "FBFCFD"
SOFT = "EAF2FA"
INK = "1E1E1E"
MUTED = "6B7480"

HEAD_FILL = PatternFill("solid", fgColor=RED)
LOCK_HEAD_FILL = PatternFill("solid", fgColor=SLATE)
HEAD_FONT = Font(name=FONT, bold=True, color="FFFFFF", size=10)
LOCK_FILL = PatternFill("solid", fgColor=LOCK_BG)
BAND_FILL = PatternFill("solid", fgColor=BAND)
SECTION_FILL = PatternFill("solid", fgColor=BLUE)
THIN = Side(style="thin", color="D6DEE8")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

ELEMENT_COLS = ["Origineel", "Naam", "Ring", "Unit", "Unit-ID", "Adres", "Index in ring",
                "Type", "Device type", "Zones", "Beschrijving", "Alarmfunctie",
                "Normaal open", "Inverteren", "Veilig", "FB master", "FB conditioneel"]
WIDTHS = [24, 26, 16, 7, 15, 7, 13, 10, 13, 10, 32, 13, 12, 11, 9, 18, 18]
LOCKED = [0, 4, 6, 9, 15, 16]
SECTIONS = {"PROJECT", "WERKWIJZE", "LEGENDE", "KOLOMMEN"}


def _style_info(ws, rows):
    ws.sheet_view.showGridLines = False
    for col, w in (("A", 4), ("B", 30), ("C", 95), ("D", 14)):
        ws.column_dimensions[col].width = w
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row, start=1):
            if val is None or val == "":
                continue
            c = ws.cell(row=i, column=j, value=val)
            key = str(val)
            if i == 1 and j == 2:
                c.font = Font(name=FONT, bold=True, size=26, color=RED)
            elif i == 1 and j == 3:
                c.font = Font(name=FONT, bold=True, size=18, color=INK)
            elif i == 2:
                c.font = Font(name=FONT, size=10, color=MUTED)
            elif key in SECTIONS:
                c.font = Font(name=FONT, bold=True, size=9, color="FFFFFF")
                c.alignment = Alignment(vertical="center")
                for k in range(2, 5):
                    ws.cell(row=i, column=k).fill = SECTION_FILL
                ws.row_dimensions[i].height = 22
            elif key.startswith("Gegenereerd"):
                c.font = Font(name=FONT, size=9, italic=True, color=MUTED)
            elif j == 2:
                c.font = Font(name=FONT, bold=True, size=10, color=INK)
            else:
                c.font = Font(name=FONT, size=10, color=MUTED)
                c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[1].height = 40


def _put(ws, r, c, val):
    """Schrijf een waarde; tekst die met '=' begint blijft tekst (geen Excel-formule)."""
    cell = ws.cell(row=r, column=c)
    cell.value = val
    if isinstance(val, str) and val.startswith("="):
        cell.data_type = "s"
    return cell


def _style_table(ws, ncols, widths, lock_cols=(), freeze="A2"):
    for i, w in enumerate(widths[:ncols], start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = LOCK_HEAD_FILL if (c - 1) in lock_cols else HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = freeze
    ws.auto_filter.ref = f"A1:{get_column_letter(ncols)}{max(ws.max_row, 1)}"
    for ri, row in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row, max_col=ncols), start=2):
        for idx, cell in enumerate(row):
            cell.border = BORDER
            if idx in lock_cols:
                cell.fill = LOCK_FILL
                cell.font = Font(name=FONT, size=10, color=LOCK_TXT)
            else:
                cell.font = Font(name=FONT, size=10, color=INK)
                if ri % 2 == 0:
                    cell.fill = BAND_FILL


def write_rows(rows, out_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Info"
    info = rows.get("Info", [])
    for r in info:
        ws.append(["" if v is None else v for v in r])
    _style_info(ws, info)

    tab_widths = {"Ringen": [6, 22, 16, 10, 16, 16], "Zones": [6, 18, 30, 10, 17]}
    for name in ("Ringen", "Zones"):
        ws = wb.create_sheet(name)
        data = rows.get(name, [])
        for r in data:
            ws.append(["" if v is None else v for v in r])
        ncols = max((len(r) for r in data), default=1)
        _style_table(ws, ncols, tab_widths[name], (), "A2")

    ws = wb.create_sheet("Elementen")
    data = rows.get("Elementen", [])
    for r in data:
        ws.append(["" if v is None else v for v in r])
    _style_table(ws, len(ELEMENT_COLS), WIDTHS, tuple(LOCKED), "A2")

    last = max(ws.max_row, 2)
    types = DataValidation(type="list", allow_blank=True,
                           formula1='"fire,smoke,di,do,motorless,smoke op,smoke cl,smoke o/c"')
    ws.add_data_validation(types); types.add(f"H2:H{last}")
    dev = DataValidation(type="list", allow_blank=True, formula1=(
        '"FIRE,FIRE_LOCAL,FIRE2M,FIRE2S,FIRE2B,SMOKE,SMOKE_LOCAL,SMOKE OP,SMOKE CL,SMOKE O/C,'
        'DIN,DIN2,DOM08,DOM12,DOM16,DOM2,MOTORLESS,MOTORLESS2M,FIO_8_8,FIO_12_0,FIO_8_4,FIO_0_12"'))
    ws.add_data_validation(dev); dev.add(f"I2:I{last}")
    bo = DataValidation(type="list", formula1='"WAAR,ONWAAR"', allow_blank=True)
    ws.add_data_validation(bo); bo.add(f"M2:M{last}"); bo.add(f"N2:N{last}")

    ws = wb.create_sheet("Zone-lidmaatschap")
    data = rows.get("Zone-lidmaatschap", [])
    for r in data:
        ws.append(["" if v is None else v for v in r])
    ncols = max((len(r) for r in data), default=3)
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = LOCK_HEAD_FILL if c <= 2 else HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell2 = ws.cell(row=2, column=c)
        cell2.fill = PatternFill("solid", fgColor=SOFT)
        cell2.font = Font(name=FONT, size=9, bold=True, color=MUTED)
        cell2.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(c)].width = 24 if c == 1 else (15 if c == 2 else 9)
    ws.row_dimensions[1].height = 24
    ws.row_dimensions[2].height = 20
    ws.freeze_panes = "C3"
    for ri, row in enumerate(ws.iter_rows(min_row=3, max_row=ws.max_row, max_col=ncols), start=3):
        for idx, cell in enumerate(row):
            cell.border = BORDER
            if idx < 2:
                cell.fill = LOCK_FILL
                cell.font = Font(name=FONT, size=10, color=LOCK_TXT)
            else:
                cell.font = Font(name=FONT, size=10, color=INK)
                if ri % 2 == 1:
                    cell.fill = BAND_FILL
    chk = DataValidation(type="list", formula1='"WAAR,ONWAAR"', allow_blank=True)
    ws.add_data_validation(chk)
    chk.add(f"C3:{get_column_letter(max(ncols, 3))}{max(ws.max_row, 3)}")

    for sh in wb.worksheets:
        for row in sh.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    cell.data_type = "s"

    from openpyxl.worksheet.properties import PageSetupProperties
    for sh in wb.worksheets:
        sh.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
        sh.page_setup.fitToWidth = 1
        sh.page_setup.fitToHeight = 0
        sh.page_setup.orientation = "landscape" if sh.title != "Info" else "portrait"
        sh.print_options.horizontalCentered = True

    wb.save(out_path)
    return out_path


def rows_from_dump(dump_path):
    """Rijen uit een dump-JSON, met dezelfde indeling als de Google Sheet."""
    d = json.load(open(dump_path, encoding="utf-8"))
    ring = d["rings"][0] if d["rings"] else {"name": "-", "host": "-"}
    zones = d["zones"]
    n_slots = max(12, len(zones) + 4)
    info = [
        ["", "ZENiX", d.get("project", ""), ""],
        ["", "Ringbus Tool  ·  projectbeheer", "", ""],
        ["", "", "", ""],
        ["", "PROJECT", "", ""],
        ["", "Ringen", f'{len(d["rings"])}  ·  {ring.get("name","-")} @ {ring.get("host","-")}', ""],
        ["", "Zones", f'{len(zones)}  ·  ' + (", ".join(z["name"] for z in zones) or "geen"), ""],
        ["", "Elementen", str(len(d["elements"])), ""],
        ["", "", "", ""],
        ["", "WERKWIJZE", "", ""],
        ["", "1", "Pas enkel de witte kolommen aan in 'Elementen'. Grijze kolommen zijn identificatie.", ""],
        ["", "2", "Wijs zones toe met de checkboxes in 'Zone-lidmaatschap'.", ""],
        ["", "3", "Nieuwe zone? Zet een rij onderaan 'Zones' met lege Id + naam.", ""],
        ["", "4", "Klaar? Luc schrijft enkel de gewijzigde velden terug in het projectbestand.", ""],
        ["", "", "", ""],
        ["", "LEGENDE", "", ""],
        ["", "\U0001F512  Vast", "grijze kolom - identificatie of formule, niet wijzigen", ""],
        ["", "Rood", "invulbaar: witte cellen mag je aanpassen", ""],
        ["", "", "", ""],
        ["", "KOLOMMEN", "", ""],
    ]
    uitleg = {
        "Origineel": "interne naam - niet wijzigen, koppeling met het project",
        "Naam": "vrije naam, mag aangepast worden",
        "Ring": "keuze uit de lijst met ringen",
        "Unit": "positie van de unit op de bus",
        "Unit-ID": "fabrieks-id van de unit - vast",
        "Adres": "punt op de unit",
        "Index in ring": "afgeleid - wordt bij openen herberekend",
        "Type": "soort punt (fire, di, do, ...)",
        "Device type": "hardwaretype van de unit",
        "Zones": "info - toewijzen gebeurt in 'Zone-lidmaatschap'",
        "Beschrijving": "vrij tekstveld",
        "Alarmfunctie": "AND/OR-combinatie van de alarmen",
        "Normaal open": "checkbox",
        "Inverteren": "checkbox",
        "Veilig": "veiligheidstand bij FIO-uitgangen",
        "FB master": "function block - vast",
        "FB conditioneel": "function block - vast",
    }
    for c in ELEMENT_COLS:
        info.append(["", c, uitleg.get(c, ""), ""])
    info += [["", "", "", ""],
             ["", f"Gegenereerd door Luc  ·  {datetime.datetime.now():%d-%m-%Y %H:%M}", "", ""]]

    rings = [["Id", "Naam", "Host (IP)", "CPU-type", "BACnet instance", "BACnet netwerk"]]
    for r in d["rings"]:
        rings.append([r["id"], r["name"], r["host"], r["cpuType"],
                      r["bacnetInstanceId"], r["bacnetNetwork"]])

    zrows = [["Id", "Naam", "Beschrijving", "Volgorde", "Aantal elementen"]]
    for z in zones:
        zrows.append([z["id"], z["name"], z.get("description") or "", z.get("order") or 0,
                      len(z.get("elements") or [])])

    header = [("\U0001F512 " + c) if i in LOCKED else c for i, c in enumerate(ELEMENT_COLS)]
    el = [header]
    for e in d["elements"]:
        el.append([e["name"], e["name"], e["ring"], e["unit"], e["unitId"], e["address"],
                   e["indexInRing"], e["typeName"], e["deviceTypeName"],
                   ",".join(str(z) for z in (e.get("zones") or [])),
                   e.get("description") or "", e.get("alarmFunction") or "",
                   bool(e.get("normalOpen")), bool(e.get("invert")),
                   e.get("safe") or "", e.get("fbMaster") or "", e.get("fbConditional") or ""])

    zone_ids = [str(z["id"]) for z in zones]
    row1 = ["\U0001F512 Origineel", "\U0001F512 Unit-ID"] + zone_ids + [""] * (n_slots - len(zone_ids))
    row2 = ["Element", ""] + [z["name"] for z in zones] + [""] * (n_slots - len(zone_ids))
    mat = [row1, row2]
    for e in d["elements"]:
        mine = {str(x) for x in (e.get("zones") or [])}
        mat.append([e["name"], e["unitId"]] + [z in mine for z in zone_ids] +
                   [False] * (n_slots - len(zone_ids)))

    return {"Info": info, "Ringen": rings, "Zones": zrows,
            "Elementen": el, "Zone-lidmaatschap": mat}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    rows = rows_from_dump(sys.argv[1])
    write_rows(rows, sys.argv[2])
    print(f"OK {sys.argv[2]}: {len(rows['Elementen']) - 1} elementen, "
          f"{len(rows['Zones']) - 1} zones")
