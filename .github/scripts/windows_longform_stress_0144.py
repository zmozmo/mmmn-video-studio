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
import shutil
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

    # Exercise an Explorer-style external copy and copy-back, without using
    # shell commands or touching user data. This is a SECOND synthetic folder,
    # NOT a guarantee of physical removable-USB media reliability.
    source=fixture.DATA/"snapshots"/snap["id"]
    external=ROOT/"simulated-external-drive"/snap["id"]
    shutil.copytree(source,external)
    contents=[x for x in source.rglob("*") if x.is_file()]
    assert len(contents)>=3
    for original_file in contents:
        relative=original_file.relative_to(source)
        assert sha(external/relative)==sha(original_file),(
            "External copy changed synthetic backup byte content")
    shutil.rmtree(source)
    assert not source.exists(),"Test did not remove simulated local snapshot"
    shutil.copytree(external,source)
    assert app.api("verify_local_backup",{"id":snap["id"]})["verified"]
    assert sha(source/"media"/f"{MEDIA_ID}.wav")==digest
    print("PASS: simulated external-folder backup copy, local loss, copy-back and SHA-256 verification",flush=True)


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


def verify_export_presets(app,ffprobe):
    """Actually encode and inspect all four full-size social media export presets.

    Exercise the packaged offline renderer through the running, installed
    Windows application. A simple 1-second synthetic WAV + PNG is the only input.
    """
    audio_id="preset-audio-qa0144"
    image_id="preset-image-qa0144"
    app.upload(audio_id,"wav",fixture.sample_audio())
    app.upload(image_id,"png",fixture.PNG)
    presets={
        "youtube":(1920,1080),
        "tiktok":(1080,1920),
        "facebook":(1080,1350),
        "square":(1080,1080),
    }
    for index,(preset,dimensions) in enumerate(presets.items(),start=60):
        params={
            "chapterNumber":index,
            "sourceVideoId":audio_id,
            "sourceVideoExt":"wav",
            "scenes":[{"assetId":image_id,"ext":"png","duration":1,
                       "motion":"still"}],
            "preset":preset,
            "recordedSeconds":1,
            "transitionMode":"cut",
            "quality":"full",
        }
        job=app.api("start_render_job",params)
        jid=job["id"]
        deadline=time.monotonic()+160
        while time.monotonic()<deadline:
            state=app.api("get_render_job_status",{"id":jid})
            if state["status"] in ("complete","failed","cancelled"):
                break
            time.sleep(.5)
        else:
            app.api("cancel_render_job",{"id":jid})
            raise TimeoutError(f"Preset render timeout: {preset}")
        assert state["status"]=="complete",f"{preset}: {state}"
        out=Path(state["output"])
        assert out.is_file() and out.stat().st_size>1024
        proc=subprocess.run([str(ffprobe),"-v","error","-count_frames",
            "-show_entries","stream=codec_type,codec_name,width,height,nb_read_frames:format=duration",
            "-of","json",str(out)],capture_output=True,text=True,timeout=100,check=True)
        info=json.loads(proc.stdout)
        streams={x["codec_type"]:x for x in info["streams"]}
        video=streams["video"]
        assert (video["width"],video["height"])==dimensions,(
            f"Wrong {preset} export resolution: {video}")
        assert video["codec_name"]=="h264" and streams["audio"]["codec_name"]=="aac"
        assert int(video["nb_read_frames"])==30,(
            f"{preset}: 1 second at 30fps should have exactly 30 frames")
        duration=float(info["format"]["duration"])
        assert .7<=duration<=1.5, f"{preset} shortened/extended: {duration}"
        print(f"PASS: {preset} FULL QUALITY {dimensions[0]}x{dimensions[1]} "
              f"H.264/AAC, 30frames, {duration:.2f}s",flush=True)
    print("PASS: all four public Windows full-quality MP4 export presets",flush=True)


