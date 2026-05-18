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


import yaml


def test_cli_default_pattern_flag(tmp_path):
    """--default-pattern F1 should produce a form with no <Grid> for all entities."""
    out = tmp_path / "out"
    cmd = [
        sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile",
        "--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
        "--endpoints", str(ROOT / "tests" / "fixtures" / "golden_endpoints.json"),
        "--default-pattern", "F1",
        "--out", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env())
    assert r.returncode == 0, r.stderr
    xfdl = (out / "nxui" / "_form_" / "customer.xfdl").read_text(encoding="utf-8")
    assert "<Grid" not in xfdl
    assert "btn_save" in xfdl


def test_cli_service_name_flag(tmp_path):
    """--service-name Order should yield SvcOrder + /uiadapter/order in patch and xfdl."""
    out = tmp_path / "out"
    cmd = [
        sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile",
        "--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
        "--endpoints", str(ROOT / "tests" / "fixtures" / "golden_endpoints.json"),
        "--service-name", "Order",
        "--out", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env())
    assert r.returncode == 0, r.stderr
    patch = (out / "patches" / "typedefinition.patch.xml").read_text(encoding="utf-8")
    assert 'id="SvcOrder"' in patch
    assert 'url="/uiadapter/order"' in patch
    xfdl = (out / "nxui" / "_form_" / "customer.xfdl").read_text(encoding="utf-8")
    assert "SvcOrder::" in xfdl


def test_cli_service_name_compound_slugified(tmp_path):
    """--service-name SalesOrder should snake_case the URL slug to sales_order."""
    out = tmp_path / "out"
    cmd = [
        sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile",
        "--blueprint", str(ROOT / "tests" / "fixtures" / "golden_blueprint.yaml"),
        "--endpoints", str(ROOT / "tests" / "fixtures" / "golden_endpoints.json"),
        "--service-name", "SalesOrder",
        "--out", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env())
    assert r.returncode == 0, r.stderr
    patch = (out / "patches" / "typedefinition.patch.xml").read_text(encoding="utf-8")
    assert 'id="SvcSalesOrder"' in patch
    assert 'url="/uiadapter/sales_order"' in patch


def test_cli_entity_pattern_overrides_default(tmp_path):
    """Entity-level pattern: in blueprint should override --default-pattern."""
    # Copy golden blueprint, inject pattern: C1 on customer entity.
    src_bp = yaml.safe_load((ROOT / "tests" / "fixtures" / "golden_blueprint.yaml").read_text(encoding="utf-8"))
    src_bp["entities"][0]["pattern"] = "C1"
    bp_path = tmp_path / "bp.yaml"
    bp_path.write_text(yaml.safe_dump(src_bp, allow_unicode=True), encoding="utf-8")

    out = tmp_path / "out"
    cmd = [
        sys.executable, str(ROOT / "scripts" / "form_gen.py"), "compile",
        "--blueprint", str(bp_path),
        "--endpoints", str(ROOT / "tests" / "fixtures" / "golden_endpoints.json"),
        "--default-pattern", "D2",  # default says D2 but entity overrides to C1
        "--out", str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, env=_env())
    assert r.returncode == 0, r.stderr
    xfdl = (out / "nxui" / "_form_" / "customer.xfdl").read_text(encoding="utf-8")
    assert "btn_save" not in xfdl  # C1 has no save
    assert "btn_select" in xfdl     # C1 has select
