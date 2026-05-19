# MD — master-detail-2-tier

상단 master grid(또는 단일 record 편집) + 하단 child line-items grid 2영역 패턴.
transactional document (주문서/발주서/송장/견적서) 표준.

## 적합한 도메인
- 주문관리: sales_order + order_item (주문서 = 헤더 + 라인)
- 재고관리: product + sku (상품 + 옵션 SKU)
- 재무관리: account + ledger_entry (계정 + 분개)
- 일반적으로 1:N 관계에서 "한 부모를 보면서 자식 라인을 편집" UX

## 비적합
- 단순 list-detail (행 선택 → 같은 entity 상세) → **L2**
- 단일 record 편집만 → **F1**
- 다행 CRUD만 → **D2**

## 영역 구성
- 상단(60~280px): 마스터 grid + 추가/삭제 버튼
- 중간(310px): 가로 divider
- 하단(320~600px): 자식 라인 grid + 저장 버튼

## 자동 wiring (Growth-5)
- `form_gen.py`가 blueprint `relations[]`에서 해당 entity를 `from`으로 하는 **첫 번째 `cardinality: 1:N` 관계**를 자동 탐지
- 자식 entity의 컬럼/endpoints를 그대로 사용해 `ds<ChildPascal>`, `grd_child`, `fn_add_child` / `fn_delete_child`, save payload(`dataList ... childList ...`)까지 일괄 wiring
- `fn_master_changed`는 부모 PK(`id` 컬럼)로 자식 dataset을 재조회하며, FK 컬럼은 관계 정의의 `fk.column`을 사용 (없으면 `parent_id` 폴백)
- D2/F1/C1/L2 패턴은 child kwargs를 받지 않으므로 무영향
- 1:N 관계가 없거나 자식 endpoints가 없으면 placeholder 영역(`hint_child`)으로 graceful degrade
