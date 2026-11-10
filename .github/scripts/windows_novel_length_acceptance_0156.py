"""True full-novel 90/120 minute published-Windows-EXE MP4 acceptance.
Synthetic WAV/image only. Verifies every decoded 1080p frame, source hashes,
backup/restore, and audio/video length. No owner data, API, or source build.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time
import wave

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1048576),b""):
            h.update(chunk)
    return h.hexdigest()

def make_wav(path,seconds):
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),"wb") as out:
        out.setnchannels(1);out.setsampwidth(2);out.setframerate(16000)
        second=b"\0\0"*16000
        for _ in range(seconds):
            out.writeframesraw(second)
    assert path.stat().st_size==44+seconds*32000

def upload(app,path,mid):
    digest=sha(path);total=path.stat().st_size
    app.api("begin_media_import",{"id":mid,"ext":"wav","total":total})
    offset=0
    with path.open("rb") as source:
        while chunk:=source.read(1048576):
            received=app.api("import_media_chunk",binary=chunk,headers={
                "x-media-id":mid,"x-media-offset":offset,
                "x-media-sha256":hashlib.sha256(chunk).hexdigest()})
            offset+=len(chunk)
            assert received==offset,"Streamed WAV offset mismatch"
    assert offset==total
    response=app.api("finalize_media_import",{"id":mid})
    assert response["sha256"]==digest and response["size"]==total
    print(f"PASS: {total:,} synthetic WAV bytes uploaded with chunk verification",flush=True)
    return digest

def wait_for_job(app,jobid,minutes):
    deadline=time.monotonic()+2600
    last_report=0
    while time.monotonic()<deadline:
        state=app.api("get_render_job_status",{"id":jobid})
        if state["status"] in ("complete","failed","cancelled"):
            return state
        if time.monotonic()-last_report>=30:
            last_report=time.monotonic()
            print(f"{minutes}min MP4 encode: {state['status']}, "
                  f"{state.get('percent')}%, {state.get('phase')}",flush=True)
        time.sleep(1.5)
    app.api("cancel_render_job",{"id":jobid})
    raise TimeoutError("Novel render exceeded safe QA timeout")

def verify_mp4(probe,output,seconds):
    outcome=subprocess.run([str(probe),"-v","error","-count_frames",
        "-show_entries",
        "stream=codec_type,codec_name,width,height,r_frame_rate,nb_read_frames:format=duration",
        "-of","json",str(output)],capture_output=True,text=True,
        check=True,timeout=900)
    info=json.loads(outcome.stdout)
    streams={x.get("codec_type"):x for x in info["streams"]}
    vid=streams["video"];aud=streams["audio"]
    frames=int(vid["nb_read_frames"]);duration=float(info["format"]["duration"])
    assert (vid["width"],vid["height"])==(1920,1080),vid
    assert vid["codec_name"]=="h264" and aud["codec_name"]=="aac",streams
    assert vid["r_frame_rate"] in ("30/1","30"),vid
    assert frames==seconds*30,f"Incorrect video frames {frames}/{seconds*30}"
    assert abs(duration-seconds)<.3,f"Wrong video length {duration}/{seconds}"
    print(f"PASS: 1920x1080 {seconds//60}min full MP4, "
          f"{frames:,} frames, {duration:.3f}s, H.264/AAC",flush=True)

def run(minutes):
    seconds=minutes*60
    root=Path(os.environ["RUNNER_TEMP"])/f"mmmn-novel-length-{minutes}min"
    os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(root)
    path=Path(__file__).with_name("windows_upgrade_0140_to_0156.py")
    spec=importlib.util.spec_from_file_location("mmmn_legacy_fixture",path)
    fix=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fix)
    exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    assert exe.is_file(),"Previously published app is not installed"
    probe_candidates=[p.with_name("ffprobe.exe") for p in exe.parent.rglob("ffmpeg.exe")
                      if p.parent.name.lower()=="bin"]
    assert probe_candidates and probe_candidates[0].is_file()
    probe=probe_candidates[0]
    root.mkdir(parents=True,exist_ok=True)
    wav=root/f"synthetic-{minutes}min-narration.wav"
    make_wav(wav,seconds)
    original_sha=sha(wav)
    aid=f"novel-{minutes}m-audio-qa0156"
    iid=f"novel-{minutes}m-picture-qa0156"
    with fix.Session(exe) as app:
        digest=upload(app,wav,aid)
        assert digest==original_sha
        app.upload(iid,"png",fix.PNG)
        project={
            "title":f"SYNTHETIC {minutes} MINUTE NOVEL - NO PRIVATE DATA",
            "chapters":[{"id":"entire-novel","number":1,"title":"Full narrated novel",
                "text":"Synthetic end-to-end Windows test",
                "audioAssetId":aid,"scenes":[]}],
            "assets":[{"id":aid,"name":wav.name,"nativeStored":True},
                      {"id":iid,"name":"synthetic.png","nativeStored":True}]}
        app.api("save_project_state",{"json":json.dumps(project)})
        snap=app.api("create_full_local_backup")
        assert snap["verified"] and snap["files"]==2,snap
        assert app.api("verify_local_backup",{"id":snap["id"]})["verified"]
        print("PASS: full-size original WAV+image+manuscript snapshot verified",flush=True)
        scenes=[{"assetId":iid,"ext":"png","duration":seconds/12,
                 "motion":"still"} for _ in range(12)]
        start=time.monotonic()
        job=app.api("start_render_job",{"chapterNumber":minutes,
             "sourceVideoId":aid,"sourceVideoExt":"wav","scenes":scenes,
             "preset":"youtube","recordedSeconds":seconds,
             "transitionMode":"cut","quality":"full"})
        result=wait_for_job(app,job["id"],minutes)
        assert result["status"]=="complete" and result["percent"]==100,result
        output=Path(result["output"])
        assert output.is_file() and output.stat().st_size>1024
        verify_mp4(probe,output,seconds)
        print(f"PASS: full {minutes}min video encoding elapsed "
              f"{time.monotonic()-start:.1f}s on disposable Windows runner",flush=True)
        output_sha=sha(output)
        assert sha(fix.DATA/"media"/f"{aid}.wav")==original_sha
        assert app.api("verify_local_backup",{"id":snap["id"]})["verified"]
        restore=app.api("restore_local_backup",{"id":snap["id"]})
        assert restore["restored"] and restore["media"]==2,restore
        stored=json.loads(app.api("load_project_state"))
        assert stored["title"]==project["title"]
        new_id=stored["chapters"][0]["audioAssetId"]
        assert new_id!=aid
        assert sha(fix.DATA/"media"/f"{new_id}.wav")==original_sha
        assert sha(output)==output_sha,"Backup restore corrupted final long MP4"
        print("PASS: backup/restore verified, long MP4 unchanged, "
              "original WAV preserved",flush=True)
    print(f"WIN 0.15.6 PUBLISHED-EXE {minutes} MINUTE REAL 1080P "
          "COMPLETE-NOVEL ACCEPTANCE PASS",flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--minutes",type=int,choices=[90,120],required=True)
    run(parser.parse_args().minutes)
