import xml.etree.ElementTree as ET
from menu_dataset_gen import build_menu_rows, render_menu_dataset


def test_build_rows_one_entity():
    rows = build_menu_rows([{"name": "customer"}])
    assert rows == [
        {"menu_id": "MENU_CUSTOMER", "menu_pid": "ROOT",
         "menu_nm": "Customer", "form_url": "_form_::customer.xfdl", "level": 1},
    ]


def test_render_emits_one_row_per_entity():
    rows = build_menu_rows([{"name": "customer"}, {"name": "customer_address"}])
    xml = render_menu_dataset(rows)
    root = ET.fromstring(xml)
    assert root.tag == "Dataset"
    assert len(root.find("Rows").findall("Row")) == 2
