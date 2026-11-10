"""Exact 0.15.5 released EXE: true 90-minute same-image video acceptance.

Unlike a unit test, this runs the actual major-scene JS planner to construct
the exact scene list, uploads synthetic narration to the installed Windows
app, and encodes a continuous 90-minute 1080p MP4 with the same photo on
both technical segments (3600+1800 seconds). All private assets are excluded.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time

root=Path(os.environ["RUNNER_TEMP"])/"mmmn-0155-same-image-novel"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(root)

def mod(name,path):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(path))
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

novel=mod("qa_0155_novel","windows_novel_length_acceptance_0155.py")
fixture=mod("qa_0155_fixture","windows_upgrade_0140_to_0155.py")

def plan_with_REAL_node(image_id:str):
    # Run the precise JS module shipped in the installer, not a Python
    # reimplementation that might disagree with the actual UI.
    program="""
import {consolidateMajorScenes} from './web/major-scene.mjs';
const id=process.argv[1];
const original=Array.from({length:180},(_,i)=>({
  id:'still-'+i,text:'နေရာတစ်နေရာတည်းတွင် တိတ်ဆိတ်စွာ စကားပြောဆိုနေကြသည်။',
  start:i*30,duration:30,assetId:id,motion:'still',
  imageMatchStatus:'suggested-review',alignment:'estimated'
}));
const plan=consolidateMajorScenes(original);
if(plan.report.majorScenes!==1 || plan.report.renderSegments!==2 ||
   plan.report.technicalSameImageContinuations!==1 ||
   plan.report.narrationSeconds!==5400 ||
   plan.scenes.some(s=>s.assetId!==id || s.duration>3600))
   throw Error('Planner violated quiet 90-minute scene policy or encoder limit');
console.log(JSON.stringify({report:plan.report,scenes:plan.scenes.map(s=>({
  assetId:s.assetId,ext:'png',duration:s.duration,motion:'still'
}))}));
"""
    proc=subprocess.run(["node","--input-type=module","-e",program,image_id],
        capture_output=True,text=True,check=True,timeout=90)
    result=json.loads(proc.stdout)
    assert [x["duration"] for x in result["scenes"]]==[3600,1800]
    assert all(x["assetId"]==image_id for x in result["scenes"])
    print("PASS: real 0.15.5 JS planner keeps ONE picture for full "
          "90-minute narration in two technical 3600/1800s segments",flush=True)
    return result["scenes"]

def main():
    seconds=5400
    exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    assert exe.is_file()
    ffprobe=next((x.with_name("ffprobe.exe") for x in exe.parent.rglob("ffmpeg.exe")
                  if x.parent.name.lower()=="bin"),None)
    assert ffprobe and ffprobe.is_file()
    root.mkdir(parents=True,exist_ok=True)
    voice=root/"synthetic-90min-static.wav"
    novel.make_wav(voice,seconds)
    aid="static-90m-voice-qa0155"
    iid="static-90m-image-qa0155"
    scenes=plan_with_REAL_node(iid)
    with fixture.Session(exe) as app:
        digest=novel.upload(app,voice,aid)
        app.upload(iid,"png",fixture.PNG)
        start=time.monotonic()
        job=app.api("start_render_job",{
            "chapterNumber":91,"sourceVideoId":aid,"sourceVideoExt":"wav",
            "scenes":scenes,"preset":"youtube","recordedSeconds":seconds,
            "transitionMode":"cut","quality":"full"})
        state=novel.wait_for_job(app,job["id"],90)
        assert state["status"]=="complete",state
        output=Path(state["output"])
        novel.verify_mp4(ffprobe,output,seconds)
        assert novel.sha(fixture.DATA/"media"/f"{aid}.wav")==digest
        print("PASS: actual installed Windows 0.15.5 built the full "
              "5400-second 1920x1080 MP4 with ONE visible background, "
              "162000 frames H264/AAC and original WAV SHA unchanged; "
              f"elapsed={time.monotonic()-start:.1f}s on hosted Windows",
              flush=True)
    print("WINDOWS 0.15.5 90MIN SAME-BACKGROUND SMART-SCENE FULL-EXE QA PASS",flush=True)

if __name__=="__main__":
    main()
