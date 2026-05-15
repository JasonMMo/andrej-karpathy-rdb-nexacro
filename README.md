# andrej-karpathy-rdb-nexacro

Stage 4 of the `business-fullstack-creater` pipeline. Generates nexacro xfdl forms
from `_blueprint.yaml` (Stage 1) + `endpoints.json` (Stage 3 v0.1.4+).

## Quick start

```bash
python scripts/form_gen.py compile \
  --blueprint <path>/_blueprint.yaml \
  --endpoints <path>/endpoints.json \
  --out       out/
```

Outputs to:
```
out/nxui/_form_/<entity>.xfdl
out/nxui/_datasets_/dsMenu.seed.xml
out/patches/typedefinition.patch.xml
out/docs/nexacro-report.md
```

Overlay onto a `nexacro-fullstack-starter` scaffold:
```bash
bash scripts/overlay.sh out/ <project-root>/
```

## Flags
- `--infer-endpoints` — synthesize endpoints from blueprint when endpoints.json absent
- `--frame packageN|minimal` — frame style (default packageN MDI)
- `--strict` — fail on type fallbacks
- `--force` — overwrite existing xfdl (writes `.bak` first)

## Validators
| ID | Check |
| :-- | :-- |
| N001 | blueprint version + validation.passed |
| N002 | endpoints.json shape |
| N003 | blueprint ↔ endpoints entity sets match |
| N004 | every entity has ≥1 PK column |
| N005 | every entity has ≥1 searchable column |
| N006 | all emitted XML parses |
| N007 | overlay conflict guard |

## Design contract
See `docs/superpowers/specs/2026-05-14-andrej-karpathy-rdb-nexacro-design.md`
in the `business-fullstack-creater` repo.