def make_short_wav(seconds):
    """Synthetic silence at 16kHz. Never uses real/private narration."""
    import io
    stream=io.BytesIO()
    with wave.open(stream,"wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(16000)
        for _ in range(seconds):
            output.writeframesraw(b"\0\0"*16000)
    return stream.getvalue()

def verify_full_hd_multi_scene_and_cancel(app,ffprobe):
    """A real 45s HD multi-scene MP4, cross-dissolve, cancel and retry.

    15-minute WAV IMPORT alone is not a long MP4 render. This explicitly
    tests encoded video durations, frame totals, and cancellation cleanup.
    """
    from urllib.error import HTTPError
    audio_id="long-hd-audio-qa0144"
    photo_id="long-hd-photo-qa0144"
    app.upload(audio_id,"wav",make_short_wav(45))
    app.upload(photo_id,"png",fixture.PNG)
    available_audio={45:audio_id}

    def begin(chapter,seconds,transition):
        # The renderer correctly rejects mismatched narration and video
        # duration. Every distinct timeline must have matching source WAV.
        if seconds not in available_audio:
            unique_id=f"long-hd-audio-{seconds}-qa0144"
            app.upload(unique_id,"wav",make_short_wav(seconds))
            available_audio[seconds]=unique_id
        scene_count=6 if seconds>=300 else 3
        scenes=[
            {"assetId":photo_id,"ext":"png","duration":seconds/scene_count,
             "motion":"still"} for _ in range(scene_count)
        ]
        return app.api("start_render_job",{
            "chapterNumber":chapter,"sourceVideoId":available_audio[seconds],
            "sourceVideoExt":"wav","scenes":scenes,"preset":"youtube",
            "recordedSeconds":seconds,"transitionMode":transition,
            "quality":"full",
        })

    def finish(job,limit=270):
        deadline=time.monotonic()+limit
        while time.monotonic()<deadline:
            state=app.api("get_render_job_status",{"id":job["id"]})
            if state["status"] in ("complete","cancelled","failed"):
                return state
            time.sleep(.5)
        app.api("cancel_render_job",{"id":job["id"]})
        raise TimeoutError("45sec Full HD encode or cancellation exceeded deadline")

    def check_video(result,expected_frames,expected_seconds,label):
        assert result["status"]=="complete",f"{label}: {result}"
        out=Path(result["output"])
        assert out.is_file() and out.stat().st_size>1024,f"{label} missing MP4"
        proc=subprocess.run([str(ffprobe),"-v","error","-count_frames",
            "-show_entries","stream=codec_type,codec_name,width,height,nb_read_frames:format=duration",
            "-of","json",str(out)],check=True,capture_output=True,text=True,timeout=120)
        info=json.loads(proc.stdout)
        streams={s["codec_type"]:s for s in info["streams"]}
        video=streams["video"]
        frames=int(video["nb_read_frames"])
        duration=float(info["format"]["duration"])
        assert (video["width"],video["height"])==(1920,1080),f"{label}: wrong resolution"
        assert video["codec_name"]=="h264" and streams["audio"]["codec_name"]=="aac"
        assert frames==expected_frames,f"{label}: missing video frames {frames}/{expected_frames}"
        assert abs(duration-expected_seconds)<.3,f"{label}: {duration} versus {expected_seconds}"
        print(f"PASS: {label}, {frames} Full HD frames, {duration:.3f}s, H.264/AAC",flush=True)
        return out

    first=finish(begin(70,45,"cut"))
    first_path=check_video(first,1350,45,"45-second 3-scene full-quality 1080p hard-cut MP4")
    before=sha(first_path)
    # Repeat to exercise the persistent reproducible scene cache; original must
    # remain byte-identical across later app actions, not necessarily new output.
    second=finish(begin(71,45,"cut"))
    check_video(second,1350,45,"45-second 3-scene repeated MP4/cache path")
    assert sha(first_path)==before,"Previous export modified on repeat render"

    # Transition makes different frame accounting than cuts. Full HD, 3 scenes.
    # Use 9 seconds for a fast transition test with a distinct chapter.
    dissolve=finish(begin(72,9,"dissolve"),limit=150)
    check_video(dissolve,270,9,"9-second Full HD multi-scene dissolve MP4")

    # Begin 45s render and immediately request cancel. No stale active job or
    # partially-published final MP4 may be left behind.
    current=begin(73,36,"cut")
    try:
        begin(74,36,"cut")
    except HTTPError as exc:
        assert exc.code in (400,409,422),f"Concurrent render returned {exc.code}"
    else:
        raise AssertionError("Second full-HD render unexpectedly started concurrently")
    app.api("cancel_render_job",{"id":current["id"]})
    state=finish(current,limit=90)
    assert state["status"]=="cancelled",f"Cancel did not stop export safely: {state}"
    assert state.get("output") is None,"Cancelled render published an output path"
    assert sha(first_path)==before,"Cancelled render corrupted an earlier MP4"
    print("PASS: concurrent export blocked; cancel stopped FFmpeg; prior MP4 intact",flush=True)

    # Cancellation must not wedge the worker or prevent a subsequent export.
    recovery=finish(begin(75,3,"cut"),limit=120)
    check_video(recovery,90,3,"retry after cancellation")
    print("PASS: multi-scene export lifecycle: encode, cache, dissolve, cancel, retry",flush=True)

    # Core production-style stress: not just a 15-minute WAV IMPORT or
    # a one-second MP4. Actually encode a continuous 5-MINUTE FULL HD MP4
    # with six scenes and 30fps/9,000 verified frames using packaged FFmpeg.
    started=time.monotonic()
    five_minutes=finish(begin(76,300,"cut"),limit=600)
    check_video(five_minutes,9000,300,"5-minute 1080p six-scene offline MP4")
    print(f"PASS: continuous 300-second real 1080p export encoded in "
          f"{time.monotonic()-started:.1f}s on disposable Windows runner",flush=True)

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
        verify_export_presets(app,ffprobe)
        verify_full_hd_multi_scene_and_cancel(app,ffprobe)
    print("WINDOWS 0.14.4 PUBLISHED-BINARY LONGFORM + FOUR-PRESET + 5-MINUTE-FULL-HD QA PASS",flush=True)

if __name__=="__main__":
    main()
