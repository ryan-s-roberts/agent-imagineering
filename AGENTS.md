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
Evidence-to-response assessment: [rubric](docs/evidence-response-rubric-v1.md).
Use development cases only to derive general rubric changes; case-specific audit
examples stay out of decision prompts. [Late targets](docs/agent-only-late-checkpoints.md)
exclude counterparty behavior and actions requiring unavailable episode information.
Keep structural validity, citation grounding, semantic support and historical
correspondence separate. Preserve unknown cost and latency as unknown, not zero.
Do not rewrite generated decisions to make a submission appear more correct.
The default decision prompt is `experiments/prompts/decision-operational-v2.txt`.
It requests the full supported action bundle, distinguishes extraction artifacts from
operational uncertainty, and uses proportionate verification requirements. This
submission revision has not been evaluated; saved runs retain their frozen prompts
and their existing scores do not validate this revision.
Model-authored bounded reference repair: [contract](docs/decision-reference-repair.md).
Preserve original proposals and identify the accepted attempt in reports.
Divergence review and proposed rubric revision: [docs/divergence-rubric-v1.md](docs/divergence-rubric-v1.md).
Classify action importance by operational effect, never by action type alone.

Attachment evidence availability, extraction and provenance: [docs/attachment-extraction.md](docs/attachment-extraction.md).

Input contract: [docs/input-format.md](docs/input-format.md). Dataset commands take
`--input-dir` directly containing numbered case directories. The public development
copy is `data/property-management`; its provenance is adjacent. Do not inject public
annotations into an unseen run by matching numeric case IDs.
