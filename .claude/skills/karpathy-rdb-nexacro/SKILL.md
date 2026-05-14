---
name: karpathy-rdb-nexacro
description: Generates entity-per-form nexacro xfdl from blueprint + endpoints.json
---

# karpathy-rdb-nexacro

Stage 4 of the business-fullstack-creater pipeline. Consumes:
- Stage 1 `_blueprint.yaml`
- Stage 3 `endpoints.json` (v0.1.4+)

Emits xfdl forms + dsMenu seed + typedefinition patch ready to overlay on
`nexacro-fullstack-starter` scaffold.

See `references/` for input contracts, type matrix, and output layout.
