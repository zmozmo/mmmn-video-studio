"""MMMN experimental LOCAL Burmese ASR long-narration segmenter (NOT app integrated).

Uses an already-present freococo/myanmar_asr Python model dir and local FFmpeg.
NO model download, cloud calls, user-file overwrite, time alignment certification,
photo generation or unattended scene changes. Never train or upload audio.
SRT cue times are clip-level approximations ONLY and need original-manuscript
agreement checks plus manual listening before use in any film.
"""
import argparse,bisect,importlib.util,json,math,os,re,subprocess,sys,tempfile,shutil
from pathlib import Path

MAX_SECONDS=5400
def split_duration(seconds,pauses=(),target=18,min_chunk=7,max_chunk=28):
    if not isinstance(seconds,(int,float)) or not math.isfinite(seconds) or not 0<seconds<=MAX_SECONDS:
        raise ValueError("Narration duration must be positive and <= 5400 seconds")
    if not 0<min_chunk<target<=max_chunk<=60:
        raise ValueError("Invalid segment bounds")
    points=sorted(float(p) for p in pauses
                  if isinstance(p,(int,float)) and math.isfinite(p) and 0<p<seconds)
    result=[]
    start=0.
    while start < seconds-0.00001:
        remain=seconds-start
        if remain<=max_chunk:
            stop=seconds
            pause_aligned=False
        else:
            low=start+min_chunk
            high=min(start+max_chunk,seconds-1)
            left=bisect.bisect_left(points,low)
            right=bisect.bisect_right(points,high)
            available=points[left:right]
            if available:
                stop=min(available,key=lambda p:(abs(p-(start+target)),p))
                pause_aligned=True
            else:
                stop=start+target
                pause_aligned=False
        if stop<=start or stop>seconds:
            raise ValueError("Chunk boundary failed safety validation")
        result.append({"start":round(start,3),"end":round(stop,3),
                       "pause_aligned":pause_aligned})
        start=stop
        if len(result)>1000:
            raise ValueError("Too many segments; refusing to overrun narration")
    if not result or abs(result[0]["start"])>.001 or abs(result[-1]["end"]-seconds)>.002:
        raise ValueError("Audio coverage was not complete")
    for a,b in zip(result,result[1:]):
        if abs(a["end"]-b["start"])>.002:raise ValueError("Gap or overlap in audio")
        if a["end"]-a["start"]>max_chunk+.002:raise ValueError("Overlong audio segment")
    return result

def timestamp(t):
    if not isinstance(t,(int,float)) or not math.isfinite(t) or t<0 or t>MAX_SECONDS:
        raise ValueError("Invalid subtitle time")
    milliseconds=round(t*1000)
    hours,rest=divmod(milliseconds,3600000)
    minutes,rest=divmod(rest,60000)
    seconds,ms=divmod(rest,1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{ms:03d}"

def srt_from_segments(segments,predictions):
    if len(segments)!=len(predictions):raise ValueError("Each chunk requires one prediction")
    output=[]
    for segment,text in zip(segments,predictions):
        if not isinstance(text,str):raise TypeError("Invalid model transcription")
        # No invented subtitles for silence or failed segments.
        text=" ".join(text.replace("\r"," ").replace("\n"," ").split())
        if len(text)>4000:raise ValueError("Implausibly long ASR response")
        if not any("\u1000"<=x<="\u109f" for x in text):continue
        start,end=segment["start"],segment["end"]
        if not 0<=start<end<=MAX_SECONDS:raise ValueError("Unsafe ASR timing")
        output.append(str(len(output)+1)+"\n"+
           timestamp(start)+" --> "+timestamp(end)+"\n"+text+"\n")
    if not output:raise ValueError("No usable Burmese speech; do not save empty SRT")
    return "\n".join(output)+"\n"

def run_program(args,timeout=120):
    p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,
        encoding="utf-8",errors="replace")
    if p.returncode:raise RuntimeError("Local FFmpeg/FFprobe failed: "+p.stderr[-350:])
    return p.stdout,p.stderr

def expose_local_ffmpeg_to_embedded_transcriber(ffmpeg):
    """Third-party Burmese ASR calls the basename 'ffmpeg' via subprocess.run.
    The packaged Studio FFmpeg is not in system PATH on clean Windows. Expose
    only the validated local binary directory in this CHILD PROCESS PATH,
    never modify global Windows PATH or fetch/download a new executable.
    """
    path=Path(ffmpeg)
    resolved=path.resolve() if path.is_file() else shutil.which(str(ffmpeg))
    if not resolved or not Path(resolved).is_file():
        raise FileNotFoundError("Local FFmpeg executable not found; no cloud fallback")
    folder=str(Path(resolved).resolve().parent)
    current=os.environ.get("PATH","")
    if folder not in current.split(os.pathsep):
        os.environ["PATH"]=folder+os.pathsep+current
    return folder

