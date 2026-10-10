"""Package saved run outputs without calling models or changing recorded decisions."""

import argparse
import json
import shutil
import tempfile
from pathlib import Path

from .experiment_artifact import assemble_experiment
from .render_run import render_document
from .run_artifact import assemble_run, resolve_artifacts
from .submission import export_answers


def finalize_run(root, from_artifact=False):
    """Publish JSON, HTML and all answer arms together; preserve prior packages."""
    root = Path(root)
    try:
        if from_artifact:
            document = json.loads((root / "run.json").read_text())
            arms = (
                document["arm_ids"] if document["format_version"] == "property-run-v2" else [None]
            )
        elif (root / "experiment.json").exists():
            configuration = json.loads((root / "experiment.json").read_text())
            baseline_path = Path(
                configuration.get("baseline_artifact_path")
                or Path(configuration["baseline_root"]) / "run.json"
            )
            baseline = json.loads(baseline_path.read_text())
            document = assemble_experiment(root, baseline)
            arms = document["arm_ids"]
        else:
            document = assemble_run(root)
            arms = (
                [None]
                if any(
                    "decisions.json" in checkpoint["artifacts"]
                    for checkpoint in document["checkpoints"]
                )
                else []
            )
        stage = Path(tempfile.mkdtemp(prefix=".packaging-", dir=root))
        (stage / "run.json").write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n")
        names = ["run.json", "index.html"]
        for arm in arms:
            name = "ANSWERS" if arm is None else "ANSWERS-" + arm
            export_answers(document, stage / name, arm)
            names.append(name)
        checkpoints = [
            (checkpoint, resolve_artifacts(document, checkpoint))
            for checkpoint in document["checkpoints"]
        ]
        identity = {"run_id": document["run_id"], "content_hash": document["content_sha256"]}
        (stage / "index.html").write_text(render_document(document, checkpoints, identity))
        previous = [name for name in names if (root / name).exists()]
        if previous:
            history = root / ".packaging-history"
            history.mkdir(exist_ok=True)
            archive = Path(tempfile.mkdtemp(prefix="package-", dir=history))
            for name in previous:
                shutil.move(str(root / name), archive / name)
        for name in names:
            shutil.move(str(stage / name), root / name)
        stage.rmdir()
        status = {
            "status": "completed",
            "artifact_sha256": document["content_sha256"],
            "generated": names,
            "model_calls": 0,
        }
    except (ValueError, KeyError, TypeError, OSError) as error:
        status = {
            "status": "failure",
            "error_type": type(error).__name__,
            "error": str(error),
            "run_outputs_preserved": True,
            "model_calls": 0,
        }
    (root / "packaging-status.json").write_text(json.dumps(status, indent=2) + "\n")
    print(json.dumps({"packaging": str(root), **status}), flush=True)
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument(
        "--from-artifact",
        action="store_true",
        help="Regenerate projections of the existing canonical JSON without reassembling it",
    )
    args = parser.parse_args()
    raise SystemExit(
        0 if finalize_run(args.run, args.from_artifact)["status"] == "completed" else 1
    )


if __name__ == "__main__":
    main()
