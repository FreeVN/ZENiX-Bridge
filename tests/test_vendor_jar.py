"""Vendor-jar-resolutie: RingBus Tool-installatie eerst, app/lib als ontwikkelroute."""
import os
import zipfile
from pathlib import Path

import pytest

import core

APP_LIB_DIR = Path(__file__).resolve().parents[1] / "app" / "lib"
BUNDLED_JAXB = APP_LIB_DIR / "jaxb-api.jar"


def _make_install(root, jar_name="configuration-9.9.9.jar"):
    lib = root / "ringbustool" / "modules" / "lib"
    lib.mkdir(parents=True)
    jar = lib / jar_name
    jar.write_bytes(b"")
    jaxb = lib / "jaxb-api.jar"
    jaxb.write_bytes(b"")
    return jar, jaxb


def test_vendor_jar_uit_ringbustool_home(tmp_path, monkeypatch):
    """RINGBUSTOOL_HOME wint van de app/lib-map in de repo (ontwikkelroute)."""
    jar, jaxb = _make_install(tmp_path)
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(tmp_path))
    # Sinds 2.4.0 gaat de meegebundelde jaxb-api.jar in app/lib voor op de
    # installatie; deze test dekt de vendor-resolutie, dus zonder app/lib.
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "geen-app-lib"))

    found = core.jars()

    assert found[0] == str(jar)
    assert found[1] == str(jaxb)


def test_vendor_jar_gesorteerd_en_deterministisch(tmp_path, monkeypatch):
    """Meerdere configuration-*.jar: de gesorteerde eerste wint."""
    lib = tmp_path / "ringbustool" / "modules" / "lib"
    lib.mkdir(parents=True)
    (lib / "configuration-2.0.0.jar").write_bytes(b"")
    first = lib / "configuration-1.4.1.jar"
    first.write_bytes(b"")
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(tmp_path))

    assert core.vendor_jar() == str(first)


def test_zonder_vendor_jar_expliciete_fout(tmp_path, monkeypatch):
    """Geen installatie en geen app/lib -> RuntimeError met beide termen."""
    monkeypatch.setattr(core, "_module_dirs", lambda: [])
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "leeg"))

    with pytest.raises(RuntimeError) as excinfo:
        core.jars()

    msg = str(excinfo.value)
    assert "RingBus Tool" in msg
    assert "RINGBUSTOOL_HOME" in msg


def test_ontwikkelroute_zonder_installatie(tmp_path, monkeypatch):
    """Zonder RingBus-installatie blijft app/lib werken (dev en tests).

    De publieke repo bevat geen vendor-jars (auteursrecht), dus de test zet
    zelf lege placeholders in een tijdelijke app/lib.
    """
    lib = tmp_path / "lib"
    lib.mkdir()
    (lib / "configuration-1.4.1.jar").write_bytes(b"")
    (lib / "jaxb-api.jar").write_bytes(b"")
    monkeypatch.setattr(core, "_module_dirs", lambda: [])
    monkeypatch.setattr(core, "APP_LIB", str(lib))

    found = core.jars()

    assert [os.path.basename(p) for p in found] == [
        "configuration-1.4.1.jar", "jaxb-api.jar"]
    assert all(os.path.exists(p) for p in found)
    assert os.path.dirname(found[0]) == os.path.dirname(found[1])


def test_cli_selftest_zonder_vendor_jar_faalt(tmp_path, monkeypatch, capsys):
    """De CLI-selftest meldt de ontbrekende vendor-jar en geeft exitcode 1."""
    import zenix_cli

    monkeypatch.setattr(core, "_module_dirs", lambda: [])
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "leeg"))

    assert zenix_cli.main(["selftest"]) == 1

    out = capsys.readouterr().out
    assert "RingBus Tool" in out
    assert "RINGBUSTOOL_HOME" in out


# ---------------- nieuwe layouts (RingBus Tool 1.4.x en nieuwer) ----------------

def _touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    return str(path)


def test_vendor_jar_in_modules_lib_en_modules_ext(tmp_path, monkeypatch):
    """Nieuwere Tool: lib/configuration-<versie>.jar; 1.4.x: ext/configuration.jar."""
    modules = tmp_path / "ringbustool" / "modules"
    lib_jar = _touch(modules / "lib" / "configuration-9.9.9.jar")
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "geen-app-lib"))
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(tmp_path))
    assert core.vendor_jar() == lib_jar

    (modules / "lib" / "configuration-9.9.9.jar").unlink()
    ext_jar = _touch(modules / "ext" / "configuration.jar")
    assert core.vendor_jar() == ext_jar


def test_vendor_jar_vaste_volgorde_lib_en_ext(tmp_path, monkeypatch):
    """lib-versioned > lib-plain > ext-versioned > ext-plain."""
    lib = tmp_path / "ringbustool" / "modules" / "lib"
    ext = tmp_path / "ringbustool" / "modules" / "ext"
    lib_versioned = _touch(lib / "configuration-1.4.1.jar")
    lib_plain = _touch(lib / "configuration.jar")
    ext_versioned = _touch(ext / "configuration-2.0.0.jar")
    ext_plain = _touch(ext / "configuration.jar")
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "geen-app-lib"))
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(tmp_path))

    assert core.vendor_jar() == str(lib_versioned)
    (lib / "configuration-1.4.1.jar").unlink()
    assert core.vendor_jar() == str(lib_plain)
    (lib / "configuration.jar").unlink()
    assert core.vendor_jar() == str(ext_versioned)
    (ext / "configuration-2.0.0.jar").unlink()
    assert core.vendor_jar() == str(ext_plain)


