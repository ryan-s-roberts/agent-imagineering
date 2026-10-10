"""Offline review of historical and proposed action sets from one canonical artifact."""

import html
import json

from .run_artifact import resolve_artifacts


def esc(value):
    return html.escape(str(value))


def label(value):
    return esc(value).replace("_", " ")


def raw_detail(title, value):
    return f"<details class='raw'><summary>{esc(title)}</summary><pre>{esc(json.dumps(value, ensure_ascii=False, indent=2))}</pre></details>"


def citation_view(citations, artifacts):
    """Use the frozen catalog's exact source text; no invented paraphrase positions."""
    catalog = artifacts.get("citation-catalog.json", {})
    sources = {(s["origin"], s["id"]): s["text"] for s in catalog.get("sources", [])}
    rows = []
    for citation in citations:
        source = sources.get((citation.get("origin"), citation.get("source_id")))
        expression = citation.get("expression", "")
        start, end = -1, 0
        if source is not None and expression:
            for _ in range(citation.get("occurrence", 1)):
                start = source.find(expression, end)
                if start < 0:
                    break
                end = start + len(expression)
        if start >= 0:
            quote = (
                esc(source[:start])
                + "<mark>"
                + esc(source[start:end])
                + "</mark>"
                + esc(source[end:])
            )
            position = f"characters {start}–{end}, end exclusive"
        else:
            quote = esc(source if source is not None else "Source not available in catalog")
            position = "Unresolved citation"
        rows.append(
            f"<details class='citation'><summary>{label(citation.get('origin', 'unknown'))} · {esc(citation.get('source_id', ''))} · {position}</summary><pre>{quote}</pre></details>"
        )
    return "".join(rows)


def action_fields(action):
    """Render the actual saved slots without adding inferred recipients or effects."""
    rows = []
    for key, value in action.items():
        if (
            key in {"id", "type", "basis_record_ids", "basis_gap_ids", "depends_on_action_ids"}
            or value is None
            or value == []
        ):
            continue
        if isinstance(value, (dict, list)):
            rendered = esc(json.dumps(value, ensure_ascii=False))
        else:
            rendered = esc(value)
        rows.append(f"<dt>{label(key)}</dt><dd>{rendered}</dd>")
    return "<dl class='slots'>" + "".join(rows) + "</dl>"


def annotation_citations(items):
    return "".join(
        f"<details class='citation'><summary>Event {esc(c['event_id'])} · lines {esc(c['line_start'])}–{esc(c['line_end'])} · characters {esc(c['char_start'])}–{esc(c['char_end'])}</summary><p class='muted'>{esc(c['offset_basis'])}</p><pre>{esc(c['quote'])}</pre></details>"
        for c in items
    )


def historical_actions(episode, checkpoint_id):
    cards = []
    for action in episode.get("actions", []):
        cards.append(
            f"<article class='action' id='{esc(checkpoint_id)}-{esc(action['id'])}'><div class='action-head'><code>{esc(action['id'])}</code><span class='tag'>{label(action['materiality'])}</span></div><h4>{label(action['intent'])}</h4><p>{esc(action['summary'])}</p>{annotation_citations(action.get('source_citations', []))}</article>"
        )
    return "".join(cards)


