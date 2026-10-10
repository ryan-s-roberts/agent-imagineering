"""Local synthetic guide track, one independently timed scene at a time."""
from pathlib import Path
import subprocess
import json

root = Path(__file__).resolve().parents[1]
lines = [
    "A property agent. An environment? Of course not!",
    "We'll use our imagination! Imagine the office. Don't imagine the evidence.",
    "Two ontologies. One structures the evidence. The other structures the choices.",
    "A real case: approval recorded, provider assigned, then paused. Manual review requested.",
    "Extract mentions. Link identities. Build typed assertions. Every claim keeps its source.",
    "The proposal: human review. Its basis: the paused request and the explicit review instruction.",
    "Open the decision. What next? Why this? What needs resolving?",
    "The agent is the small part. Build the vocabulary. Connect the evidence. Make the next step inspectable.",
    "Imagination for the environment. Evidence for the reasoning. An inspectable decision.",
]
clips = list(enumerate(lines)) + [('tennis', "No deterministic structure? Tennis without a net. Build the net: an ontology, not a whole simulated world.")]
durations = dict(enumerate([4,5,6,6,6,6,5,8,6])) | {'tennis': 8}
for i, text in clips:
    aiff = root / f'public/voice-{i}.aiff'
    target = root / f'public/voice-{i}.wav'
    subprocess.run(['say', '-v', 'Samantha', '-r', '190', '-o', str(aiff), text], check=True)
    info = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(aiff)]))
    duration = float(info['format']['duration'])
    tempo = max(1.0, duration / (durations[i] - 0.45))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(aiff), '-af', f'atempo={tempo:.6f}', '-ar', '48000', str(target)], check=True)
    aiff.unlink()
print('Generated ten synthetic narration clips.')
