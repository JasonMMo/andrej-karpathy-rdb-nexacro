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
