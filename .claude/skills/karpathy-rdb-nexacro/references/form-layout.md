# Form Layout (form.xfdl.j2 핵심)

2단 구조 — Search 상단 (60px) + 편집 가능 Grid 중단 (520px) + 버튼.

- `<Layout>` width=900, height=620
- `<Dataset id="dsSearch">` — PK / business key / NOT NULL 후보 컬럼으로 구성
- `<Dataset id="ds{Pascal}">` — Grid 의 단일 메인 dataset (편집 in-place)
- `<Grid binddataset="ds{Pascal}" autofittype="col">` — `<Format>` 의 각 `<Cell>` 에 컬럼별 `edittype` 지정
  - varchar/text → `edittype="text"`
  - numeric → `edittype="masknumber"`
  - date/timestamp → `edittype="date"`
  - char(1) + `*_yn` → `edittype="combo"` (combodataset = 인라인 Y/N)
  - boolean → `edittype="checkbox"`
  - PK / auto-key → `edittype="none"` (readonly)
- `<Script>`
  - `fn_search()` → `this.transaction("select", ".../select_datalist_map.do", "dsSearch=dsSearch", "output1=ds{Pascal}")`
  - `fn_add()` → `ds{Pascal}.addRow()` + 현재 row 로 Grid 포커스 이동 (PK 초기값: bigserial=공란, varchar(uuid)=공란, 사용자 입력 또는 server-side fill)
  - `fn_save()` → `_RowType_` 검사 후 `this.transaction("save", ".../save_datalist_map.do", "dataList=ds{Pascal}:U")`
  - `fn_delete()` → 선택 row `deleteRow()` + 저장 시 D 로 dispatch
