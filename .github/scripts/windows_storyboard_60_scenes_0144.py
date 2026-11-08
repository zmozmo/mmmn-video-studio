"""Full-quality 60 DISTINCT image shots / 15-minute offline dissolve acceptance.
Runs EXACT verified public Windows EXE; generated synthetic data only. This
exercises shot complexity independently of 90/120min video length acceptance.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import struct
import subprocess
import time
import zlib

root=Path(os.environ["RUNNER_TEMP"])/"mmmn-0144-60-scene-acceptance"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(root)

def mod(name,path):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(path))
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

novel=mod("qa_novel_helpers","windows_novel_length_acceptance_0144.py")
fix=mod("qa_installed_session","windows_upgrade_0140_to_0144.py")

def png_rgb(index,width=128,height=72):
    # Encode 60 distinct valid RGB PNGs without downloading image libraries.
    rgb=bytes(((index*53)%256,(index*97)%256,(index*173)%256))
    raw=(b"\0"+rgb*width)*height
    def chunk(name,body):
        return (struct.pack(">I",len(body))+name+body+
                struct.pack(">I",zlib.crc32(name+body)&0xffffffff))
    head=struct.pack(">IIBBBBB",width,height,8,2,0,0,0)
    return (b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",head)+
            chunk(b"IDAT",zlib.compress(raw,6))+chunk(b"IEND",b""))

def check(ffprobe,path,seconds):
    process=subprocess.run([str(ffprobe),"-v","error","-count_frames",
      "-show_entries","stream=codec_type,codec_name,width,height,nb_read_frames:format=duration",
      "-of","json",str(path)],capture_output=True,text=True,timeout=600,check=True)
    info=json.loads(process.stdout)
    streams={v["codec_type"]:v for v in info["streams"]}
    v=streams["video"];a=streams["audio"]
    assert (v["width"],v["height"])==(1920,1080)
    assert v["codec_name"]=="h264" and a["codec_name"]=="aac"
    assert int(v["nb_read_frames"])==seconds*30
    assert abs(float(info["format"]["duration"])-seconds)<.3

def main():
    exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    assert exe.is_file(),"Missing verified installed Windows release"
    probe=next((p.with_name("ffprobe.exe") for p in exe.parent.rglob("ffmpeg.exe")
                 if p.parent.name.lower()=="bin"),None)
    assert probe and probe.is_file()
    root.mkdir(parents=True,exist_ok=True)
    seconds=900; audio=root/"synthetic-15minute-60scene.wav"
    novel.make_wav(audio,seconds)
    images=[];assets=[]
    with fix.Session(exe) as app:
        audio_id="sixty-scene-narration-qa0144"
        original=novel.upload(app,audio,audio_id)
        assets.append({"id":audio_id,"name":"synthetic-narration.wav","nativeStored":True})
        for i in range(60):
            mid=f"sixty-scene-image-{i:03d}-qa0144"
            data=png_rgb(i)
            app.upload(mid,"png",data)
            images.append({"assetId":mid,"ext":"png",
                           "duration":seconds/60,"motion":"still"})
            assets.append({"id":mid,"name":f"synthetic-shot-{i:03d}.png",
                           "nativeStored":True})
        project={"title":"SYNTHETIC 60 DISTINCT SHOTS",
                 "chapters":[{"id":"scene-test","number":1,
                    "title":"60-shot full-quality dissolve chapter",
                    "text":"Synthetic only","audioAssetId":audio_id,
                    "scenes":[]}],"assets":assets}
        app.api("save_project_state",{"json":json.dumps(project)})
        backup=app.api("create_full_local_backup")
        assert backup["verified"] and backup["files"]==61,backup
        assert app.api("verify_local_backup",{"id":backup["id"]})["verified"]
        print("PASS: 60 unique PNGs, 15-minute WAV, 61-file verified backup",flush=True)
        started=time.monotonic()
        job=app.api("start_render_job",{"chapterNumber":1,
            "sourceVideoId":audio_id,"sourceVideoExt":"wav",
            "scenes":images,"preset":"youtube","recordedSeconds":seconds,
            "transitionMode":"dissolve","quality":"full"})
        result=novel.wait_for_job(app,job["id"],15)
        assert result["status"]=="complete",result
        output=Path(result["output"])
        assert output.is_file() and output.stat().st_size>1024
        check(probe,output,seconds)
        assert novel.sha(fix.DATA/"media"/f"{audio_id}.wav")==original
        assert app.api("verify_local_backup",{"id":backup["id"]})["verified"]
        print("PASS: 60 DISTINCT images + 59 dissolves, 900-second "
              "1920x1080 H.264/AAC MP4 at exactly 27,000 frames, "
              f"elapsed {time.monotonic()-started:.1f}s on hosted Windows",flush=True)
    print("WINDOWS 0.14.4 60-SCENE DISTINCT STORYBOARD OFFLINE QA PASS",flush=True)

if __name__=="__main__":
    main()
