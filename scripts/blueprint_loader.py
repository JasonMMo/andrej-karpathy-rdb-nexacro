import pathlib
import yaml


class BlueprintError(Exception):
    pass


def load_blueprint(path):
    p = pathlib.Path(path)
    if not p.exists():
        raise BlueprintError(f"N001 blueprint not found: {p}")
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if data.get("version") != 1:
        raise BlueprintError(f"N001 unsupported version: {data.get('version')!r}")
    if not (data.get("validation") or {}).get("passed"):
        raise BlueprintError("N001 blueprint validation.passed != true")
    for e in data.get("entities") or []:
        pk_cols = [c for c in (e.get("columns") or []) if c.get("pk")]
        if not pk_cols:
            raise BlueprintError(f"N004 entity {e.get('name')!r} has no pk column")
    return data
