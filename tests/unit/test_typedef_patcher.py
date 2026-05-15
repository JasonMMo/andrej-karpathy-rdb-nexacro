import xml.etree.ElementTree as ET
from typedef_patcher import build_service_entries, render_patch


def test_build_entries():
    out = build_service_entries([
        {"name": "customer", "endpoint_base": "/customer"},
    ])
    assert out == [{"pascal": "Customer", "endpoint_base": "/customer"}]


def test_render_patch_well_formed():
    xml = render_patch(
        build_service_entries([{"name": "customer", "endpoint_base": "/customer"}]),
        context_path="/uiadapter",
    )
    root = ET.fromstring(xml)
    svc = root.find("Service")
    assert svc.get("id") == "SvcCustomer"
    assert svc.get("url") == "/uiadapter/customer"