def test_vendor_jar_modules_root_fallback(tmp_path, monkeypatch):
    """Oudere/afwijkende installatie: configuration*.jar direct in modules/."""
    root_jar = _touch(tmp_path / "ringbustool" / "modules" / "configuration-3.1.jar")
    (tmp_path / "ringbustool" / "modules" / "lib").mkdir()
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "geen-app-lib"))
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(tmp_path))

    assert core.vendor_jar() == root_jar


@pytest.mark.parametrize("form", ["install", "ringbustool", "modules"])
def test_module_dirs_drie_ringbustool_home_vormen(tmp_path, monkeypatch, form):
    """RINGBUSTOOL_HOME mag de installatiemap, de ringbustool-map of modules zijn."""
    install = tmp_path / "install"
    modules = install / "ringbustool" / "modules"
    (modules / "lib").mkdir(parents=True)
    home = {"install": install,
            "ringbustool": install / "ringbustool",
            "modules": modules}[form]
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(home))

    assert core._module_dirs()[0] == str(modules)


def test_jaxb_jar_app_lib_wint_van_installatie(tmp_path, monkeypatch):
    """De meegebundelde app/lib/jaxb-api.jar heeft voorrang op de Tool."""
    bundled = _touch(tmp_path / "app-lib" / "jaxb-api.jar")
    _touch(tmp_path / "install" / "ringbustool" / "modules" / "lib" / "jaxb-api.jar")
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "app-lib"))
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(tmp_path / "install"))

    assert core.jaxb_jar() == bundled


def test_jaxb_jar_lib_wint_van_ext(tmp_path, monkeypatch):
    """Zonder app/lib: <modules>/lib/jaxb-api.jar wint van ext/."""
    lib_jar = _touch(tmp_path / "ringbustool" / "modules" / "lib" / "jaxb-api.jar")
    _touch(tmp_path / "ringbustool" / "modules" / "ext" / "jaxb-api.jar")
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "geen-app-lib"))
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(tmp_path))

    assert core.jaxb_jar() == lib_jar


def test_jaxb_jar_zonder_enige_jaxb_expliciete_fout(tmp_path, monkeypatch):
    """Geen jaxb-api.jar: RuntimeError die 'jaxb-api.jar' en 'app/lib' noemt."""
    monkeypatch.setattr(core, "_module_dirs", lambda: [])
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "leeg"))

    with pytest.raises(RuntimeError) as excinfo:
        core.jaxb_jar()

    msg = str(excinfo.value)
    assert "jaxb-api.jar" in msg
    assert "app/lib" in msg


def test_classpath_bevat_vendor_en_jaxb_jar(tmp_path, monkeypatch):
    """classpath() bevat app/build, de vendor-jar en jaxb-api.jar."""
    jar, jaxb = _make_install(tmp_path)
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "geen-app-lib"))
    monkeypatch.setenv("RINGBUSTOOL_HOME", str(tmp_path))

    parts = core.classpath().split(";" if os.name == "nt" else ":")

    assert parts[0].endswith(os.path.join("app", "build"))
    assert str(jar) in parts
    assert str(jaxb) in parts


# ---------------- meegebundelde JAXB-jar (AC11) ----------------

def test_gebundelde_jaxb_jar_is_geldige_api_en_impl():
    """app/lib/jaxb-api.jar is een geldig archief met JAXB-API en -impl-klassen."""
    assert BUNDLED_JAXB.is_file(), f"{BUNDLED_JAXB} ontbreekt"
    with zipfile.ZipFile(BUNDLED_JAXB) as archive:
        assert archive.testzip() is None
        names = archive.namelist()

    assert any(name.startswith("javax/xml/bind/") for name in names), (
        "JAXB-API (javax/xml/bind) ontbreekt in de gebundelde jar")
    assert any(name.startswith("com/sun/xml/bind/") for name in names), (
        "JAXB-implementatie (com/sun/xml/bind) ontbreekt in de gebundelde jar")
    assert any(name.startswith("javax/activation/") for name in names), (
        "JAXB-activation (javax/activation) ontbreekt in de gebundelde jar")


def test_app_lib_bevat_geen_vendor_jar():
    """De repo/exe bevat nooit een configuration*.jar (auteursrecht)."""
    leftovers = sorted(p.name for p in APP_LIB_DIR.glob("configuration*.jar"))
    assert leftovers == [], f"vendor-jar hoort niet in de repo: {leftovers}"


def test_classpath_zonder_vendor_jar_bestaande_fout(tmp_path, monkeypatch):
    """Zonder vendor-jar blijft de bestaande melding met beide termen."""
    monkeypatch.setattr(core, "_module_dirs", lambda: [])
    monkeypatch.setattr(core, "APP_LIB", str(tmp_path / "leeg"))

    with pytest.raises(RuntimeError) as excinfo:
        core.classpath()

    msg = str(excinfo.value)
    assert "RingBus Tool" in msg
    assert "RINGBUSTOOL_HOME" in msg
