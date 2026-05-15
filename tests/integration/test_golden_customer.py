import json
import pathlib
import yaml
from form_composer import compose_form

ROOT = pathlib.Path(__file__).resolve().parents[2]


def test_golden_customer_xfdl_byte_exact():
    bp = yaml.safe_load((ROOT / "tests" / "fixtures" / "golden_blueprint.yaml").read_text(encoding="utf-8"))
    ep = json.loads((ROOT / "tests" / "fixtures" / "golden_endpoints.json").read_text(encoding="utf-8"))
    got = compose_form(bp["entities"][0], ep["entities"][0])
    expected = (ROOT / "tests" / "fixtures" / "expected" / "customer.xfdl").read_text(encoding="utf-8")
    assert got == expected
