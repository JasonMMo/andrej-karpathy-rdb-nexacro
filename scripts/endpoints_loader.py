import json
import pathlib

REQUIRED_METHODS = {"select_datalist_map", "save_datalist_map"}


class EndpointsError(Exception):
    pass


def load_endpoints(path):
    p = pathlib.Path(path)
    if not p.exists():
        raise EndpointsError(f"N002 endpoints.json not found: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise EndpointsError(f"N002 endpoints.json is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise EndpointsError(
            f"N002 endpoints.json must be a JSON object, got {type(data).__name__}"
        )
    if data.get("version") != 1:
        raise EndpointsError(f"N002 unsupported version: {data.get('version')!r}")
    for e in data.get("entities") or []:
        methods = {ep.get("method") for ep in e.get("endpoints") or []}
        missing = REQUIRED_METHODS - methods
        if missing:
            raise EndpointsError(
                f"N002 entity {e.get('name')!r} missing methods: {sorted(missing)}"
            )
    return data


def infer_endpoints(entities, context_path="/uiadapter"):
    out = []
    for e in entities:
        name = e["name"]
        base = f"/{name}"
        out.append({
            "name": name,
            "endpoint_base": base,
            "endpoints": [
                {"method": "select_datalist_map",
                 "http_path": f"{base}/select_datalist_map.do",
                 "input": {"dsSearch": "param-dataset"},
                 "output": {"output1": "list-dataset"}},
                {"method": "save_datalist_map",
                 "http_path": f"{base}/save_datalist_map.do",
                 "input": {"dataList": "row-dispatch"},
                 "output": {}},
            ],
        })
    return {"version": 1, "context_path": context_path, "entities": out}


def cross_check(blueprint_entities, endpoints_payload):
    bp_names = {e["name"] for e in blueprint_entities}
    ep_names = {e["name"] for e in endpoints_payload.get("entities") or []}
    only_bp = bp_names - ep_names
    only_ep = ep_names - bp_names
    if only_bp or only_ep:
        raise EndpointsError(
            f"N003 entity sets diverge — blueprint-only={sorted(only_bp)}, "
            f"endpoints-only={sorted(only_ep)}"
        )
