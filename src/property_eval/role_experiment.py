"""Fresh model role extraction, then decision; separate from frozen-packet ladders."""

import argparse
import asyncio
import hashlib
import json
import shutil
import time
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .citation_catalog import SelectedJudgment, build_catalog, materialize, selection_schema
from .cli import write_json
from .decision_alignment import align_decision
from .decision_replay import digest, extract_packet, structured_call
from .models import (
    EVIDENCE_ONTOLOGY_VERSION,
    EntityExtraction,
    LinkExtraction,
    MentionExtraction,
    RecordExtraction,
)
from .prefix import load_prefix
from .rejudge_spans import SelectionValidator
from .response import DecisionResponse, validate_response
from .soft_eval import mechanical_comparison
from .soft_experiment import citation_checks, decision_payload, judge_payload, request

CASES = {"011", "016", "025", "026", "028", "035", "038"}


def prepare(args):
    root = args.output
    root.mkdir(parents=True, exist_ok=False)
    prior = Path("runs/decision-soft-v1").resolve()
    oldconfig = json.loads((prior / "experiment.json").read_text())
    manifest = json.loads((prior / "manifest.json").read_text())
    manifest["jobs"] = [j for j in manifest["jobs"] if j["case"] in CASES]
    manifest["cohort"] = "seven_role_identity_diagnostics"
    assert len(manifest["jobs"]) == 7
    tbox = json.loads((prior / "tbox.json").read_text())
    tbox.update(
        {
            "version": "property-tbox-v2-role-identity",
            "evidence_ontology_version": EVIDENCE_ONTOLOGY_VERSION,
            "response_ontology_version": "property-response-v4",
            "result": DecisionResponse.model_json_schema(),
            "evidence": {
                m.__name__: m.model_json_schema()
                for m in [MentionExtraction, LinkExtraction, EntityExtraction, RecordExtraction]
            },
        }
    )
    tbox["semantics"] += (
        "\n\n" + Path("docs/role-identity-v5.md").read_text().split("The intervention evaluates")[0]
    )
    prompt = (
        (prior / "prompts/control.txt").read_text()
        + "\nSource-described role_party entities are legitimate case-scoped identities. Use their supplied IDs for communications and approval requests; absent personal names or CRM identifiers alone are not blockers. Preserve genuine conflicting referents, ambiguous task linkage and missing authority scope. This run tests model-extracted role identities: use the extracted parties, without synthesizing a named person or a benchmark-context binding.\n"
    )
    judge = Path("experiments/prompts/soft-judge-v2.txt").read_text()
    for name in ["evidence", "targets", "prompts"]:
        (root / name).mkdir()
    (root / "prompts/role-model.txt").write_text(prompt)
    (root / "judge-prompt.txt").write_text(judge)
    write_json(root / "manifest.json", manifest)
    write_json(root / "tbox.json", tbox)
    write_json(root / "response-schema.json", DecisionResponse.model_json_schema())
    write_json(root / "judge-schema.json", SelectedJudgment.model_json_schema())
    shutil.copy2(prior / "target-review.json", root / "target-review.json")
    entries = []
    for job in manifest["jobs"]:
        shutil.copy2(
            prior / "targets" / f"{job['id']}.json", root / "targets" / f"{job['id']}.json"
        )
        target = json.loads((root / "targets" / f"{job['id']}.json").read_text())
        entries.append(
            {
                **job,
                "baseline_path": str(Path(oldconfig["baseline_root"]) / job["id"]),
                "target_sha256": digest(target),
                "arms": {
                    "role-model": {"path": f"arms/role-model/{job['id']}", "status": "pending"}
                },
            }
        )
    contrast = load_prefix(args.source, "012", 21)
    config = {
        "version": "role-identity-experiment-v2"
        if args.mention_coverage
        else "role-identity-experiment-v1",
        "mode": "role_extraction",
        "baseline_root": oldconfig["baseline_root"],
        "model": "openai/gpt-6-luna",
        "hypothesis": "Model recognition/linking of case-scoped role parties removes missing-name blockers while preserving real referent and authority uncertainty.",
        "factor": "Evidence ontology, extraction prompts and role semantics changed; fresh extraction+decision. Not a pure decision-prompt arm.",
        "scope": "Seven exposed development prefixes; separate later012 contrast, no holdout/generalization claim.",
        "arms": [
            {
                "id": "role-model",
                "prompt_path": "prompts/role-model.txt",
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            }
        ],
        "tboxes": {"combined": "tbox.json", "sha256": digest(tbox)},
        "response_schema_sha256": digest(DecisionResponse.model_json_schema()),
        "judge_version": "soft-judge-v2",
        "judge_schema_sha256": digest(SelectedJudgment.model_json_schema()),
        "judge_prompt_sha256": hashlib.sha256(judge.encode()).hexdigest(),
        "settings": {
            "seed": 42,
            "temperature": "unsupported/omitted",
            "reasoning_effort": "provider_default",
            "decision_max_tokens": 8000,
            "judge_max_tokens": 6000,
            "extraction_max_tokens": 16000,
            "concurrency": 24,
            "mention_coverage": args.mention_coverage,
            "timeout_seconds": 480,
        },
        "planned_calls": {
            "extraction": 28 if args.no_contrast else 24,
            "decisions": 7 if args.no_contrast else 8,
            "judgments": 7,
            "max_interface_repair_calls": 42 if args.mention_coverage else 39,
        },
        "stop_rule": "One pass perprefix, bounded interface repair only. No target-dependent prompt retuning.",
        "contrast": {
            "id": "012-at-021",
            "case": "012",
            "cutoff": 21,
            "prefix_sha256": contrast.source_sha256,
            "path": "contrast/012-at-021",
            "scored": False,
            "meaning": "Novel development contrast for task/label uncertainty, excluded seven-case historical correspondence denominator.",
        },
    }
    if args.no_contrast:
        config.pop("contrast")
    write_json(root / "experiment.json", config)
    write_json(
        root / "corpus-index.json",
        {
            "version": "role-identity-experiment-v2"
            if args.mention_coverage
            else "role-identity-experiment-v1",
            "denominator": 7,
            "entries": entries,
        },
    )
    write_json(
        root / "implementation-snapshot.json",
        {
            name: {
                "source": (Path(__file__).parent / name).read_text(),
                "sha256": hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest(),
            }
            for name in [
                "role_experiment.py",
                "mention_coverage.py",
                "models.py",
                "prompt.py",
                "client.py",
                "grounding.py",
                "validation.py",
                "canonicalization.py",
                "response.py",
                "citation_catalog.py",
                "decision_replay.py",
            ]
        },
    )


