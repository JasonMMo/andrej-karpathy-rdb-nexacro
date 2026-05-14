# Overlay Policy

Stage 4 emits to a separate output directory; `overlay.sh` (also emitted) copies onto the `nexacro-fullstack-starter` scaffold.

## Conflict handling

| Layer | Policy |
| :-- | :-- |
| **CLI** | All validator failures → stderr `[Nxxx] ...` + exit 1. Output goes to tmp dir → atomic move (rollback on failure). |
| **Template** | Jinja `UndefinedError` is re-thrown including entity + column + missing key. |
| **Type mapper (unmapped type)** | Fallback (`STRING/Edit/100`) + one line in `warnings.md`. `--strict` flag turns this into exit 1. |
| **Overlay file collision** | If `<entity>.xfdl` already exists at the target, stop with `[N007]`. `--force` flag backs up the existing file as `<entity>.xfdl.bak` and overwrites. |
| **endpoints.json missing** | `[N002] not found` message; user can opt into synthesis via `--infer-endpoints`. |
