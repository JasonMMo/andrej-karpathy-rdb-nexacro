# MT — Multi-Tab

탭별로 다른 dataset/grid를 보여주는 패턴. Lazy loading 지원.

- **Tab 0 (기본정보)**: 주 entity grid + CRUD 버튼
- **Tab 1 (관련내역)**: blueprint relations에서 첫 1:N child가 있으면 자동 wiring (없으면 hint)
- **Tab 2 (변경이력)**: `dsHistory` 자리표시 (event_time/actor/action/detail) — 도메인 audit endpoint 후속 wiring

## 사용 예
- 사용자 계정 (기본정보 + 권한 + 로그인이력)
- 거래처 (기본정보 + 거래내역 + 신용변동이력)

## blueprint 예
```yaml
entities:
  - name: user_account
    pattern: MT
```

Child 1:N relation이 blueprint에 있으면 form_gen이 자동으로 Tab 1 grid에 wiring한다. 출처: nexacro-claude-skills `references/patterns/multi-tab.md`.
