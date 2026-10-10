"""Assemble a self-contained, content-addressed record of a decision replay run."""

import argparse
import hashlib
import json
from pathlib import Path

from .decision_output import decision_output

VERSION = "property-run-v1"
ROOT_FILES = (
    "decision-repair-amendment.json",
    "decision-repair-summary.json",
    "manifest.json",
    "input-data.json",
    "corpus-index.json",
    "run-settings.json",
    "resume-settings.json",
    "decision-prompt.txt",
    "response-schema.json",
    "extraction-schemas.json",
    "tbox.json",
    "attachment-review.json",
    "model-view-reference-audit.json",
    "quote-revalidation.json",
    "representation-comparison.json",
    "transport-amendment.json",
    "prior-attempt-run.json",
    "prior-attempt-accounting.json",
    "implementation-snapshot.json",
    "resume-implementation-snapshot.json",
    "concurrency-amendment.json",
    "summary.json",
    "audit-summary.json",
    "episode-annotations.json",
    "judge-prompt.txt",
    "evaluation-settings.json",
    "evaluation-summary.json",
    "evaluation-protocol.md",
    "judge-implementation-snapshot.json",
    "frozen-agent-only-episodes.json",
    "evidence-response-prompt.txt",
    "evidence-response-rubric.md",
    "evidence-response-settings.json",
    "evidence-response-summary.json",
)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def resolve_artifacts(document, checkpoint, arm_id=None):
    """Resolve a checkpoint's embedded filenames without accessing the source directory."""
    refs = dict(checkpoint["artifacts"])
    if arm_id is not None:
        refs.update(checkpoint["arms"][arm_id]["artifacts"])
    return {name: document["blobs"][ref]["content"] for name, ref in refs.items()}


