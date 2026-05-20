"""Tests for resolve_shell (Growth-16 P1-b)."""
import pathlib
import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

from pattern_loader import resolve_shell, ShellNotFoundError

BUNDLED = REPO_ROOT / ".claude" / "skills" / "karpathy-rdb-nexacro" / "patterns"


def test_resolve_shell_MDI_default():
    s = resolve_shell("MDI", bundled_root=BUNDLED, global_root=None)
    assert s.variant == "MDI"
    assert s.source == "bundled"
    # MDI manifest lists 5 frames
    for name in ("frame_main", "frame_mdi", "frame_left", "frame_top", "frame_login"):
        assert name in s.frames, f"missing frame {name}"
        assert s.frames[name].exists()
    assert s.typedef_template.exists()
    assert s.xadl_template.exists()
    # manifest contains both variants
    variant_ids = {v["id"] for v in s.manifest["variants"]}
    assert {"MDI", "SDI"} <= variant_ids


def test_resolve_shell_SDI_falls_back_to_MDI_for_shared_frames():
    """SDI only defines frame_sdi.xfdl.j2; the rest fall back to MDI templates."""
    s = resolve_shell("SDI", bundled_root=BUNDLED, global_root=None)
    assert s.variant == "SDI"
    # frame_sdi resolves to SDI-specific template
    assert "frame_sdi" in s.frames
    assert s.frames["frame_sdi"].parent.name == "SDI"
    # shared frames fall back to MDI directory
    for shared in ("frame_main", "frame_left", "frame_top", "frame_login"):
        assert shared in s.frames
        assert s.frames[shared].parent.name == "MDI", (
            f"{shared} should fall back to MDI base, got {s.frames[shared]}"
        )


def test_resolve_shell_unknown_variant_raises():
    with pytest.raises(ShellNotFoundError) as exc:
        resolve_shell("ZZZ", bundled_root=BUNDLED, global_root=None)
    assert "ZZZ" in str(exc.value)


def test_resolve_shell_frame_overrides_take_priority(tmp_path):
    """Project-local frame_overrides win over bundled templates."""
    override = tmp_path / "my_login.xfdl.j2"
    override.write_text("<Custom/>", encoding="utf-8")
    s = resolve_shell(
        "MDI",
        bundled_root=BUNDLED,
        global_root=None,
        frame_overrides={"frame_login": override},
    )
    assert s.frames["frame_login"] == override
    # other frames remain bundled
    assert s.frames["frame_main"].parent.parent.parent.name == "SHELL"
