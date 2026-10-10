"""Static types; dynamically constrained instance IDs; strict OpenRouter transport."""

import asyncio
import json

import httpx

from .models import LinkExtraction, MentionExtraction, RecordExtraction
from .prompt import EXAMPLES, LINK_SYSTEM, MENTION_SYSTEM, RECORD_SYSTEM
from .validation import RANGES


def constrain_schema(schema, units, entities=None):
    source_ids = [u["id"] for u in units]

    def visit(node, field=None):
        if not isinstance(node, dict):
            return
        if node.get("type") == "string":
            if field in {"source_id", "source_ids"}:
                node["enum"] = source_ids
            elif (
                entities is not None
                and field
                and (field in RANGES or field in {"left_id", "right_id", "entity_ids"})
            ):
                allowed = [
                    e.id
                    for e in entities.entities
                    if field not in RANGES or e.kind in RANGES[field]
                ]
                if allowed:
                    node["enum"] = allowed
                else:
                    node["description"] = (
                        "No suitable entity exists; emit a gap instead of this record"
                    )
        for key, value in node.items():
            if key == "properties":
                for name, child in value.items():
                    visit(child, name)
            elif isinstance(value, dict):
                visit(value, field)
            elif isinstance(value, list):
                for child in value:
                    visit(child, field)

    visit(schema)
    return schema


def request_body(prefix, units, model, max_tokens, entities=None, *, mentions=None, few_shot=False):
    response_type = (
        RecordExtraction
        if entities is not None
        else LinkExtraction
        if mentions is not None
        else MentionExtraction
    )
    stage = "records" if entities is not None else "links" if mentions is not None else "mentions"
    system = {"records": RECORD_SYSTEM, "links": LINK_SYSTEM, "mentions": MENTION_SYSTEM}[stage]
    schema = constrain_schema(response_type.model_json_schema(), units, entities)
    payload = {"case_id": prefix.case_id, "cutoff": prefix.cutoff, "sources": units}
    if entities is not None:
        payload["entities"] = entities.model_dump()["entities"]
    if mentions is not None:
        payload["mentions"] = mentions
        if entities is None and mentions:
            for field in ("left_mention_id", "right_mention_id"):
                schema["$defs"]["IdentityLink"]["properties"][field]["enum"] = [
                    m["id"] for m in mentions
                ]
    return {
        "model": model,
        **({} if model == "openai/gpt-6-luna" else {"temperature": 0}),
        "max_tokens": max_tokens,
        "provider": {"require_parameters": True},
        "messages": [
            {"role": "system", "content": system + (EXAMPLES if few_shot else "")},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": stage,
                "strict": True,
                "schema": schema,
            },
        },
    }


async def complete(client: httpx.AsyncClient, key: str, body: dict) -> dict:
    for attempt in range(3):
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}"},
                json=body,
            )
        except httpx.TransportError:
            if attempt == 2:
                raise
        else:
            if response.status_code not in {429, 500, 502, 503, 504} or attempt == 2:
                response.raise_for_status()
                return response.json()
        await asyncio.sleep(2**attempt)
    raise RuntimeError("Unreachable retry state")


def parse_response(response: dict, response_type):
    choice = response["choices"][0]
    if choice.get("finish_reason") != "stop":
        raise ValueError(f"Incomplete response: {choice.get('finish_reason')}")
    content = choice["message"].get("content")
    if not isinstance(content, str):
        raise TypeError("Missing textual structured output")
    return response_type.model_validate(json.loads(content))
