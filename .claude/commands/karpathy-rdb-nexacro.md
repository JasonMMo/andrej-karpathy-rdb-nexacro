---
name: karpathy-rdb-nexacro
description: Compile blueprint + endpoints.json → nexacro xfdl forms
argument-hint: compile --blueprint <path> --endpoints <path> --out <dir>
---

# /karpathy-rdb-nexacro

Generate nexacro xfdl forms from Stage 1 blueprint + Stage 3 endpoints.json.

## Usage

```
/karpathy-rdb-nexacro compile \
  --blueprint  <path>/_blueprint.yaml \
  --endpoints  <path>/endpoints.json \
  --out        <out-dir>
```

Optional flags: `--infer-endpoints`, `--frame {packageN|minimal}`, `--strict`, `--force`.

See SKILL.md for full reference.
