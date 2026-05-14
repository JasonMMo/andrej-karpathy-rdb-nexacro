import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MapResult:
    dataset_type: str
    size: Optional[int] = None
    search_component: Optional[str] = None  # None = exclude from search
    grid_edittype: str = "text"
    grid_displaytype: str = "text"
    combo_options: list = field(default_factory=list)
    fallback: bool = False


_VARCHAR_RE  = re.compile(r"^varchar\((\d+)\)$", re.I)
_CHAR_RE     = re.compile(r"^char\((\d+)\)$", re.I)
_NUMERIC_RE  = re.compile(r"^(numeric|decimal)\((\d+)(?:,\d+)?\)$", re.I)


def map_column(col):
    name = col["name"]
    t = (col.get("type") or "").strip().lower()
    pk = bool(col.get("pk"))

    if t in {"bigserial", "serial", "bigint", "integer", "int", "int4", "int8"}:
        return MapResult(
            dataset_type="BIGDECIMAL",
            search_component="Edit",
            grid_edittype="none" if pk else "masknumber",
            grid_displaytype="number",
        )

    m = _VARCHAR_RE.match(t)
    if m:
        return MapResult(
            dataset_type="STRING", size=int(m.group(1)),
            search_component="Edit", grid_edittype="text", grid_displaytype="text",
        )
    if t == "text":
        return MapResult(
            dataset_type="STRING", size=4000,
            search_component="Edit", grid_edittype="text", grid_displaytype="text",
        )

    m = _CHAR_RE.match(t)
    if m:
        size = int(m.group(1))
        if size == 1 and name.lower().endswith("_yn"):
            return MapResult(
                dataset_type="STRING", size=1,
                search_component="Combo",
                grid_edittype="combo", grid_displaytype="combotext",
                combo_options=[("Y", "Y"), ("N", "N")],
            )
        return MapResult(
            dataset_type="STRING", size=size,
            search_component="Edit", grid_edittype="text", grid_displaytype="text",
        )

    m = _NUMERIC_RE.match(t)
    if m:
        precision = int(m.group(2))
        return MapResult(
            dataset_type="BIGDECIMAL", size=precision,
            search_component="Edit",
            grid_edittype="masknumber", grid_displaytype="number",
        )

    if t == "boolean":
        return MapResult(
            dataset_type="STRING", size=1,
            search_component="Combo",
            grid_edittype="checkbox", grid_displaytype="checkbox",
        )

    if t == "date":
        return MapResult(
            dataset_type="STRING", size=8,
            search_component="Calendar",
            grid_edittype="date", grid_displaytype="date",
        )

    if t in {"timestamp", "timestamptz"}:
        return MapResult(
            dataset_type="STRING", size=14,
            search_component="Calendar",
            grid_edittype="date", grid_displaytype="date",
        )

    if t == "time":
        return MapResult(
            dataset_type="STRING", size=6,
            search_component="Edit", grid_edittype="mask", grid_displaytype="text",
        )

    if t in {"json", "jsonb"}:
        return MapResult(
            dataset_type="STRING", size=4000,
            search_component=None,  # excluded
            grid_edittype="text", grid_displaytype="text",
        )

    if t == "uuid":
        return MapResult(
            dataset_type="STRING", size=36,
            search_component="Edit",
            grid_edittype="none" if pk else "text", grid_displaytype="text",
        )

    return MapResult(
        dataset_type="STRING", size=100,
        search_component="Edit", grid_edittype="text", grid_displaytype="text",
        fallback=True,
    )
