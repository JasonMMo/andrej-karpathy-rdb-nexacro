import pathlib
import yaml
from dataclasses import dataclass, field


class PatternNotFoundError(Exception):
    pass


class ShellNotFoundError(Exception):
    pass


@dataclass
class ResolvedPattern:
    name: str
    template_path: pathlib.Path
    manifest: dict
    source: str  # "bundled" or "global"


@dataclass
class ResolvedShell:
    variant: str
    manifest: dict
    frames: dict = field(default_factory=dict)  # frame_name -> pathlib.Path
    typedef_template: pathlib.Path = None
    xadl_template: pathlib.Path = None
    # Variant-independent project build artifacts (pom.xml, Application.java,
    # application.yml). Each tuple is (template_path, target_relative_path).
    # `target_relative_path` may contain `{pkg_path}` for the overlay to
    # substitute from target_pkg_prefix.
    build_files: list = field(default_factory=list)
    # Growth-21a-2: Spring Security + Nexacro auth bundle, filtered by
    # auth_mode (none|session|jwt|oauth2). Each tuple is
    # (template_path, target_relative_path, modes_list). The overlay filters
    # by the active auth_mode at render time. Empty list when auth_mode="none"
    # or when the manifest has no auth_files block.
    auth_files: list = field(default_factory=list)
    source: str = "bundled"  # "bundled" or "global"


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


_SHELL_BASE_VARIANT = "MDI"  # shared-frame fallback base


def _rewrite_auth_source(source: str, auth_lane: str) -> str:
    """Growth-23: Rewrite auth/config source paths for non-jakarta lanes.

    auth_lane="jakarta" → no change (legacy auth/ and config/ stay default).
    auth_lane="javax"   → auth/X.j2 → auth-javax/X.j2, config/X.j2 → config-javax/X.j2.

    The leading directory must be exactly "auth/" or "config/" — anything
    else is returned unchanged so non-Java assets (xfdl, xml, yml) are
    unaffected.
    """
    if auth_lane == "jakarta":
        return source
    for prefix in ("auth/", "config/"):
        if source.startswith(prefix):
            return f"{prefix.rstrip('/')}-{auth_lane}/" + source[len(prefix):]
    return source


def resolve_shell(
    variant: str,
    bundled_root: pathlib.Path | str,
    global_root: pathlib.Path | str | None = None,
    frame_overrides: dict | None = None,
    auth_lane: str = "jakarta",
) -> ResolvedShell:
    """Resolve a SHELL pattern variant into concrete frame template paths.

    Lookup order per file: frame_overrides > variants/<variant>/ > variants/MDI/
    (shared-frame fallback). Source priority: bundled then global root.

    Growth-23: auth_lane selects the auth bundle's servlet/Spring-Security
    flavor. "jakarta" (default) reads from variants/<variant>/auth/ and
    config/ as before. "javax" reads from auth-javax/ and config-javax/
    (Spring Security 5 + javax.servlet, no fallback to jakarta — missing
    files raise ShellNotFoundError).
    """
    frame_overrides = frame_overrides or {}

    for label, root in (("bundled", bundled_root), ("global", global_root)):
        if root is None:
            continue
        shell_dir = pathlib.Path(root) / "SHELL"
        manifest_path = shell_dir / "manifest.yaml"
        if not manifest_path.exists():
            continue
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        variants = {v["id"]: v for v in manifest.get("variants", [])}
        if variant not in variants:
            continue

        variant_dir = shell_dir / "variants" / variant
        base_dir = shell_dir / "variants" / _SHELL_BASE_VARIANT
        frame_names = variants[variant].get("frames", [])

        def _resolve_frame(name: str) -> pathlib.Path:
            if name in frame_overrides:
                return pathlib.Path(frame_overrides[name])
            specific = variant_dir / f"{name}.xfdl.j2"
            if specific.exists():
                return specific
            shared = base_dir / f"{name}.xfdl.j2"
            if shared.exists():
                return shared
            raise ShellNotFoundError(
                f"Frame '{name}' for variant '{variant}' not found in "
                f"{variant_dir} or {base_dir}"
            )

        frames = {name: _resolve_frame(name) for name in frame_names}

        def _resolve_aux(filename: str) -> pathlib.Path:
            specific = variant_dir / filename
            if specific.exists():
                return specific
            shared = base_dir / filename
            if shared.exists():
                return shared
            raise ShellNotFoundError(
                f"Auxiliary template '{filename}' missing for variant "
                f"'{variant}' (looked in {variant_dir} and {base_dir})"
            )

        build_files: list = []
        for entry in manifest.get("build", []) or []:
            src = entry.get("source")
            tgt = entry.get("target")
            if not src or not tgt:
                continue
            build_files.append((_resolve_aux(src), tgt))

        # Growth-21a-2: auth_files are resolved eagerly (same variant→MDI
        # fallback) but mode-filtered later by the overlay using auth_mode.
        # Growth-23: source path is rewritten by auth_lane (jakarta default,
        # javax → auth-javax/, config-javax/). No silent fallback to jakarta.
        auth_files: list = []
        for entry in manifest.get("auth_files", []) or []:
            src = entry.get("source")
            tgt = entry.get("target")
            modes = entry.get("modes") or []
            if not src or not tgt:
                continue
            src_resolved = _rewrite_auth_source(src, auth_lane)
            auth_files.append((_resolve_aux(src_resolved), tgt, list(modes)))

        return ResolvedShell(
            variant=variant,
            manifest=manifest,
            frames=frames,
            typedef_template=_resolve_aux("typedefinition.xml.j2"),
            xadl_template=_resolve_aux("packageN.xadl.j2"),
            build_files=build_files,
            auth_files=auth_files,
            source=label,
        )

    searched = [
        str(pathlib.Path(r) / "SHELL")
        for label, r in (("bundled", bundled_root), ("global", global_root))
        if r is not None
    ]
    raise ShellNotFoundError(
        f"Shell variant '{variant}' not found. Searched: {searched}"
    )
