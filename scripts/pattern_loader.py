import pathlib
import yaml
from dataclasses import dataclass


class PatternNotFoundError(Exception):
    pass


@dataclass
class ResolvedPattern:
    name: str
    template_path: pathlib.Path
    manifest: dict
    source: str  # "bundled" or "global"


def resolve_pattern(
    name: str,
    bundled_root: pathlib.Path | str,
    global_root: pathlib.Path | str | None = None,
) -> ResolvedPattern:
    for label, root in (("bundled", bundled_root), ("global", global_root)):
        if root is None:
            continue
        pat_dir = pathlib.Path(root) / name
        manifest = pat_dir / "manifest.yaml"
        tpl = pat_dir / "form.xfdl.j2"
        if manifest.exists() and tpl.exists():
            return ResolvedPattern(
                name=name,
                template_path=tpl,
                manifest=yaml.safe_load(manifest.read_text(encoding="utf-8")) or {},
                source=label,
            )
    searched = [
        str(pathlib.Path(r) / name)
        for label, r in (("bundled", bundled_root), ("global", global_root))
        if r is not None
    ]
    raise PatternNotFoundError(
        f"Pattern '{name}' not found. Searched: {searched}"
    )
