"""Offline, audited citation-interface canonicalization; never edits choice values."""

import argparse
import json
from copy import deepcopy
from pathlib import Path

from .canonicalization import align_references
from .cli import write_json
from .response import DecisionResponse, validate_response


def align_decision(data, units):
    trace, issues = [], []

    def walk(value, path="response"):
        if isinstance(value, dict):
            return {key: walk(child, f"{path}.{key}") for key, child in value.items()}
        if isinstance(value, list):
            result = []
            for index, child in enumerate(value):
                location = f"{path}[{index}]"
                if (
                    isinstance(child, dict)
                    and {"source_id", "expression", "occurrence"} <= child.keys()
                ):
                    try:
                        aligned, change = align_references(child, units)
                        result.extend(aligned)
                        if change:
                            trace.append({"path": location, **change})
                    except ValueError as error:
                        result.append(child)
                        issues.append({"path": location, "code": str(error), "original": child})
                else:
                    result.append(walk(child, location))
            return result
        return value

    return {
        "response": walk(deepcopy(data)),
        "canonicalization": trace,
        "unresolved_citations": issues,
        "meaning": "Citation text/offset interface only; no action, rationale assertion, entity ID or confidence rewritten",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    index = json.loads((args.run / "corpus-index.json").read_text())
    if any(e["status"] == "pending" for e in index["entries"]):
        raise ValueError("Wait until the baseline run finishes before updating its index")
    reviews = []
    for entry in index["entries"]:
        directory = args.run / entry["path"]
        review = json.loads((directory / "decision-review.json").read_text())
        response_path = directory / "decisions.json"
        if response_path.exists():
            original_path = directory / "decisions-raw-parsed.json"
            if original_path.exists():
                raise ValueError(
                    "Citation canonicalization already applied; refusing to erase history"
                )
            original = json.loads(response_path.read_text())
            write_json(original_path, original)
            packet = json.loads((directory / "evidence-packet.json").read_text())
            canonical = align_decision(original, packet["sources"])
            response = DecisionResponse.model_validate(canonical["response"])
            checks = validate_response(response, packet)
            write_json(directory / "decisions-canonicalization.json", canonical)
            write_json(response_path, response.model_dump())
            write_json(directory / "decisions-validation.json", checks)
            review["response"] = response.model_dump()
            review["checks"] = checks
            review["citation_canonicalization"] = {
                "changes": len(canonical["canonicalization"]),
                "unresolved": canonical["unresolved_citations"],
            }
            write_json(directory / "decision-review.json", review)
            result_path = directory / "result.json"
            result = json.loads(result_path.read_text())
            result["checks"] = checks
            result["citation_canonicalization"] = review["citation_canonicalization"]
            write_json(result_path, result)
            entry["checks"] = checks
        reviews.append(review)
    write_json(args.run / "corpus-index.json", index)
    summary = json.loads((args.run / "summary.json").read_text())
    summary["results"] = reviews
    summary["citation_alignment"] = (
        "Audited deterministic interface normalization after generation; original parsed/raw responses retained"
    )
    write_json(args.run / "summary.json", summary)


if __name__ == "__main__":
    main()
