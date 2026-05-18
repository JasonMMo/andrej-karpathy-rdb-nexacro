import json
import pathlib
import pytest
import yaml

from form_composer import compose_form
from pattern_loader import PatternNotFoundError

FIXTURES = pathlib.Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture
def sample_entity():
    bp = yaml.safe_load((FIXTURES / "golden_blueprint.yaml").read_text(encoding="utf-8"))
    return bp["entities"][0]


@pytest.fixture
def sample_endpoints():
    ep = json.loads((FIXTURES / "golden_endpoints.json").read_text(encoding="utf-8"))
    # endpoints.json has top-level entities[]; pull the first entity's endpoints block
    if isinstance(ep, dict) and "entities" in ep:
        return ep["entities"][0]
    return ep


def test_compose_form_default_is_D2(sample_entity, sample_endpoints):
    out = compose_form(sample_entity, sample_endpoints)
    assert "<Grid id=\"grd_main\"" in out
    assert "fn_search" in out
    assert "btn_save" in out


def test_compose_form_explicit_D2(sample_entity, sample_endpoints):
    out = compose_form(sample_entity, sample_endpoints, pattern="D2")
    assert "<Grid id=\"grd_main\"" in out


def test_compose_form_unknown_pattern_raises(sample_entity, sample_endpoints):
    with pytest.raises(PatternNotFoundError):
        compose_form(sample_entity, sample_endpoints, pattern="ZZZ")


def test_compose_form_F1_no_grid(sample_entity, sample_endpoints):
    out = compose_form(sample_entity, sample_endpoints, pattern="F1")
    assert "<Grid" not in out
    assert "btn_save" in out
    assert "fn_save" in out
