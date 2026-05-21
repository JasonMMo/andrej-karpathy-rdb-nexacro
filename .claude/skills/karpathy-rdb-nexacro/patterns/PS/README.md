# PS — Popup Search

코드 마스터/거래처/사원/품목 조회용 **modal popup** 화면.
부모 폼이 `gfnOpenPopup`(또는 동등) 으로 열고, 선택된 row 를 `opener.fnReceivePopupData(oData)` 로 받는다.

- `<Form classname="Popup">` — popup 전용 분류
- `form_onload` 에서 `getOwnerFrame().arguments` 로 초기 검색조건 prepopulate
- 결과 grid `oncelldblclick="fn_select_row"` + 하단 `btn_select` 둘 다 동일 핸들러
- `fn_select_row` 가 선택 row 의 모든 컬럼을 객체로 직렬화 → `opener.fnReceivePopupData(oData)` 호출 → close

## 부모 폼 측 사용 패턴

```javascript
// 부모 폼
this.fn_open_popup_customer = function() {
  var args = { name_like: this.dsSearch.getColumn(0, "name_like") };
  this.gfnOpenPopup(this, "popCust", "popupSearchCustomer.xfdl", 600, 500, args, "fn_popup_callback", true);
};

// 부모 폼에서 popup 이 호출하는 콜백
this.fnReceivePopupData = function(oData) {
  this.ds주문.setColumn(this.ds주문.rowposition, "customer_id",   oData.id);
  this.ds주문.setColumn(this.ds주문.rowposition, "customer_name", oData.name);
};
```

## blueprint 예

```yaml
entities:
  - name: customer
    pattern: PS    # popup-search 화면도 함께 생성
```

`pattern: PS` 만으로는 `select_datalist_map` endpoint 가 필요하다 (`save` 는 사용 안 함). 출처: nexacro-claude-skills `references/patterns/popup-search.md`.
