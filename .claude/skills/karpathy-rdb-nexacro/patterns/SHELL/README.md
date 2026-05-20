# SHELL Pattern (Growth-16)

Project-level nexacro shell — entity 패턴 (D2/F1/C1/L2/MD/TR/RO) 과 달리 `applies_to: project`.

**Variants:** MDI (default), SDI. `extensible: true` — 사용자 등록 variant 허용.

**Frames per variant:**
- MDI: frame_main + frame_mdi + frame_left + frame_top + frame_login
- SDI: frame_main + frame_sdi + frame_left + frame_top + frame_login

**확장 슬롯:**
- `blueprint.shell.menu.extensions` — 자동 메뉴 트리에 merge (sort 키로 정렬)
- `blueprint.shell.typedef.extra_services` — 합성된 `<Services>` 노드에 append
- `blueprint.shell.frame_overrides` — 사용자 frame 으로 교체. 우선순위: **project local > skill local > global catalog**

**Variant 확장 절차:**
1. (local) `<project>/.karpathy-rdb-nexacro/patterns/SHELL/variants/<ID>/` 에 frame_*.xfdl.j2 작성 + manifest entry 추가
2. (global) `/karpathy-rdb-nexacro contribute --kind shell-variant <ID>` 로 환류 (Phase 후속)

상세 spec: `business-fullstack-creater/docs/superpowers/specs/2026-05-20-growth-16-shell-pattern-design.md`
