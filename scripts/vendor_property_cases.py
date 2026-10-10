"""Vendor the unmodified property directory from a clean, pinned upstream checkout."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from property_eval.dataset import inventory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, required=True)
    args = parser.parse_args()

    def git(*parts):
        return subprocess.check_output(["git", "-C", str(args.checkout), *parts], text=True).strip()

    remote = git("remote", "get-url", "origin")
    if remote != "https://github.com/DwellyOrg/HackatonPublicCases.git":
        raise ValueError("Unexpected upstream")
    if git("status", "--porcelain", "--", "Property Management"):
        raise ValueError("Upstream dataset has local modifications")
    destination = Path(__file__).resolve().parents[1] / "data/property-management"
    shutil.copytree(args.checkout / "Property Management", destination)
    info = inventory(destination)
    info.pop("input_dir")
    info.update(
        upstream_repository=remote,
        upstream_commit=git("rev-parse", "HEAD"),
        upstream_path="Property Management",
        local_modifications=False,
    )
    (destination.parent / "property-management-provenance.json").write_text(
        json.dumps(info, indent=2) + "\n"
    )
    shutil.copy2(args.checkout / "README.md", destination.parent / "UPSTREAM_README.md")
    print(
        json.dumps(
            {
                "destination": str(destination),
                "cases": len(info["cases"]),
                "files": len(info["files"]),
                "dataset_sha256": info["dataset_sha256"],
            }
        )
    )


if __name__ == "__main__":
    main()
