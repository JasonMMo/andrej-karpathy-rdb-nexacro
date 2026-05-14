import pathlib
import pytest
from revalidator import (
    check_search_candidates, check_xml_wellformed, RevalidationError
)


def test_n005_search_candidates_ok():
    e = {"name": "customer", "columns": [
        {"name": "id", "type": "varchar(36)", "pk": True, "nullable": False},
        {"name": "name", "type": "varchar(100)", "nullable": False},
    ]}
    check_search_candidates([e])  # OK


def test_n005_rejects_no_searchable_columns():
    e = {"name": "x", "columns": [
        {"name": "id", "type": "varchar(36)", "pk": False, "nullable": True},
        {"name": "memo", "type": "text", "nullable": True},
    ]}
    with pytest.raises(RevalidationError, match="N005"):
        check_search_candidates([e])


def test_n006_xml_wellformed_pass(tmp_path):
    f = tmp_path / "a.xml"
    f.write_text("<root><a/></root>")
    check_xml_wellformed([f])  # OK


def test_n006_xml_wellformed_fail(tmp_path):
    f = tmp_path / "b.xml"
    f.write_text("<root><a></root>")
    with pytest.raises(RevalidationError, match="N006"):
        check_xml_wellformed([f])


def test_n005_passes_on_not_null_only():
    e = {"name": "t", "columns": [{"name": "code", "type": "varchar(10)", "nullable": False}]}
    check_search_candidates([e])


def test_n005_passes_on_pk_only():
    e = {"name": "t", "columns": [{"name": "id", "type": "varchar(36)", "pk": True, "nullable": True}]}
    check_search_candidates([e])


def test_n006_missing_file_raises_revalidation_error(tmp_path):
    missing = tmp_path / "does_not_exist.xfdl"
    with pytest.raises(RevalidationError, match="N006"):
        check_xml_wellformed([missing])
