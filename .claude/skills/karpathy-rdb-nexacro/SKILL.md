---
name: karpathy-rdb-nexacro
description: Generates entity-per-form nexacro xfdl from blueprint + endpoints.json
---

# karpathy-rdb-nexacro

Stage 4 of the business-fullstack-creater pipeline.

## Inputs
- `_blueprint.yaml` — see `references/blueprint-input-contract.md`
- `endpoints.json` — see `references/endpoints-input-contract.md`

## Outputs
See `references/output-layout.md`.

## Form layout
2-tier — Search panel (top) + editable Grid (middle) + action buttons.
See `references/form-layout.md`.

## Type mapping
See `references/type-mapping-matrix.md`.

## Overlay
See `references/overlay-policy.md`.

## Run
```
python scripts/form_gen.py compile --blueprint <bp> --endpoints <ep> --out <dir>
```
