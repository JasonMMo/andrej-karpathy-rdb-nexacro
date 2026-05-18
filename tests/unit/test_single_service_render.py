"""Phase E1: assert render_patch emits exactly one Service per domain."""
import xml.etree.ElementTree as ET
import pytest
from typedef_patcher import render_patch


def test_single_service_id():
    xml = render_patch(service_pascal="Order", service_slug="order")
    root = ET.fromstring(xml)
    services = root.findall("Service")
    assert len(services) == 1
    assert services[0].get("id") == "SvcOrder"


def test_single_service_url_default_context():
    xml = render_patch(service_pascal="Order", service_slug="order")
    root = ET.fromstring(xml)
    assert root.find("Service").get("url") == "/uiadapter/order"


def test_single_service_url_custom_context():
    xml = render_patch(service_pascal="Payment", service_slug="payment",
                       context_path="/api/nexacro")
    root = ET.fromstring(xml)
    svc = root.find("Service")
    assert svc.get("id") == "SvcPayment"
    assert svc.get("url") == "/api/nexacro/payment"


def test_single_service_type_and_version():
    xml = render_patch(service_pascal="SalesOrder", service_slug="sales_order")
    root = ET.fromstring(xml)
    svc = root.find("Service")
    assert svc.get("type") == "default"
    assert svc.get("version") == "1.0"


def test_compound_service_name_slugified():
    """Compound PascalCase name maps to snake_case slug in both id and url."""
    xml = render_patch(service_pascal="SalesOrder", service_slug="sales_order")
    root = ET.fromstring(xml)
    svc = root.find("Service")
    assert svc.get("id") == "SvcSalesOrder"
    assert svc.get("url") == "/uiadapter/sales_order"
