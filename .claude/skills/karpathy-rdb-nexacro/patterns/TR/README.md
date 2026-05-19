# TR — tree-1-tier

검색 + 트리 Grid + CRUD 패턴. self-FK(self-hierarchy) entity 전용.
Nexacro Grid 의 `treeuseyn="true"` 모드를 활용해 parent/child 노드를 들여쓰기로 표시.

## 적합한 도메인
- 인사관리 department (부서 → 하위 부서)
- 재무관리 account (계정과목 트리)
- 게시판 comment (대댓글)
- 상품 category, 메뉴, 권한 트리, 카테고리 분류 일반

## 비적합
- 단순 다행 CRUD (self-FK 없음) → **D2**
- 부모-자식이 서로 다른 entity → **MD**
- 좌측 list + 우측 detail 게시판형 → **L2**

## 자동 wiring (Growth-6)
- `form_gen.py` 가 blueprint `relations[]` 에서 해당 entity 가 `from == to` 인
  `cardinality: self` 관계를 자동 탐지 → `fk.column` 값을 `self_parent_column` 컨텍스트로 전달
- "자식 추가" 버튼은 현재 선택 노드의 `id` 를 부모 PK로 잡아 새 행에 set
- "루트 추가" 버튼은 parent FK 를 null 로 set
- self relation 미정의 시 컨벤션 fallback: `parent_id`

## 영역 구성
- 상단(0~60px): 검색 패널
- 중간(70~570px): 트리 Grid (treeuseyn=true, 초기 전체 확장)
- 하단(580~608px): 루트 추가 / 자식 추가 / 삭제 / 저장 버튼

## DDL 요구사항
- self-FK 컬럼 (`parent_id` 등) 이 nullable 이어야 root 노드 허용
- 순환 참조 방지는 DB 제약이 아니라 UI/서비스 레이어 책임
