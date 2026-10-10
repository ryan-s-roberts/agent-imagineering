# Extraction implementation review

Reviewed 2026-10-10 against accessible primary sources. This is an engineering comparison,
not a claim that our implementation or any chosen model is state of the art on these cases.
No reinforcement learning, training corpus, graph database or agent orchestration is required.

## Relevant prior art

| Technique / implementation | What it supplies | Implication for us |
| --- | --- | --- |
| [Google LangExtract](https://github.com/google/langextract) | Example-guided extraction, source-span alignment, chunking, parallel extraction and multiple passes; standalone visual review | Closest methodological reference. Adopt grounding and review discipline. Our entity mentions have exact spans; record evidence currently identifies entire source lines. We lack few-shot examples and recall passes. |
| [GLiNER2](https://github.com/fastino-ai/GLiNER2) | Pretrained schema-driven entity, structured-data and directional relation extraction; optional spans and confidence | Credible compact baseline for mentions and local relations, without our own training. Cross-event permission scope, reported speech and identity still require evaluation. Confidence is not a calibrated correctness score for our domain. |
| [NuExtract 2.0](https://huggingface.co/numind/NuExtract-2.0-8B) | Pretrained template-driven extraction including verbatim and normalized field types | Candidate extraction-model baseline. Template matching does not establish cross-event attribution or identity. Evaluate identical contracts before replacing the provider. |
| [Microsoft structured entity extraction](https://arxiv.org/abs/2402.04437) | Treats structured entities as richer evaluation objects than isolated triples | Evaluate complete records and argument roles as well as entity mentions; a correct participant paired with an incorrect owner or permission scope is a substantive error. |

These are available techniques, not measured winners on this corpus. Published or vendor results
on other datasets cannot rank their performance on synthetic property histories.

## Our implementation against that standard

**Implemented:** a fixed entity vocabulary and ten typed assertion schemas; entity extraction
followed by relation/record slot filling; request-specific enums for available references;
strict structured output; deterministic span/reference/domain checks; retained contradictory
assertions; separate origin, modality and polarity; an evidence packet and a response contract.
This is ontology-guided information extraction: models populate a schema authored in code.
It is not ontology discovery at inference time, nor a formal OWL reasoner.

**Incomplete:** entity discovery and entity linking are still combined in the first model call.
One incorrectly merged entity contaminates subsequent relations. Mention validation checks text
occurrence, not whether the entity label/type/link is justified. Repeated substrings expose an
occurrence count but do not disambiguate the chosen mention. Record citations identify source
lines, not the precise evidence span for each argument, qualifier or normalized value.

There is no document-level recall measurement, independent annotated reference set, calibrated
abstention, normalized temporal interval model, or formal policy model. Whole-prefix extraction
can omit facts as histories grow. Strict JSON and passing reference checks cannot detect those
omissions. An empty extraction can be structurally valid. Static ontology coverage is also a
hypothesis: quote/invoice entities exist but rich financial records and payment actions are not
yet represented. The current ontology is maintenance-focused, not all property operations.

## Recommended minimal next iteration

1. Freeze the ontology and annotation guide for an evaluation round. Hand-author reviewed
   references for development prefixes and an untouched evaluation split. Mark genuinely
   ambiguous cases as alternative acceptable annotations, rather than guessing a unique truth.
2. Separate **mention detection → entity linking → typed assertion extraction**. Keep mention
   IDs anchored to event/offset and record explicit same-entity links. Never merge on name
   similarity alone. Entity identity is case-local; stability across prefixes needs explicit design.
3. Add field-level evidence spans to records. Preserve quoted expressions alongside normalized
   values. Resolve offsets in code, and require an occurrence selector where text repeats.
4. Use short, independently authored examples for negation, quoted reports, conditional approval,
   unresolved actors and rescheduling. Keep evaluation examples out of prompts. Then compare
   zero-shot versus few-shot with all other factors fixed.
5. Measure omissions before adding chunking or another extraction pass. If needed, extract over
   bounded event windows with earlier entity context, merge exact duplicates deterministically,
   and retain unresolved identity links. A second pass may improve recall while lowering precision.
6. Compare one alternate pretrained extractor only after the reference set exists. GLiNER2 is
   particularly relevant to the mention stage; NuExtract is a structured-field alternative.

No library installation is necessary to implement steps 1–4. Keep Python/Pydantic/HTTPX and
OpenRouter for the present experiment. Adopting LangExtract is reasonable if its span alignment
and chunk orchestration replace meaningful custom work; wrapping the same prompts alone would
not improve semantics. Do not add a graph store solely to hold a small evidence packet.

## Deterministic evaluation without an LLM judge

Score exact mention spans and entity types with precision/recall/F1; score entity-link pairs;
compare normalized assertion tuples including argument direction, scope, attribution, polarity,
modality and conditions. Match through gold mention anchors rather than arbitrary generated IDs.
Score source support separately from field correctness. Report exact whole-record match and
per-field errors; do not let easy role facts hide wrong authorization or ownership.

Normalization rules must be authored and frozen: arbitrary conditions expressed in prose do
not yet support deterministic semantic equivalence. For those fields, use reviewed categorical
labels or narrowly specified accepted forms, while retaining original text. Unknown private
test cases still permit extraction with the same ontology, but semantic accuracy cannot be
scored automatically unless someone supplies reference annotations or an explicit oracle.

Response validation checks proposal types, references and selected evidence compatibility.
It is not a correctness score for the next action. Response gold data should admit sets of
acceptable actions and required/forbidden constraints, not assume that the historical action
was uniquely correct. Extraction and decision quality need separate scores.
