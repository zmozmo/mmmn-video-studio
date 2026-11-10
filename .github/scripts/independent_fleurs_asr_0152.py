"""Research-only CPU Burmese ASR measurement on third-party FLEURS test speech.
Public licensed clips ONLY; no private narration, no production integration.
Possible training-data overlap with FLEURS is NOT ruled out.
"""
import itertools,json,os,subprocess,sys,tempfile,time,unicodedata
from pathlib import Path
import numpy as np
import soundfile as sf
from datasets import load_dataset

def clean(s):
    return "".join(c for c in unicodedata.normalize("NFC",str(s))
                   if 0x1000<=ord(c)<=0x109f or 0xaa60<=ord(c)<=0xaa7f)
def distance(a,b):
    prev=list(range(len(b)+1))
    for i,c in enumerate(a,1):
        row=[i]
        for j,d in enumerate(b,1):
            row.append(min(row[-1]+1,prev[j]+1,prev[j-1]+(c!=d)))
        prev=row
    return prev[-1]
def infer(location,wav):
    proc=subprocess.run([sys.executable,"transcribe.py",str(wav),"--device","cpu"],
        cwd=location,capture_output=True,text=True,encoding="utf-8",errors="replace",
        timeout=240,env={**os.environ,"HF_HUB_OFFLINE":"1",
                         "TRANSFORMERS_OFFLINE":"1","CUDA_VISIBLE_DEVICES":""})
    if proc.returncode:raise RuntimeError("CPU inference failed: "+proc.stderr[-900:])
    lines=[clean(x) for x in proc.stdout.splitlines()]
    lines=[x for x in lines if len(x)>=3]
    if not lines:raise RuntimeError("Model emitted no Myanmar text")
    return lines[-1]
def main():
    model=Path(os.environ["MMMN_CANDIDATE_MODEL_DIR"]).resolve()
    for f in ("model.safetensors","model.py","transcribe.py","vocab.json"):
        if not (model/f).is_file():raise FileNotFoundError(f)
    dataset=load_dataset("google/fleurs","my_mm",split="test",streaming=True)
    rows=[]
    for idx,example in enumerate(itertools.islice(dataset,50)):
        audio=example.get("audio")
        if not isinstance(audio,dict) or "array" not in audio:
            raise RuntimeError("Public FLEURS audio decoding format unsupported")
        reference=clean(example.get("transcription",""))
        samples=np.asarray(audio["array"],dtype=np.float32)
        sr=int(audio["sampling_rate"])
        seconds=len(samples)/sr
        if len(reference)<10 or not 2<=seconds<=24:continue
        with tempfile.TemporaryDirectory(prefix="mmmn-public-asr-") as d:
            source=Path(d)/"source.wav"
            wav=Path(d)/"input.wav"
            sf.write(str(source),samples,sr,subtype="PCM_16")
            r=subprocess.run(["ffmpeg","-loglevel","error","-y","-i",
                str(source),"-ar","16000","-ac","1",str(wav)],
                capture_output=True,text=True,timeout=90)
            if r.returncode:raise RuntimeError("Local audio decode failed: "+r.stderr[-400:])
            start=time.monotonic()
            prediction=infer(model,wav)
            elapsed=time.monotonic()-start
        edits=distance(reference,prediction)
        rows.append({"public_index":idx,"audio_seconds":round(seconds,2),
                     "reference_chars":len(reference),"edits":edits,
                     "observed_cer":round(edits/len(reference),4),
                     "cpu_seconds":round(elapsed,2)})
        print("Public clip",len(rows),"CER",f"{edits/len(reference):.1%}",
              "CPU seconds",round(elapsed,2),flush=True)
        if len(rows)>=6:break
    if len(rows)<4:raise RuntimeError("Fewer than 4 valid third-party public clips")
    agg=sum(x["edits"] for x in rows)/sum(x["reference_chars"] for x in rows)
    report={"status":"RESEARCH_MEASURED_NOT_PRODUCTION_APPROVED",
        "model":"freococo/myanmar_asr","model_license":"Apache-2.0",
        "dataset":"google/fleurs my_mm test","dataset_license":"CC BY 4.0",
        "examples":rows,"aggregate_cer":round(agg,5),
        "private_audio_used":False,"private_text_used":False,
        "training_overlap_excluded":False,"novel_timing_certified":False,
        "user_app_modified":False}
    Path("public-burmese-asr-0152.json").write_text(
        json.dumps(report,indent=2),encoding="utf-8")
    print("AGGREGATE PUBLIC FLEURS CER",f"{agg:.1%}",flush=True)
    print("No full-length word alignment or private voice evaluated.",flush=True)
if __name__=="__main__":main()
