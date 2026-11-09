"""Published Windows 0.14.9 real Edge test: bad Burmese ASR MUST NOT steer images.

Two synthetic 320s chapters are used, one with a wrong but valid
timestamped SRT and one with an agreement-matching SRT. No real Whisper
inference is claimed; local API responses are mocked to exercise the REAL
button, real agreement gate, save and reload. No personal assets are used.
"""
import importlib.util, json, os, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(os.environ["RUNNER_TEMP"])/"mmmn-asr-agreement-qa0149"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(ROOT)
spec=importlib.util.spec_from_file_location(
 "mmmn_0149_fixture",Path(__file__).with_name("windows_upgrade_0140_to_0149.py"))
fixture=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

PHRASES=[
 "ဦးဘသိန်းသည် ရွာဟောင်းသို့ သွားရောက်ပြီး သင်္ချိုင်းအနီးတွင် ရပ်နေသည်။",
 "မိုးရွာနေသော်လည်း သူတို့ စကားပြောနေကြသည်။",
 "မိုးသည်းထန်၍ ညနေမှောင်မိုက်လာသည်။ သင်္ချိုင်းလမ်း မမြင်နိုင်တော့ပါ။",
 "မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။ ဦးဘသိန်းက မေးလိုက်သည်။"
]
WRONG="စီးပွားရေးဆိုင်ရာ လေယာဉ်ပျံနှင့် ဈေးကွက်များအကြောင်း ကမ္ဘာတစ်ဝန်း ထုတ်ပြန်ကြေညာချက်များ။"
BOOK=" ".join(PHRASES)+" "+" ".join(PHRASES)
def stamp(seconds):
 seconds=int(seconds)
 return "%02d:%02d:%02d,000"%(seconds//3600,(seconds//60)%60,seconds%60)
def srt(bad):
 return "\n".join(
  str(i+1)+"\n"+stamp(i*8)+" --> "+stamp((i+1)*8)+"\n"+
   (WRONG if bad else PHRASES[i//10])+"\n" for i in range(40))

def main():
 exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
 assert exe.is_file()
 with fixture.Session(exe) as app, sync_playwright() as tool:
  browser=tool.chromium.launch(channel="msedge",headless=True,
    args=["--disable-background-networking","--disable-gpu"])
  try:
   for bad in (True,False):
    page=browser.new_page()
    dialogs=[];errors=[]
    page.on("dialog",lambda dialog:(dialogs.append(dialog.message),dialog.accept()))
    page.on("pageerror",lambda error:errors.append(str(error)))
    try:
     page.goto(app.url,wait_until="domcontentloaded",timeout=45000)
     page.locator(".shell").wait_for(state="visible",timeout=30000)
     project=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state'))""")
     assert project and project["chapters"]
     c=project["chapters"][0]
     c["text"]=BOOK
     c["scenes"]=[{
      "id":"agreement-beat-"+str(i),"title":"QA","text":p,
      "start":80*i,"duration":80,"assetId":"synthetic-background-"+str(i),
      "motion":"still","alignment":"estimated"
     } for i,p in enumerate(PHRASES)]
     c["recordedSeconds"]=320
     c["subtitleCues"]=[]
     c["scenePolicy"]="unreviewed"
     c["audioAssetId"]="synthetic-original-voice-0149"
     c["videoAssetId"]=None
     c["undoHistory"]=[];c["redoHistory"]=[]
     project["visualRequirements"]=[]
     project["assets"]=[a for a in project.get("assets",[])
       if a.get("id")!="synthetic-original-voice-0149"]
     project["assets"].append({"id":"synthetic-original-voice-0149",
        "type":"audio/wav","name":"synthetic-voice.wav","size":1024})
     app.api("save_project_state",{"json":json.dumps(project,ensure_ascii=False)})
     page.reload(wait_until="domcontentloaded")
     page.locator(".shell").wait_for(state="visible",timeout=30000)
     page.locator('[data-tab="timeline"]').first.click()
     raw=srt(bad)
     page.evaluate("""(srt) => {
       const original=window.__TAURI__.core.invoke.bind(window.__TAURI__.core);
       window.__qa_asr_calls=[];
       window.__qa_native_errors=[];
       window.__qa_native_commands=[];
       window.__TAURI__.core.invoke=async (command,args) => {
         window.__qa_native_commands.push(command);
         if(['offline_speech_status','start_transcription_job',
             'get_transcription_job_status'].includes(command)){
           window.__qa_asr_calls.push(command);
           if(command==='offline_speech_status') return {
             ready:true,modelName:'QA-only-model.bin',problems:[]};
           if(command==='start_transcription_job') return {
             id:'speech-aaaaaaaaaaaaaaaaaaaaaaaa',status:'queued'};
           return {id:'speech-aaaaaaaaaaaaaaaaaaaaaaaa',status:'complete',
              result:{srt,modelName:'QA-only-model.bin',humanReviewRequired:true,
                  source:'QA-only simulated local model'}};
         }
         try {return await original(command,args);}
         catch(error) {window.__qa_native_errors.push({command,message:String(error)});throw error;}
       };
     }""",raw)
     button=page.locator('[data-action="audio-first-major-plan"]')
     assert button.first.is_visible()
     button.first.click()
     for _ in range(80):
      result=json.loads(app.api("load_project_state"))["chapters"][0]
      if result.get("scenePolicy")=="major-only-conservative":break
      time.sleep(.3)
     else:
      state=page.evaluate("""() => ({
        calls:window.__qa_asr_calls||[],
        nativeCommands:window.__qa_native_commands||[],
        nativeErrors:window.__qa_native_errors||[],
        appText:document.body.innerText.slice(-1800),
        activeSpeech:window.__MMMN_ACTIVE_SPEECH_JOB__,
        currentChapter:JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]?.scenePolicy
      })""")
      backend=json.loads(app.api("load_project_state"))["chapters"][0]
      print("QA DEBUG: bad=",bad,"dialogs=",dialogs,"pageErrors=",errors,
            "backendScenePolicy=",backend.get("scenePolicy"),
            "backendSceneCount=",len(backend.get("scenes",[])),
            "lastState=",state,flush=True)
      raise AssertionError("Smart Scene button did not save after verified UI action")
     calls=page.evaluate("""() => window.__qa_asr_calls||[]""")
     assert all(x in calls for x in
       ("offline_speech_status","start_transcription_job","get_transcription_job_status")),calls
     expected_cues=0 if bad else 40
     assert len(result.get("subtitleCues") or [])==expected_cues,(
       "Hallucinated Burmese SRT was accepted" if bad else "Matching SRT was rejected",
       len(result.get("subtitleCues") or []))
     assert result["recordedSeconds"]==320
     assert len(result["scenes"])>=1
     assert not errors,errors
     page.reload(wait_until="domcontentloaded")
     page.locator(".shell").wait_for(state="visible",timeout=30000)
     reread=json.loads(app.api("load_project_state"))["chapters"][0]
     assert reread["subtitleCues"]==result["subtitleCues"]
     print("PASS: 0.14.9 installed Edge "+
         ("REJECTED grossly WRONG Burmese ASR; no bogus SRT persisted" if bad
          else "ACCEPTED matching Burmese ASR as REVIEW-REQUIRED SRT")+
         "; original 320s and save/reload preserved",flush=True)
    finally:page.close()
  finally:browser.close()

if __name__=="__main__":main()
