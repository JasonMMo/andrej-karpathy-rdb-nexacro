# Type Mapping Matrix (D6 확정)

PostgreSQL 타입 → (Dataset type, size, Search 컴포넌트, Grid cell `edittype`/`displaytype`, 비고). Edit panel 제거 (D1) — 편집은 Grid cell 에서 직접 수행.

| PG type | Dataset | size | Search 컴포넌트 | Grid `edittype` | Grid `displaytype` | 비고 |
| :-- | :-- | :-: | :-- | :-- | :-- | :-- |
| `bigserial`, `serial`, `bigint`, `integer` | `BIGDECIMAL` | — | `Edit` | `none` (pk) / `masknumber` | `number` | PK readonly |
| `varchar(n)`, `text` | `STRING` | n or 4000 | `Edit` | `text` | `text` | — |
| `char(1)` + name matches `*_yn` | `STRING` | 1 | `Combo` (Y/N/전체) | `combo` (inline Y/N) | `combotext` | 한국 컨벤션 |
| `char(n)` | `STRING` | n | `Edit` | `text` | `text` | — |
| `numeric(p,s)`, `decimal` | `BIGDECIMAL` | p | `Edit` | `masknumber` | `number` | — |
| `boolean` | `STRING` | 1 | `Combo` | `checkbox` | `checkbox` | Y/N 변환 |
| `date` | `STRING` | 8 | `Calendar` range | `date` | `date` | YYYYMMDD |
| `timestamp`, `timestamptz` | `STRING` | 14 | `Calendar` | `date` | `date` | YYYYMMDDHHMISS |
| `time` | `STRING` | 6 | `Edit` | `mask` (HH:MM:SS) | `text` | — |
| `json`, `jsonb` | `STRING` | 4000 | (검색 제외) | `text` | `text` (truncate) | — |
| `uuid` | `STRING` | 36 | `Edit` | `none` (pk) / `text` | `text` | — |
| **(미매핑)** | `STRING` | 100 | `Edit` | `text` | `text` | `warnings.md` 기록, `--strict` 시 exit 1 |
