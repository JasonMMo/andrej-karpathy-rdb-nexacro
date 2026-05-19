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


def test_compose_form_C1_readonly_grid(sample_entity, sample_endpoints):
    out = compose_form(sample_entity, sample_endpoints, pattern="C1")
    assert "btn_search" in out
    assert "btn_save" not in out      # C1 = 읽기 위주
    assert "btn_select" in out         # 단순 선택 버튼


def _mk_child_entity():
    return {
        "name": "order_item",
        "columns": [
            {"name": "id",             "type": "bigserial",   "pk": True,  "nullable": False},
            {"name": "sales_order_id", "type": "bigint",      "nullable": False},
            {"name": "product_id",     "type": "bigint",      "nullable": False},
            {"name": "quantity",       "type": "int",         "nullable": False},
            {"name": "unit_price",     "type": "numeric(12,2)", "nullable": False},
        ],
    }


def _mk_child_endpoints():
    return {
        "name": "order_item",
        "endpoints": [
            {"method": "select_datalist_map", "http_path": "/sales-orders/items/select"},
            {"method": "save_datalist_map",   "http_path": "/sales-orders/items/save"},
        ],
    }


def test_compose_form_MD_without_child_keeps_placeholder(sample_entity, sample_endpoints):
    """Growth-5: MD without child entity falls back to empty-hint placeholder (backward-compat)."""
    out = compose_form(sample_entity, sample_endpoints, pattern="MD")
    assert "grd_master" in out
    assert "hint_child" in out          # placeholder static present
    assert "grd_child" not in out       # no child grid wired


def test_compose_form_MD_with_child_auto_wires_grid(sample_entity, sample_endpoints):
    """Growth-5: MD with child entity emits child grid, dataset, buttons, and combined save payload."""
    out = compose_form(
        sample_entity, sample_endpoints, pattern="MD",
        child_entity=_mk_child_entity(),
        child_endpoints=_mk_child_endpoints(),
        child_fk_column="sales_order_id",
    )
    assert "grd_master" in out
    assert "grd_child" in out
    assert 'binddataset="dsOrderItem"' in out
    assert "btn_child_add" in out and "btn_child_del" in out
    assert "fn_add_child" in out and "fn_delete_child" in out
    assert "childList=dsOrderItem:U" in out
    assert "sales_order_id" in out      # FK referenced in fn_master_changed/fn_add_child
    assert "hint_child" not in out      # placeholder removed
