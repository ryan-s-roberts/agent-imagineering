# Action-set prompt ablation v1

Four preregistered prompt arms reused the same 40 development evidence packets,
model settings, response ontology and episode judge. No extraction reruns or
holdout calls. Requests shared a 24-call concurrency limit.

| Arm | Decisions | Actions | Structurally valid | Completed judgments | Full operational coverage |
|---|---:|---:|---:|---:|---:|
| Control | 40 | 45 | 31 | 40 | 0 |
| Coverage | 40 | 68 | 31 | 39 | 0 |
| Action-local uncertainty | 40 | 46 | 32 | 40 | 1 |
| Combined | 40 | 70 | 32 | 39 | 0 |

The coverage wording changes output cardinality, but most extra actions are waits:
control has 3 `await_response` actions, coverage 26 and combined 23. These counts
do not establish useful additional progress. No prompt was promoted.

Two judge calls remained invalid after the bounded interface repair: coverage
case 012 and combined case 018. Their generated decisions remain available;
semantic comparisons must report the missing judgments. Fresh control itself
changed action count at five checkpoints and historical label at eight relative
to the earlier control (42 vs 45 actions). Single-sample differences are exploratory.

The canonical `runs/actionset-ablation-v1/run.json` embeds the exact prompts,
all generated outputs, source evidence, judgments, accounting and the paired
statistics in `ablation-analysis.json`. Its adjacent HTML explicitly separates
decision-agent outputs, historical observations and judge assessments.

This experiment used early prefixes. The subsequent late-episode selection is a
different evaluation population; these results do not measure late-case decisions.
