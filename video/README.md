# AI Transformation of Services — design film

A 60-second Remotion design pitch, branded only as Plasm. Its warm paper, olive, Georgia and Avenir Next styling follows the existing property evidence review HTML. The opening uses original paper-theatre imagery, tumbling letters and imaginary offices as a cheerful joke about the missing environment. A tennis court gains a net: the metaphor for building deterministic structure with an ontology rather than simulating an entire world. The main story shows the design: evidence ontology → source-linked extraction → response ontology → inspectable proposal.

## Preview and render

```sh
cd video
npm ci
npm run score
python3 scripts/narration.py
npm run typecheck
npm run studio
npm run render
```

Output: `out/plasm-hackathon.mp4`. Narration is a local synthetic Samantha guide track generated with macOS `say`; `ffmpeg` converts the clips. Music is an original deterministic composition generated with Python's standard library. The composition uses system Georgia and Avenir Next; reproduce on macOS to match the reviewed frames.

## Story

| Seconds | Beat |
| --- | --- |
| 0–4 | Build a property agent. Environment not included. |
| 4–9 | Use our IMAGINATION! Imagine the office; don't imagine the evidence. |
| 9–17 | Tennis without a net: build deterministic structure with an ontology. |
| 17–23 | Evidence ontology structures what is reported; response ontology structures the next choice. |
| 23–29 | Case 004: approval, assignment, pause, explicit manual-review request. |
| 29–35 | Mentions → linked identities → typed assertions with source spans. |
| 35–41 | The recorded response proposes human review and explains why. |
| 41–46 | Open up the decision: action, basis, rationale and alternatives. |
| 46–54 | The agent is the small part; two ontologies define its domain. |
| 54–60 | Imagination for the environment. Evidence for the reasoning. |

## Source provenance

The film reads `src/run-data.json`, a minimal projection of canonical `../runs/decision-dev-v1/run.json`. Refresh from the project root with `.venv/bin/python video/scripts/extract-run.py`. The exporter first runs the repository's canonical artifact validation, then extracts checkpoint `004-at-004`, its actual source expressions and recorded rationale. It never changes a generated decision or reads later observations into the film's story.

Canonical content hash: `aa92c05f81dc79b696fa294ce7ef34149eaae03b08a0ef1ca5a7ece2211f1493`.

The frozen run specifies `property-evidence-v4` and `property-response-v3`. These frozen versions take precedence over potentially older narrative documentation. Plasm is the film's brand; the film makes no claim that this prototype invokes Plasm's runtime, MCP tools or API catalogs.

This is a design pitch, not a benchmark report. The underlying development run has 40 proposals, 26 passing decision checks, and no extraction packet marked fully validated. These remain in the source projection and original artifacts; the film makes no accuracy or completion claim. The highlighted decision is a saved proposal, not an executed intervention. Canonical validation checks artifact integrity, not semantic correctness.

No live model calls or external writes were made to produce the film. Remotion references: https://www.remotion.dev/docs/the-fundamentals and https://www.remotion.dev/docs/cli/render.
