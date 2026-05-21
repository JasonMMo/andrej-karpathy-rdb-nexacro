# Form Pattern Catalog (v0.7+, Growth-41 — 4 Complex Patterns)

## 개요
Stage 4 의 form layout 은 명명된 file-based pattern 디렉터리로 분리되어 있다.
하드코딩된 단일 layout 대신, blueprint entity 의 `pattern:` 필드 (또는 CLI `--default-pattern`) 로
선택한다.

## 카탈로그 위치 (우선순위)
1. 번들: `<repo>/.claude/skills/karpathy-rdb-nexacro/patterns/<name>/`
2. 글로벌 fallback: `~/.karpathy-rdb/catalog/patterns/<name>/`
3. 미발견 시 명시적 에러 (`PatternNotFoundError`) — silent fallback 금지

## 디렉터리 규약
```
patterns/<name>/
  manifest.yaml     # name, kind, description, required_endpoints
  form.xfdl.j2      # Jinja2 템플릿 (form_composer 가 제공하는 컨텍스트 사용)
  README.md         # 사람 읽기용 설명
```

### manifest.yaml 필드
| 필드 | 설명 |
| :-- | :-- |
| `name` | 패턴 이름 (디렉터리 이름과 일치) |
| `kind` | 분류 라벨 (예: `detail-2-tier`, `form-1-tier`, `card-1-tier`) |
| `description` | 한 줄 요약 |
| `required_endpoints` | 패턴이 호출하는 endpoint method 이름 배열 (예: `[select_datalist_map, save_datalist_map]`) |

## 컨텍스트 변수 (form.xfdl.j2 에서 사용 가능)
`scripts/form_composer.py:compose_form` 이 모든 패턴 템플릿에 동일하게 제공:

| 변수 | 설명 |
| :-- | :-- |
| `form_id` | entity 이름 (snake_case) |
| `title` | 화면 제목 (보통 `<Pascal> 관리`) |
| `entity_pascal` | PascalCase 변환 entity 이름 |
| `search_fields` | search 입력 컴포넌트 XML 조각 |
| `grid_format` | grid 컬럼 정의 XML 조각 (패턴이 grid 를 안 써도 항상 제공됨) |
| `datasets` | dsSearch + ds<Pascal> 데이터셋 XML 조각 |
| `select_path` | select_datalist_map 의 http_path |
| `save_path` | save_datalist_map 의 http_path |

## 번들 패턴 (v0.7 — Growth-7 RO 추가)
| 이름 | 종류 | 용도 |
| :-- | :-- | :-- |
| **D2** | detail-2-tier | 검색 + grid + CRUD 버튼. 기본값. 다행 CRUD. |
| **F1** | form-1-tier | 단일 record 편집. grid 없음. 1:1 entity / 디테일 측. |
| **C1** | card-1-tier | 검색 + 읽기 전용 grid + 선택 버튼. picker / popup. |
| **L2** | list-detail-2-tier | 좌측 list grid + 우측 detail 편집 패널. 게시판/공지/명단 등 list-heavy 도메인 표준. |
| **MD** | master-detail-2-tier | 상단 master + 하단 child line-items. 주문서/발주서/송장 등 transactional document. blueprint `relations` 의 첫 번째 1:N 자식이 자동 wiring (Growth-5). 없을 시 placeholder graceful degrade. |
| **TR** | tree-1-tier | 검색 + 트리 Grid(treeuseyn=true) + 루트/자식 추가/삭제/저장. self-hierarchy entity (department/account/comment/category) 전용. blueprint `relations` 의 첫 번째 `cardinality: self` 의 `fk.column` 이 `self_parent_column` 으로 자동 주입 (Growth-6). 없으면 컨벤션 `parent_id` 로 fallback. |
| **RO** | read-only-list-1-tier | 검색 + 읽기 전용 Grid + 새로고침/내보내기. CRUD 버튼 없음. audit/history/log/ledger 등 INSERT-only 추적 데이터 전용 (Growth-7). `required_endpoints` 는 `select_datalist_map` 만 (save 미사용). `fn_export_dataset` 후크는 Stage 5 overlay 에서 lane 별 exporter 어댑터로 주입. |

## Growth-41 신규 복합 화면 패턴 (Complex Screen Patterns)
출처: [nexacro-claude-skills/.../nexacro-form-maker/SKILL.md#복잡-화면-패턴](https://github.com/JasonMMo/nexacro-claude-skills/blob/master/plugins/nexacro-claude-skills/skills/nexacro-form-maker/SKILL.md#%EB%B3%B5%EC%9E%A1-%ED%99%94%EB%A9%B4-%ED%8C%A8%ED%84%B4-complex-screen-patterns)

| 이름 | 종류 | 용도 |
| :-- | :-- | :-- |
| **MT** | multi-tab-N-tier | 동일 entity 의 view 를 3개 탭으로 분할 (기본정보/관련내역/변경이력). `fn_tab_changed` lazy loading + per-tab dispatch. `child_entity` 있으면 탭2 자동 wiring. |
| **TG** | tree-grid-2-pane | 좌측 카테고리 트리(`dsCategory` displaytype=treeitemcontrol) + 우측 entity 그리드. 좌측 선택이 `dsSearch.{category_fk_column\|default('category_id')}` 으로 자동 주입 후 재조회. MD 와 구별: MD = 1:N 수직, TG = navigation 수평. |
| **PS** | popup-search-1-tier | `<Form classname="Popup">` 분류. 검색 + 읽기 grid (oncelldblclick 선택) + 확인/취소. 부모 폼이 `gfnOpenPopup` 으로 열고 `opener.fnReceivePopupData(oData)` 콜백으로 row 객체 수신. `required_endpoints` 는 `select` 만. |
| **MDS** | multi-dataset-save-header-lines | 헤더(Form-style BindItem) + 라인(child grid) → `dataList=ds{Master}:U,dsChildList=ds{Child}:U` 단일 transaction 동시 저장. 주문서/발주서/송장 작성·수정 (MD 의 form-oriented 상위 변종). 헤더 필드는 `templates/header_field.xml.j2` 가 자동 렌더. |

> **MD vs MDS**: MD = master grid 클릭 → child 조회/저장 (browse-oriented). MDS = 신규문서 작성·수정 (form-oriented, header+lines 한 트랜잭션). MD 는 두 개의 select+save, MDS 는 한 개의 combined save.

## 새 패턴 추가
1. `patterns/<name>/` 디렉터리 생성 (manifest.yaml + form.xfdl.j2 + README.md)
2. `tests/unit/test_form_composer_unit.py` 에 케이스 추가
3. (선택) `/karpathy-rdb contribute --kind pattern <name>` 으로 글로벌 카탈로그 승격

## 선택 우선순위 (form_gen.py)
1. blueprint entity frontmatter `pattern: <name>`
2. CLI `--default-pattern <name>`
3. 기본값 `D2`

## 하위 호환
- `pattern:` 없는 기존 blueprint → D2 로 처리 (현재 동작 그대로)
- blueprint `version: 1` 유지 (선택 필드 추가는 호환 변경)
- Stage 2 (DDL), Stage 3 (MyBatis) 는 `pattern:` 필드를 무시
