import pathlib
from jinja2 import Environment, FileSystemLoader

TEMPLATES = pathlib.Path(__file__).resolve().parents[1] / "templates"
ENV = Environment(loader=FileSystemLoader(TEMPLATES),
                  trim_blocks=True, lstrip_blocks=True,
                  keep_trailing_newline=False)


def _pascal(name):
    return "".join(p.capitalize() for p in name.split("_"))


def build_menu_rows(entities, parent="ROOT", level=1):
    rows = []
    for e in entities:
        name = e["name"]
        rows.append({
            "menu_id":  f"MENU_{name.upper()}",
            "menu_pid": parent,
            "menu_nm":  _pascal(name),
            "form_url": f"_form_::{name}.xfdl",
            "level":    level,
        })
    return rows


def render_menu_dataset(rows):
    tpl = ENV.get_template("menu_dataset.xml.j2")
    return tpl.render(rows=rows)
