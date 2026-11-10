"""REAL third-party public Burmese speech model + chunker E2E on disposable CPU.

Combines short public FLEURS Burmese clips into a synthetic longer local
recording. Never uses or uploads private MMMN manuscripts or author voices.
Does not certify true novel-length audio or word-perfect timings.
"""
import hashlib,os,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
import soundfile as sf
from datasets import load_dataset

def run(args):
 p=subprocess.run(args,capture_output=True,text=True,encoding="utf-8",
  errors="replace",timeout=600)
 if p.returncode:raise RuntimeError(p.stderr[-1200:])
 return p.stdout

def main():
 model=Path(os.environ["MMMN_CANDIDATE_MODEL_DIR"]).resolve()
 sample=list(load_dataset("google/fleurs","my_mm",split="test",streaming=True).take(8))
 pieces=[]
 for row in sample:
  audio=row["audio"]
  arr=np.asarray(audio["array"],dtype=np.float32)
  sr=int(audio["sampling_rate"])
  if len(arr)/sr<2:continue
  pieces.append((arr,sr))
  if len(pieces)>=6:break
 assert len(pieces)==6
 with tempfile.TemporaryDirectory(prefix="mmmn-third-party-public-") as folder:
  path=Path(folder)
  chunks=[]
  for i,(arr,sr) in enumerate(pieces):
   wav=path/f"public-{i}.wav"
   resampled=path/f"resampled-{i}.wav"
   sf.write(wav,arr,sr)
   run(["ffmpeg","-hide_banner","-loglevel","error","-y",
    "-i",str(wav),"-ar","16000","-ac","1",str(resampled)])
   decoded,rate=sf.read(resampled,dtype="float32")
   assert rate==16000
   chunks.extend([decoded,np.zeros(rate//2,dtype=np.float32)])
  combined=np.concatenate(chunks)
  recording=path/"PUBLIC-FLEURS-CONCAT.wav"
  sf.write(recording,combined,16000)
  original=hashlib.sha256(recording.read_bytes()).hexdigest()
  target=path/"PUBLIC-SYNTHETIC-REVIEW-ONLY.srt"
  print("PUBLIC concat seconds",round(len(combined)/16000,2),flush=True)
  out=run([sys.executable,"scripts/burmese_asr_chunker_0153.py",
   "--input",str(recording),"--model-dir",str(model),
   "--output",str(target)])
  print("LOCAL MODEL RESULT:",out[-700:],flush=True)
  assert target.is_file()
  data=target.read_text(encoding="utf-8")
  assert data.count("-->")>=2,"No long-form segment-level timings"
  assert any("\u1000"<=c<="\u109f" for c in data)
  assert hashlib.sha256(recording.read_bytes()).hexdigest()==original
  assert "00:" in data and "-->" in data
  assert len(data.encode("utf-8"))<100_000
  again=subprocess.run([sys.executable,"scripts/burmese_asr_chunker_0153.py",
   "--input",str(recording),"--model-dir",str(model),
   "--output",str(target)],capture_output=True,text=True)
  assert again.returncode!=0,"Must NEVER overwrite private reviewed SRT"
  print("PASS: REAL Burmese CPU model, multiple local chunks, actual review-only SRT,"+
   " no source audio changes, corrected subtitle overwrite blocked.",flush=True)
  print("CAUTION: PUBLIC sample concat is NOT a real 90min author's novel.",flush=True)
if __name__=="__main__":main()
