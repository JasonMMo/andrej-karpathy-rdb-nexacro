import json
import pathlib
import pytest
from endpoints_loader import load_endpoints, infer_endpoints, EndpointsError

FX = pathlib.Path(__file__).resolve().parents[1] / "fixtures" / "golden_endpoints.json"


def test_load_golden():
    data = load_endpoints(FX)
    assert data["version"] == 1
    assert data["entities"][0]["name"] == "customer"


def test_n002_rejects_version(tmp_path):
    p = tmp_path / "ep.json"
    p.write_text('{"version": 2, "entities": []}')
    with pytest.raises(EndpointsError, match="N002"):
        load_endpoints(p)


def test_n002_rejects_missing_method(tmp_path):
    p = tmp_path / "ep.json"
    p.write_text(json.dumps({
        "version": 1,
        "entities": [{"name": "x", "endpoint_base": "/x",
                      "endpoints": [{"method": "select_datalist_map",
                                     "http_path": "/x/select_datalist_map.do",
                                     "input": {}, "output": {}}]}],
    }))
    with pytest.raises(EndpointsError, match="N002"):
        load_endpoints(p)


def test_infer_from_blueprint_entities():
    inferred = infer_endpoints(
        [{"name": "customer"}, {"name": "customer_address"}],
        context_path="/uiadapter",
    )
    assert inferred["version"] == 1
    assert [e["name"] for e in inferred["entities"]] == ["customer", "customer_address"]
    assert inferred["entities"][0]["endpoints"][0]["http_path"] == "/customer/select_datalist_map.do"


def test_n003_cross_check_entities_match():
    from endpoints_loader import cross_check
    ep = {"entities": [{"name": "customer"}]}
    cross_check([{"name": "customer"}], ep)  # OK
    with pytest.raises(EndpointsError, match="N003"):
        cross_check([{"name": "customer"}, {"name": "order"}], ep)
