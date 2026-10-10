"""Canonical multi-arm artifacts over immutable baseline evidence."""

import argparse
import copy
import hashlib
import json
from pathlib import Path

from .decision_output import decision_output
from .run_artifact import accounting, digest

VERSION = "property-run-v2"
ROOT_FILES = (
    "manifest.json",
    "experiment.json",
    "tbox.json",
    "judge-prompt.txt",
    "response-schema.json",
    "judge-schema.json",
    "corpus-index.json",
    "summary.json",
    "implementation-snapshot.json",
    "target-review.json",
    "inherited-experiment.json",
    "decision-difference-review.json",
    "benchmark-context.json",
    "role-review.json",
    "episode-review.json",
    "episode-annotation-guide.md",
    "episode-annotations.json",
    "ablation-analysis.json",
)
DECISION_FILES = {
    "decision-review.json",
    "result.json",
    "observed-later.json",
}


def read_json(path):
    return json.loads(path.read_text())


def assemble_experiment(root, baseline):
    from .run_artifact import validate_artifact

    baseline_issues = validate_artifact(baseline)
    if baseline_issues or baseline.get("format_version") != "property-run-v1":
        raise ValueError("A valid immutable v1 baseline artifact is required")
    blobs = copy.deepcopy(baseline["blobs"])

    def embed(path):
        blob = {
            "media_type": "application/json" if path.suffix == ".json" else "text/plain",
            "content": read_json(path) if path.suffix == ".json" else path.read_text(),
        }
        ref = "sha256:" + digest(blob)
        blobs[ref] = blob
        return ref

    def files(directory):
        return {p.name: embed(p) for p in sorted(directory.glob("*.json")) if p.is_file()}

    root_refs = {name: embed(root / name) for name in ROOT_FILES if (root / name).exists()}
    prompt_refs = {p.stem: embed(p) for p in sorted((root / "prompts").glob("*.txt"))}
    manifest = read_json(root / "manifest.json")
    experiment = read_json(root / "experiment.json")
    judge_only = experiment.get("mode") == "judge_only"
    role_extraction = experiment.get("mode") == "role_extraction"
    # Arms are declared in the experiment, not inferred from completed output folders.
    declared_arms = experiment["arms"]
    arm_ids = sorted(
        declared_arms
        if isinstance(declared_arms, dict)
        else [a if isinstance(a, str) else a["id"] for a in declared_arms]
    )
    if len(arm_ids) != len(set(arm_ids)) or not arm_ids:
        raise ValueError("Experiment needs unique declared arms")
    if any(Path(arm).name != arm for arm in arm_ids):
        raise ValueError("Arm IDs must be basenames")
    if role_extraction and len(arm_ids) != 1:
        raise ValueError("Role extraction intervention requires one declared arm")
    if role_extraction and "benchmark-context.json" in root_refs:
        raise ValueError("Role extraction must not inject benchmark party assumptions")
    baseline_checkpoints = {c["id"]: c for c in baseline["checkpoints"]}
    jobs = sorted(manifest["jobs"], key=lambda job: job["id"])
    selected_ids = {job["id"] for job in jobs}
    if len(selected_ids) != len(jobs):
        raise ValueError("Duplicate manifest checkpoint")
    calls = [
        dict(c, accounting_scope="inherited_baseline", arm_id=None)
        for c in baseline["calls"]
        if c["checkpoint_id"] in selected_ids
    ]
    checkpoints = []
    for job in jobs:
        checkpoint_id = job["id"]
        prior = baseline_checkpoints[checkpoint_id]
        if prior["prefix_sha256"] != job["prefix_sha256"]:
            raise ValueError("Manifest changed frozen prefix: " + checkpoint_id)
        original_refs = prior["artifacts"]
        refs = {
            name: ref
            for name, ref in original_refs.items()
            if name not in DECISION_FILES
            and name != "citation-catalog.json"
            and not name.startswith(("decisions", "judge", "episode-"))
        }
        packet_ref = refs["evidence-packet.json"]
        evidence_path = root / "evidence" / f"{checkpoint_id}.json"
        if role_extraction:
            original_packet = blobs[packet_ref]["content"]
            refs = {
                name: ref
                for name, ref in original_refs.items()
                if name in {"input.json", "sources.json"}
            }
            fresh = files(root / "arms" / arm_ids[0] / checkpoint_id)
            refs.update(
                {
                    name: ref
                    for name, ref in fresh.items()
                    if name.startswith(("mention", "link", "record", "entities"))
                    or name in {"input.json", "sources.json"}
                }
            )
            packet_ref = (
                embed(evidence_path)
                if evidence_path.exists()
                else fresh.get("evidence-packet.json")
            )
            if packet_ref:
                packet = blobs[packet_ref]["content"]
                if packet.get("prefix_sha256") != prior["prefix_sha256"] or packet.get(
                    "sources"
                ) != original_packet.get("sources"):
                    raise ValueError("Role extraction changed frozen prefix/source units")
                refs["evidence-packet.json"] = packet_ref
        elif evidence_path.exists() and embed(evidence_path) != packet_ref:
            raise ValueError("Experiment changed frozen evidence: " + checkpoint_id)
        target_path = root / "targets" / f"{checkpoint_id}.json"
        target_ref = embed(target_path) if target_path.exists() else None
        arms = {}
        for arm_id in arm_ids:
            directory = root / "arms" / arm_id / checkpoint_id
            arm_refs = files(directory)
            result = blobs[arm_refs["result.json"]]["content"] if "result.json" in arm_refs else {}
            arm_calls = []
            for name, request_ref in arm_refs.items():
                if not name.endswith("-request.json") or name.endswith("-canonical-request.json"):
                    continue
                stage = name.removesuffix("-request.json")
                response_ref = arm_refs.get(stage + "-response.json")
                response = blobs[response_ref]["content"] if response_ref else {}
                usage = response.get("usage", {})
                call_id = "call:" + digest(
                    {
                        "checkpoint": checkpoint_id,
                        "arm": arm_id,
                        "stage": stage,
                        "request": request_ref,
                        "response": response_ref,
                    }
                )
                call = {
                    "id": call_id,
                    "checkpoint_id": checkpoint_id,
                    "arm_id": arm_id,
                    "stage": stage,
                    "accounting_scope": "inherited_decisions"
                    if judge_only and stage.startswith("decisions")
                    else "experiment",
                    "request_ref": request_ref,
                    "response_ref": response_ref,
                    "observed_in": [f"arms/{arm_id}/{checkpoint_id}"],
                    "usage": usage,
                    "provider_response_id": response.get("id"),
                    "served_model": response.get("model"),
                    "status": "response_saved" if response_ref else "response_not_saved",
                    "cost_usd": usage.get("cost"),
                    "latency_seconds": None,
                    "latency_status": "not_instrumented",
                    "transport_attempt_count": None,
                }
                calls.append(call)
                arm_calls.append(call_id)
            arms[arm_id] = {
                "decision_agent_output": decision_output(
                    {name: blobs[ref]["content"] for name, ref in arm_refs.items()}
                ),
                "id": arm_id,
                "artifacts": arm_refs,
                "call_ids": arm_calls,
                "status": result.get("status", "incomplete"),
                "decision_available": "decisions.json" in arm_refs,
                "judge_available": "judge.json" in arm_refs,
                "evidence_ref": packet_ref,
                "latency": {
                    "checkpoint_seconds": result.get("latency_seconds"),
                    "phases": result.get("timings", {}),
                    "scope": "Arm execution and measured structured-call phases; phases include any bounded repair and local processing, not isolated HTTP latency",
                },
                "assessment_kind": "model_assisted_semantic_judge",
                "dimensions": ["historical_agreement", "evidence_support", "target_predictability"],
            }
        checkpoints.append(
            {
                "id": checkpoint_id,
                "case_id": prior["case_id"],
                "cutoff": prior["cutoff"],
                "prefix_sha256": prior["prefix_sha256"],
                "artifacts": refs,
                "baseline_artifacts": original_refs,
                "baseline_interrupted_artifacts": prior["interrupted_artifacts"],
                "historical_target": {
                    "artifact_ref": target_ref,
                    "evaluation_only": True,
                    "status": "available" if target_ref else "missing",
                    "semantics": "Soft annotation of observed behavior, not unique gold truth",
                },
                "arms": arms,
            }
        )
    contrasts = []
    for directory in sorted((root / "contrast").glob("*")):
        if not directory.is_dir():
            continue
        contrast_refs = files(directory)
        contrast_calls = []
        for name, request_ref in contrast_refs.items():
            if not name.endswith("-request.json") or name.endswith("-canonical-request.json"):
                continue
            stage = name.removesuffix("-request.json")
            response_ref = contrast_refs.get(stage + "-response.json")
            response = blobs[response_ref]["content"] if response_ref else {}
            usage = response.get("usage", {})
            call_id = "call:" + digest(
                {
                    "contrast": directory.name,
                    "stage": stage,
                    "request": request_ref,
                    "response": response_ref,
                }
            )
            calls.append(
                {
                    "id": call_id,
                    "checkpoint_id": directory.name,
                    "arm_id": None,
                    "stage": stage,
                    "accounting_scope": "contrast",
                    "request_ref": request_ref,
                    "response_ref": response_ref,
                    "observed_in": ["contrast/" + directory.name],
                    "usage": usage,
                    "provider_response_id": response.get("id"),
                    "served_model": response.get("model"),
                    "status": "response_saved" if response_ref else "response_not_saved",
                    "cost_usd": usage.get("cost"),
                    "latency_seconds": None,
                    "latency_status": "not_instrumented",
                    "transport_attempt_count": None,
                }
            )
            contrast_calls.append(call_id)
        contrasts.append(
            {
                "id": directory.name,
                "artifacts": contrast_refs,
                "call_ids": contrast_calls,
                "included_in_primary_denominator": False,
                "semantics": "Separate diagnostic contrast; no historical target or semantic judge required",
            }
        )
    document = {
        "format_version": VERSION,
        "run_id": root.name,
        "baseline": {
            "run_id": baseline["run_id"],
            "content_sha256": baseline["content_sha256"],
            "root_artifacts": baseline["root_artifacts"],
        },
        "root_artifacts": root_refs,
        "prompt_artifacts": prompt_refs,
        "arm_ids": arm_ids,
        "ontology": {
            "tbox_ref": root_refs.get("tbox.json"),
            "response_schema_ref": root_refs.get("response-schema.json"),
        },
        "benchmark_context": {
            "artifact_ref": root_refs.get("benchmark-context.json"),
            "semantics": "Explicit benchmark assumptions, distinct from extracted case evidence and model-authored assumptions",
        },
        "checkpoints": checkpoints,
        "contrasts": contrasts,
        "calls": calls,
        "accounting": accounting(calls),
        "accounting_by_scope": {
            scope: accounting([c for c in calls if c["accounting_scope"] == scope])
            for scope in ("inherited_baseline", "inherited_decisions", "experiment", "contrast")
        },
        "completion": {
            "expected_checkpoints": len(jobs),
            "expected_arm_results": len(jobs) * len(arm_ids),
            "decisions_available": sum(
                a["decision_available"] for c in checkpoints for a in c["arms"].values()
            ),
            "judge_assessments_available": sum(
                a["judge_available"] for c in checkpoints for a in c["arms"].values()
            ),
        },
        "interpretation": {
            **baseline["interpretation"],
            "judge": "Model-assisted semantic assessment is separate from deterministic validation and manual review.",
            "targets": "Historical choices are soft targets; predictability and evidence support must be judged separately from agreement.",
            "submission": "Explicit arm selection required; never export targets or judge rationale as agent answers.",
        },
        "run_wall_clock": {
            "seconds": None,
            "status": "not_instrumented",
            "note": "Arm durations overlap and do not establish whole-run wall time.",
        },
        "blobs": dict(sorted(blobs.items())),
    }
    summary_ref = root_refs.get("summary.json")
    summary = blobs[summary_ref]["content"] if summary_ref else {}
    if isinstance(summary.get("wall_clock_seconds"), (int, float)):
        document["run_wall_clock"] = {
            "seconds": summary["wall_clock_seconds"],
            "status": "measured",
            "scope": summary.get(
                "wall_clock_scope", "Producer-defined run interval; inspect summary"
            ),
        }
    document["content_sha256"] = digest(document)
    issues = validate_experiment(document)
    if issues:
        raise ValueError("Invalid experiment artifact: " + "; ".join(issues))
    return document


