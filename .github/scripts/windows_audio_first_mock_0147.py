"""0.14.7 REAL installed Edge Audio-first button QA (synthetic mock ASR only).

Tests the UI's OPTIONAL whisper.cpp transcription orchestration with a
MOCKED local model result. This is *not* a Burmese speech accuracy test.
No external network, real user manuscript, recording or drive files.
"""
import importlib.util
import json
import os
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

ROOT=Path(os.environ["RUNNER_TEMP"])/"mmmn-audio-first-mock-qa0147"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(ROOT)
file=Path(__file__).with_name("windows_upgrade_0140_to_0147.py")
spec=importlib.util.spec_from_file_location("qa_fixture_0147",file)
fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)

def timestamp(seconds):
    seconds=int(seconds)
    return ("%02d:%02d:%02d,000" % (seconds//3600,(seconds%3600)//60,seconds%60))

def srt():
    texts=[
      "သူတို့ စကားပြောနေကြသည်။",
      "မိုးရွာနေသည်။",
      "မိုးသည်းထန်၍ ညနေမှောင်မိုက်လာသည်။",
      "မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။"
    ]
    return "\n".join(
      str(i+1)+"\n"+timestamp(i*8)+" --> "+timestamp((i+1)*8)+
      "\n"+texts[i//10]+"\n"
      for i in range(40))

def main():
    exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    assert exe.is_file()
    with fixture.Session(exe) as app, sync_playwright() as tool:
        browser=tool.chromium.launch(channel="msedge",headless=True,
           args=["--disable-background-networking","--disable-gpu"])
        page=browser.new_page()
        dialogs=[]
        page.on("dialog",lambda dialog:(dialogs.append(dialog.message),dialog.accept()))
        try:
            page.goto(app.url,wait_until="domcontentloaded",timeout=40000)
            page.locator(".shell").wait_for(state="visible",timeout=30000)
            proj=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state'))""")
            assert proj and proj["chapters"]
            c=proj["chapters"][0]
            phrases=[
              "သူတို့ စကားပြောနေကြသည်။",
              "မိုးရွာနေသည်။",
              "မိုးသည်းထန်၍ ညနေမှောင်မိုက်လာသည်။",
              "မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။"
            ]
            c["scenes"]=[{
              "id":"audio-beat-"+str(i),"title":"Synthetic Test",
              "text":p,"start":i*80,"duration":80,
              "assetId":"synthetic-asset-"+str(i),"motion":"still",
              "alignment":"estimated"} for i,p in enumerate(phrases)]
            c["recordedSeconds"]=320
            c["subtitleCues"]=[]
            c["audioAssetId"]="asr-local-synthetic-recording"
            c["videoAssetId"]=None
            c["undoHistory"]=[];c["redoHistory"]=[]
            proj["visualRequirements"]=[]
            proj["assets"].append({
              "id":"asr-local-synthetic-recording","type":"audio/wav",
              "name":"test-synthetic-narrator.wav","size":1024})
            app.api("save_project_state",{"json":json.dumps(proj,ensure_ascii=False)})
            page.reload(wait_until="domcontentloaded")
            page.locator(".shell").wait_for(state="visible",timeout=30000)
            page.locator('[data-tab="timeline"]').first.click()
            transcript=srt()
            verify=page.evaluate("""async (srt) => {
               const mod=await import('./core.mjs');
               const cues=mod.parseSRT(srt);
               const diagnostics=mod.subtitleDiagnostics(cues,320);
               return {cues:cues.length,warnings:diagnostics.warnings};
            }""",transcript)
            assert verify["cues"]==40 and not verify["warnings"],verify
            page.evaluate("""(transcript) => {
              window.__qa_asr_calls=[];
              const original=window.__TAURI__.core.invoke.bind(window.__TAURI__.core);
              window.__TAURI__.core.invoke=async (command,params) => {
                if(command==='offline_speech_status'){
                  window.__qa_asr_calls.push(command);
                  return {ready:true,modelName:'synthetic-test-multilingual.bin',problems:[]};
                }
                if(command==='transcribe_narration'){
                  window.__qa_asr_calls.push(command);
                  return {srt:transcript,modelName:'synthetic-test-multilingual.bin',
                    humanReviewRequired:true,source:'QA-only fake local whisper model'};
                }
                return original(command,params);
              };
            }""",transcript)
            button=page.locator('[data-action="audio-first-major-plan"]')
            assert button.first.is_visible()
            button.first.click()
            deadline=time.monotonic()+22
            while time.monotonic()<deadline:
                changed=json.loads(app.api("load_project_state"))["chapters"][0]
                if changed.get("scenePolicy")=="major-only-conservative":
                    break
                time.sleep(.35)
            else:
                raise AssertionError("Audio-first button did not save a draft: dialogs="+repr(dialogs))
            calls=page.evaluate("""() => window.__qa_asr_calls||[]""")
            assert "offline_speech_status" in calls and "transcribe_narration" in calls,calls
            assert len(changed["subtitleCues"])==40,"Recognized SRT not persisted with confirmed draft"
            assert changed["recordedSeconds"]==320
            assert len(changed["scenes"])==2,changed["scenes"]
            assert [x["assetId"] for x in changed["scenes"]]==[
              "synthetic-asset-0","synthetic-asset-2"],changed["scenes"]
            assert len(dialogs)>=2,dialogs
            assert "must proofread" in changed["alignmentSummary"]
            page.reload(wait_until="domcontentloaded")
            saved=json.loads(app.api("load_project_state"))["chapters"][0]
            assert saved["subtitleCues"]==changed["subtitleCues"]
            assert saved["scenes"]==changed["scenes"]
            print("PASS: exact published Windows 0.14.7 Edge Audio-FIRST button calls local Whisper status + transcribe only with consent, "
                  "takes 40 SYNTHETIC SRT cues, retains 320s, picks 2 visual beats from 4, and safely saves/reloads. "
                  "ASR response was mocked; REAL Burmese recognition NOT proven.",flush=True)
        finally:
            browser.close()

if __name__=="__main__":main()
