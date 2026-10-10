"""Project a minimal, cited film dataset from the immutable canonical run."""
import json
from pathlib import Path
from property_eval.run_artifact import validate_artifact

root = Path(__file__).resolve().parents[2]
source = root / 'runs/decision-dev-v1/run.json'
run = json.loads(source.read_text())
errors = validate_artifact(run)
if errors:
    raise ValueError(errors)
checkpoint = next(c for c in run['checkpoints'] if c['id'] == '004-at-004')
artifacts = {name: run['blobs'][ref]['content'] for name, ref in checkpoint['artifacts'].items()}
packet = artifacts['evidence-packet.json']
decision = artifacts['decisions.json']
quotes = []
for source_id in ['002:L5', '003:L5', '004:L6', '004:L7']:
    row = next(s for s in artifacts['sources.json']['sources'] if s['id'] == source_id)
    quotes.append({key: row[key] for key in ['id', 'text', 'start', 'end']})
valid = 0
valid_packets = 0
for c in run['checkpoints']:
    a = {name: run['blobs'][ref]['content'] for name, ref in c['artifacts'].items()}
    valid += int(a['decisions-validation.json']['valid'])
    valid_packets += int(a['evidence-packet.json']['validated_decision_state'])
data = {
    'runId': run['run_id'], 'hash': run['content_sha256'], 'checkpoint': checkpoint['id'],
    'evidenceVersion': packet['ontology_version'], 'responseVersion': decision['ontology_version'],
    'quotes': quotes, 'rationale': decision['rationale'], 'action': decision['actions'][0],
    'records': [{k: record[k] for k in ['id', 'type', 'status'] if k in record}
                for record in packet['records'] if record['id'] in ['status-request-paused', 'intervention-manual-review-required']],
    'diagnostics': packet['diagnostics'], 'decisionValidation': artifacts['decisions-validation.json'],
    'completion': run['completion'], 'decisionChecksPassed': valid,
    'validatedEvidencePackets': valid_packets,
    'source': 'runs/decision-dev-v1/run.json',
}
target = root / 'video/src/run-data.json'
target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f'Validated canonical container; exported {checkpoint["id"]}; {valid}/40 decision checks; {valid_packets}/40 validated evidence packets.')