def validate_experiment(document):
    issues = []
    if document.get("format_version") != VERSION:
        issues.append("Unsupported experiment format")
    if digest({k: v for k, v in document.items() if k != "content_sha256"}) != document.get(
        "content_sha256"
    ):
        issues.append("Document content hash mismatch")
    blobs = document["blobs"]
    for ref, blob in blobs.items():
        if ref != "sha256:" + digest(blob):
            issues.append("Blob hash mismatch: " + ref)
    refs = list(document["root_artifacts"].values()) + list(
        document["baseline"]["root_artifacts"].values()
    )
    refs.extend(document["prompt_artifacts"].values())
    calls = {c["id"]: c for c in document["calls"]}
    checkpoint_ids = [c["id"] for c in document["checkpoints"]]
    contrast_ids = [c["id"] for c in document.get("contrasts", [])]
    frozen_requests = {}
    experiment_ref = document["root_artifacts"].get("experiment.json")
    experiment = blobs[experiment_ref]["content"] if experiment_ref in blobs else {}
    episode_judge = experiment.get("judge_version") == "episode-judge-v1"
    selection_judge = experiment.get("judge_version") in {
        "soft-judge-v2",
        "soft-judge-v3",
        "episode-judge-v1",
    }
    contextual = experiment.get("mode") == "contextual_baseline"
    role_extraction = experiment.get("mode") == "role_extraction"
    context_ref = document["root_artifacts"].get("benchmark-context.json")
    benchmark_contexts = (
        blobs[context_ref]["content"].get("cases", {}) if context_ref in blobs else {}
    )
    corpus_ref = document["root_artifacts"].get("corpus-index.json")
    corpus_entries = (
        {entry["id"]: entry for entry in blobs[corpus_ref]["content"].get("entries", [])}
        if corpus_ref in blobs
        else {}
    )
    if len(calls) != len(document["calls"]) or len(checkpoint_ids) != len(set(checkpoint_ids)):
        issues.append("Duplicate call or checkpoint ID")
    for checkpoint in document["checkpoints"]:
        if role_extraction:
            new_ref = checkpoint["artifacts"].get("evidence-packet.json")
            prior_ref = checkpoint["baseline_artifacts"].get("evidence-packet.json")
            if new_ref in blobs and prior_ref in blobs:
                new_packet, old_packet = blobs[new_ref]["content"], blobs[prior_ref]["content"]
                if new_packet.get("prefix_sha256") != checkpoint["prefix_sha256"] or new_packet.get(
                    "sources"
                ) != old_packet.get("sources"):
                    issues.append("Role extraction changed frozen prefix/source units")
            if document["benchmark_context"]["artifact_ref"] is not None:
                issues.append("Role extraction includes benchmark assumptions")
        for key in ("artifacts", "baseline_artifacts", "baseline_interrupted_artifacts"):
            refs.extend(checkpoint[key].values())
        target = checkpoint["historical_target"]
        if target["artifact_ref"]:
            refs.append(target["artifact_ref"])
        if not target["evaluation_only"]:
            issues.append("Historical target must be evaluation-only")
        if sorted(checkpoint["arms"]) != document["arm_ids"]:
            issues.append("Arm denominator differs from declaration")
        for arm_id, arm in checkpoint["arms"].items():
            refs.extend(arm["artifacts"].values())
            if arm["evidence_ref"] is not None:
                refs.append(arm["evidence_ref"])
            if arm["evidence_ref"] != checkpoint["artifacts"].get("evidence-packet.json"):
                issues.append("Arm changed shared evidence")
            if arm["decision_available"] and arm["evidence_ref"] is None:
                issues.append("Decision has no extracted evidence packet")
            for call_id in arm["call_ids"]:
                call = calls.get(call_id)
                if (
                    not call
                    or call["checkpoint_id"] != checkpoint["id"]
                    or call["arm_id"] != arm_id
                ):
                    issues.append("Invalid arm call reference")
            if (
                all(ref in blobs for ref in arm["artifacts"].values())
                and arm["evidence_ref"] in blobs
            ):
                files = {name: blobs[ref]["content"] for name, ref in arm["artifacts"].items()}
                if "decision_agent_output" in arm and arm[
                    "decision_agent_output"
                ] != decision_output(files):
                    issues.append("Decision agent output differs from saved arm artifacts")
                frozen_prediction = (
                    corpus_entries.get(checkpoint["id"], {})
                    .get("arms", {})
                    .get(arm_id, {})
                    .get("frozen_prediction_sha256")
                )
                if frozen_prediction and "decisions.json" in files:
                    actual_digest = hashlib.sha256(
                        json.dumps(
                            files["decisions.json"], sort_keys=True, ensure_ascii=False
                        ).encode()
                    ).hexdigest()
                    if frozen_prediction != actual_digest:
                        issues.append("Judge-only rerun changed frozen prediction")
                packet = blobs[arm["evidence_ref"]]["content"]
                tbox_ref = document["ontology"]["tbox_ref"]
                tbox = blobs[tbox_ref]["content"] if tbox_ref in blobs else None
                expected_decision = {"ontology_tbox": tbox, "prefix_evidence": packet}
                if contextual:
                    if checkpoint["id"] not in benchmark_contexts:
                        issues.append("Missing checkpoint benchmark context")
                    expected_decision["benchmark_context"] = benchmark_contexts.get(
                        checkpoint["id"]
                    )
                if "decisions-request.json" in files:
                    from .run_artifact import validate_model_view_artifacts

                    issues.extend(
                        validate_model_view_artifacts(
                            {"sources.json": {"sources": packet["sources"]}, **files}
                        )
                    )
                    request = files.get(
                        "decisions-canonical-request.json", files["decisions-request.json"]
                    )
                    if user_payload(request) != expected_decision:
                        issues.append("Decision input differs from frozen prefix and Tboxes")
                    prompt_ref = document["prompt_artifacts"].get(arm_id)
                    if (
                        prompt_ref not in blobs
                        or request["messages"][0].get("content") != blobs[prompt_ref]["content"]
                    ):
                        issues.append("Decision prompt differs from declared arm")
                if "judge-request.json" in files:
                    prediction = files.get("decisions.json")
                    target_ref = checkpoint["historical_target"]["artifact_ref"]
                    historical_target = (
                        blobs[target_ref]["content"] if target_ref in blobs else None
                    )
                    expected_judge = {
                        "ontology_tbox": tbox,
                        "prefix_evidence": packet,
                        "historical_target": historical_target,
                        "prediction": prediction,
                        "prediction_source": {
                            "id": "prediction",
                            "text": json.dumps(prediction, ensure_ascii=False, sort_keys=True),
                        },
                    }
                    if contextual:
                        expected_judge["benchmark_context"] = benchmark_contexts.get(
                            checkpoint["id"]
                        )
                    if selection_judge:
                        catalog = files.get("citation-catalog.json", {})
                        expected_judge["citation_catalog"] = catalog.get("spans")
                        issues.extend(validate_citation_catalog(catalog))
                        expected_sources = {
                            ("prefix", s["id"]): s["text"] for s in packet.get("sources", [])
                        }
                        if historical_target:
                            source = historical_target["source"]
                            expected_sources[("target", source["id"])] = source["text"]
                        expected_sources[("prediction", "prediction")] = expected_judge[
                            "prediction_source"
                        ]["text"]
                        actual_sources = {
                            (s["origin"], s["id"]): s["text"] for s in catalog.get("sources", [])
                        }
                        if actual_sources != expected_sources:
                            issues.append("Citation catalog differs from saved sources")
                        issues.extend(validate_materialization(files, catalog))
                        schema_ref = document["root_artifacts"].get("judge-schema.json")
                        if schema_ref in blobs:
                            expected_schema = copy.deepcopy(blobs[schema_ref]["content"])
                            try:
                                for definition, origin in (
                                    ("SpanSelection", None),
                                    ("PrefixSpanSelection", "prefix"),
                                ):
                                    expected_schema["$defs"][definition]["properties"]["span_id"][
                                        "enum"
                                    ] = [
                                        span["id"]
                                        for span in catalog.get("spans", [])
                                        if origin is None or span["origin"] == origin
                                    ]
                                if episode_judge:
                                    specialize_episode_schema(
                                        expected_schema, historical_target, prediction
                                    )
                                actual_schema = files["judge-request.json"]["response_format"][
                                    "json_schema"
                                ]["schema"]
                                if actual_schema != expected_schema:
                                    issues.append(
                                        "Judge selection schema differs from frozen schema/catalog"
                                    )
                            except KeyError:
                                issues.append(
                                    "Judge selection schema lacks declared span selectors"
                                )
                        else:
                            issues.append("Missing generic judge selection schema")
                    if user_payload(files["judge-request.json"]) != expected_judge:
                        issues.append("Judge input differs from saved prefix/target/prediction")
                    judge_prompt_ref = document["root_artifacts"].get("judge-prompt.txt")
                    if (
                        judge_prompt_ref not in blobs
                        or files["judge-request.json"]["messages"][0].get("content")
                        != blobs[judge_prompt_ref]["content"]
                    ):
                        issues.append("Judge prompt differs from frozen rubric")
                for stage in ("decisions", "judge"):
                    request = files.get(
                        stage + "-canonical-request.json", files.get(stage + "-request.json")
                    )
                    if request:
                        fixed = copy.deepcopy(
                            {
                                key: value
                                for key, value in request.items()
                                if key not in {"messages", "session_id", "prompt_cache_key"}
                            }
                        )
                        if stage == "judge" and selection_judge:
                            catalog_ids = {
                                span["id"]
                                for span in files.get("citation-catalog.json", {}).get("spans", [])
                            }
                            normalize_catalog_enums(fixed, catalog_ids)
                            if episode_judge:
                                schema_ref = document["root_artifacts"].get("judge-schema.json")
                                if schema_ref in blobs:
                                    fixed["response_format"]["json_schema"]["schema"] = blobs[
                                        schema_ref
                                    ]["content"]
                        if stage in frozen_requests and fixed != frozen_requests[stage]:
                            issues.append("Model/schema/settings differ across experiment arms")
                        frozen_requests[stage] = fixed
    for call in calls.values():
        refs.append(call["request_ref"])
        if call["response_ref"]:
            refs.append(call["response_ref"])
            blob = blobs.get(call["response_ref"])
            if blob:
                usage = blob["content"].get("usage", {})
                if call["usage"] != usage or call["cost_usd"] != usage.get("cost"):
                    issues.append("Call usage differs from provider response")
        if call["checkpoint_id"] not in checkpoint_ids + contrast_ids:
            issues.append("Unknown call checkpoint")
    for contrast in document.get("contrasts", []):
        refs.extend(contrast["artifacts"].values())
        if contrast["included_in_primary_denominator"]:
            issues.append("Contrast incorrectly included in primary denominator")
        for call_id in contrast["call_ids"]:
            if (
                call_id not in calls
                or calls[call_id]["accounting_scope"] != "contrast"
                or calls[call_id]["checkpoint_id"] != contrast["id"]
            ):
                issues.append("Invalid contrast call reference")
        if all(ref in blobs for ref in contrast["artifacts"].values()):
            files = {name: blobs[ref]["content"] for name, ref in contrast["artifacts"].items()}
            if "decisions-request.json" in files:
                tbox_ref = document["ontology"]["tbox_ref"]
                tbox = blobs[tbox_ref]["content"] if tbox_ref in blobs else None
                expected = {
                    "ontology_tbox": tbox,
                    "prefix_evidence": files.get("evidence-packet.json"),
                }
                if user_payload(files["decisions-request.json"]) != expected:
                    issues.append("Contrast decision input differs from its prefix/Tboxes")
    if any(ref not in blobs for ref in refs):
        issues.append("Dangling blob reference")
    if document["accounting"] != accounting(document["calls"]):
        issues.append("Accounting mismatch")
    for scope, totals in document["accounting_by_scope"].items():
        if totals != accounting([c for c in document["calls"] if c["accounting_scope"] == scope]):
            issues.append("Scope accounting mismatch")
    completion = document["completion"]
    if completion["expected_checkpoints"] != len(checkpoint_ids) or completion[
        "expected_arm_results"
    ] != len(checkpoint_ids) * len(document["arm_ids"]):
        issues.append("Denominator mismatch")
    manifest_ref = document["root_artifacts"].get("manifest.json")
    if manifest_ref in blobs and sorted(
        row["id"] for row in blobs[manifest_ref]["content"]["jobs"]
    ) != sorted(checkpoint_ids):
        issues.append("Checkpoint inventory differs from manifest")
    available_decisions = sum(
        "decisions.json" in arm["artifacts"]
        for c in document["checkpoints"]
        for arm in c["arms"].values()
    )
    available_judgments = sum(
        "judge.json" in arm["artifacts"]
        for c in document["checkpoints"]
        for arm in c["arms"].values()
    )
    if (
        available_decisions != completion["decisions_available"]
        or available_judgments != completion["judge_assessments_available"]
    ):
        issues.append("Availability counts mismatch")
    return issues


