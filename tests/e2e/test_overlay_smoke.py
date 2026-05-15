import os
import pathlib
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _env():
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    scripts = str(ROOT / "scripts")
    env["PYTHONPATH"] = scripts + (os.pathsep + existing if existing else "")
    return env


def test_e2e_blueprint_to_overlay(tmp_path):
    out = tmp_path / "out"
    cmd = [
        sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile",
        "--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
        "--endpoints", str(ROOT / "tests" / "fixtures" / "golden_endpoints.json"),
        "--out", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env())
    assert r.returncode == 0, r.stderr

    targets = [
        out / "nxui" / "_form_" / "customer.xfdl",
        out / "nxui" / "_datasets_" / "dsMenu.seed.xml",
        out / "patches" / "typedefinition.patch.xml",
    ]
    for p in targets:
        assert p.exists()
        ET.parse(p)

    scaffold = tmp_path / "scaffold"
    (scaffold / "nxui" / "_form_").mkdir(parents=True)
    (scaffold / "nxui" / "_datasets_").mkdir(parents=True)
    shutil.copy(out / "nxui" / "_form_" / "customer.xfdl",
                scaffold / "nxui" / "_form_" / "customer.xfdl")
    shutil.copy(out / "nxui" / "_datasets_" / "dsMenu.seed.xml",
                scaffold / "nxui" / "_datasets_" / "dsMenu.seed.xml")
    assert (scaffold / "nxui" / "_form_" / "customer.xfdl").exists()
