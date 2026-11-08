"""Independent QA of the exact public Windows 0.14.4 installer.
Synthetic 15-minute WAV streaming, verified backup/restore, 3-chapter MP4 join.
No private data, no online service, no need to rebuild the EXE.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time
import wave

ROOT = Path(os.environ["RUNNER_TEMP"])/"mmmn-0144-longform-acceptance"
os.environ["MMMN_UPGRADE_TEST_ROOT"] = str(ROOT)
spec = importlib.util.spec_from_file_location(
    "mmmn_qa_fixture", Path(__file__).with_name("windows_upgrade_0140_to_0144.py"))
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
MEDIA_ID="synthetic-long-narration-0144"
CHAPTERS=["chapter-1-qa0144aaa.mp4","chapter-2-qa0144bbb.mp4","chapter-3-qa0144ccc.mp4"]

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def make_wav(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),"wb") as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000)
        one_second=b"\0\0"*16000
        for _ in range(900):
            w.writeframesraw(one_second)
    assert 28_000_000<path.stat().st_size<30_000_000

def upload_long_wav(app,path):
    total=path.stat().st_size
    digest=sha(path)
    app.api("begin_media_import",{"id":MEDIA_ID,"ext":"wav","total":total})
    offset=0
    with path.open("rb") as f:
        while chunk:=f.read(1024*1024):
            result=app.api("import_media_chunk",binary=chunk,headers={
                "x-media-id":MEDIA_ID,"x-media-offset":offset,
                "x-media-sha256":hashlib.sha256(chunk).hexdigest()})
            offset+=len(chunk)
            assert result==offset, f"Chunk offset mismatch: {result}/{offset}"
    assert offset==total
    result=app.api("finalize_media_import",{"id":MEDIA_ID})
    assert result["sha256"]==digest and result["size"]==total
    assert sha(fixture.DATA/"media"/f"{MEDIA_ID}.wav")==digest
    print(f"PASS: real EXE streamed {total:,} WAV bytes, every chunk SHA-256 verified",flush=True)
    return digest

def backup_restore_long_wav(app,digest):
    original={
        "title":"SYNTHETIC FIFTEEN MINUTE NARRATION",
        "assets":[{"id":MEDIA_ID,"name":"narration.wav","nativeStored":True}],
        "chapters":[{"id":"synthetic-qa-chapter-1","number":1,
                     "title":"SYNTHETIC LONG CHAPTER",
                     "text":"Synthetic fifteen-minute narration",
                     "audioAssetId":MEDIA_ID,"scenes":[]}]}
    app.api("save_project_state",{"json":json.dumps(original)})
    snap=app.api("create_full_local_backup")
    assert snap["verified"] and snap["files"]==1
    verified=app.api("verify_local_backup",{"id":snap["id"]})
    assert verified["verified"] and verified["bytes"]>28_000_000
    oldfile=fixture.DATA/"media"/f"{MEDIA_ID}.wav"
    backup=fixture.DATA/"snapshots"/snap["id"]/"media"/f"{MEDIA_ID}.wav"
    assert sha(backup)==digest
    edited=json.loads(json.dumps(original))
    edited["chapters"][0]["text"]="SYNTHETIC ACCIDENTAL EDIT"
    app.api("save_project_state",{"json":json.dumps(edited)})
    restored=app.api("restore_local_backup",{"id":snap["id"]})
    assert restored["restored"] and restored["media"]==1
    content=json.loads(app.api("load_project_state"))
    assert content["chapters"][0]["text"]==original["chapters"][0]["text"]
    new_id=content["chapters"][0]["audioAssetId"]
    assert new_id!=MEDIA_ID
    assert sha(fixture.DATA/"media"/f"{new_id}.wav")==digest
    assert sha(oldfile)==digest and app.api("verify_local_backup",{"id":snap["id"]})["verified"]
    print("PASS: large full-media backup, real restore, original WAV and metadata intact",flush=True)

def make_chapter_mp4s(exe):
    found=[p for p in exe.parent.rglob("ffmpeg.exe") if p.parent.name.lower()=="bin"]
    assert found,"Bundled ffmpeg.exe not found in published installed app"
    ffmpeg=found[0]
    ffprobe=ffmpeg.with_name("ffprobe.exe")
    assert ffprobe.is_file(),"Bundled ffprobe.exe not found"
    directory=fixture.DATA/"exports"
    directory.mkdir(parents=True,exist_ok=True)
    hashes={}
    for i,name in enumerate(CHAPTERS):
        path=directory/name
        cmd=[str(ffmpeg),"-nostdin","-hide_banner","-loglevel","error","-y",
             "-f","lavfi","-i",f"color=c=0x{(i+1)*300011:06x}:s=320x180:r=30:d=2",
             "-f","lavfi","-i","sine=frequency=440:sample_rate=44100:duration=2",
             "-t","2","-c:v","libx264","-pix_fmt","yuv420p","-r","30",
             "-c:a","aac","-b:a","96k","-movflags","+faststart",str(path)]
        proc=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
        assert proc.returncode==0,proc.stderr[-1600:]
        assert path.stat().st_size>1024
        hashes[name]=sha(path)
    print("PASS: installed bundled FFmpeg encoded 3 synthetic H.264/AAC chapters",flush=True)
    return ffprobe,hashes

def combine_book(app,ffprobe,hashes):
    response=app.api("start_book_merge_job",{"filenames":CHAPTERS})
    jid=response["id"]
    deadline=time.monotonic()+150
    while time.monotonic()<deadline:
        state=app.api("get_render_job_status",{"id":jid})
        if state["status"] in ("complete","failed","cancelled"):
            break
        time.sleep(.4)
    else:
        app.api("cancel_render_job",{"id":jid})
        raise TimeoutError("Full book merge timed out")
    assert state["status"]=="complete",repr(state)
    output=Path(state["output"])
    assert output.is_file() and output.name.startswith("book-") and output.stat().st_size>1024
    proc=subprocess.run([str(ffprobe),"-v","error","-count_frames","-show_entries",
         "stream=codec_type,codec_name,nb_read_frames:format=duration",
         "-of","json",str(output)],capture_output=True,text=True,timeout=90,check=True)
    info=json.loads(proc.stdout)
    streams={s["codec_type"]:s for s in info["streams"]}
    frames=int(streams["video"]["nb_read_frames"])
    seconds=float(info["format"]["duration"])
    assert streams["video"]["codec_name"]=="h264" and streams["audio"]["codec_name"]=="aac"
    assert frames==180, f"Expected 180 frames from 3 chapters, got {frames}"
    assert 5.6<seconds<6.5,f"Incomplete merged book MP4: {seconds}s"
    for name,digest in hashes.items():
        assert sha(fixture.DATA/"exports"/name)==digest,"Source chapter MP4 changed"
    print(f"PASS: 3 chapter MP4s joined to {seconds:.3f}s, {frames} frames, H.264/AAC",flush=True)

def main():
    exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    assert exe.is_file(),"Published EXE not installed"
    ROOT.mkdir(parents=True,exist_ok=True)
    wav=ROOT/"synthetic-fifteen-minute.wav"
    make_wav(wav)
    with fixture.Session(exe) as app:
        digest=upload_long_wav(app,wav)
        backup_restore_long_wav(app,digest)
        ffprobe,hashes=make_chapter_mp4s(exe)
        combine_book(app,ffprobe,hashes)
    print("WINDOWS 0.14.4 PUBLISHED-BINARY LONG-FORM OFFLINE QA PASS",flush=True)

if __name__=="__main__":
    main()