def validate_citation_catalog(catalog):
    """Spans are a deterministic source projection, never model-authored quotations."""
    issues = []
    sources = {(row["origin"], row["id"]): row["text"] for row in catalog.get("sources", [])}
    ids = []
    for span in catalog.get("spans", []):
        ids.append(span["id"])
        source = sources.get((span["origin"], span["source_id"]))
        start, end = span["start"], span["end"]
        if (
            source is None
            or not isinstance(start, int)
            or not isinstance(end, int)
            or not 0 <= start < end <= len(source)
        ):
            issues.append("Invalid citation catalog source/range")
        elif source[start:end] != span["expression"]:
            issues.append("Citation catalog expression differs from source slice")
        elif source[:start].count(span["expression"]) + 1 != span["occurrence"]:
            issues.append("Citation catalog occurrence differs from source position")
    if len(ids) != len(set(ids)):
        issues.append("Duplicate citation catalog span ID")
    return issues


def validate_materialization(files, catalog):
    """Verify the visible judgment is exactly the host projection of selected IDs."""
    if "judge-selections.json" not in files:
        return [] if "judge.json" not in files else ["Missing raw judge selections"]
    spans = {span["id"]: span for span in catalog.get("spans", [])}
    selected = []
    issues = []

    def walk(value, path=""):
        if isinstance(value, dict):
            if set(value) == {"span_id"}:
                span = spans.get(value["span_id"])
                if span is None:
                    issues.append("Unknown selected citation span")
                    return None
                if (
                    any(
                        part in path
                        for part in ("/support_citations/", "/predictability_citations/")
                    )
                    and span["origin"] != "prefix"
                ):
                    issues.append("Evidence support citation uses a non-prefix source")
                selected.append({"judgment_path": path, **span})
                return {
                    key: span[key] for key in ("origin", "source_id", "expression", "occurrence")
                }
            return {key: walk(child, path + "/" + key) for key, child in value.items()}
        if isinstance(value, list):
            return [walk(child, path + "/" + str(index)) for index, child in enumerate(value)]
        return value

    materialized = walk(files["judge-selections.json"])
    if "judge.json" in files and materialized != files["judge.json"]:
        issues.append("Visible judgment differs from selected-span materialization")
    if "judge-spans.json" in files and selected != files["judge-spans.json"]:
        issues.append("Visible judge spans differ from selected-span materialization")
    return issues