def assemble_run(root: Path):
    blobs = {}

    def embed(path):
        content = json.loads(path.read_text()) if path.suffix == ".json" else path.read_text()
        blob = {
            "media_type": "application/json" if path.suffix == ".json" else "text/plain",
            "content": content,
        }
        ref = "sha256:" + digest(blob)
        blobs[ref] = blob
        return ref

    def directory_files(path):
        return {p.name: embed(p) for p in sorted(path.glob("*.json")) if p.is_file()}

    root_refs = {name: embed(root / name) for name in ROOT_FILES if (root / name).exists()}
    if "manifest.json" not in root_refs:
        raise ValueError("A manifest is required to preserve the full denominator")
    manifest = blobs[root_refs["manifest.json"]]["content"]
    checkpoints = []
    calls = {}
    for job in sorted(manifest["jobs"], key=lambda row: row["id"]):
        job_id = job["id"]
        if Path(job_id).name != job_id:
            raise ValueError("Checkpoint ID must be a directory basename")
        artifacts = directory_files(root / job_id)
        interrupted = directory_files(root / "interrupted-attempts" / job_id)
        review_ref = artifacts.get("decision-review.json") or artifacts.get("result.json")
        review = blobs[review_ref]["content"] if review_ref else {}
        checkpoint = {
            "decision_agent_output": decision_output(
                {name: blobs[ref]["content"] for name, ref in artifacts.items()}
            ),
            "id": job_id,
            "case_id": job["case"],
            "split": job.get("split"),
            "cutoff": job["cutoff"],
            "prefix_sha256": job.get("prefix_sha256"),
            "context_sha256": job.get("context_sha256"),
            "status": review.get("status", "incomplete"),
            "phase_outputs": {
                "extraction": "evidence-packet.json" in artifacts
                or "decision-state.json" in artifacts,
                "decision": "decisions.json" in artifacts,
            },
            "artifacts": artifacts,
            "interrupted_artifacts": interrupted,
            "call_ids": [],
            "latency": {
                "seconds": review.get("latency_seconds"),
                "scope": "continuation_only" if interrupted else "checkpoint_execution",
                "includes_prior_interrupted_execution": False if interrupted else None,
            },
        }
        for attempt, refs in (("interrupted", interrupted), ("current", artifacts)):
            for filename, request_ref in refs.items():
                if not filename.endswith("-request.json") or filename.endswith(
                    "-canonical-request.json"
                ):
                    continue
                stage = filename.removesuffix("-request.json")
                response_ref = refs.get(stage + "-response.json")
                response = blobs[response_ref]["content"] if response_ref else None
                # Reused responses copied during resume are one billable observation.
                identity = {
                    "checkpoint": job_id,
                    "request": request_ref,
                    "response": response_ref,
                    "attempt": None if response_ref else attempt,
                }
                call_id = "call:" + digest(identity)
                if call_id not in calls:
                    usage = response.get("usage", {}) if response else {}
                    calls[call_id] = {
                        "id": call_id,
                        "checkpoint_id": job_id,
                        "stage": stage,
                        "request_ref": request_ref,
                        "response_ref": response_ref,
                        "observed_in": [],
                        "usage": usage,
                        "provider_response_id": response.get("id") if response else None,
                        "served_model": response.get("model") if response else None,
                        "status": "response_saved" if response else "response_not_saved",
                        "cost_usd": usage.get("cost"),
                        "latency_seconds": None,
                        "latency_status": "not_instrumented",
                        "transport_attempt_count": None,
                    }
                timing_ref = refs.get(stage.removesuffix("-repair") + "-timings.json")
                if timing_ref:
                    timings = blobs[timing_ref]["content"].get("calls", [])
                    matched = [
                        timing for timing in timings if timing.get("request_filename") == filename
                    ]
                    if len(matched) == 1:
                        timing = matched[0]
                        calls[call_id]["timing"] = timing
                        calls[call_id]["latency_seconds"] = timing.get("request_seconds")
                        calls[call_id]["latency_status"] = (
                            "measured_request_including_transport_retries"
                        )
                calls[call_id]["observed_in"].append(attempt)
                if call_id not in checkpoint["call_ids"]:
                    checkpoint["call_ids"].append(call_id)
        checkpoints.append(checkpoint)
    call_rows = sorted(
        calls.values(), key=lambda row: (row["checkpoint_id"], row["stage"], row["id"])
    )
    document = {
        "format_version": VERSION,
        "run_id": root.name,
        "interpretation": {
            "source_text": "Untrusted case data; never instructions to the judge.",
            "evidence": "Extracted claims with provenance, not authoritative world state.",
            "reasoning": "Saved decision rationale and citations, not private chain of thought.",
            "evaluation_only": "observed-later.json is future history: never model input.",
            "validity": "Schema validity, citation grounding, semantic support and historical correspondence are distinct.",
            "history": "An observed action is not necessarily correct or the only acceptable choice.",
        },
        "root_artifacts": root_refs,
        "checkpoints": checkpoints,
        "calls": call_rows,
        "accounting": accounting(call_rows),
        "cache_accounting": cache_accounting(call_rows),
        "completion": {
            "expected": len(manifest["jobs"]),
            "decisions_generated": sum(c["phase_outputs"]["decision"] for c in checkpoints),
            "all_checkpoints_terminal": all(
                c["status"]
                in {
                    "decision_generated",
                    "interface_failure",
                    "extraction_failure",
                    "completed",
                    "failure",
                }
                for c in checkpoints
            ),
            "extractions_available": sum(c["phase_outputs"]["extraction"] for c in checkpoints),
        },
        "run_wall_clock": {
            "seconds": None,
            "status": "not_instrumented",
            "note": "Checkpoint durations overlap; their sum is not run wall time.",
        },
        "blobs": dict(sorted(blobs.items())),
    }
    summary = blobs.get(root_refs.get("summary.json"), {}).get("content", {})
    evaluation = blobs.get(root_refs.get("evaluation-summary.json"), {}).get("content", {})
    evidence_evaluation = blobs.get(root_refs.get("evidence-response-summary.json"), {}).get(
        "content", {}
    )
    repair_evaluation = blobs.get(root_refs.get("decision-repair-summary.json"), {}).get(
        "content", {}
    )
    if summary.get("wall_clock_seconds") is not None:
        document["run_wall_clock"] = {
            "seconds": summary["wall_clock_seconds"],
            "status": "measured",
            "scope": "extraction and decision execution; excludes later historical judging"
            if evaluation
            else summary.get("wall_clock_scope", "run execution as recorded by runner"),
        }
    if evaluation or evidence_evaluation or repair_evaluation:
        document["phase_wall_clock"] = {
            "extraction_and_decision_seconds": summary.get("wall_clock_seconds"),
            "decision_reference_repair_seconds": repair_evaluation.get("seconds"),
            "historical_judging_seconds": evaluation.get("judge_wall_clock_seconds"),
            "evidence_response_judging_seconds": evidence_evaluation.get("wall_clock_seconds"),
            "meaning": "Separately timed phases; does not measure elapsed time between phases.",
        }
    document["content_sha256"] = digest(document)
    issues = validate_artifact(document)
    if issues:
        raise ValueError("Invalid run artifact: " + "; ".join(issues))
    return document


