# V2 development run

Model: `anthropic/claude-sonnet-4.6`; manifest: `experiments/ontology-v2.json`.
Artifacts: `runs/ontology-v2`. Three development prefixes; no held-out accuracy claim.
Schema, prompt and pipeline changed together, so comparison with v1 is not a causal ablation.

| Prefix | Entities | Invalid mentions | Record stage | Latency | Reported USD cost |
| --- | ---: | ---: | --- | ---: | ---: |
| 012 through 011 | 11 | 2 | not run | 13.159s | 0.033741 |
| 012 through 024 | 18 | 2 | not run | 23.852s | 0.069675 |
| 038 through 013 | 12 | 2 | not run | 20.164s | 0.043854 |

Total reported cost: $0.147270. All outputs parsed. All failed the exact entity grounding gate;
no record extraction or decision packet was produced. Nine offline tests passed afterward.

## Reviewed failure

All six unmatched mentions replace U+2019 curly apostrophes with ASCII apostrophes. Case 12
extracts `dishwasher door isn't closing` where the source uses `isn’t`. Case 38 similarly
changes `it’s` to `it's`. This is an exact-alignment failure, not demonstrated semantic failure.
Valid references alone would have hidden the difference. The pipeline correctly retained
the failed artifacts and did not silently rewrite evidence or proceed with partial state.

The present gate is brittle for typographic variation. A deliberate alignment design could
map normalized text back to original offsets, while marking normalization and ambiguity;
this has not been implemented or used to improve these reported results. An alternative is
shorter exact mention spans with explicit occurrence selection. Neither proves correct linking.

Manual inspection also shows separate role-only Tenant and named Leo entities. Whether and how
they should link requires source-supported identity resolution. We have not scored the full
entity lists against a reference annotation. There is no v2 semantic precision/recall estimate.

The [viewer](../runs/ontology-v2/012-at-024/evidence-review.html) exposes original source lines,
valid mention positions and grounding diagnostics. It explicitly states that mentions alone
cannot support the response ontology. Typed relational statement rendering is implemented,
but this live run contains no relation-stage output to demonstrate it.

## Next gate

Resolve the [choice-to-evidence coverage gaps](choice-evidence-contract.md), freeze an annotation
guide, and measure extraction against reviewed annotations before claiming decision readiness.
The [prior-art review](implementation-review.md) describes a minimal approach without RL,
an LLM judge, or an extensive supporting system.