def probe_seconds(source,ffprobe):
    out,_=run_program([ffprobe,"-v","error","-show_entries",
        "format=duration","-of","default=noprint_wrappers=1:nokey=1",str(source)])
    return float(out.strip())

def detect_pause_midpoints(source,ffmpeg):
    _,err=run_program([ffmpeg,"-hide_banner","-nostats","-i",str(source),
       "-af","silencedetect=n=-35dB:d=0.35","-f","null","-"],timeout=900)
    starts=re.findall(r"silence_start:\s*([0-9.]+)",err)
    ends=re.findall(r"silence_end:\s*([0-9.]+)",err)
    # Skip ambiguous unmatched silence annotations; fixed chunks will be flagged.
    count=min(len(starts),len(ends))
    return [(float(starts[i])+float(ends[i]))/2 for i in range(count)
            if float(starts[i])<=float(ends[i])]

def load_model_only_from_disk(location):
    location=Path(location).resolve()
    required=("transcribe.py","model.py","model.safetensors","vocab.json")
    if not location.is_dir() or any(not (location/x).is_file() for x in required):
        raise FileNotFoundError("Local Myanmar model files missing; no network download will occur")
    sys.path.insert(0,str(location))
    spec=importlib.util.spec_from_file_location("mmmn_local_burmese_asr",location/"transcribe.py")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.BurmeseASR(device="cpu")  # Load weights ONCE for entire novel.

def transcribe(source,model,ffmpeg,segments):
    predictions=[]
    with tempfile.TemporaryDirectory(prefix="mmmn-private-voice-") as tmp:
        folder=Path(tmp)
        for i,segment in enumerate(segments):
            path=folder/"segment.wav"
            duration=segment["end"]-segment["start"]
            run_program([ffmpeg,"-hide_banner","-loglevel","error","-nostdin",
                "-y","-ss",f'{segment["start"]:.3f}',"-i",str(source),
                "-t",f"{duration:.3f}","-ac","1","-ar","16000",
                "-acodec","pcm_s16le",str(path)],timeout=180)
            if not path.exists() or path.stat().st_size<44:
                raise RuntimeError("FFmpeg did not produce a valid private local chunk")
            predictions.append(model.transcribe(str(path)))
            path.unlink(missing_ok=True)
            print("PRIVATE CPU ASR segment",i+1,"/",len(segments),flush=True)
    return predictions

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--model-dir",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--ffmpeg",default="ffmpeg")
    p.add_argument("--ffprobe",default="ffprobe")
    p.add_argument("--dry-run",action="store_true")
    args=p.parse_args()
    original=args.input.resolve()
    target=args.output.resolve()
    if not original.is_file() or not original.stat().st_size:
        raise FileNotFoundError("Missing local original voice recording")
    if target.exists():raise FileExistsError("Never overwrite an existing user SRT")
    if target==original:raise ValueError("Output must never be the original audio")
    # The third-party local model internally spawns "ffmpeg" by name.
    # Use the exact FFmpeg bundled with Studio in THIS subprocess only.
    expose_local_ffmpeg_to_embedded_transcriber(args.ffmpeg)
    seconds=probe_seconds(original,args.ffprobe)
    if not 0<seconds<=MAX_SECONDS:raise ValueError("Only narration up to 90 minutes is accepted")
    pauses=detect_pause_midpoints(original,args.ffmpeg)
    segments=split_duration(seconds,pauses)
    if args.dry_run:
        print(json.dumps({"status":"SEGMENT_PLAN_ONLY",
           "chunks":len(segments),"duration_seconds":seconds,
           "forced_unsilenced_cuts":sum(not c["pause_aligned"] for c in segments)},
           indent=2))
        return
    # No cloud; no model download; do not make empty or partial SRT visible.
    model=load_model_only_from_disk(args.model_dir)
    lines=srt_from_segments(segments,transcribe(original,model,args.ffmpeg,segments))
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile("w",encoding="utf-8",newline="\n",
       prefix=".mmmn-asr-review-",suffix=".tmp",dir=target.parent,
       delete=False) as f:
        provisional=Path(f.name)
        try:
            f.write(lines)
            f.flush()
            os.fsync(f.fileno())
        except BaseException:
            provisional.unlink(missing_ok=True)
            raise
    try:
        if target.exists():raise FileExistsError("Do not overwrite corrected SRT")
        # A successful atomic file write still does not approve subtitles.
        provisional.rename(target)
    finally:
        provisional.unlink(missing_ok=True)
    print("PRIVATE REVIEW-ONLY SRT created. Timings are clip estimates, NOT aligned words.")

if __name__=="__main__":main()
