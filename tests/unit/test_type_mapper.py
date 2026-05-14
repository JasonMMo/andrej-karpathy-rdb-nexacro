import pytest
from type_mapper import map_column, MapResult


def test_bigserial_pk_readonly():
    r = map_column({"name": "id", "type": "bigserial", "pk": True, "nullable": False})
    assert r.dataset_type == "BIGDECIMAL"
    assert r.grid_edittype == "none"
    assert r.grid_displaytype == "number"
    assert r.search_component == "Edit"


def test_varchar_default():
    r = map_column({"name": "name", "type": "varchar(100)", "nullable": False})
    assert r.dataset_type == "STRING"
    assert r.size == 100
    assert r.grid_edittype == "text"
    assert r.search_component == "Edit"


def test_char1_yn_convention():
    r = map_column({"name": "active_yn", "type": "char(1)", "nullable": False})
    assert r.dataset_type == "STRING"
    assert r.size == 1
    assert r.grid_edittype == "combo"
    assert r.grid_displaytype == "combotext"
    assert r.search_component == "Combo"
    assert r.combo_options == [("Y", "Y"), ("N", "N")]


def test_char1_non_yn_falls_to_text():
    r = map_column({"name": "grade", "type": "char(1)", "nullable": True})
    assert r.grid_edittype == "text"
    assert r.search_component == "Edit"


def test_numeric():
    r = map_column({"name": "amount", "type": "numeric(15,2)", "nullable": False})
    assert r.dataset_type == "BIGDECIMAL"
    assert r.grid_edittype == "masknumber"
    assert r.grid_displaytype == "number"


def test_boolean():
    r = map_column({"name": "is_locked", "type": "boolean", "nullable": False})
    assert r.grid_edittype == "checkbox"
    assert r.search_component == "Combo"


def test_date():
    r = map_column({"name": "birth_dt", "type": "date", "nullable": True})
    assert r.size == 8
    assert r.grid_edittype == "date"
    assert r.search_component == "Calendar"


def test_timestamp():
    r = map_column({"name": "created_at", "type": "timestamp", "nullable": False})
    assert r.size == 14
    assert r.grid_edittype == "date"


def test_json_search_excluded():
    r = map_column({"name": "payload", "type": "jsonb", "nullable": True})
    assert r.search_component is None  # excluded
    assert r.grid_edittype == "text"


def test_unknown_falls_back():
    r = map_column({"name": "xy", "type": "geometry", "nullable": True})
    assert r.dataset_type == "STRING"
    assert r.size == 100
    assert r.grid_edittype == "text"
    assert r.fallback is True


def test_char1_yn_pk_is_readonly():
    r = map_column({"name": "active_yn", "type": "char(1)", "pk": True, "nullable": False})
    assert r.grid_edittype == "none"


def test_missing_name_raises_typemappererror():
    from type_mapper import TypeMapperError
    with pytest.raises(TypeMapperError, match="missing 'name'"):
        map_column({"type": "varchar(10)"})
