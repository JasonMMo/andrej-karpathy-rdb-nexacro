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

## Patterns (v0.3+)
Form layout 은 명명된 file-based pattern 으로 분리.
- 기본: `D2` (detail-2-tier). 다른 옵션: `F1` (form-1-tier), `C1` (card-1-tier).
- 선택: blueprint entity `pattern:` 필드 또는 CLI `--default-pattern`.
- 카탈로그: `<repo>/.claude/skills/karpathy-rdb-nexacro/patterns/` (번들) → `~/.karpathy-rdb/catalog/patterns/` (글로벌 fallback).
- 상세: `references/patterns-spec.md`.

## Type mapping
See `references/type-mapping-matrix.md`.

## Overlay
See `references/overlay-policy.md`.

## Run
```
python scripts/form_gen.py compile --blueprint <bp> --endpoints <ep> --out <dir>
```

## Ownership & Self-Check (Phase A — 2026-05-22)

이 skill 은 **business-fullstack-creater 5축 책임표의 `nexacro (Stage 4+5)` 축**을 담당. 활동 뷰는 `business-fullstack-creater/learn-log.md` §0.

- **깊이 누적 위치**: `patterns/` (D2/F1/C1/L2/MD/MDS/MT/PS/RO/TG/TR 11개) + UI overlay (nexacro/react)
- **단위 테스트**: `tests/` (pytest)
- **누적 트랩 (0)**: 없음 (frontend 패턴 레이어)
- **미해결 환류**: 없음
- **Self-check (Growth 종료 시)**: 새 frontend pattern 또는 overlay 변종이 발생했다면 `business-fullstack-creater/learn-log.md` §0 nexacro 행 + §3 (패턴) 한 줄 환류했는가?
