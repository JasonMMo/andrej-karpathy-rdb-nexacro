# RO — Read-Only List (1-tier)

## 용도

audit / history / log / ledger 등 **INSERT-only 추적 데이터**의 조회 전용 화면.
CRUD 버튼 없음 → audit 무결성 보장.

대상 엔티티 (Growth-7 시점):
- `order_status_history` — 주문 상태 변경 이력
- `stock_movement` — 재고 입출고 이력
- `contact_log` — 고객 접촉 이력
- `ledger_entry` — 회계 분개 (마감된 period 보호)

## 컴포넌트

| 컴포넌트 | 동작 |
| :-- | :-- |
| `btn_search` | dsSearch 기준 조회 |
| `btn_refresh` | 마지막 검색 조건 재조회 |
| `grd_main` | `readonly=true` 그리드 |
| `btn_export` | overlay 단계에서 lane별 exporter 어댑터에 위임 (`fn_export_dataset` 후크) |
| `lbl_hint` | "조회 전용" 가이드 라벨 |

## 호출 endpoint

`select_datalist_map` 만 사용. `save_datalist_map` 은 의도적으로 호출하지 않음.

## 왜 D2 대신 RO 인가

D2 는 btn_add/del/save 가 항상 렌더된다. audit 엔티티에 D2 를 쓰면:
- 사용자가 임의로 history 행을 수정/삭제할 수 있는 UI 가 노출되어 무결성 위반 가능
- backend 단에서 막더라도 UI 가 "쓸 수 있는 것처럼" 보여 사용자 혼동
- 마감 회계기간(closed_at) 보호 정책과 UI 가 불일치

RO 는 처음부터 "조회 + 내보내기" 만 노출해 정책과 UI 를 정렬한다.

## blueprint 사용

```yaml
type: entity
name: order_status_history
pattern: RO
```

## 향후 확장

- Stage 5 overlay 단계에서 `fn_export_dataset` 어댑터를 lane 별 (nexacro=xlsx, react=csv) 로 주입
- date-range 검색 필드 자동 wiring (`*_at` 컬럼이 있는 RO 엔티티 한정)