def arm_section(arm, artifacts, target, checkpoint_id, number):
    checkpoint_id = checkpoint_id + "-" + arm
    prediction = artifacts.get("decisions.json", {})
    judgment = artifacts.get("judge.json", {})
    actions = prediction.get("actions", [])
    target_actions = target.get("episode", {}).get("actions", [])
    assessment = {
        row["prediction_action_id"]: row for row in judgment.get("prediction_assessments", [])
    }
    cards = []
    for action in actions:
        review = assessment.get(action["id"], {})
        dependencies = action.get("depends_on_action_ids", [])
        cards.append(
            f"<article class='action'><div class='action-head'><code>{esc(action['id'])}</code><span class='tag'>{label(review.get('supportedness', 'not assessed'))}</span></div><h4>{label(action['type'])}</h4>{action_fields(action)}<p class='muted'>Recorded dependencies: {esc(', '.join(dependencies) or 'none')}</p><details><summary>Judge assessment · {label(review.get('extra_status', 'pending'))}</summary><p>{esc(review.get('explanation', 'No assessment available.'))}</p>{citation_view(review.get('citations', []), artifacts)}{citation_view(review.get('support_citations', []), artifacts)}</details></article>"
        )
    rationale = prediction.get("rationale", {})
    rationale_view = f"<details class='rationale'><summary>Recorded decision rationale</summary><p>{esc(rationale.get('selected_because') or 'No recorded rationale available.')}</p>{raw_detail('Recorded uncertainties and assumptions', {key: rationale.get(key, []) for key in ('uncertainties', 'assumptions', 'alternatives_considered')})}</details>"
    target_lookup = {action["id"]: action for action in target_actions}
    mappings = []
    for row in judgment.get("target_assessments", []):
        action = target_lookup.get(row["target_action_id"], {})
        mapped = row["prediction_action_ids"]
        mappings.append(
            f"<div class='mapping'><div class='mapping-title'><a href='#{esc(checkpoint_id)}-{esc(row['target_action_id'])}'>{esc(row['target_action_id'])}</a><span class='arrow'>←</span><span>{esc(', '.join(mapped) or 'No proposed action mapped')}</span><span class='tag'>{label(row['coverage'])}</span></div><p>{esc(action.get('summary', 'Unknown target action'))}</p><div class='submetrics'><span>Category: {label(action.get('materiality', 'unknown'))}</span><span>Participants: {label(row['participants'])}</span><span>Scope: {label(row['scope_conditions'])}</span><span>Predictability: {label(row['prefix_predictability'])}</span></div><details><summary>Why this alignment?</summary><p>{esc(row['explanation'])}</p>{citation_view(row.get('citations', []), artifacts)}<h5>Prefix support for predictability</h5>{citation_view(row.get('predictability_citations', []), artifacts)}{raw_detail('Unobservable specifics', row.get('unobservable_specifics', []))}</details></div>"
        )
    missing_material = [
        row["target_action_id"]
        for row in judgment.get("target_assessments", [])
        if row["coverage"] == "missing"
        and target_lookup.get(row["target_action_id"], {}).get("materiality") == "material"
    ]
    supporting_omissions = [
        row["target_action_id"]
        for row in judgment.get("target_assessments", [])
        if row["coverage"] == "missing"
        and target_lookup.get(row["target_action_id"], {}).get("materiality") == "auxiliary"
    ]
    workflow_omissions = [
        row["target_action_id"]
        for row in judgment.get("target_assessments", [])
        if row["coverage"] == "missing"
        and target_lookup.get(row["target_action_id"], {}).get("materiality") == "workflow"
    ]
    unassessable_targets = sum(
        action.get("materiality") == "unassessable" for action in target_actions
    )
    unassessable_note = (
        f"<p class='change-note'>{unassessable_targets} unassessable historical target(s): the source does not identify a classifiable act. This limits historical correspondence; proposal support can still be assessed against the prefix. Unknown acts are not counted as missing.</p>"
        if unassessable_targets
        else ""
    )
    extras = [
        row for row in judgment.get("prediction_assessments", []) if row["extra_status"] != "mapped"
    ]
    necessity = {order["id"]: order for order in target.get("necessary_order", [])}
    orders = []
    for row in judgment.get("necessary_order_assessments", []):
        orders.append(
            f"<article class='mapping'><strong>{esc(row['order_id'])} · {label(row['verdict'])}</strong>{raw_detail('Annotated necessary dependency', necessity.get(row['order_id'], {}))}<p>{esc(row['explanation'])}</p>{citation_view(row.get('citations', []), artifacts)}</article>"
        )
    extras_view = (
        "".join(
            f"<p><code>{esc(row['prediction_action_id'])}</code> · {label(row['extra_status'])} · {label(row['supportedness'])}</p>"
            for row in extras
        )
        or "<p>No extra proposals assessed.</p>"
    )
    return f"""<section class='arm-content' data-arm='{esc(arm)}'>
<div class='sets'><section><div class='column-label'>Observed episode · evaluation only</div><h3>{len(target_actions)} historical actions</h3><p class='muted'>Observed acts may be material, auxiliary or workflow updates. They are not a normative checklist.</p>{historical_actions(target.get("episode", {}), checkpoint_id)}</section>
<section><div class='column-label'>Frozen prediction · {esc(arm)}</div><h3>{len(actions)} proposed actions</h3><p class='muted'>These are the original recorded proposals. Episode rescoring did not regenerate them.</p>{"".join(cards)}{rationale_view}<a class='inspect' href='case-{number:03}-{esc(arm)}.html'>Inspect original prefix and extraction →</a></section></div>
<section class='alignments'><div class='column-label'>Many-to-many comparison · model-assisted</div><h3>Which proposals cover which observed actions?</h3><p class='muted'>One proposal may cover several observed acts; one observed act may need several proposals. Empty mappings stay visible.</p>{unassessable_note}<div class='omissions'><div><strong>{len(missing_material)}</strong> missing material acts <span>{esc(", ".join(missing_material) or "none")}</span></div><div><strong>{len(workflow_omissions)}</strong> missing workflow effects <span>{esc(", ".join(workflow_omissions) or "none")}</span></div><div><strong>{len(supporting_omissions)}</strong> omitted notifications <span>{esc(", ".join(supporting_omissions) or "none")}</span></div></div>{"".join(mappings) or "<p>Episode assessment not yet available.</p>"}</section>
<div class='sets'><section><h3>Extra proposals & support</h3>{extras_view}</section><section><h3>Necessary dependencies</h3>{"".join(orders) or "<p>No necessary dependency was annotated.</p>"}<p class='muted'>This is distinct from historical timestamp order. Concurrent or independent communications need not be serialized.</p>{raw_detail("Observed ordering annotations", target.get("episode", {}).get("partial_order", []))}</section></div>
<details><summary>Assessment limitations and integrity</summary><p>Boundary assessability: {label(judgment.get("boundary_assessability", "pending"))}</p>{raw_detail("Boundary concerns", judgment.get("boundary_concerns", []))}<p>{esc(judgment.get("explanation", ""))}</p>{citation_view(judgment.get("citations", []), artifacts)}{raw_detail("Citation and action-reference checks", artifacts.get("judge-validation.json", {}))}{raw_detail("Decision reference checks", artifacts.get("decisions-validation.json", {}))}{raw_detail("Full action-set judgment", judgment)}</details>
</section>"""


