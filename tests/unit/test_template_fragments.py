import pathlib
from jinja2 import Environment, FileSystemLoader

ROOT = pathlib.Path(__file__).resolve().parents[2]
ENV = Environment(
    loader=FileSystemLoader(ROOT / "templates"),
    trim_blocks=True, lstrip_blocks=True,
    keep_trailing_newline=False,
)


def test_dataset_render():
    tpl = ENV.get_template("dataset.xml.j2")
    out = tpl.render(ds_id="dsCustomer", columns=[
        {"name": "id", "dataset_type": "BIGDECIMAL", "size": None},
        {"name": "name", "dataset_type": "STRING", "size": 100},
    ], rows=None)
    assert '<Dataset id="dsCustomer">' in out
    assert '<Column id="id" type="BIGDECIMAL"/>' in out
    assert '<Column id="name" type="STRING" size="100"/>' in out


def test_grid_format_render():
    tpl = ENV.get_template("grid_format.xml.j2")
    out = tpl.render(columns=[
        {"name": "id", "label": "ID", "size": 80,
         "grid_edittype": "none", "grid_displaytype": "number"},
        {"name": "name", "label": "이름", "size": 200,
         "grid_edittype": "text", "grid_displaytype": "text"},
    ])
    assert 'text="bind:id"' in out
    assert 'edittype="none"' in out
    assert 'edittype="text"' in out
    assert 'text="이름"' in out


def test_search_field_calendar():
    tpl = ENV.get_template("search_field.xml.j2")
    out = tpl.render(comp="Calendar", col_name="created_at", label="등록일",
                     x=10, y=10)
    assert "Calendar" in out and "cal_created_at" in out
