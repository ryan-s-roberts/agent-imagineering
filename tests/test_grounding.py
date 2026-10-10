import pytest

from property_eval.grounding import link_entities, resolve_mentions, resolve_span
from property_eval.models import LinkExtraction, MentionExtraction


def units():
    return [
        {
            "id": "001:L5",
            "event_id": "001",
            "text": "Jo said Jo’s pump failed. Jo confirmed.",
            "start": 70,
        }
    ]


def test_occurrences_and_auditable_apostrophe_alignment():
    span = resolve_span({"source_id": "001:L5", "expression": "Jo", "occurrence": 3}, units())
    assert span["start"] == 96
    aligned = resolve_span({"source_id": "001:L5", "expression": "Jo's", "occurrence": 1}, units())
    assert aligned["source_expression"] == "Jo’s"
    assert aligned["expression"] == "Jo's"
    assert aligned["alignment"] == "apostrophe_alignment"
    with pytest.raises(ValueError):
        resolve_span({"source_id": "001:L5", "expression": "Joe", "occurrence": 1}, units())


def test_mentions_stable_but_names_never_implicitly_merge():
    extracted = MentionExtraction.model_validate(
        {
            "mentions": [
                {"source_id": "001:L5", "expression": "Jo", "occurrence": i, "kind": "person"}
                for i in (1, 3)
            ]
        }
    )
    resolved = resolve_mentions(extracted, units(), "case-x")
    assert resolved["valid"]
    entities, checks = link_entities(LinkExtraction(links=[]), resolved["mentions"], units())
    assert checks["valid"] and len(entities.entities) == 2
    assert resolve_mentions(extracted, units(), "case-x") == resolved


def test_link_conflict_is_rejected():
    extracted = MentionExtraction.model_validate(
        {
            "mentions": [
                {"source_id": "001:L5", "expression": "Jo", "occurrence": i, "kind": "person"}
                for i in (1, 3)
            ]
        }
    )
    mentions = resolve_mentions(extracted, units(), "case-x")["mentions"]
    link = {
        "left_mention_id": mentions[0]["id"],
        "right_mention_id": mentions[1]["id"],
        "evidence": [{"source_id": "001:L5", "expression": "Jo confirmed.", "occurrence": 1}],
    }
    _, checks = link_entities(
        LinkExtraction.model_validate(
            {"links": [{**link, "relationship": r} for r in ("same", "different")]}
        ),
        mentions,
        units(),
    )
    assert not checks["valid"]


def test_role_party_links_require_explicit_model_identity_assertion():
    source = [{"id": "e1:L1", "event_id": "e1", "text": "Landlord Mara agreed.", "start": 0}]
    extraction = MentionExtraction.model_validate(
        {
            "mentions": [
                {
                    "source_id": "e1:L1",
                    "expression": "Landlord",
                    "occurrence": 1,
                    "kind": "role_party",
                },
                {"source_id": "e1:L1", "expression": "Mara", "occurrence": 1, "kind": "person"},
            ]
        }
    )
    mentions = resolve_mentions(extraction, source, "invented")["mentions"]
    separate, checks = link_entities(LinkExtraction(links=[]), mentions, source)
    assert checks["valid"] and len(separate.entities) == 2
    linked, checks = link_entities(
        LinkExtraction.model_validate(
            {
                "links": [
                    {
                        "left_mention_id": mentions[0]["id"],
                        "right_mention_id": mentions[1]["id"],
                        "relationship": "same",
                        "evidence": [
                            {"source_id": "e1:L1", "expression": "Landlord Mara", "occurrence": 1}
                        ],
                    }
                ]
            }
        ),
        mentions,
        source,
    )
    assert checks["valid"] and len(linked.entities) == 1
    assert linked.entities[0].kind == "person"
    assert linked.entities[0].label == "Mara"
