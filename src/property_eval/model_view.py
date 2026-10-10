"""Invertible model-facing identity aliases; source prose is never rewritten."""

import copy
import json

from .validation import RANGES


class ModelView:
    """One global prefix map, extended between stages and shared by all batches."""

    def __init__(self, sources, *, version="model-view-v2"):
        if version not in {"model-view-v1", "model-view-v2"}:
            raise ValueError("Unsupported model view version: " + version)
        self.version = version
        self.maps = {kind: {} for kind in ("source", "mention", "entity", "record")}
        self.sources = copy.deepcopy(sources)
        self._extend("source", [source["id"] for source in sources], "s")

    def _extend(self, kind, identifiers, prefix):
        mapping = self.maps[kind]
        for identifier in sorted(set(identifiers) - mapping.keys()):
            mapping[identifier] = f"{prefix}{len(mapping) + 1}"

    def extend_mentions(self, mentions):
        self._extend("mention", [row["id"] for row in mentions], "m")

    def extend_entities(self, entities):
        self._extend("entity", [row["id"] for row in entities], "e")

    def extend_records(self, records):
        self._extend("record", [row["id"] for row in records], "r")

    @staticmethod
    def _kind(field, version="model-view-v2"):
        if version == "model-view-v2":
            if field in {
                "supersedes_record_id",
                "responds_to_record_id",
                "constrains_record_id",
                "previous_intervention_record_id",
                "completion_record_ids",
                "authorization_record_ids",
                "about_record_ids",
                "obligation_record_id",
            }:
                return "record"
            if field == "replaces_appointment_id":
                return "entity"
        if field in {"source_id", "source_ids", "primary_source_ids", "context_source_ids"}:
            return "source"
        if field in {"left_mention_id", "right_mention_id", "mention_id", "mention_ids"}:
            return "mention"
        if field in {
            "record_id",
            "record_ids",
            "basis_record_ids",
            "conclusion_record_ids",
            "blocked_record_ids",
            "response_record_ids",
        }:
            return "record"
        if field in RANGES or field in {"entity_id", "entity_ids", "left_id", "right_id"}:
            return "entity"
        return None

    def _rewrite(self, value, field=None, *, decode=False, collection=None):
        if isinstance(value, list):
            return [self._rewrite(v, field, decode=decode, collection=collection) for v in value]
        if isinstance(value, dict):
            result = {}
            for key, child in value.items():
                child_collection = {
                    "sources": "source",
                    "mentions": "mention",
                    "preliminary_mentions": "mention",
                    "entities": "entity",
                    "records": "record",
                }.get(key)
                child_field = key
                if key == "id" and collection:
                    child_field = collection + "_id"
                result[key] = self._rewrite(
                    child, child_field, decode=decode, collection=child_collection
                )
            return result
        kind = self._kind(field, self.version)
        if isinstance(value, str) and kind:
            mapping = self.maps[kind]
            if decode:
                mapping = {alias: original for original, alias in mapping.items()}
            return mapping.get(value, value)
        return value

    def encode_output(self, value):
        """Encode typed references in stage additions, never expressions or rationale."""
        return self._rewrite(value)

    def decode_output(self, value):
        return self._rewrite(value, decode=True)

    def _source_projection(self, sources):
        groups, group_ids, source_groups = [], {}, {}
        for source in self.sources:
            metadata = {
                key: value
                for key, value in source.items()
                if key
                not in {
                    "id",
                    "text",
                    "start",
                    "end",
                    "text_sha256",
                    "document_sha256",
                    "anchor_namespace",
                    "offset_basis",
                }
            }
            key = json.dumps(metadata, sort_keys=True, ensure_ascii=False)
            if key not in group_ids:
                group_ids[key] = f"g{len(group_ids) + 1}"
                groups.append({"id": group_ids[key], **metadata})
            source_groups[source["id"]] = group_ids[key]
        selected = {source_groups[source["id"]] for source in sources}
        rows = [
            {
                "id": self.maps["source"][source["id"]],
                "text": source["text"],
                "group_id": source_groups[source["id"]],
            }
            for source in sources
        ]
        return rows, [group for group in groups if group["id"] in selected]

    def encode_call(self, payload, schema):
        """Project source tables recursively and alias schema enums by typed field."""

        def project(value):
            if isinstance(value, list):
                return [project(v) for v in value]
            if not isinstance(value, dict):
                return value
            result = {key: project(child) for key, child in value.items()}
            sources = value.get("sources")
            if isinstance(sources, list) and all(
                isinstance(s, dict) and "text" in s for s in sources
            ):
                result["sources"], result["source_groups"] = self._source_projection(sources)
            return result

        def schema_view(node, field=None):
            if isinstance(node, list):
                return [schema_view(v, field) for v in node]
            if not isinstance(node, dict):
                return node
            result = {}
            for key, value in node.items():
                if key == "properties":
                    result[key] = {name: schema_view(child, name) for name, child in value.items()}
                elif key == "enum":
                    result[key] = self._rewrite(value, field)
                else:
                    result[key] = schema_view(value, field)
            return result

        return self._rewrite(project(payload)), schema_view(copy.deepcopy(schema))

    def encode_body(self, body, *, omit_record_source_ids=False):
        """Encode every structured message while preserving a common cached prefix."""
        result = copy.deepcopy(body)
        schema = result["response_format"]["json_schema"]["schema"]
        _, schema = self.encode_call({}, schema)
        if omit_record_source_ids:
            from .record_wire import record_wire_schema

            schema = record_wire_schema(schema)
        result["response_format"]["json_schema"]["schema"] = schema
        for message in result.get("messages", []):
            content = message.get("content")
            if not isinstance(content, str):
                continue
            try:
                payload = json.loads(content)
            except (ValueError, TypeError):
                continue
            if isinstance(payload, (dict, list)):
                compact, _ = self.encode_call(payload, {})
                message["content"] = json.dumps(compact, ensure_ascii=False)
        return result

    def alias_artifact(self):
        return {
            "version": self.version,
            "scope": "global prefix; shared across batches",
            "maps": copy.deepcopy(self.maps),
            "meaning": "Canonical identity to model alias. Prose and quoted expressions unchanged. Full source metadata retained in sources.json.",
        }