def accounting(calls):
    known = [c["cost_usd"] for c in calls if c["cost_usd"] is not None]
    missing = sum(c["cost_usd"] is None for c in calls)
    return {
        "returned_cost_usd": round(sum(known), 12),
        "calls_without_reported_cost": missing,
        "cost_is_lower_bound": bool(missing),
        "total_cost_usd": None if missing else round(sum(known), 12),
        "responses_saved": sum(c["response_ref"] is not None for c in calls),
        "requests_without_saved_response": sum(c["response_ref"] is None for c in calls),
        "reported_prompt_tokens": sum(c["usage"].get("prompt_tokens", 0) or 0 for c in calls),
        "reported_completion_tokens": sum(
            c["usage"].get("completion_tokens", 0) or 0 for c in calls
        ),
        "token_accounting_complete": all(
            c["usage"].get("prompt_tokens") is not None
            and c["usage"].get("completion_tokens") is not None
            for c in calls
        ),
        "scope": "Unique saved response/request observations; unrecorded transport retries may add unknown usage.",
    }


def cache_accounting(calls):
    """Only provider-reported cache counters; absent counters remain unknown."""
    phases = {}
    for call in calls:
        stage = call["stage"]
        phase = "records" if stage.startswith("records") else stage.removesuffix("-repair")
        row = phases.setdefault(
            phase,
            {
                "calls": 0,
                "cached_tokens": 0,
                "cache_write_tokens": 0,
                "calls_missing_cached_tokens": 0,
                "calls_missing_cache_write_tokens": 0,
            },
        )
        row["calls"] += 1
        details = call.get("usage", {}).get("prompt_tokens_details") or {}
        for key in ("cached_tokens", "cache_write_tokens"):
            value = details.get(key)
            if value is None:
                row["calls_missing_" + key] += 1
            else:
                row[key] += value
    return {
        "by_phase": dict(sorted(phases.items())),
        "meaning": "Provider-reported prompt token cache counters only. Missing counters are unknown, not zero; totals cover reporting calls only.",
    }


