# Form Pattern Catalog (v0.4+)

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

## 번들 패턴 (v0.4 — Growth-3 L2 추가)
| 이름 | 종류 | 용도 |
| :-- | :-- | :-- |
| **D2** | detail-2-tier | 검색 + grid + CRUD 버튼. 기본값. 다행 CRUD. |
| **F1** | form-1-tier | 단일 record 편집. grid 없음. 1:1 entity / 디테일 측. |
| **C1** | card-1-tier | 검색 + 읽기 전용 grid + 선택 버튼. picker / popup. |
| **L2** | list-detail-2-tier | 좌측 list grid + 우측 detail 편집 패널. 게시판/공지/명단 등 list-heavy 도메인 표준. |

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
