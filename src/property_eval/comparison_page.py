"""Escaped, offline rendering of advisory paired historical correspondence."""

import html
import json
from collections import Counter

from .run_artifact import resolve_artifacts


def esc(value):
    return html.escape(str(value))


def words(value):
    return esc(value or "Not available").replace("_", " ")


def details(label, value):
    return f"<details><summary>{esc(label)}</summary><pre>{esc(json.dumps(value, ensure_ascii=False, indent=2))}</pre></details>"


def citations(items, artifacts, target):
    sources = {s["id"]: s for s in artifacts.get("sources.json", {}).get("sources", [])}
    rows = []
    for cite in items:
        origin = cite.get("origin")
        source = (
            target.get("source", {})
            if origin == "target"
            else sources.get(cite.get("source_id"), {})
            if origin == "prefix"
            else {}
        )
        text = source.get("text", "")
        if origin == "prediction":
            text = json.dumps(
                artifacts.get("decisions.json", {}), ensure_ascii=False, sort_keys=True
            )
        expression = cite.get("expression", "")
        start, cursor = -1, 0
        for _ in range(cite.get("occurrence", 1)):
            start = text.find(expression, cursor)
            if start < 0:
                break
            cursor = start + len(expression)
        position = (
            f"chars {start + source.get('start', 0)}–{cursor + source.get('start', 0)}, end exclusive"
            if start >= 0
            else "Literal span not resolved"
        )
        original = (
            esc(text[:start]) + "<mark>" + esc(text[start:cursor]) + "</mark>" + esc(text[cursor:])
            if start >= 0
            else esc(text)
        )
        rows.append(
            f'<details class="citation"><summary>{words(origin)} · {esc(cite.get("source_id"))} · {esc(position)}</summary><blockquote>{esc(expression)}</blockquote><pre>{original}</pre></details>'
        )
    return "".join(rows)


def arm_view(arm, artifacts, target, href):
    response = artifacts.get("decisions.json", {})
    judge = artifacts.get("judge.json", {})
    rationale = response.get("rationale", {})
    actions = response.get("actions", [])
    action_list = "".join(
        f"<li>{words(a.get('type'))}: {esc(a.get('question') or a.get('reason') or a.get('intervention_detail') or a.get('message') or '; '.join(a.get('steps', [])) or a.get('requested_feedback') or ', '.join(a.get('scope', [])) or a.get('purpose') or '')}</li>"
        for a in actions
    )
    summary = f'<h3>{esc(arm)}</h3><p class="choice">{words(response.get("disposition"))} · {len(actions)} proposals</p><ul>{action_list}</ul><p>{esc(rationale.get("selected_because", "No decision available"))}</p>'
    summary += details("Full proposed actions", actions)
    for key in ("uncertainties", "assumptions"):
        summary += (
            f"<details><summary>{words(key)} · {len(rationale.get(key, []))}</summary><ul>"
            + "".join(f"<li>{esc(x)}</li>" for x in rationale.get(key, []))
            + "</ul></details>"
        )
    summary += f'<a class="inspect" href="{href}">Inspect decision, evidence & original positions →</a><div class="judge"><span class="eyebrow">Model-assisted assessment · advisory</span>'
    invalid = artifacts.get("judge-validation.json", {}).get("invalid_citations", [])
    if invalid:
        summary += f'<p class="citation-warning">{len(invalid)} judge citations failed literal alignment. Treat the assessment as requiring review.</p>'
    summary += f"<dl><dt>Historical correspondence</dt><dd>{words(judge.get('overall_correspondence'))}</dd><dt>Prediction support</dt><dd>{words(judge.get('prediction_supportedness'))}</dd><dt>Target predictability</dt><dd>{words(judge.get('target_predictability'))}</dd></dl>"
    summary += f"<p>{esc(judge.get('support_explanation', 'No judgment available'))}</p>"
    summary += citations(judge.get("support_citations", []), artifacts, target)
    summary += "<details><summary>Correspondence dimensions & cited reasoning</summary>"
    for key in (
        "action_intent",
        "participants_roles",
        "scope_conditions",
        "sequencing",
        "omissions_extras",
    ):
        dimension = judge.get(key, {})
        summary += (
            f"<h4>{words(key)} · {words(dimension.get('verdict'))}</h4><p>{esc(dimension.get('explanation', ''))}</p>"
            + citations(dimension.get("citations", []), artifacts, target)
        )
    summary += "</details>" + details(
        "Unobservable historical specifics", judge.get("unobservable_target_specifics", [])
    )
    summary += details(
        "Annotation concerns & judge confidence",
        {"concerns": judge.get("target_encoding_concerns"), "confidence": judge.get("confidence")},
    )
    summary += details(
        "Literal citation checks — not entailment", artifacts.get("judge-validation.json", {})
    )
    summary += details("Decision reference checks", artifacts.get("decisions-validation.json", {}))
    return '<section class="arm">' + summary + "</div></section>"


