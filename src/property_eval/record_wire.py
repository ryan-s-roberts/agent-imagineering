"""Remove redundant model provenance IDs; derive their exact evidence union in code."""

from copy import deepcopy

VERSION = "record-wire-v1"


def record_wire_schema(schema):
    schema = deepcopy(schema)
    provenance = schema["$defs"]["Provenance"]
    provenance["properties"].pop("source_ids", None)
    provenance["required"] = [key for key in provenance["required"] if key != "source_ids"]
    return schema


def derive_record_source_ids(output):
    """No assertions/evidence invented; empty citation union stays empty and invalid."""
    output = deepcopy(output)
    for record in output.get("records", []):
        sources = set()
        for field in record.get("field_evidence", []):
            for span in field.get("spans", []):
                if isinstance(span.get("source_id"), str):
                    sources.add(span["source_id"])
        for cause in record.get("causes", []):
            for span in cause.get("evidence", []):
                if isinstance(span.get("source_id"), str):
                    sources.add(span["source_id"])
        if isinstance(record.get("provenance"), dict):
            record["provenance"]["source_ids"] = sorted(sources)
    return output
