# Blueprint Input Contract (Stage 1 → Stage 4)

Source: `wiki/_blueprint.yaml` produced by `/karpathy-rdb compile`.

## Required top-level keys
- `version`: must equal `1`
- `project`: string
- `entities[]`: `{name, table, columns[], indexes?, constraints?}`
- `validation.passed`: must equal `true`

## Entity column shape (post nullable refactor)
```yaml
columns:
  - { name: customer_id, type: varchar(36), pk: true, nullable: false }
  - { name: name,        type: varchar(100), nullable: true }
```

## Hard rejects (Stage 4 N001)
- `version != 1`
- `validation.passed != true`
- Any entity with zero `pk: true` columns (N004)