def comparison_page(document):
    counts = {arm: Counter() for arm in document["arm_ids"]}
    rows = []
    for number, checkpoint in enumerate(document["checkpoints"], 1):
        target_ref = checkpoint.get("historical_target", {}).get("artifact_ref")
        target = document["blobs"][target_ref]["content"] if target_ref else {}
        columns = []
        brief = []
        for arm in document["arm_ids"]:
            artifacts = resolve_artifacts(document, checkpoint, arm)
            judge = artifacts.get("judge.json", {})
            verdict = judge.get("overall_correspondence", "pending")
            counts[arm][verdict] += 1
            brief.append(f"{arm}: {verdict}")
            columns.append(arm_view(arm, artifacts, target, f"case-{number:03}-{arm}.html"))
        source = target.get("source", {})
        history = f'<details class="history"><summary>Historical target · evaluation only · {words(target.get("intent_assessability"))}</summary><p>Withheld from both decisions. An observed act is not a gold-standard action or proof of completed work.</p><pre>{esc(source.get("text", "No historical source"))}</pre>{details("Partial typed annotation and unknown slots", target)}</details>'
        rows.append(
            f'<details class="case" data-search="{esc(checkpoint["case_id"])}"><summary><strong>{esc(checkpoint["case_id"])}</strong><span>Through event {esc(checkpoint["cutoff"])}</span><small>{esc(" · ".join(brief))}</small></summary>{history}<div class="pair">{"".join(columns)}</div></details>'
        )
    totals = "".join(
        f"<p><strong>{esc(arm)}</strong> "
        + " · ".join(f"{esc(k)} {v}" for k, v in counts[arm].items())
        + "</p>"
        for arm in document["arm_ids"]
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Property · Paired review</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#fbfaf7;color:#293129;font:14px/1.65 'Avenir Next',system-ui,sans-serif}}main{{max-width:1320px;margin:auto;padding:42px 4vw}}h1{{font:38px/1.2 Georgia,serif}}h3{{font:26px Georgia,serif;margin-top:0}}h4{{font-size:13px}}.eyebrow{{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#66745e}}.intro{{max-width:850px;color:#687060}}.totals{{font-size:12px;margin:24px 0}}input{{padding:10px;background:transparent;border:1px solid #daddd2;font:inherit;margin:12px 0 24px;width:280px}}.case{{border-top:1px solid #daddd2}}summary{{cursor:pointer}}.case>summary{{padding:18px 0;display:flex;gap:22px;align-items:center}}small{{color:#64705e;margin-left:auto}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:38px;padding:26px 0 40px}}.arm{{min-width:0}}.arm+.arm{{border-left:1px solid #daddd2;padding-left:38px}}.choice{{color:#5b7049}}.inspect{{display:block;margin:20px 0;color:#536e42}}details details{{font-size:12px;margin:14px 0}}.judge{{border-top:1px solid #daddd2;padding-top:24px}}dl{{display:grid;grid-template-columns:1fr 1fr;font-size:12px}}dd{{margin:0;color:#536e42}}pre{{font:12px/1.6 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere}}blockquote{{margin:12px 0;padding-left:12px;border-left:2px solid #879777}}mark{{background:#e5ecce}}.history{{background:#f3f0e8;padding:14px;margin-top:4px}}.citation{{color:#52684c}}a:focus-visible,summary:focus-visible,input:focus-visible{{outline:2px solid #6d805c;outline-offset:4px}}@media(max-width:760px){{main{{padding:24px 20px}}h1{{font-size:31px}}.pair{{grid-template-columns:1fr}}.arm+.arm{{border-left:0;border-top:1px solid #daddd2;padding:25px 0 0}}.case>summary{{display:block}}.case>summary>*{{display:block;margin:4px 0}}}}
</style></head><body><main><div class="eyebrow">Exposed development cases · paired prompt comparison</div><h1>What changed in the next decision?</h1><p class="intro">The same frozen evidence, two decision prompts. Compare the choices and advisory judgments below. Historical correspondence, prefix support and target predictability answer different questions; none is an accuracy score.</p><div class="totals">{totals}</div><input type="search" aria-label="Search cases" placeholder="Find case…">{"".join(rows)}{details("Run identity and experiment metadata", {k: v for k, v in document.items() if k not in {"blobs", "checkpoints", "calls"}})}</main><script>document.querySelector('input').addEventListener('input',event=>document.querySelectorAll('.case').forEach(row=>row.hidden=!row.dataset.search.toLowerCase().includes(event.target.value.toLowerCase())));</script></body></html>"""