def specialize_episode_schema(schema, target, prediction):
    """Apply only declared case-local action IDs/cardinalities to the frozen schema."""
    target_ids = [action["id"] for action in target["episode"]["actions"]]
    prediction_ids = [action["id"] for action in prediction["actions"]]
    order_ids = [order["id"] for order in target["necessary_order"]]
    definitions = schema["$defs"]
    for definition, field, ids in (
        ("TargetAssessment", "target_action_id", target_ids),
        ("PredictionAssessment", "prediction_action_id", prediction_ids),
        ("OrderAssessment", "order_id", order_ids),
    ):
        if ids:
            definitions[definition]["properties"][field]["enum"] = ids
    mapping = definitions["TargetAssessment"]["properties"]["prediction_action_ids"]
    if prediction_ids:
        mapping["items"]["enum"] = prediction_ids
    else:
        mapping["maxItems"] = 0
    for field, ids in (
        ("target_assessments", target_ids),
        ("prediction_assessments", prediction_ids),
        ("necessary_order_assessments", order_ids),
    ):
        schema["properties"][field]["minItems"] = len(ids)
        schema["properties"][field]["maxItems"] = len(ids)


def normalize_catalog_enums(value, catalog_ids):
    """Remove only case-local catalog ID choices when comparing fixed request schemas."""
    if isinstance(value, dict):
        enum = value.get("enum")
        if (
            isinstance(enum, list)
            and enum
            and all(isinstance(v, str) and v in catalog_ids for v in enum)
        ):
            value["enum"] = ["<case-local-citation-span>"]
        for child in value.values():
            normalize_catalog_enums(child, catalog_ids)
    elif isinstance(value, list):
        for child in value:
            normalize_catalog_enums(child, catalog_ids)


def user_payload(request):
    users = [m for m in request.get("messages", []) if m.get("role") == "user"]
    try:
        return json.loads(users[0]["content"]) if len(users) == 1 else None
    except (ValueError, TypeError, KeyError):
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    document = assemble_experiment(args.run, read_json(args.baseline))
    output = args.output or args.run / "run.json"
    if output.resolve() == args.baseline.resolve():
        raise ValueError("Experiment output must not overwrite its baseline")
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(output)
    print(
        json.dumps(
            {
                "path": str(output),
                "content_sha256": document["content_sha256"],
                "completion": document["completion"],
                "accounting_by_scope": document["accounting_by_scope"],
            }
        )
    )


if __name__ == "__main__":
    main()
