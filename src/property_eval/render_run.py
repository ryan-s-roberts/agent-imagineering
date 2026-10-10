"""Render a canonical run artifact as one self-contained offline HTML workspace."""

import argparse
import html
import json
from pathlib import Path

from .corpus_page import PAGE as CORPUS_PAGE
from .render import render_job
from .render_corpus import summarize_checkpoint


def embedded_page(page: str) -> str:
    """Route the existing case navigation through the single document shell."""
    page = page.replace(
        "location.href=select.value",
        "parent.postMessage({propertyReviewPage:select.value},'*')",
    )
    bridge = """<script>
document.addEventListener('click',event=>{
  const link=event.target.closest('a');if(!link)return;
  const destination=link.getAttribute('href');
  if(destination==='index.html'||/^case-\\d+(?:-[a-z]+)?\\.html$/.test(destination)){
    event.preventDefault();parent.postMessage({propertyReviewPage:destination},'*');
  }
});</script>"""
    return page.replace("</body>", bridge + "</body>")


def render_document(document: dict, checkpoints: list[tuple[dict, dict]], identity: dict) -> str:
    """Use only decoded artifacts supplied by the canonical document adapter."""
    prepared = []
    experiment = document.get("format_version") == "property-run-v2"
    for number, (checkpoint, artifacts) in enumerate(checkpoints, 1):
        entry = {
            "id": checkpoint["id"],
            "case": checkpoint["case_id"],
            "split": checkpoint.get("split"),
            "cutoff": checkpoint["cutoff"],
            "status": checkpoint.get("status", "pending"),
        }
        if experiment:
            from .run_artifact import resolve_artifacts

            for arm in document["arm_ids"]:
                arm_artifacts = resolve_artifacts(document, checkpoint, arm)
                target_ref = checkpoint.get("historical_target", {}).get("artifact_ref")
                target = document["blobs"][target_ref]["content"] if target_ref else {}
                event = target.get("source", {}).get("event")
                arm_artifacts["observed-later.json"] = {
                    "events": [event] if event else [],
                    "visibility": "review_only",
                    "review_status": target.get("review_status"),
                    "caveat": "Historical target withheld from both decision arms; not a gold-standard action.",
                }
                row = summarize_checkpoint(
                    arm_artifacts, {**entry, "status": checkpoint["arms"][arm]["status"]}, number
                )
                row["href"] = f"case-{number:03}-{arm}.html"
                row["label"] += f" · {arm}"
                row["arm"] = arm
                prepared.append((arm_artifacts, row))
        else:
            prepared.append((artifacts, summarize_checkpoint(artifacts, entry, number)))
    rows = [row for _, row in prepared]
    pages = {}
    for artifacts, row in prepared:
        pages[row["href"]] = embedded_page(
            render_job(
                Path(identity["run_id"] + (" · " + row["arm"] if experiment else "")) / row["id"],
                corpus={"entries": rows, "entry": row, "current": row["href"]},
                artifacts=artifacts,
            )
        )
    payload = {
        "run": identity["run_id"],
        "entries": rows,
        "metadata": {
            "identity": identity,
            "evaluation": document["blobs"][document["root_artifacts"]["evaluation-summary.json"]][
                "content"
            ]
            if "evaluation-summary.json" in document.get("root_artifacts", {})
            else None,
            **{
                key: value for key, value in document.items() if key not in {"blobs", "checkpoints"}
            },
        },
    }
    pages["index.html"] = embedded_page(
        CORPUS_PAGE.replace(
            "__CORPUS_PAYLOAD__", json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
        )
    )
    if experiment:
        configuration_ref = document["root_artifacts"].get("experiment.json")
        configuration = document["blobs"][configuration_ref]["content"] if configuration_ref else {}
        if configuration.get("judge_version") == "episode-judge-v1":
            from .episode_page import episode_page

            pages["index.html"] = embedded_page(episode_page(document))
        else:
            from .comparison_page import comparison_page

            pages["index.html"] = embedded_page(comparison_page(document))
    encoded = json.dumps(pages, ensure_ascii=False).replace("<", "\\u003c")
    run_id = html.escape(identity["run_id"])
    digest = html.escape(identity["content_hash"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Property review · {run_id}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f7f6f1;color:#30352e;font:11px system-ui}}
.identity{{height:38px;display:flex;align-items:center;gap:14px;padding:0 18px;border-bottom:1px solid #d9ddd2;overflow:hidden}}
.identity a{{color:inherit;white-space:nowrap}}.identity span{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.identity code{{font-size:10px}}iframe{{display:block;border:0;width:100%;height:calc(100dvh - 38px)}}
@media(max-width:600px){{.identity{{gap:8px;padding:0 10px}}.identity code{{display:none}}}}
</style></head><body><div class="identity"><a href="#index.html">All cases</a><span>{run_id}</span>
<code title="{digest}">Artifact {digest[:20]}…</code><a href="run.json">Source JSON</a></div>
<iframe title="Property evidence and decision review" sandbox="allow-scripts"></iframe>
<script type="application/json" id="pages">{encoded}</script><script>
const pages=JSON.parse(document.getElementById('pages').textContent),frame=document.querySelector('iframe');
function show(){{const key=location.hash.slice(1)||'index.html';frame.srcdoc=pages[key]||pages['index.html']}}
window.addEventListener('message',event=>{{if(event.source!==frame.contentWindow)return;
const key=event.data?.propertyReviewPage;if(Object.hasOwn(pages,key))location.hash=key}});
window.addEventListener('hashchange',show);show();
</script></body></html>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    document = json.loads(args.artifact.read_text())
    from .run_artifact import resolve_artifacts, validate_artifact

    issues = validate_artifact(document)
    if issues:
        parser.error("Canonical artifact integrity failed: " + "; ".join(issues))

    checkpoints = [
        (checkpoint, resolve_artifacts(document, checkpoint))
        for checkpoint in document["checkpoints"]
    ]
    destination = args.output or args.artifact.with_name("index.html")
    if destination.exists():
        parser.error("Output already exists; choose a new path")
    identity = {"run_id": document["run_id"], "content_hash": document["content_sha256"]}
    destination.write_text(render_document(document, checkpoints, identity), encoding="utf-8")
    print(destination.resolve())


if __name__ == "__main__":
    main()
