"""Model-only mention recall audit; no host role synthesis."""

import json

from .client import request_body
from .prompt import MENTION_SYSTEM

COVERAGE_SYSTEM = """Review a preliminary mention inventory against every supplied source unit.
Return the complete corrected mention inventory, retaining valid mentions and adding omitted
mentions with literal source expressions and occurrence selectors. This is mention detection,
not entity linking or action prediction. Sources, not the preliminary inventory, are authoritative.

Inspect participants in message headers, narrative, quoted messages, instructions, status and
workflow notes. Role descriptions denote case-scoped role_party identities even without names:
agent/agency, landlord, tenant and a contextually identified contractor. A role inside a requested
future action still denotes its participant; mentioning approval does not establish approval.
Missing contact details do not erase a source-described role. Generic unknown people remain
unresolved_party where their referent is unclear. Never add a party absent from the source.
Check each source unit independently so short trailing instructions are not missed after long text.
Do not invent property or request expressions; retain exact source words and their real kind.

Independent invented mechanics examples:
- 'Ask the caretaker to unlock the gate.' includes caretaker as role_party; unlocking is not completed.
- Header 'From: Agent' and body 'the occupier called' contain two source-described role parties.
- 'Supplier approval pending' includes Supplier as role_party; no supplier name is required.
- 'Someone should inspect it' contains unresolved_party someone, not an invented contractor.
These examples teach extraction mechanics only. Output the required mention schema, no commentary.
"""


def coverage_request(prefix, units, candidates, model, max_tokens):
    body = request_body(prefix, units, model, max_tokens)
    payload = json.loads(body["messages"][1]["content"])
    payload["preliminary_mentions"] = candidates.model_dump()["mentions"]
    body["messages"][0]["content"] = MENTION_SYSTEM + "\n\n" + COVERAGE_SYSTEM
    body["messages"][1]["content"] = json.dumps(payload, ensure_ascii=False)
    return body
