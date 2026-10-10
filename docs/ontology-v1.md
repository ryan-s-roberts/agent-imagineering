# Implemented ontology v1

The executable contract is `src/property_eval/models.py`; the corpus evidence and fuller
candidate model are in [ontology-evidence.md](ontology-evidence.md). This v1 is deliberately a
small baseline and has known gaps measured in [results.md](results.md).

## Objects

- **Event:** sequential ID, recording timestamp, channel, sender, recipient and immutable text.
- **Entity:** local ID, kind, label, and one or more source mentions.
- **Claim:** local ID, subject, predicate, optional entity object and/or textual value,
  epistemic status, optional attribution, and source quotations.
- **Unresolved issue:** category, description, affected entities and source quotations.
- **Evidence:** event ID and verbatim quote. Offsets are derived by the validator.

Entity kinds: person, organization, role, property, asset, maintenance_request, work_order,
appointment, approval, quote, invoice, inspection, work_report, document, key.

Predicates: concerns, located_at, occupies, owns, manages, assigned_to, authorizes,
scheduled_for, reports_condition, reports_completion, requires, requests, has_status,
costs, same_as_candidate.

Statuses: reported, recorded, requested, planned, negated, uncertain. These are an initial
compressed representation: source status, polarity and modality should eventually be orthogonal.

## Meaning and boundaries

Local entity IDs are extraction identifiers, not invented CRM database IDs. A reference to an
approval can exist as a claim without establishing its authenticity or full scope. Historical
claims are not collapsed into one current status. Facts not supported by the prefix remain absent
or explicitly unresolved. Source sender labels can remain generic; a role is not automatically
a resolved person. `same_as_candidate` proposes a link and does not merge entities.

The current validator checks all graph references, exact quotes, duplicate IDs, the approval
subject domain for `authorizes`, and provider object range for `assigned_to`. It does not yet
enforce all ontology domain/range rules, infer identity, normalize money/time, or establish
semantic entailment. See the result report before consuming a graph downstream.
