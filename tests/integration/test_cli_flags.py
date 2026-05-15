import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _env():
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    scripts = str(ROOT / "scripts")
    env["PYTHONPATH"] = scripts + (os.pathsep + existing if existing else "")
    return env


def _run(args):
    cmd = [sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile"] + args
    return subprocess.run(cmd, capture_output=True, text=True, env=_env())


def test_n007_conflict_without_force(tmp_path):
    out = tmp_path / "out"
    base = ["--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
            "--endpoints", str(ROOT / "tests" / "fixtures" / "golden_endpoints.json"),
            "--out", str(out)]
    assert _run(base).returncode == 0
    r2 = _run(base)
    assert r2.returncode == 1
    assert "N007" in r2.stderr


def test_force_creates_bak(tmp_path):
    out = tmp_path / "out"
    base = ["--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
            "--endpoints", str(ROOT / "tests" / "fixtures" / "golden_endpoints.json"),
            "--out", str(out)]
    assert _run(base).returncode == 0
    assert _run(base + ["--force"]).returncode == 0
    assert (out / "nxui" / "_form_" / "customer.xfdl.bak").exists()
