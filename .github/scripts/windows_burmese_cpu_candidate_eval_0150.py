"""Research-only CPU evaluation of a public Burmese ASR model.

This NEVER uses private novel/voice data and NEVER claims a novel-wide
accuracy benchmark from one publisher-supplied short example. Does not
change the MMMN Windows installer or request an external API for user data.
"""
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

EXPECTED="စစ်ကောင်စီအတွက်လေယာဉ်ဆီရောင်းချဖြန့်ဖြူးပေးနေတဲ့လူ"

def clean(value):
    s=unicodedata.normalize("NFC",value)
    return "".join(x for x in s if 0x1000 <= ord(x) <= 0x109f)

def distance(a,b):
    prev=list(range(len(b)+1))
    for i,c in enumerate(a,1):
        row=[i]
        for j,d in enumerate(b,1):
            row.append(min(row[-1]+1,prev[j]+1,prev[j-1]+int(c!=d)))
        prev=row
    return prev[-1]

def main():
    location=Path(os.environ["MMMN_CANDIDATE_MODEL_DIR"])
    required=["model.safetensors","transcribe.py","model.py","example.mp3",
              "vocab.json","config.json"]
    assert all((location/p).is_file() for p in required),required
    assert (location/"model.safetensors").stat().st_size > 50_000_000
    start=time.monotonic()
    finished=subprocess.run([sys.executable,"transcribe.py","example.mp3",
        "--device","cpu"],cwd=location,capture_output=True,text=True,
        encoding="utf-8",errors="replace",timeout=240,env={
            **os.environ,"CUDA_VISIBLE_DEVICES":"","HF_HUB_OFFLINE":"1",
            "TRANSFORMERS_OFFLINE":"1"})
    if finished.returncode:
        raise RuntimeError("CPU model inference failed: "+
             finished.stderr[-1400:])
    lines=[x.strip() for x in finished.stdout.splitlines() if clean(x)]
    if not lines:raise ValueError("Model produced no Myanmar characters")
    # Prefer the last line with Burmese as the decoded model result.
    # The model authors' example sentence is the only printed reference.
    predicted=clean(lines[-1])
    reference=clean(EXPECTED)
    cer=distance(predicted,reference)/max(1,len(reference))
    print("CANDIDATE RESEARCH — official publisher-supplied 3.13-second Burmese sample",flush=True)
    print("Predicted Myanmar characters:",len(predicted),
          "Reference Myanmar characters:",len(reference),flush=True)
    print("Observed single-public-example CER: %.1f%%"%(cer*100),flush=True)
    print("CPU inference wall seconds: %.1f"%(time.monotonic()-start),flush=True)
    print("CAVEAT: publisher test clip, not independent real novel narration;",
          "does NOT certify full 90-min audio, speaker variation or timestamps.",flush=True)
    if len(predicted)<10 or cer>1.0:
        raise AssertionError("Burmese model sample is not useful enough even as a CPU smoke test")
    print("PASS: open licensed Burmese-specific CPU ASR inference smoke test only",flush=True)

if __name__=="__main__":main()
