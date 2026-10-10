"""Local synthetic guide track, one independently timed scene at a time."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
lines = [
    "Today, we're building a property agent. Do we have an environment? Of course not!",
    "So we'll use our... imagination! Imagine the office. Don't imagine the evidence.",
    "Two ontologies give it a skeleton. One describes the evidence. The other describes the choices.",
    "Here's a real saved case. Approval recorded. Provider assigned. Then, paused. Please review and resolve this manually.",
    "Extract mentions. Link identities. Build typed assertions. Every claim keeps its source, and every unknown stays unknown.",
    "The recorded proposal is to escalate for human review. The request is paused. Manual review is still outstanding.",
    "Open up the decision. What next? Why this? What needs resolving? The response ontology gives the answer a shape you can inspect.",
    "The agent is the small part. One ontology structures the history. The other structures the choice. Build the vocabulary. Connect the evidence. Make the next step inspectable.",
    "A tiny agent. An ontological skeleton. An inspectable decision. Imagination for the environment. Evidence for the reasoning.",
]
clips = list(enumerate(lines)) + [('tennis', "No deterministic structure? Tennis without a net. Build the net: an ontology. Types, relationships, response shapes. No whole-world simulation required.")]
for i, text in clips:
    aiff = root / f'public/voice-{i}.aiff'
    target = root / f'public/voice-{i}.wav'
    subprocess.run(['say', '-v', 'Samantha', '-r', '205' if i == 'tennis' else '177', '-o', str(aiff), text], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(aiff), '-ar', '48000', str(target)], check=True)
    aiff.unlink()
print('Generated ten synthetic narration clips.')
