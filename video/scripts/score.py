"""Original deterministic 120 BPM score; Python standard library only."""
import math
import random
import struct
import wave
from pathlib import Path

RATE = 44100
SECONDS = 60
random.seed(99)
out = Path(__file__).resolve().parents[1] / 'public' / 'score.wav'
out.parent.mkdir(exist_ok=True)
notes = [130.8128, 174.6141, 195.9977, 164.8138]
with wave.open(str(out), 'wb') as wav:
    wav.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
    for second in range(SECONDS):
        chunk = bytearray()
        for n in range(RATE):
            t = second + n / RATE
            beat = t % .5
            bar = int(t / 2)
            root = notes[(bar // 4) % 4]
            kick = math.sin(2*math.pi*(48*beat+9*(1-math.exp(-beat*35))))*math.exp(-beat*18)*.35
            tick = t % .25
            hat = (random.random()*2-1)*math.exp(-tick*170)*.045
            snare_phase = (t-.5) % 1
            snare = (random.random()*2-1)*math.exp(-snare_phase*35)*.085
            arp_phase = t % .25
            pitch = root * [2, 2.5, 3, 4, 3, 2.5, 2, 3][int(t*4)%8]
            arp = (math.sin(2*math.pi*pitch*t)+.2*math.sin(4*math.pi*pitch*t))*math.exp(-arp_phase*12)*.08
            bass = math.sin(2*math.pi*root/2*t)*math.exp(-beat*5)*.13
            pad = sum(math.sin(2*math.pi*root*r*t) for r in [1,1.25,1.5])/3*.065
            energy = .45 if t < 4 else (1 if t < 54 else .65)
            fade = min(1,t/1.5,max(0,(SECONDS-t)/2))
            sample = (kick+hat+snare+bass+arp+pad)*energy*fade
            left = int(max(-1,min(1,sample))*29000)
            right = int(max(-1,min(1,sample+math.sin(2*math.pi*pitch*t+.15)*math.exp(-arp_phase*12)*.015*fade))*29000)
            chunk.extend(struct.pack('<hh',left,right))
        wav.writeframes(chunk)
print(out)
