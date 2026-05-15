import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = str(ROOT / "scripts")


def _env():
    """Return env with scripts/ on PYTHONPATH so subprocess imports resolve."""
    e = dict(os.environ)
    existing = e.get("PYTHONPATH", "")
    e["PYTHONPATH"] = SCRIPTS + (os.pathsep + existing if existing else "")
    return e


def test_cli_emits_full_output_tree(tmp_path):
    out = tmp_path / "out"
    cmd = [
        sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile",
        "--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
        "--endpoints", str(ROOT / "tests" / "fixtures" / "golden_endpoints.json"),
        "--out", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env())
    assert r.returncode == 0, r.stderr
    assert (out / "nxui" / "_form_" / "customer.xfdl").exists()
    assert (out / "nxui" / "_datasets_" / "dsMenu.seed.xml").exists()
    assert (out / "patches" / "typedefinition.patch.xml").exists()
    assert (out / "docs" / "nexacro-report.md").exists()


def test_cli_infer_endpoints(tmp_path):
    out = tmp_path / "out"
    cmd = [
        sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile",
        "--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
        "--infer-endpoints",
        "--out", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env())
    assert r.returncode == 0, r.stderr
    assert (out / "nxui" / "_form_" / "customer.xfdl").exists()


def test_cli_rejects_missing_endpoints(tmp_path):
    out = tmp_path / "out"
    cmd = [
        sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile",
        "--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
        "--endpoints", str(tmp_path / "missing.json"),
        "--out", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env())
    assert r.returncode == 1
    assert "N002" in r.stderr
