# Syntactic completion before decision evaluation

Purely syntactic failures are pipeline defects, not useful decision-quality observations.
`canonicalization.py` removes mechanically recoverable interface friction before evidence
reaches the decision stage. Archive raw output and the canonicalization trace separately.

Host-owned operations:

- Align case, apostrophe and whitespace variation to a unique original source span; retain
  original Unicode text and offsets. Ambiguous normalized matches are not guessed.
- Repair a wrong source line only when the exact expression occurs uniquely within the
  same event. Never search later events or another event for a convenient supporting quote.
- Split a wrapped expression into exact per-line evidence spans within the cited event.
- Deduplicate identical mentions and merge repeated evidence for a field.
- Derive parent cause evidence from nested cause spans, and union field/cause source IDs into
  record provenance. These are redundant structures that should not be independently generated.

No operation rewrites an assertion, invents an actor or resolves a semantic contradiction.
Source alignment establishes text location, not entailment. Missing evidence for a field
remains explicitly unsupported. A diagnostic decision run can consume that uncertainty
without pretending the packet passed a stricter completeness contract.

Offline replay of the three human-v4 outputs: all mention outputs become valid, including
the two capitalisation mismatches in case038. Cases003 and012 have no remaining quote-alignment
or redundant-provenance errors. Their remaining two/five missing-field-evidence findings are
support gaps. Original historical run results are unchanged; these are host-side corrections
evaluated against retained artifacts, not new model generations or new semantic accuracy scores.
