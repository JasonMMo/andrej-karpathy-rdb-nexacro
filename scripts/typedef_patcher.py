import pathlib
from jinja2 import Environment, FileSystemLoader

TEMPLATES = pathlib.Path(__file__).resolve().parents[1] / "templates"
ENV = Environment(loader=FileSystemLoader(TEMPLATES),
                  trim_blocks=True, lstrip_blocks=True,
                  keep_trailing_newline=False)


def _pascal(name):
    return "".join(p.capitalize() for p in name.split("_"))


def build_service_entries(endpoint_entities):
    return [
        {"pascal": _pascal(e["name"]), "endpoint_base": e["endpoint_base"]}
        for e in endpoint_entities
    ]


def render_patch(service_entries, context_path="/uiadapter"):
    tpl = ENV.get_template("typedefinition_patch.xml.j2")
    return tpl.render(entities=service_entries, context_path=context_path)
