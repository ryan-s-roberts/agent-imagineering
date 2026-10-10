"""Directory-format input discovery and provenance, independent of evaluation labels."""

import argparse
import hashlib
import json
import re
from pathlib import Path

from .prefix import HEADER, load_prefix


def inventory(input_dir):
    root = Path(input_dir).resolve(strict=True)
    cases = []
    for path in sorted(root.glob("*/history.md")):
        case = path.parent.name
        if not re.fullmatch(r"\d{3}", case):
            raise ValueError(f"Case directory must contain three digits: {case}")
        count = len(list(HEADER.finditer(path.read_text())))
        prefix = load_prefix(root, case, count)
        cases.append(
            {
                "case": case,
                "event_count": len(prefix.events),
                "history_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    if not cases:
        raise ValueError(
            "Input directory must directly contain numbered case directories with history.md"
        )
    files = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Input symlinks are not permitted: {path.relative_to(root)}")
        if path.is_file():
            files.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "bytes": path.stat().st_size,
                }
            )
    fingerprint = hashlib.sha256(
        json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "version": "property-input-directory-v1",
        "input_dir": str(root),
        "dataset_sha256": fingerprint,
        "cases": cases,
        "files": files,
        "model_input_policy": "Only the selected history prefix and attachments explicitly linked by that prefix. Case index/summary files are never model input.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--split", required=True, choices=["development", "unseen"])
    parser.add_argument(
        "--cutoff-policy",
        required=True,
        choices=["end"],
        help="Use all supplied history as input, without inventing future scoring labels",
    )
    args = parser.parse_args()
    info = inventory(args.input_dir)
    if args.output.exists():
        raise ValueError("Manifest already exists; preserve the frozen selection")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "version": "property-input-manifest-v1",
        "dataset_sha256": info["dataset_sha256"],
        "selection": "End of each supplied history; prediction only unless separate evaluation references are provided",
        "jobs": [
            {"case": c["case"], "cutoff": c["event_count"], "split": args.split}
            for c in info["cases"]
        ],
    }
    args.output.write_text(json.dumps(document, indent=2) + "\n")
    print(
        json.dumps(
            {
                "cases": len(info["cases"]),
                "dataset_sha256": info["dataset_sha256"],
                "manifest": str(args.output),
            }
        )
    )


if __name__ == "__main__":
    main()
