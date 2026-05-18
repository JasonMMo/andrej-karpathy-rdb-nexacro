import argparse
import pathlib
import sys

GLOBAL_PATTERN_ROOT = pathlib.Path.home() / ".karpathy-rdb" / "catalog" / "patterns"

from blueprint_loader  import load_blueprint, BlueprintError
from endpoints_loader  import load_endpoints, infer_endpoints, cross_check, EndpointsError
from revalidator       import check_search_candidates, check_xml_wellformed, RevalidationError
from form_composer     import compose_form
from menu_dataset_gen  import build_menu_rows, render_menu_dataset
from typedef_patcher   import build_service_entries, render_patch  # build_service_entries kept for back-compat


def _parse_args(argv):
    p = argparse.ArgumentParser(prog="karpathy-rdb-nexacro")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compile")
    c.add_argument("--blueprint", required=True)
    c.add_argument("--endpoints", default=None)
    c.add_argument("--infer-endpoints", action="store_true")
    c.add_argument("--out", required=True)
    c.add_argument("--frame", default="packageN", choices=["packageN", "minimal"])
    c.add_argument("--strict", action="store_true")
    c.add_argument("--force", action="store_true")
    c.add_argument("--default-pattern", default="D2",
                   help="Default form pattern when entity has no 'pattern:' field")
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv or sys.argv[1:])
    out = pathlib.Path(args.out)
    form_dir   = out / "nxui" / "_form_"
    ds_dir     = out / "nxui" / "_datasets_"
    patch_dir  = out / "patches"
    docs_dir   = out / "docs"
    for d in (form_dir, ds_dir, patch_dir, docs_dir):
        d.mkdir(parents=True, exist_ok=True)

    warnings = []

    try:
        bp = load_blueprint(args.blueprint)
    except BlueprintError as e:
        print(f"[{e}]", file=sys.stderr)
        return 1

    try:
        if args.endpoints:
            ep = load_endpoints(args.endpoints)
        elif args.infer_endpoints:
            ep = infer_endpoints(bp["entities"])
        else:
            raise EndpointsError("N002 --endpoints or --infer-endpoints required")
        cross_check(bp["entities"], ep)
    except EndpointsError as e:
        print(f"[{e}]", file=sys.stderr)
        return 1

    try:
        check_search_candidates(bp["entities"])
    except RevalidationError as e:
        print(f"[{e}]", file=sys.stderr)
        return 1

    # Derive service_pascal: blueprint may supply it explicitly (E2 will add CLI flag).
    # For E1, fall back to "Default" when not specified.
    service_pascal = bp.get("service_pascal", "Default")
    service_slug = service_pascal.lower()

    ep_by_name = {x["name"]: x for x in ep["entities"]}
    written = []
    for entity in bp["entities"]:
        target = form_dir / f"{entity['name']}.xfdl"
        if target.exists() and not args.force:
            print(f"[N007 overlay conflict: {target} exists — use --force]", file=sys.stderr)
            return 1
        if target.exists() and args.force:
            target.replace(target.with_suffix(target.suffix + ".bak"))
        pattern = entity.get("pattern") or args.default_pattern
        global_root = GLOBAL_PATTERN_ROOT if GLOBAL_PATTERN_ROOT.exists() else None
        xfdl = compose_form(
            entity,
            ep_by_name[entity["name"]],
            pattern=pattern,
            global_pattern_root=global_root,
            service_pascal=service_pascal,
        )
        target.write_text(xfdl, encoding="utf-8")
        written.append(target)

    menu_xml = render_menu_dataset(build_menu_rows(bp["entities"]))
    menu_path = ds_dir / "dsMenu.seed.xml"
    menu_path.write_text(menu_xml, encoding="utf-8")

    patch_xml = render_patch(
        service_pascal=service_pascal,
        service_slug=service_slug,
        context_path=ep.get("context_path", "/uiadapter"),
    )
    patch_path = patch_dir / "typedefinition.patch.xml"
    patch_path.write_text(patch_xml, encoding="utf-8")

    try:
        check_xml_wellformed(written + [menu_path, patch_path])
    except RevalidationError as e:
        print(f"[{e}]", file=sys.stderr)
        return 1

    report = ["# nexacro-report", "", f"- project: {bp.get('project','')}", "",
              "| entity | form | endpoints |", "| :-- | :-- | :-- |"]
    for entity in bp["entities"]:
        eps = ep_by_name[entity["name"]]["endpoints"]
        urls = ", ".join(e["http_path"] for e in eps)
        report.append(f"| {entity['name']} | _form_/{entity['name']}.xfdl | {urls} |")
    (docs_dir / "nexacro-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    if warnings:
        (docs_dir / "warnings.md").write_text("\n".join(warnings) + "\n", encoding="utf-8")
        if args.strict:
            print("[--strict] warnings present, failing", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
