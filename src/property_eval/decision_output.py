"""Explicit, lossless reading surface for saved decision-agent outputs."""


def decision_output(files):
    attempts = []
    names = ["decisions-response.json", "decisions-repair-response.json"]
    names.extend(
        sorted(
            name
            for name in files
            if name.startswith("decisions-reference-repair-")
            and name.endswith("-response.json")
            and not name.endswith("-canonical-response.json")
        )
    )
    for name in names:
        if name in files:
            response = files[name]
            attempts.append(
                {
                    "artifact": name,
                    "provider_response_id": response.get("id"),
                    "messages": [choice.get("message") for choice in response.get("choices", [])],
                }
            )
    return {
        "semantics": "Recorded model proposals, not executed actions. Judge assessments are separate.",
        "available": "decisions.json" in files,
        "provider_attempts": attempts,
        "decoded_before_citation_normalization": files.get("decisions-raw-parsed.json"),
        "normalized_response": files.get("decisions.json"),
        "citation_normalization": files.get("decisions-canonicalization.json"),
        "validation": files.get("decisions-validation.json"),
        "reference_repair": files.get("decisions-resolution.json"),
        "original_response": files.get("decisions-before-reference-repair.json"),
    }
