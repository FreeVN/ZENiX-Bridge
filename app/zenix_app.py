#!/usr/bin/env python3
"""ZENiX Bridge — sleep een .rbtproject of .xlsx en krijg het andere terug.

GUI in FlexPoll-huisstijl (rood #E4002B, blauw #2271B1, Montserrat).
"""
import os
import queue
import sys
import threading
import traceback
import webbrowser

import tkinter as tk
from tkinter import filedialog, font as tkfont

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except Exception:                                  # pragma: no cover
    HAS_DND = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core

VERSION = "2.0.0"
RED = "#E4002B"
BLUE = "#2271B1"
INK = "#1E1E1E"
MUTED = "#6B7480"
LINE = "#E3E8EF"
BG = "#F4F6F9"
WHITE = "#FFFFFF"
GREEN = "#16A34A"
AMBER = "#E08B0A"


def pick_font(root):
    families = set(tkfont.families(root))
    for name in ("Montserrat", "Segoe UI", "Helvetica Neue", "Arial"):
        if name in families:
            return name
    return "TkDefaultFont"


def register_fonts():
    if os.name != "nt":
        return
    try:
        import ctypes
        import glob
        for f in glob.glob(core.res("app", "assets", "*.ttf")):
            ctypes.windll.gdi32.AddFontResourceExW(f, 0x10, 0)
    except Exception:
        pass


