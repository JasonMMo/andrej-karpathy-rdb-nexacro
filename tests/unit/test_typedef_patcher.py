import xml.etree.ElementTree as ET
from typedef_patcher import build_service_entries, render_patch


def test_build_entries():
    out = build_service_entries([
        {"name": "customer", "endpoint_base": "/customer"},
    ])
    assert out == [{"pascal": "Customer", "endpoint_base": "/customer"}]


def test_render_patch_well_formed():
    xml = render_patch(
        service_pascal="Customer",
        service_slug="customer",
        context_path="/uiadapter",
    )
    root = ET.fromstring(xml)
    svc = root.find("Service")
    assert svc.get("id") == "SvcCustomer"
    assert svc.get("url") == "/uiadapter/customer"


def test_render_patch_single_service():
    """Single domain → exactly one Service element."""
    xml = render_patch(service_pascal="Order", service_slug="order")
    root = ET.fromstring(xml)
    services = root.findall("Service")
    assert len(services) == 1
    assert services[0].get("id") == "SvcOrder"
    assert services[0].get("url") == "/uiadapter/order"
    assert services[0].get("type") == "default"
    assert services[0].get("version") == "1.0"
