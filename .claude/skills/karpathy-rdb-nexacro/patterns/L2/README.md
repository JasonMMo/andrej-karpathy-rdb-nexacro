# L2 — list-detail-2-tier

좌측 list grid + 우측 detail 편집 패널 1폼 2영역 패턴.

## 적합한 도메인
- 게시판: board, post (목록 조회 후 한 행 선택 → 상세 편집)
- 공지: notice
- 직원 명단: employee
- 일반적인 "list 보다가 한 행 선택해서 자세히" UX

## 비적합
- 단순 multi-row CRUD만 필요한 마스터 테이블 → **D2**
- 1:1 detail 편집만 → **F1**
- 카드형 dashboard → **C1**

## 영역 구성
- 좌측 (0~400px): 검색 + grid + 페이지 버튼
- 우측 (410~900px): 선택 행의 detail 편집 폼 + Save 버튼
- 그리드 row 선택 변경 시 detail 영역은 동일 dataset의 rowposition을 따라 자동 갱신
