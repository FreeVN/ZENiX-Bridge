#!/usr/bin/env python3
"""ZENiX Bridge — CLI (Linux, Docker, Pi).

    zenix_cli.py to-xlsx    <project.rbtproject> [out.xlsx]
    zenix_cli.py to-project <werkboek.xlsx>      [out.rbtproject]
    zenix_cli.py xlsx-to-project <werkboek.xlsx> [out.rbtproject]   # alias van to-project
    zenix_cli.py keys                       # welke sleutels zijn geladen
    zenix_cli.py read-key  [project]        # sleutel(s) uit de HASP-dongle
    zenix_cli.py selftest
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core


def out_name(path, suffix):
    stem, _ = os.path.splitext(path)
    return f"{stem}{suffix}"


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]

    if cmd == "to-xlsx":
        src = args[0]
        dst = args[1] if len(args) > 1 else out_name(src, " - elementen.xlsx")
        info = core.project_to_xlsx(src, dst, progress=lambda m: print(m, file=sys.stderr))
        print(json.dumps(info, ensure_ascii=False))
        return 0

    if cmd in ("to-project", "xlsx-to-project"):
        src = args[0]
        dst = args[1] if len(args) > 1 else out_name(src, " - aangepast.rbtproject")
        info = core.xlsx_to_project(src, dst, progress=lambda m: print(m, file=sys.stderr))
        print(json.dumps(info, ensure_ascii=False))
        return 0

    if cmd == "keys":
        ks = core.load_keys()
        print(json.dumps({"count": len(ks), "ids": [core.key_id(k) for k in ks],
                          "file": core.keys_file()}, ensure_ascii=False))
        return 0

    if cmd == "read-key":
        proj = args[0] if args else None
        keys = core.read_dongle(proj)
        path, n = core.add_keys(keys)
        print(json.dumps({"found": len(keys), "new": n, "file": path}, ensure_ascii=False))
        return 0

    if cmd == "selftest":
        info = {"java": None, "jars": [], "keys": len(core.load_keys())}
        try:
            info["java"] = core.java_exe()
        except Exception as e:
            info["error"] = str(e)
        try:
            info["jars"] = [[os.path.basename(j), os.path.exists(j)] for j in core.jars()]
        except RuntimeError as e:
            info["error"] = str(e)
        info["java_check"] = (core.java_check()
                              if info["java"] and info["jars"] else [False, "geen jars"])
        print(json.dumps(info, ensure_ascii=False))
        return 0 if (info["java"] and info["jars"] and "error" not in info
                     and all(x[1] for x in info["jars"])
                     and info["java_check"][0]) else 1

    print(__doc__)
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except RuntimeError as e:
        print(f"Fout: {e}", file=sys.stderr)
        raise SystemExit(1)
