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

## ⚠️ MVP 한계 (Growth-4)
- 자식 dataset(`ds<Pascal>Items`)과 자식 grid 컬럼은 **사용자가 자식 entity에 맞춰 보강**해야 함
- `fn_master_changed`에서 부모 PK로 자식 재조회 로직도 사용자 보강 영역
- 다음 Growth 사이클에서 compose_form이 자식 entity까지 받도록 확장 예정 (현재는 D2/F1/C1/L2 무영향 유지가 우선)
