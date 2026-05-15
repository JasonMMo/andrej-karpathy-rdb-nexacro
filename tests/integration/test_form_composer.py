import pathlib
import xml.etree.ElementTree as ET
from form_composer import compose_form


def test_compose_form_for_customer():
    entity = {
        "name": "customer",
        "table": "TB_CUSTOMER",
        "columns": [
            {"name": "customer_id", "type": "varchar(36)", "pk": True,  "nullable": False},
            {"name": "name",        "type": "varchar(100)",              "nullable": False},
            {"name": "email",       "type": "varchar(200)",              "nullable": True},
            {"name": "active_yn",   "type": "char(1)",                   "nullable": False},
            {"name": "created_at",  "type": "timestamp",                 "nullable": False},
        ],
    }
    endpoints = {
        "endpoint_base": "/customer",
        "endpoints": [
            {"method": "select_datalist_map", "http_path": "/customer/select_datalist_map.do"},
            {"method": "save_datalist_map",   "http_path": "/customer/save_datalist_map.do"},
        ],
    }
    xfdl = compose_form(entity, endpoints)
    # well-formed XML
    root = ET.fromstring(xfdl)
    assert root.tag == "FDL"
    # main dataset id appears
    assert 'id="dsCustomer"' in xfdl
    # dsSearch dataset appears
    assert 'id="dsSearch"' in xfdl
    # *_yn rendered as combo
    assert 'edittype="combo"' in xfdl
    # PK is readonly
    assert 'edittype="none"' in xfdl
    # service path embedded
    assert "/customer/select_datalist_map.do" in xfdl
    assert "/customer/save_datalist_map.do" in xfdl
