# MDS — Multi-Dataset Save (Header + Lines, one transaction)

정형 문서(주문서/발주서/송장/품의서) 작성·수정 화면.
**헤더(Master, 1 row)** + **라인(Child, N rows)** 을 한 transaction 으로 동시 저장.

## MDS vs MD

| | MD | MDS |
|---|---|---|
| 화면 모드 | master 조회 + child 조회/저장 (browse-oriented) | 문서 단위 작성·수정·저장 (form-oriented) |
| 저장 단위 | child 그리드 :U 단독 | **header + lines 동시** (`dataList=...:U,dsChildList=...:U`) |
| 헤더 표현 | grid 한 row 클릭 | grid 클릭 후 **하단 form 필드(BindItem)** 로 직접 편집 |
| 신규 신청 | "추가" 버튼 1단계 | **"신규문서"** → header clear + 1 row 자동 추가 → 라인 추가 |

> 즉, MDS 는 MD 의 상위 변종이다 — 헤더 자체도 편집 대상이고, 트랜잭션 경계가 "문서 1건" 으로 묶인다.

## blueprint 예

```yaml
entities:
  - name: sales_order
    pattern: MDS
    child:
      entity: order_item
      fk_column: order_id
```

`form_composer.py` 가 child entity 의 endpoints (`select_datalist_map`, `save_datalist_map`) 도 함께 로드해야 한다 (MD 와 동일 컨벤션).

## 핵심 트랜잭션 라인

```
dataList=ds{Master}:U,dsChildList=ds{Child}:U
```

서버 측은 두 dataset 의 변경 row 를 **하나의 DB transaction** 안에서 처리해야 한다 (header insert/update 후 returning PK 로 lines FK 채워 저장). 출처: nexacro-claude-skills `references/patterns/multi-dataset-save.md`.
