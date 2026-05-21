# TG — Tree + Grid

좌측 카테고리/트리 + 우측 데이터 grid (수평 2분할 navigation).

- 좌측 `dsCategory` Grid (treeitemcontrol displaytype) → 선택 시 `dsSearch.category_id` 세팅 → 우측 자동 재조회
- 우측 `ds{Entity}` 일반 CRUD grid

## MD vs TG
- **MD**: FK 1:N — 상하 분할, master 행 변경 시 child 재조회 (한 트랜잭션 도큐먼트)
- **TG**: navigation — 좌우 분할, 카테고리는 entity의 외래 dimension (별도 도메인 또는 dynamic FK)

## blueprint 예
```yaml
entities:
  - name: product
    pattern: TG
    category_fk_column: category_id   # 좌측 트리 선택과 매칭될 FK
```

좌측 트리 데이터(`dsCategory`)는 form_onload에서 별도 endpoint로 로드해야 한다 (현재 패턴은 grid + bind만 깔고 빈 dataset로 시작). 출처: nexacro-claude-skills `references/patterns/tree-grid.md`.
