# Case review information architecture

Audience: the project owner trying to understand what happened in a case and what the agent
understood or chose. The main task is sense-making, followed by checking the supporting source.

## Reading order

1. Case and prefix: what history is visible, what is unavailable, what stage completed.
2. What happened: readable timeline and material observations.
3. What the agent chose: real decision outputs, or an explicit absence. Demonstrations are labelled.
4. Why: supporting assertions, qualifications and original text on selection.
5. Where a human is needed: cause, requested intervention, responsibility and blocking effect.
6. Technical detail: ontology type, IDs, character offsets and diagnostics through disclosure.

Do not lead with entity counts, raw JSON, a metric dashboard or a giant warning. Keep provenance
available beside the claim, with source positions intact. Invalid extraction needs a clear
status and explanation without overwhelming the case story. Unknown is distinct from absent.

## Contemporary reference direction

[Linear's 2026 interface refresh](https://linear.app/now/behind-the-latest-design-refresh)
describes predictable headers and a calmer navigation hierarchy. Borrow that consistency and
scanability, not branding. [Linear issue views](https://linear.app/docs/creating-issues) keep the
unit of work central. [Langfuse's observation model](https://langfuse.com/docs/observability/data-model)
provides a useful precedent for selecting a step and inspecting its context. Here the central
unit is a case event or choice, with source evidence as the inspector.

Visual direction: warm neutral reading surfaces, restrained accent, thin dividers, deliberate
type hierarchy and compact navigation. Avoid repeated bordered cards, dark dashboard banners,
permanent monospace dumps, decorative charts and unlabeled schema jargon.

Acceptance: understand case status without reading JSON; select an assertion and see its
source; distinguish proposal from historical action; see why intervention is needed; reach
technical positions when needed; preserve these paths on a narrow screen and keyboard.
