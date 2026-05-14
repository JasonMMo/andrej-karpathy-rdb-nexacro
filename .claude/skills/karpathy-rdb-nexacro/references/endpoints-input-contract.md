# Endpoints Input Contract (Stage 3 v0.1.4 → Stage 4)

Source: `<OUT_BACKEND>/endpoints.json`.

## Shape
```json
{
  "version": 1,
  "context_path": "/uiadapter",
  "entities": [
    {
      "name": "customer",
      "endpoint_base": "/customer",
      "endpoints": [
        {"method": "select_datalist_map", "http_path": "/customer/select_datalist_map.do",
         "input": {"dsSearch": "param-dataset"}, "output": {"output1": "list-dataset"}},
        {"method": "save_datalist_map", "http_path": "/customer/save_datalist_map.do",
         "input": {"dataList": "row-dispatch"}, "output": {}}
      ]
    }
  ]
}
```

## Hard rejects (Stage 4 N002)
- `version != 1`
- Any entity missing one of {select_datalist_map, save_datalist_map}
- Any entity in blueprint not present in endpoints.entities (N003)

## Infer mode (`--infer-endpoints`)
If endpoints.json is missing, synthesize from blueprint:
`endpoint_base = /<entity.name>`, two fixed methods, http_path = `<base>/<method>.do`.