def episode_page(document):
    rows = []
    total_actions = material_actions = uncertain_boundaries = 0
    annotation_ref = document["root_artifacts"].get("episode-annotations.json")
    annotations = (
        {
            episode["checkpoint_id"]: episode
            for episode in document["blobs"][annotation_ref]["content"].get("episodes", [])
        }
        if annotation_ref
        else {}
    )
    for number, checkpoint in enumerate(document["checkpoints"], 1):
        ref = checkpoint["historical_target"]["artifact_ref"]
        target = document["blobs"][ref]["content"] if ref else {}
        episode = annotations.get(checkpoint["id"], target.get("episode", {}))
        actions = episode.get("actions", [])
        boundary = episode.get("boundary", {})
        total_actions += len(actions)
        material_actions += sum(action["materiality"] == "material" for action in actions)
        uncertain_boundaries += boundary.get("confidence") == "uncertain"
        arm_sections = []
        cardinalities = []
        for arm in document["arm_ids"]:
            artifacts = resolve_artifacts(document, checkpoint, arm)
            cardinalities.append(
                f"{arm}: {len(artifacts.get('decisions.json', {}).get('actions', []))} proposed"
            )
            arm_sections.append(arm_section(arm, artifacts, target, checkpoint["id"], number))
        search = (
            checkpoint["case_id"] + " " + " ".join(action.get("summary", "") for action in actions)
        )
        overlap = sorted(
            set(episode.get("included_event_ids", [])) & set(boundary.get("event_ids", []))
        )
        boundary_sentence = (
            "Boundary falls within event "
            + esc(", ".join(overlap))
            + "; only the explicitly annotated part is included. Speaker/action ambiguity remains visible."
            if overlap
            else "Stops before boundary events "
            + esc(", ".join(boundary.get("event_ids", [])) or "not annotated")
            + "."
        )
        rows.append(f"""<details class='case' data-search='{esc(search.lower())}'><summary><span class='case-number'>Case {esc(checkpoint["case_id"])}</span><span>{len(actions)} observed actions</span><span class='case-counts'>{esc(" · ".join(cardinalities))}</span></summary>
<div class='case-body'><section class='boundary'><div class='column-label'>The decision episode</div><p><strong>Prefix ends at {esc(checkpoint["cutoff"])}.</strong> Episode events: {esc(", ".join(episode.get("included_event_ids", [])) or "not annotated")}. {boundary_sentence}</p><p>{esc(boundary.get("reason", "No boundary explanation available."))}</p><span class='tag'>{label(boundary.get("confidence", "unassessable"))} boundary</span><details><summary>Boundary sources and alternative continuations</summary>{annotation_citations(boundary.get("citations", []))}<p>Excluded alternative continuation event IDs: {esc(", ".join(episode.get("alternative_continuation_event_ids", [])) or "none")}.</p><p class='muted'>Boundary and excluded continuation evidence is evaluation-only. It was not available to the decision model.</p>{raw_detail("Episode limits", episode.get("limits", []))}</details></section>{"".join(arm_sections)}</div></details>""")
    buttons = "".join(
        f"<button type='button' data-select-arm='{esc(arm)}' aria-pressed='false'>{esc(arm)}</button>"
        for arm in document["arm_ids"]
    )
    current_cost = document["accounting_by_scope"]["experiment"]["returned_cost_usd"]
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Decision episodes · {esc(document["run_id"])}</title><style>
*{{box-sizing:border-box}}:root{{color-scheme:light}}body{{margin:0;background:#f6f7f9;color:#182534;font:14px/1.55 ui-sans-serif,system-ui,-apple-system,sans-serif}}main{{max-width:1320px;margin:auto;padding:40px 4vw 70px}}h1{{font-size:clamp(28px,4vw,44px);letter-spacing:-1.6px;line-height:1.1;margin:14px 0}}h3{{font-size:19px;letter-spacing:-.5px;margin:8px 0 10px}}h4{{font-size:15px;margin:12px 0 6px}}h5{{font-size:12px}}p{{margin:8px 0 14px}}.eyebrow,.column-label{{font-size:10px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:#58718a}}.lead{{max-width:830px;color:#536476;font-size:16px}}.change-note{{border-left:3px solid #3865cf;padding:12px 16px;background:#eaf0fc;margin:24px 0}}.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:24px 0}}.stats>div{{padding:18px;background:white;border:1px solid #e0e6ee;border-radius:12px}}.stats strong{{display:block;font-size:28px;letter-spacing:-1px}}.stats span,.muted{{color:#617184;font-size:12px}}.toolbar{{position:sticky;top:0;z-index:2;display:flex;gap:12px;align-items:center;padding:14px 0;background:#f6f7f9f5;backdrop-filter:blur(8px)}}input{{font:inherit;min-width:100px;flex:1;padding:11px 14px;border:1px solid #cdd7e3;border-radius:9px;background:white}}.arm-buttons{{display:flex;padding:3px;border:1px solid #cdd7e3;border-radius:10px}}button{{border:0;border-radius:7px;padding:9px 16px;background:transparent;font:inherit;cursor:pointer}}button[aria-pressed=true]{{background:#233f68;color:white}}.case{{margin:12px 0;border:1px solid #dce3ec;background:white;border-radius:13px;overflow:hidden}}summary{{cursor:pointer}}.case>summary{{display:flex;align-items:center;gap:18px;list-style:none;padding:20px 22px;font-size:12px}}.case-number{{font-size:15px;font-weight:750}}.case-counts{{margin-left:auto;color:#617184}}.case-body{{padding:0 24px 24px}}.boundary{{background:#f2f5fa;border-radius:10px;padding:18px;margin-bottom:24px}}.sets{{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin:20px 0 30px}}.sets>section{{min-width:0}}.action{{border:1px solid #e0e6ee;border-radius:10px;padding:16px;margin:12px 0}}.action-head{{display:flex;gap:8px;justify-content:space-between;align-items:center}}code{{font:11px ui-monospace,monospace;color:#54657a;overflow-wrap:anywhere}}.tag{{display:inline-block;font-size:10px;font-weight:650;border-radius:5px;padding:3px 7px;background:#edf2f8;color:#435875;white-space:nowrap}}.slots{{display:grid;grid-template-columns:130px 1fr;gap:6px 12px;font-size:12px;margin:12px 0}}dt{{color:#617184}}dd{{margin:0;overflow-wrap:anywhere}}details details{{margin:12px 0;font-size:12px}}.citation summary{{color:#355f91}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:11px/1.6 ui-monospace,monospace;background:#f5f7fa;border-radius:6px;padding:12px}}mark{{background:#dce8ff}}.inspect,a{{color:#2d5eab}}.inspect{{display:block;font-size:12px;margin-top:14px}}.alignments{{border-top:1px solid #e0e6ee;padding-top:24px}}.omissions{{display:flex;gap:16px;margin:18px 0}}.omissions>div{{flex:1;padding:12px;background:#f6f7f9;border-radius:8px;font-size:12px}}.omissions strong{{font-size:18px;margin-right:4px}}.omissions span{{display:block;color:#617184}}.mapping{{padding:15px 0;border-bottom:1px solid #e8edf3}}.mapping-title{{display:flex;gap:12px;align-items:center;font-size:12px;font-weight:650}}.mapping-title .tag{{margin-left:auto}}.arrow{{color:#889bb1}}.submetrics{{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:11px;color:#617184}}.raw{{font-size:11px}}[hidden]{{display:none!important}}:focus-visible{{outline:3px solid #80aaf1;outline-offset:3px}}@media(max-width:760px){{main{{padding:24px 15px}}.stats{{grid-template-columns:1fr 1fr}}.sets{{grid-template-columns:1fr;gap:12px}}.toolbar{{flex-wrap:wrap}}input{{flex-basis:100%}}.case>summary{{flex-wrap:wrap;padding:17px}}.case-counts{{margin-left:0;flex-basis:100%}}.case-body{{padding:0 16px 20px}}.slots{{grid-template-columns:100px 1fr}}.mapping-title{{flex-wrap:wrap}}.omissions{{flex-direction:column}}}}
</style></head><body><main><div class='eyebrow'>Frozen decisions · episode-level rescoring</div><h1>One decision can contain several actions.</h1><p class='lead'>Compare the full observed episode with each original proposal set. Inspect coverage, notifications, extra proposals, evidence support and necessary dependencies separately.</p><div class='change-note'><strong>The evaluation unit changed.</strong> Earlier first-message scores are superseded for episode-level comparison. The predictions and their evidence were frozen; only historical targets and assessment changed. Historical behavior is a soft target, not a unique correct answer.</div>
<section class='stats'><div><strong>{len(document["checkpoints"])}</strong><span>decision episodes</span></div><div><strong>{total_actions}</strong><span>observed actions · {material_actions} material</span></div><div><strong>{document["completion"]["decisions_available"]}</strong><span>frozen prediction sets</span></div><div><strong>{uncertain_boundaries}</strong><span>uncertain episode boundaries</span></div></section>
<div class='toolbar'><input type='search' aria-label='Find case or observed action' placeholder='Find a case or observed action…'><span class='muted'>Prediction arm</span><div class='arm-buttons'>{buttons}</div></div>{"".join(rows)}<p class='muted'>New episode-judge reported spend: ${current_cost:.6f}. Inherited costs remain separate in the source artifact. Model-assisted judgments are advisory; citation validity is not semantic proof.</p>{raw_detail("Run identity, completion and accounting", {"run_id": document["run_id"], "content_sha256": document["content_sha256"], "completion": document["completion"], "accounting_by_scope": document["accounting_by_scope"]})}</main><script>
const controls=[...document.querySelectorAll('[data-select-arm]')];function choose(arm){{controls.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.selectArm===arm)));document.querySelectorAll('[data-arm]').forEach(section=>section.hidden=section.dataset.arm!==arm)}}controls.forEach(b=>b.addEventListener('click',()=>choose(b.dataset.selectArm)));if(controls.length)choose(controls[0].dataset.selectArm);document.querySelector('input').addEventListener('input',event=>document.querySelectorAll('.case').forEach(row=>row.hidden=!row.dataset.search.includes(event.target.value.toLowerCase())));
</script></body></html>"""
