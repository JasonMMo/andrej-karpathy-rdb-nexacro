import pathlib
import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

from pattern_loader import resolve_pattern, PatternNotFoundError

BUNDLED = REPO_ROOT / ".claude" / "skills" / "karpathy-rdb-nexacro" / "patterns"


def test_resolve_bundled_D2():
    p = resolve_pattern("D2", bundled_root=BUNDLED, global_root=None)
    assert p.name == "D2"
    assert p.template_path.name == "form.xfdl.j2"
    assert p.template_path.exists()
    assert p.manifest["name"] == "D2"
    assert p.source == "bundled"


def test_resolve_bundled_L2():
    """Growth-3: list-detail-2-tier pattern for list-heavy domains (게시판, 공지...)."""
    p = resolve_pattern("L2", bundled_root=BUNDLED, global_root=None)
    assert p.name == "L2"
    assert p.template_path.exists()
    assert p.manifest["name"] == "L2"
    assert p.manifest["kind"] == "list-detail-2-tier"
    assert "select_datalist_map" in p.manifest["required_endpoints"]
    assert "save_datalist_map" in p.manifest["required_endpoints"]


def test_resolve_bundled_MD():
    """Growth-4: master-detail-2-tier pattern for transactional documents (주문서/발주서/송장)."""
    p = resolve_pattern("MD", bundled_root=BUNDLED, global_root=None)
    assert p.name == "MD"
    assert p.template_path.exists()
    assert p.manifest["name"] == "MD"
    assert p.manifest["kind"] == "master-detail-2-tier"
    assert "select_datalist_map" in p.manifest["required_endpoints"]
    assert "save_datalist_map" in p.manifest["required_endpoints"]


def test_resolve_bundled_TR():
    """Growth-6: tree-1-tier pattern for self-hierarchy entities (department/account/comment)."""
    p = resolve_pattern("TR", bundled_root=BUNDLED, global_root=None)
    assert p.name == "TR"
    assert p.template_path.exists()
    assert p.manifest["name"] == "TR"
    assert p.manifest["kind"] == "tree-1-tier"
    assert "select_datalist_map" in p.manifest["required_endpoints"]
    assert "save_datalist_map" in p.manifest["required_endpoints"]


def test_resolve_bundled_RO():
    """Growth-7: read-only-list-1-tier pattern for audit/history entities."""
    p = resolve_pattern("RO", bundled_root=BUNDLED, global_root=None)
    assert p.name == "RO"
    assert p.template_path.exists()
    assert p.manifest["name"] == "RO"
    assert p.manifest["kind"] == "read-only-list-1-tier"
    assert "select_datalist_map" in p.manifest["required_endpoints"]
    # RO is intentionally read-only — no save endpoint required
    assert "save_datalist_map" not in p.manifest["required_endpoints"]


def test_resolve_bundled_F1():
    """Gap 6: form-1-tier pattern for single-record forms."""
    p = resolve_pattern("F1", bundled_root=BUNDLED, global_root=None)
    assert p.name == "F1"
    assert p.template_path.exists()
    assert p.manifest["name"] == "F1"


def test_resolve_bundled_C1():
    """Gap 6: card-1-tier pattern for lookup-picker style entities."""
    p = resolve_pattern("C1", bundled_root=BUNDLED, global_root=None)
    assert p.name == "C1"
    assert p.template_path.exists()
    assert p.manifest["name"] == "C1"


@pytest.mark.parametrize("pat", ["D2", "F1", "C1", "L2", "MD", "TR", "RO"])
def test_all_seven_bundled_patterns_resolve(pat):
    """Gap 6 freeze: every shipped pattern must be loadable via the generic resolver.

    Catches regressions where a manifest or template gets deleted/renamed and
    blueprint entities declaring that pattern silently fall back to D2.
    """
    p = resolve_pattern(pat, bundled_root=BUNDLED, global_root=None)
    assert p.source == "bundled"
    assert p.template_path.exists()
    assert p.manifest.get("name") == pat


@pytest.mark.parametrize("pat,kind", [
    ("MT",  "multi-tab-N-tier"),
    ("TG",  "tree-grid-2-pane"),
    ("PS",  "popup-search-1-tier"),
    ("MDS", "multi-dataset-save-header-lines"),
])
def test_growth41_complex_patterns_resolve(pat, kind):
    """Growth-41: 4 complex screen patterns mirrored from nexacro-claude-skills.

    Each shipped pattern must be resolvable via the generic loader and declare
    the documented kind. Catches regressions where a manifest gets renamed and
    blueprint entities declaring the pattern silently fall back to D2.
    """
    p = resolve_pattern(pat, bundled_root=BUNDLED, global_root=None)
    assert p.source == "bundled"
    assert p.template_path.exists()
    assert p.manifest.get("name") == pat
    assert p.manifest.get("kind") == kind
    assert "select_datalist_map" in p.manifest["required_endpoints"]
    # MDS, MT, TG all save; PS is read-only lookup
    if pat == "PS":
        assert "save_datalist_map" not in p.manifest["required_endpoints"]
    else:
        assert "save_datalist_map" in p.manifest["required_endpoints"]


def test_unknown_pattern_raises(tmp_path):
    with pytest.raises(PatternNotFoundError) as exc:
        resolve_pattern("ZZ", bundled_root=BUNDLED, global_root=tmp_path)
    assert "ZZ" in str(exc.value)


def test_global_fallback(tmp_path):
    pat_dir = tmp_path / "X9"
    pat_dir.mkdir()
    (pat_dir / "manifest.yaml").write_text("name: X9\nkind: detail\n", encoding="utf-8")
    (pat_dir / "form.xfdl.j2").write_text("<dummy/>", encoding="utf-8")
    p = resolve_pattern("X9", bundled_root=BUNDLED, global_root=tmp_path)
    assert p.template_path.read_text(encoding="utf-8") == "<dummy/>"
    assert p.source == "global"
