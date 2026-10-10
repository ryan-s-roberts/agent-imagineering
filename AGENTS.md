# Run artifacts and evaluation

Read [the canonical run artifact contract](docs/run-artifact-format.md) before
assembling, rendering, exporting or judging a run. `run.json` is the self-contained
source of truth; adjacent HTML and `ANSWERS/<case>/ANSWER.md` + `REASONING.md`
are deterministic projections of it.

For controlled prompt arms and model-assisted semantic judging, also read
[the semantic comparison contract](docs/semantic-experiment-artifact.md).
Keep historical agreement, evidence support and target predictability separate.
Multi-arm submission exports must explicitly identify the selected arm.

Current role-identity experiments require the model to extract and link role
parties from the case prefix. Do not manufacture person/role entities or inject
contextual-addressability assumptions in the host. The proposed contextual
baseline was superseded before execution; see the role-extraction section of the
semantic comparison contract.

Never put evaluation-only future observations in model input or submission answers.
Keep structural validity, citation grounding, semantic support and historical
correspondence separate. Preserve unknown cost and latency as unknown, not zero.
Do not rewrite generated decisions to make a submission appear more correct.

Attachment evidence availability, extraction and provenance: [docs/attachment-extraction.md](docs/attachment-extraction.md).
