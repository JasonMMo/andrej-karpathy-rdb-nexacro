import pathlib
import xml.etree.ElementTree as ET


class RevalidationError(Exception):
    pass


def check_search_candidates(entities):
    for e in entities:
        cands = [c for c in (e.get("columns") or [])
                 if c.get("pk") or c.get("nullable") is False]
        if not cands:
            raise RevalidationError(
                f"N005 entity {e.get('name')!r} has no searchable columns "
                "(no PK and no NOT NULL columns)"
            )


def check_xml_wellformed(paths):
    bad = []
    for p in paths:
        p = pathlib.Path(p)
        try:
            ET.parse(p)
        except (ET.ParseError, OSError) as e:
            bad.append(f"{p}: {e}")
    if bad:
        raise RevalidationError(
            "N006 malformed XML:\n  " + "\n  ".join(bad)
        )