async def run(args):
    root = args.output
    config = json.loads((root / "experiment.json").read_text())
    index = json.loads((root / "corpus-index.json").read_text())
    tbox = json.loads((root / "tbox.json").read_text())
    prompt = (root / "prompts/role-model.txt").read_text()
    judge = (root / "judge-prompt.txt").read_text()
    assert digest(tbox) == config["tboxes"]["sha256"]
    assert digest(DecisionResponse.model_json_schema()) == config["response_schema_sha256"]
    assert hashlib.sha256(prompt.encode()).hexdigest() == config["arms"][0]["prompt_sha256"]
    key = dotenv_values(args.env_file)["OPENROUTER_API_KEY"]
    args.model = config["model"]
    args.max_tokens = 16000
    args.mention_coverage = config["settings"].get("mention_coverage", False)
    semaphore = asyncio.Semaphore(config["settings"]["concurrency"])

    async def one(job, client, contrast=False):
        async with semaphore:
            directory = root / job["path"] if contrast else root / job["arms"]["role-model"]["path"]
            directory.mkdir(parents=True, exist_ok=True)
            usage, timings = {}, {}
            started = time.monotonic()
            result = {
                "id": job["id"],
                "arm": "role-model",
                "status": "running",
                "scored": not contrast,
            }
            try:
                async with asyncio.timeout(480):
                    before = time.monotonic()
                    packet = await extract_packet(job, args, directory, client, key, usage)
                    timings["extraction_seconds"] = time.monotonic() - before
                    write_json(directory / "evidence-packet.json", packet)
                    if not contrast:
                        write_json(root / "evidence" / f"{job['id']}.json", packet)
                        job["evidence_sha256"] = digest(packet)
                    body = request(
                        decision_payload(packet, tbox),
                        prompt,
                        DecisionResponse.model_json_schema(),
                        args.model,
                        8000,
                        "decision",
                    )
                    before = time.monotonic()
                    raw = await structured_call(
                        client, key, body, DecisionResponse, directory, "decisions", usage
                    )
                    timings["decision_seconds"] = time.monotonic() - before
                    write_json(directory / "decisions-raw-parsed.json", raw.model_dump())
                    aligned = align_decision(raw.model_dump(), packet["sources"])
                    write_json(directory / "decisions-canonicalization.json", aligned)
                    prediction = DecisionResponse.model_validate(aligned["response"])
                    write_json(directory / "decisions.json", prediction.model_dump())
                    write_json(
                        directory / "decisions-validation.json",
                        validate_response(prediction, packet),
                    )
                    result.update(
                        {
                            "evidence_sha256": digest(packet),
                            "prediction_sha256": digest(prediction.model_dump()),
                            "tbox_sha256": digest(tbox),
                            "decision_request_sha256": digest(body),
                        }
                    )
                    if not contrast:
                        target = json.loads((root / "targets" / f"{job['id']}.json").read_text())
                        catalog = build_catalog(packet, target, prediction.model_dump())
                        write_json(directory / "citation-catalog.json", catalog)
                        write_json(
                            directory / "mechanical.json",
                            mechanical_comparison(prediction.model_dump(), target),
                        )
                        payload = judge_payload(packet, tbox, target, prediction.model_dump())
                        payload["citation_catalog"] = catalog["spans"]
                        body = request(
                            payload, judge, selection_schema(catalog), args.model, 6000, "judgment"
                        )
                        before = time.monotonic()
                        selected = await structured_call(
                            client,
                            key,
                            body,
                            SelectionValidator(catalog),
                            directory,
                            "judge",
                            usage,
                        )
                        timings["judge_seconds"] = time.monotonic() - before
                        write_json(directory / "judge-selections.json", selected.model_dump())
                        judged, spans = materialize(selected.model_dump(), catalog)
                        write_json(directory / "judge.json", judged)
                        write_json(directory / "judge-spans.json", spans)
                        write_json(
                            directory / "judge-validation.json",
                            citation_checks(judged, packet, target, prediction.model_dump()),
                        )
                        result["judge_request_sha256"] = digest(body)
                    result["status"] = "completed"
            except (
                ValueError,
                TypeError,
                KeyError,
                IndexError,
                TimeoutError,
                httpx.HTTPError,
                AssertionError,
            ) as error:
                result.update(
                    {"status": "failure", "error_type": type(error).__name__, "error": str(error)}
                )
            result.update(
                {
                    "usage_by_stage": usage,
                    "timings": timings,
                    "latency_seconds": time.monotonic() - started,
                    "cost_usd": sum(u.get("cost", 0) or 0 for u in usage.values()),
                }
            )
            write_json(directory / "result.json", result)
            if not contrast:
                job["arms"]["role-model"].update(
                    {"status": result["status"], "cost_usd": result["cost_usd"]}
                )
                write_json(root / "corpus-index.json", index)
            print(f"{job['id']}: {result['status']} (${result['cost_usd']:.5f})", flush=True)
            return result

    async with httpx.AsyncClient(timeout=180) as client:
        results = await asyncio.gather(
            *[one(job, client) for job in index["entries"]],
            *([one(config["contrast"], client, True)] if "contrast" in config else []),
        )
    write_json(
        root / "summary.json",
        {
            "primary_denominator": 7,
            "primary_results": results[:7],
            "contrast": results[-1] if "contrast" in config else None,
            "cost_usd": sum(r["cost_usd"] for r in results),
            "meaning": "Fresh model role-identity diagnostic, not frozen-packet prompt comparison",
        },
    )
    from .finalization import finalize_run

    finalize_run(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "run"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", type=Path, default=Path("/Users/ryan/code/HackatonPublicCases"))
    parser.add_argument("--env-file", type=Path, default=Path("/Users/ryan/code/plasm/.env"))
    parser.add_argument("--mention-coverage", action="store_true")
    parser.add_argument("--no-contrast", action="store_true")
    args = parser.parse_args()
    prepare(args) if args.mode == "prepare" else asyncio.run(run(args))


if __name__ == "__main__":
    main()
