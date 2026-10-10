# Case review workspace

The audience is the person trying to understand what happened in a case, what an
agent chose, why it chose it, and where a human needs to intervene. The default
Overview follows that sequence. Ontology IDs and diagnostics are secondary.

```sh
uv run python -m property_eval.render runs/round3-zero/012-at-003 --output runs/round3-zero/012-at-003/case-review.html
```

The standalone HTML works offline, without dependencies, external assets or a
server. The source inspector shows original text next to a selected claim. Fields
can be selected individually to reveal their grounded spans. Timeline preserves
the original event sequence. Evidence, Entities and Review issues offer deeper
inspection and local search. `/` focuses search; Escape closes the mobile inspector.

## Evidence and decisions

The viewer reads current `mentions.json`, `entities.json`, `records.json` and
`decision-state.json` artifacts, including `field_spans`. Partial or invalid runs
remain inspectable and are clearly marked. Structural success is never labelled
semantic accuracy. No decisions are fabricated when the artifact is absent.

Current `decisions.json` uses `property-response-v3`. The viewer also
accepts an envelope `{ "illustrative": true, "response": ... }` for an explicitly
authored illustration. The flag is shown in the Overview, Decisions and inspector.
Escalation inspection follows **cause → original evidence → responsible person →
requested intervention → blocked action**. Observed `human_interventions` are
rendered separately from proposed escalations; no proposal is labelled sent.

The included `docs/illustrative-decisions.json` fixture is a historical v2,
human-authored UI example for `round3-zero/012-at-003`, not an agent output, current
v3 schema fixture or gold recommendation:

```sh
uv run python -m property_eval.render runs/round3-zero/012-at-003 --decisions docs/illustrative-decisions.json --output runs/round3-zero/012-at-003/illustrative-review.html
```

The renderer displays supplied choices but does not run response validation or
execute them. Validate decisions using the response contract before treating them
as acceptable proposals. Raw JSON remains available in a collapsed inspector.

## Development corpus replay

The corpus renderer includes **every** entry in `corpus-index.json`, including
pending jobs and interface failures. It creates an offline index and a separate
self-contained page for every checkpoint. Render a new snapshot after a run ends:

```sh
uv run python -m property_eval.render_corpus runs/decision-dev-v1 --output runs/decision-dev-v1/review
```

Each page has a case selector and a return link to the index. The index can be
filtered by decision availability, interface repair, support review or evidence
uncertainty. It does not assign a semantic correctness score. A development run
is not presented as a held-out evaluation or a prompt comparison.

Decision replay uses `evidence-packet.json` (a diagnostic evidence packet) and
`property-response-v3` decisions. The root rationale shows why the agent selected
its response, quoted source evidence, uncertainties, assumptions and alternatives.
Malformed or unsupported quotations remain visible with a warning and their
claimed text; they are never silently presented as exact source matches.
Completed deterministic normalization stays in the collapsed interface audit.
Unresolved interface failures and missing semantic support are distinct review
conditions. Baseline model and prompt hashes stay in run details.

`observed-later.json` is isolated in **Later history**. Its event text is never
added to the prefix source lookup or used to support a decision citation. The
historical action annotation and coarse type correspondence are labelled review
material, not a unique correct choice. No later outcome is used to generate the
Overview title, extracted statements or rationale.

The corpus HTML is a snapshot, not a live polling interface. Regenerate into a
new output directory to show later completion. Old snapshots remain auditable.

## Positions and interpretation

Coordinates are zero-based Unicode character offsets into each original **event
text**, with an exclusive end. They are not byte or whole-Markdown offsets. Source
IDs identify one-based event line numbers. Validated field spans and mention
spans use their recorded offsets. Unsupported field selections show the original
line with an explicit line-level qualification. Decision cause quotations use
their exact occurrence when found, otherwise show the cited source line.

Source data are escaped at the HTML boundary; the inert JSON payload cannot
terminate its script element. The page makes no network requests. Existing output
files are not overwritten. Normal document flow becomes a compact horizontal
navigation on phones, with the source inspector as a dismissible side sheet.

## Design references

Reviewed primary references on 2026-10-10:

- [Linear issues](https://linear.app/docs/creating-issues): a stable case title and
  status, with deeper properties subordinate to the work item.
- [Linear search](https://linear.app/docs/search): a consistent navigation/search
  entry point. Here search remains local to the active case section.
- [LangSmith tracing quickstart, trace inspection](https://docs.langchain.com/langsmith/observability-quickstart#4-view-your-trace): separate the readable trajectory
  from detailed input/output inspection. Here the case story remains central while
  original evidence occupies an adjacent inspector.

These are interaction references, not copied visual assets. The visual direction
is editorial: warm paper surfaces, a narrow olive accent, fine rules, serif case
titles and compact system text. Lists replace the previous wall of cards.

## Canonical run artifact and adjacent HTML

The complete development run uses one canonical `run.json` and one adjacent
`index.html`. Generate the HTML exclusively from the canonical JSON:

```sh
uv run python -m property_eval.render_run runs/decision-dev-v1/run.json
```

The HTML embeds the corpus index and every checkpoint view. It requires no server,
network requests, or neighbouring per-case files; only its “Source JSON” link refers
to the adjacent artifact. The header carries the source run ID and content hash.
Case navigation and browser history stay within the single HTML document. The
renderer resolves each checkpoint's content-addressed artifacts through
`run_artifact.resolve_artifacts`, rather than rereading the original run directory.

Completed citation and record normalization remain in the collapsed interface
audit. Ambiguous evidence, decision support checks, assumptions, and uncertainties
remain visible in the review flow. Historical actions remain isolated in Later
history and never enter the prefix source inspector. No semantic correctness score
is inferred from schema validity, citations, or agreement with historical action.

`property-run-v2` artifacts render a paired control/progress overview with one
checkpoint disclosure per case. Each arm has its own decision, rationale, full
source inspector, and advisory model judgment. Historical correspondence, prediction
support, and target predictability are displayed independently. Invalid judge
citations remain visibly flagged; exact quotations expand to their original source
with character positions. Target material is marked evaluation-only, and is never
merged into the prefix source table. The same canonical command handles both versions.