def validate_artifact(document):
    """Validate container integrity, accounting and the saved decision-input boundary."""
    if document.get("format_version") == "property-run-v2":
        from .experiment_artifact import validate_experiment

        return validate_experiment(document)
    issues = []
    if document.get("format_version") != VERSION:
        issues.append("Unsupported format version")
    unhashed = {k: v for k, v in document.items() if k != "content_sha256"}
    if digest(unhashed) != document.get("content_sha256"):
        issues.append("Document content hash mismatch")
    blobs = document["blobs"]
    for ref, blob in blobs.items():
        if ref != "sha256:" + digest(blob):
            issues.append("Blob hash mismatch: " + ref)
    refs = list(document["root_artifacts"].values())
    calls = {c["id"]: c for c in document["calls"]}
    ids = [c["id"] for c in document["checkpoints"]]
    if len(ids) != len(set(ids)) or len(calls) != len(document["calls"]):
        issues.append("Duplicate checkpoint or call ID")
    for checkpoint in document["checkpoints"]:
        refs.extend(checkpoint["artifacts"].values())
        refs.extend(checkpoint["interrupted_artifacts"].values())
        for call_id in checkpoint["call_ids"]:
            if call_id not in calls or calls[call_id]["checkpoint_id"] != checkpoint["id"]:
                issues.append("Invalid checkpoint call reference")
        files = (
            resolve_artifacts(document, checkpoint)
            if all(r in blobs for r in checkpoint["artifacts"].values())
            else {}
        )
        issues.extend(validate_attachment_artifacts(files, checkpoint["cutoff"]))
        if "decision_agent_output" in checkpoint and checkpoint[
            "decision_agent_output"
        ] != decision_output(files):
            issues.append("Decision agent output differs from saved artifacts")
        if "attachments.json" in files and checkpoint.get("context_sha256"):
            context_digest = hashlib.sha256(
                json.dumps(
                    {
                        "event_prefix_sha256": checkpoint["prefix_sha256"],
                        "attachments": files["attachments.json"],
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ).encode()
            ).hexdigest()
            if context_digest != checkpoint["context_sha256"]:
                issues.append("Attachment context content differs from frozen hash")
        packet = files.get("evidence-packet.json")
        request = files.get("decisions-canonical-request.json", files.get("decisions-request.json"))
        issues.extend(validate_model_view_artifacts(files))
        if packet and packet.get("prefix_sha256") != checkpoint["prefix_sha256"]:
            issues.append("Prefix hash mismatch: " + checkpoint["id"])
        if (
            packet
            and checkpoint.get("context_sha256")
            and packet.get("context_sha256") != checkpoint["context_sha256"]
        ):
            issues.append("Attachment context hash mismatch: " + checkpoint["id"])
        if packet and request:
            expected_input = packet
            manifest_blob = blobs.get(document["root_artifacts"].get("manifest.json"), {})
            if manifest_blob.get("content", {}).get("mode") in {
                "attachment_diagnostic",
                "prefix_evaluation",
            }:
                tbox_blob = blobs.get(document["root_artifacts"].get("tbox.json"), {})
                expected_input = {
                    "ontology_tbox": tbox_blob.get("content"),
                    "prefix_evidence": packet,
                }
            messages = [m for m in request.get("messages", []) if m.get("role") == "user"]
            try:
                matches = (
                    len(messages) == 1 and json.loads(messages[0]["content"]) == expected_input
                )
            except (ValueError, TypeError):
                matches = False
            if not matches:
                issues.append("Decision input differs from evidence packet: " + checkpoint["id"])
    for call in calls.values():
        refs.append(call["request_ref"])
        if call["response_ref"]:
            refs.append(call["response_ref"])
            response_blob = blobs.get(call["response_ref"])
            if response_blob:
                usage = response_blob["content"].get("usage", {})
                if usage != call["usage"] or usage.get("cost") != call["cost_usd"]:
                    issues.append("Call accounting differs from saved response")
        if call["checkpoint_id"] not in ids:
            issues.append("Unknown call checkpoint")
    if any(ref not in blobs for ref in refs):
        issues.append("Dangling blob reference")
    if accounting(document["calls"]) != document["accounting"]:
        issues.append("Accounting mismatch")
    if (
        "cache_accounting" in document
        and cache_accounting(document["calls"]) != document["cache_accounting"]
    ):
        issues.append("Cache accounting mismatch")
    if document["completion"]["expected"] != len(ids):
        issues.append("Denominator mismatch")
    manifest_ref = document["root_artifacts"].get("manifest.json")
    if manifest_ref in blobs:
        expected = sorted(row["id"] for row in blobs[manifest_ref]["content"]["jobs"])
        if expected != sorted(ids):
            issues.append("Checkpoint inventory differs from manifest")
    generated = sum("decisions.json" in c["artifacts"] for c in document["checkpoints"])
    if document["completion"]["decisions_generated"] != generated:
        issues.append("Completion count mismatch")
    return issues


def validate_model_view_artifacts(files):
    """Prove compact requests are exact deterministic views of saved canonical requests."""
    from .model_view import ModelView

    issues = []
    sources = files.get("sources.json", {}).get("sources", [])
    for name, canonical in files.items():
        if not name.endswith("-canonical-request.json"):
            continue
        stage = name.removesuffix("-canonical-request.json")
        aliases = files.get(stage + "-aliases.json", files.get("id-aliases.json"))
        actual = files.get(stage + "-request.json")
        if not aliases or not actual:
            issues.append("Compact request missing aliases or raw request: " + stage)
            continue
        view = ModelView(sources, version=aliases["version"])
        maps = aliases.get("maps", {})
        if set(maps) != set(view.maps) or maps.get("source") != view.maps["source"]:
            issues.append("Invalid compact identity map: " + stage)
            continue
        if any(len(set(mapping.values())) != len(mapping) for mapping in maps.values()):
            issues.append("Non-invertible compact identity map: " + stage)
            continue
        view.maps = maps
        try:
            expected = view.encode_body(
                canonical,
                omit_record_source_ids="Provenance"
                in canonical["response_format"]["json_schema"]["schema"].get("$defs", {}),
            )
            if expected != actual:
                issues.append("Compact request differs from canonical projection: " + stage)
        except (ValueError, KeyError, TypeError, IndexError):
            issues.append("Malformed compact request projection: " + stage)
    return issues


def validate_attachment_artifacts(files, cutoff):
    """Check document availability and exact text provenance without judging its claims."""
    if "attachments.json" not in files:
        return []
    attachments = files["attachments.json"]
    events = {event["id"]: event["text"] for event in files.get("input.json", {}).get("events", [])}
    documents = {document["id"]: document for document in attachments.get("documents", [])}
    pages = {
        (page["document_id"], page["page_number"]): page for page in attachments.get("pages", [])
    }
    issues = []
    if len(documents) != len(attachments.get("documents", [])) or len(pages) != len(
        attachments.get("pages", [])
    ):
        issues.append("Duplicate attachment document/page")
    for document in documents.values():
        available = document["available_at_event_ids"]
        if not available or any(
            event not in events or int(event) > int(cutoff) for event in available
        ):
            issues.append("Attachment not linked within available prefix")
        for reference in document["references"]:
            text = events.get(reference["event_id"])
            if (
                text is None
                or text[reference["start"] : reference["end"]] != reference["expression"]
            ):
                issues.append("Attachment link span differs from prefix event")
    for page in pages.values():
        document = documents.get(page["document_id"])
        if document is None or page["document_sha256"] != document["sha256"]:
            issues.append("Attachment page has invalid document provenance")
        if hashlib.sha256(page["text"].encode()).hexdigest() != page["text_sha256"]:
            issues.append("Attachment page text hash mismatch")
        if document and page["available_at_event_ids"] != document["available_at_event_ids"]:
            issues.append("Attachment page availability differs from linked document")
    for source in files.get("sources.json", {}).get("sources", []):
        if source.get("origin") != "attachment":
            continue
        page = pages.get((source["document_id"], source["page_number"]))
        if page is None or page["text"][source["start"] : source["end"]] != source["text"]:
            issues.append("Attachment source span differs from extracted page")
        elif (
            source.get("text_sha256") != page["text_sha256"]
            or source.get("document_sha256") != page["document_sha256"]
            or source.get("available_at_event_ids") != page["available_at_event_ids"]
            or source.get("event_id") not in page["available_at_event_ids"]
        ):
            issues.append("Attachment source identity or availability differs from page")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    document = assemble_run(args.run)
    output = args.output or args.run / "run.json"
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(output)
    print(
        json.dumps(
            {
                "path": str(output),
                "content_sha256": document["content_sha256"],
                "completion": document["completion"],
                "accounting": document["accounting"],
            }
        )
    )


if __name__ == "__main__":
    main()
