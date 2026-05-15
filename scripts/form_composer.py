import pathlib
from jinja2 import Environment, FileSystemLoader
from type_mapper import map_column

TEMPLATES = pathlib.Path(__file__).resolve().parents[1] / "templates"
ENV = Environment(
    loader=FileSystemLoader(TEMPLATES),
    trim_blocks=True, lstrip_blocks=True,
    keep_trailing_newline=False,
)


def _pascal(name):
    return "".join(p.capitalize() for p in name.split("_"))


def _search_columns(entity):
    return [c for c in entity["columns"]
            if c.get("pk") or c.get("nullable") is False]


def _label(col_name):
    return col_name.replace("_", " ").title()


def compose_form(entity, endpoints):
    pascal = _pascal(entity["name"])
    cols = []
    for c in entity["columns"]:
        m = map_column(c)
        pk = bool(c.get("pk"))
        cols.append({
            "name": c["name"],
            "label": _label(c["name"]),
            "dataset_type": m.dataset_type,
            "size": m.size,
            "grid_edittype": "none" if pk else m.grid_edittype,
            "grid_displaytype": m.grid_displaytype,
            "search_component": m.search_component,
        })

    search_cols = []
    for c in _search_columns(entity):
        m = map_column(c)
        if m.search_component is None:
            continue
        search_cols.append({
            "name": c["name"],
            "label": _label(c["name"]),
            "dataset_type": m.dataset_type,
            "size": m.size,
            "search_component": m.search_component,
        })

    # Datasets fragment (dsSearch + ds{Pascal})
    ds_tpl = ENV.get_template("dataset.xml.j2")
    datasets_xml = "\n".join([
        ds_tpl.render(ds_id="dsSearch", columns=search_cols, rows=None),
        ds_tpl.render(ds_id=f"ds{pascal}", columns=cols, rows=None),
    ])

    # Search fragment
    sf_tpl = ENV.get_template("search_field.xml.j2")
    pieces = []
    x = 140
    for sc in search_cols:
        pieces.append(sf_tpl.render(
            comp=sc["search_component"],
            col_name=sc["name"],
            label=sc["label"],
            x=x, y=20,
        ))
        x += 260
    search_fields = "\n".join(pieces) if pieces else ""

    # Grid format
    gf_tpl = ENV.get_template("grid_format.xml.j2")
    grid_format = gf_tpl.render(columns=cols)

    # Resolve paths
    sel_path = next(e["http_path"] for e in endpoints["endpoints"]
                    if e["method"] == "select_datalist_map")
    sav_path = next(e["http_path"] for e in endpoints["endpoints"]
                    if e["method"] == "save_datalist_map")

    # Main form
    form_tpl = ENV.get_template("form.xfdl.j2")
    return form_tpl.render(
        form_id=entity["name"],
        title=f"{pascal} 관리",
        entity_pascal=pascal,
        search_fields=search_fields,
        grid_format=grid_format,
        datasets=datasets_xml,
        select_path=sel_path,
        save_path=sav_path,
    )