class App:
    def __init__(self, root):
        self.root = root
        self.q = queue.Queue()
        self.last_out = None
        self.busy = False

        root.title("ZENiX Bridge")
        root.configure(bg=BG)
        root.geometry("780x620")
        root.minsize(680, 540)

        self.f = pick_font(root)

        self._build_header()
        self._build_dropzone()
        self._build_status()
        self._build_footer()

        if HAS_DND:
            for w in (self.zone, self.zone_label, self.zone_hint, self.zone_click):
                w.drop_target_register(DND_FILES)
                w.dnd_bind("<<Drop>>", self.on_drop)

        self.root.after(120, self.poll)

    # ---------- opbouw ----------
    def _build_header(self):
        bar = tk.Frame(self.root, bg=WHITE, height=98)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        left = tk.Frame(bar, bg=WHITE)
        left.pack(side="left", padx=26, pady=12)
        word = tk.Frame(left, bg=WHITE)
        word.pack(anchor="w")
        tk.Label(word, text="ZENiX", bg=WHITE, fg=RED,
                 font=(self.f, 24, "bold")).pack(side="left")
        tk.Label(word, text=" Bridge", bg=WHITE, fg=INK,
                 font=(self.f, 24, "bold")).pack(side="left")
        tk.Label(left, text="Ringbus project  ⇄  Excel", bg=WHITE, fg=MUTED,
                 font=(self.f, 10)).pack(anchor="w")
        right = tk.Frame(bar, bg=WHITE)
        right.pack(side="right", padx=26)
        tk.Label(right, text=f"v{VERSION}", bg=WHITE, fg=MUTED,
                 font=(self.f, 9)).pack(anchor="e")
        tk.Frame(self.root, bg=RED, height=3).pack(fill="x")

    def _build_dropzone(self):
        wrap = tk.Frame(self.root, bg=BG)
        wrap.pack(fill="both", expand=True, padx=26, pady=18)

        self.zone = tk.Canvas(wrap, bg=WHITE, highlightthickness=0, height=280)
        self.zone.pack(fill="both", expand=True)
        self.zone.bind("<Configure>", lambda e: self._draw_zone())
        self.zone.bind("<Button-1>", lambda e: self.choose_file())

        self.zone_label = tk.Label(self.zone, text="Sleep je bestand hierheen",
                                   bg=WHITE, fg=INK, font=(self.f, 17, "bold"))
        self.zone_hint = tk.Label(self.zone,
                                  text=".rbtproject  →  Excel        .xlsx  →  projectbestand",
                                  bg=WHITE, fg=MUTED, font=(self.f, 10))
        self.zone_label.place(relx=0.5, rely=0.44, anchor="center")
        self.zone_hint.place(relx=0.5, rely=0.545, anchor="center")
        self.zone_click = tk.Label(self.zone, text="of klik in dit vak om te kiezen",
                                   bg=WHITE, fg=BLUE, font=(self.f, 9))
        self.zone_click.place(relx=0.5, rely=0.62, anchor="center")
        self.zone_click.bind("<Button-1>", lambda e: self.choose_file())

        btns = tk.Frame(wrap, bg=BG)
        btns.pack(fill="x", pady=(12, 0))
        self.btn_pick = tk.Button(btns, text="Bestand kiezen…", command=self.choose_file,
                                  bg=RED, fg=WHITE, activebackground="#C00025",
                                  activeforeground=WHITE, relief="flat", bd=0,
                                  font=(self.f, 10, "bold"), padx=18, pady=8,
                                  cursor="hand2")
        self.btn_pick.pack(side="left")
        self.btn_open = tk.Button(btns, text="Map openen", command=self.open_folder,
                                  bg=WHITE, fg=INK, activebackground=BG,
                                  relief="flat", bd=0, highlightthickness=1,
                                  highlightbackground=LINE, font=(self.f, 10),
                                  padx=16, pady=8, cursor="hand2", state="disabled")
        self.btn_open.pack(side="left", padx=10)

        self.btn_key = tk.Button(btns, text="Sleutel invoeren…", command=self.enter_key,
                                 bg=WHITE, fg=INK, activebackground=BG, relief="flat", bd=0,
                                 highlightthickness=1, highlightbackground=LINE,
                                 font=(self.f, 10), padx=14, pady=8, cursor="hand2")
        self.btn_key.pack(side="right")
        self.btn_dongle = tk.Button(btns, text="Sleutel inlezen (dongle)", command=self.read_key,
                                    bg=WHITE, fg=INK, activebackground=BG, relief="flat", bd=0,
                                    highlightthickness=1, highlightbackground=LINE,
                                    font=(self.f, 10), padx=14, pady=8, cursor="hand2")
        self.btn_dongle.pack(side="right", padx=8)
        if not core.hasp_home():
            self.btn_dongle.configure(state="disabled", fg=MUTED)

    def _build_status(self):
        wrap = tk.Frame(self.root, bg=WHITE, highlightthickness=1,
                        highlightbackground=LINE)
        wrap.pack(fill="x", padx=26)
        inner = tk.Frame(wrap, bg=WHITE)
        inner.pack(fill="x", padx=16, pady=12)
        self.dot = tk.Canvas(inner, width=12, height=12, bg=WHITE, highlightthickness=0)
        self.dot.pack(side="left", padx=(0, 10))
        self._dot_item = self.dot.create_oval(1, 1, 11, 11, fill=MUTED, outline="")
        self.msg = tk.Label(inner, text="Klaar om te converteren.", bg=WHITE, fg=INK,
                            font=(self.f, 10), anchor="w", justify="left")
        self.msg.pack(side="left", fill="x", expand=True)

    def _build_footer(self):
        foot = tk.Frame(self.root, bg=BG)
        foot.pack(fill="x", padx=26, pady=(10, 14))
        n = len(core.load_keys())
        txt = f"{n} sleutel{'s' if n != 1 else ''} geladen"
        if not n:
            txt = "geen sleutel gevonden — lees de dongle in of voer er een in"
        self.key_label = tk.Label(foot, text=txt, bg=BG, fg=MUTED, font=(self.f, 9))
        self.key_label.pack(side="left")
        tk.Label(foot, text="sleutel nodig om .rbtproject te openen",
                 bg=BG, fg=MUTED, font=(self.f, 9)).pack(side="right")

    def _draw_zone(self, colour=LINE):
        c = self.zone
        c.delete("border")
        w, h = c.winfo_width(), c.winfo_height()
        c.create_rectangle(14, 14, w - 14, h - 14, outline=colour, width=2,
                           dash=(7, 5), tags="border")

    # ---------- acties ----------
    def choose_file(self):
        if self.busy:
            return
        path = filedialog.askopenfilename(
            title="Kies een bestand",
            filetypes=[("ZENiX bestanden", "*.rbtproject *.xlsx"),
                       ("Projectbestand", "*.rbtproject"),
                       ("Excel", "*.xlsx")])
        if path:
            self.handle(path)

    def on_drop(self, event):
        if self.busy:
            return
        raw = event.data
        if raw.startswith("{"):
            raw = raw[1:raw.index("}")]
        else:
            raw = raw.split()[0]
        self.handle(raw)

    def handle(self, path):
        path = path.strip().strip('"')
        if not os.path.isfile(path):
            self.set_status("Dat bestand bestaat niet.", AMBER)
            return
        ext = os.path.splitext(path)[1].lower()
        if ext not in (".rbtproject", ".xlsx"):
            self.set_status("Alleen .rbtproject of .xlsx.", AMBER)
            return
        self.busy = True
        self.btn_pick.configure(state="disabled")
        self.btn_open.configure(state="disabled")
        self._draw_zone(BLUE)
        threading.Thread(target=self._work, args=(path,), daemon=True).start()

    def _work(self, path):
        try:
            stem, ext = os.path.splitext(path)
            if ext.lower() == ".rbtproject":
                out = f"{stem} - elementen.xlsx"
                self.q.put(("status", "Project ontsleutelen…", BLUE))
                info = core.project_to_xlsx(path, out, self._progress)
                self.q.put(("ok", f"{info['project']} → Excel  ·  {info['elements']} elementen, "
                                  f"{info['zones']} zones, {info['rings']} ring(en)", out))
            else:
                out = f"{stem} - aangepast.rbtproject"
                self.q.put(("status", "Excel lezen…", BLUE))
                info = core.xlsx_to_project(path, out, self._progress)
                extra = ""
                if info.get("unknown"):
                    extra = f"  ·  {len(info['unknown'])} rij(en) niet herkend"
                self.q.put(("ok", f"Project geschreven  ·  {info['changes']} wijzigingen"
                                  f"{extra}", out))
        except KeyError as e:
            self.q.put(("err", str(e).strip("'"), None))
        except Exception as e:
            detail = str(e) or e.__class__.__name__
            self.q.put(("err", detail, traceback.format_exc()))

    def _progress(self, text):
        self.q.put(("status", text, BLUE))

    def poll(self):
        try:
            while True:
                kind, text, extra = self.q.get_nowait()
                if kind == "status":
                    self.set_status(text, extra)
                elif kind == "keys":
                    self.refresh_keys()
                    self.set_status(text, GREEN)
                elif kind == "ok":
                    self.busy = False
                    self.btn_pick.configure(state="normal")
                    self.last_out = extra
                    self.btn_open.configure(state="normal")
                    self._draw_zone(GREEN)
                    self.set_status(text, GREEN)
                else:
                    self.busy = False
                    self.btn_pick.configure(state="normal")
                    self._draw_zone(RED)
                    self.set_status(text, RED)
                    if extra:
                        print(extra, file=sys.stderr)
        except queue.Empty:
            pass
        self.root.after(120, self.poll)

    def set_status(self, text, colour=MUTED):
        self.dot.itemconfigure(self._dot_item, fill=colour)
        self.msg.configure(text=text)

    def refresh_keys(self):
        n = len(core.load_keys())
        self.key_label.configure(
            text=f"{n} sleutel{'s' if n != 1 else ''} geladen" if n
            else "geen sleutel gevonden — lees de dongle in of voer er een in")

    def enter_key(self):
        from tkinter import simpledialog
        val = simpledialog.askstring("Sleutel invoeren",
                                     "Plak de hex-sleutel (64 tekens):", parent=self.root)
        if not val:
            return
        try:
            path, n = core.add_keys([val])
        except Exception as e:
            self.set_status(str(e), RED)
            return
        self.refresh_keys()
        self.set_status(f"Sleutel {'toegevoegd' if n else 'bestond al'} ({path}).", GREEN)

    def read_key(self):
        if self.busy:
            return
        self.set_status("Dongle uitlezen…", BLUE)
        threading.Thread(target=self._read_key_worker, daemon=True).start()

    def _read_key_worker(self):
        try:
            keys = core.read_dongle()
            path, n = core.add_keys(keys)
            self.q.put(("keys", f"{n} sleutel(s) uit de dongle toegevoegd." if n
                        else "De sleutel(s) stonden al in keys.txt.", None))
        except Exception as e:
            self.q.put(("err", str(e), None))

    def open_folder(self):
        if not self.last_out:
            return
        folder = os.path.dirname(os.path.abspath(self.last_out))
        try:
            if os.name == "nt":
                os.startfile(folder)
            elif sys.platform == "darwin":
                os.system(f'open "{folder}"')
            else:
                webbrowser.open(f"file://{folder}")
        except Exception:
            pass


def selftest():
    """--selftest: controleer of alles aanwezig is (gebruikt door CI)."""
    import json
    ok = {"java": None, "jars": [], "keys": len(core.load_keys()), "dnd": HAS_DND}
    try:
        ok["java"] = core.java_exe()
    except Exception as e:
        ok["error"] = str(e)
    try:
        for j in core.jars():
            ok["jars"].append([os.path.basename(j), os.path.exists(j)])
    except RuntimeError as e:
        ok["error"] = str(e)
    if ok.get("error"):
        print(json.dumps(ok))
        return 1
    print(json.dumps(ok))
    ok["java_check"] = core.java_check() if ok["java"] else [False, "geen java"]
    good = (ok["java"] and all(x[1] for x in ok["jars"]) and ok["java_check"][0])
    return 0 if good else 1


def main():
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    register_fonts()
    root = TkinterDnD.Tk() if HAS_DND else tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
