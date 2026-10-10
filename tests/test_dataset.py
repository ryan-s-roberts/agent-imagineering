import shutil

import pytest

from property_eval.dataset import inventory
from property_eval.prefix import load_prefix


def write_case(root):
    case = root / "101"
    case.mkdir(parents=True)
    (case / "history.md").write_text(
        "# Case 101 history\n\n## 2026-01-01 09:00:00 UTC — event 001\n\n- **Channel:** Email\n- **From:** Tenant\n- **To:** Agency / system\n\nThe tap leaks.\n"
    )
    (case / "index.md").write_text("SECRET FUTURE OUTCOME: repaired")


def test_new_case_range_and_arbitrary_directory_are_supported(tmp_path):
    root = tmp_path / "totally-new-input"
    write_case(root)
    data = inventory(root)
    assert data["cases"][0]["case"] == "101"
    prefix = load_prefix(root, "101", 1)
    assert "SECRET FUTURE" not in prefix.model_dump_json()
    copied = tmp_path / "relocated"
    shutil.copytree(root, copied)
    assert inventory(copied)["dataset_sha256"] == data["dataset_sha256"]


def test_wrong_wrapper_root_fails_explicitly(tmp_path):
    write_case(tmp_path / "nested")
    with pytest.raises(ValueError, match="directly contain"):
        inventory(tmp_path)
