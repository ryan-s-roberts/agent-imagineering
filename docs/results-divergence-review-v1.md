# Development response divergences

Source: `runs/late-dev-eval-v1/divergence-review-summary.json`, with per-checkpoint
reviews, literal prefix citations and resolved offsets. All 102 checkpoints were
classified. Three interface failures were repaired without changing the classifier's
labels, explanation text or row order. Original attempts remain recorded.

This is model-assisted exploratory diagnosis, not a new ground-truth score.
Categories overlap and counts below are checkpoints, not action counts.

| Category | Checkpoints |
|---|---:|
| Historical target warrant needs review | 44 |
| Workflow omission | 33 |
| Partial scope | 30 |
| Reasonable alternative | 29 |
| Unnecessary clarification | 15 |
| Communication omission | 11 |
| No material divergence | 10 |
| Equivalent effect | 9 |
| Dependency difference | 8 |
| Extraction-induced blocker | 7 |
| Boundary or annotation issue | 5 |
| Material operational omission | 4 |
| Ontology representation limit | 3 |
| Unnecessary escalation | 2 |

## Concrete distinctions

- **001-at-033:** the proposal seeks a provider report and awaits it; the historical
  target persists a hold. The reviewer also finds a hold already in the prefix.
  Distinguish business progress, a persisted workflow effect, and redundant updates.
- **002-at-034:** requesting missing invoice/photo evidence is plausible; it differs
  from moving to Result and marking complete. Whether closure requires those
  documents is a policy question the log may not answer.
- **005-at-016:** reviewing an explicit pause differs from instructing cleaning.
  The target also expands carpet scope beyond the quoted bedroom. Review authority,
  scope and prerequisite availability rather than marking escalation wrong by type.
- **017-at-002:** requesting landlord approval only partly covers asking about the
  landlord's contractor preference. This is a difference in operational information,
  not merely a different action label.
- **029-at-010:** resuming after a tenant response differs from holding for a
  contractor appointment. The log does not establish whether these share a single
  workflow state; preserve that boundary uncertainty.
- **Case 010:** sensible requests for a meter photograph cannot bind to an eligible
  request entity because extraction supplied none. Score intent and grounding
  separately from that reference failure.

## Rubric changes

Use [the revised rubric](divergence-rubric-v1.md): assess choice quality, evidence
warrant, historical effects and reference integrity separately. Classify action
importance by purpose, not type. The new reviewer labels 46 historical actions as
consequential communication and only 10 as courtesy; the previous adapter labelled
all `notify` actions auxiliary. These are review labels, not silently replaced targets.

“Supported” must distinguish useful progress from redundant or blocking proposals.
The reviewer classifies the 155 proposals as 123 advancing, 12 justified waits,
9 unnecessary blockers, 9 redundant and 2 unsupported. These labels are advisory.

The target-warrant flags are especially policy-sensitive. The reviewer sometimes
assumes stronger completion-verification prerequisites than the supplied process
defines. Do not promote those assumptions into deterministic failure criteria.
Separate already-satisfied targets and unknown prerequisites before revising scores.

## Continuity prompt experiment

Both arms generated all 102 first-pass responses before API credit interruption.
The first-pass outputs are complete and comparable descriptively:

| First-pass proposals | Control | Continuity candidate |
|---|---:|---:|
| All actions | 141 | 191 |
| Clarifications | 45 | 50 |
| Escalations | 34 | 40 |
| Waits | 19 | 38 |
| Workflow changes | 6 | 12 |

The candidate improves some individual continuity decisions, including following up
with the known provider in 001-at-038, but it does not reduce clarification or
escalation counts overall. More actions is not evidence of better decisions.
The candidate is **not promoted**.

After payment-interrupted assessment resumed, the unchanged historical rubric
completed 98 control and 97 candidate judgments. Full operational correspondence
was 2/102 and 4/102 respectively. Six judgments exceeded model context and three
failed mapping consistency; they remain unassessed. These results do not establish
a reliable prompt improvement, especially given the rubric concerns above.

No holdout was used for this diagnosis or prompt experiment. Existing scores remain
preserved; no revised headline score is claimed.
