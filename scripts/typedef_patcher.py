import pathlib
from jinja2 import Environment, FileSystemLoader

TEMPLATES = pathlib.Path(__file__).resolve().parents[1] / "templates"
ENV = Environment(loader=FileSystemLoader(TEMPLATES),
                  trim_blocks=True, lstrip_blocks=True,
                  keep_trailing_newline=False)


def _pascal(name):
    return "".join(p.capitalize() for p in name.split("_"))


def build_service_entries(endpoint_entities):
    """Kept for back-compat; no longer used by render_patch."""
    return [
        {"pascal": _pascal(e["name"]), "endpoint_base": e["endpoint_base"]}
        for e in endpoint_entities
    ]


def render_patch(service_pascal: str, service_slug: str, context_path: str = "/uiadapter") -> str:
    """Render a single-Service typedefinition patch for the given domain.

    Args:
        service_pascal: PascalCase service name, e.g. ``"Order"`` → id ``"SvcOrder"``.
        service_slug:   URL path segment, e.g. ``"order"`` → ``/uiadapter/order``.
        context_path:   Context root prefix (default ``"/uiadapter"``).
    """
    tpl = ENV.get_template("typedefinition_patch.xml.j2")
    return tpl.render(
        service_pascal=service_pascal,
        service_slug=service_slug,
        context_path=context_path,
    )
