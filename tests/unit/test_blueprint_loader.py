import pathlib
import pytest
from blueprint_loader import load_blueprint, BlueprintError

FX = pathlib.Path(__file__).resolve().parents[1] / "fixtures" / "golden_blueprint.yaml"


def test_load_golden_blueprint():
    bp = load_blueprint(FX)
    assert bp["version"] == 1
    assert bp["validation"]["passed"] is True
    assert bp["entities"][0]["name"] == "customer"


def test_n001_rejects_version_mismatch(tmp_path):
    p = tmp_path / "bp.yaml"
    p.write_text("version: 2\nentities: []\nvalidation: {passed: true}\n")
    with pytest.raises(BlueprintError, match="N001"):
        load_blueprint(p)


def test_n001_rejects_validation_false(tmp_path):
    p = tmp_path / "bp.yaml"
    p.write_text("version: 1\nentities: []\nvalidation: {passed: false}\n")
    with pytest.raises(BlueprintError, match="N001"):
        load_blueprint(p)


def test_n004_rejects_entity_without_pk(tmp_path):
    p = tmp_path / "bp.yaml"
    p.write_text(
        "version: 1\nvalidation: {passed: true}\n"
        "entities:\n"
        "  - name: x\n    table: T\n    columns:\n"
        "      - {name: c, type: varchar(10), nullable: true}\n"
    )
    with pytest.raises(BlueprintError, match="N004"):
        load_blueprint(p)
