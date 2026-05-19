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
| `btn_export` | Growth-8: lane=nexacro → `this.parent.fn_export_dataset(...)` (Stage 5 가 자동 `Export.xjs` 발행); lane=react → entity 모듈의 `exportToCsv()` 호출 |
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

## Stage 5 export 어댑터 (Growth-8 완료)

| lane | 발행물 | 동작 |
| :-- | :-- | :-- |
| nexacro | `nxui/packageN/<domain>/Export.xjs` | `fn_export_dataset(ds, name)` → `Dataset.saveCSV(name+'.csv')` (UTF-8 BOM 포함, 네이티브 저장 다이얼로그) |
| react | 각 `frontend/src/api/<entity>.ts` 에 `exportToCsv(params?, filename?)` | `selectDataListMap()` 결과를 Blob 으로 다운로드 |

nexacro 어댑터는 blueprint 에 **하나라도 RO 엔티티가 있으면** 발행된다. 사용자는 발행된 `Export.xjs` 를 TypeDefinition `<Scripts>` 에 등록하고 parent frame 에서 include 하기만 하면 된다 (one-time wiring). react 어댑터는 lane 차원에서 보편적이므로 모든 entity 모듈에 부여된다.

## 향후 확장

- xlsx 출력 지원 (현재는 CSV)
- date-range 검색 필드 자동 wiring (`*_at` 컬럼이 있는 RO 엔티티 한정)
