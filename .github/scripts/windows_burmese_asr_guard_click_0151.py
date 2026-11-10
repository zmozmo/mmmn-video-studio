"""Published Windows 0.15.1 real Edge test: bad Burmese ASR MUST NOT steer images.

Two synthetic 320s chapters are used, one with a wrong but valid
timestamped SRT and one with an agreement-matching SRT. No real Whisper
inference is claimed; local API responses are mocked to exercise the REAL
button, real agreement gate, save and reload. No personal assets are used.
"""
import importlib.util, json, os, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(os.environ["RUNNER_TEMP"])/"mmmn-asr-agreement-qa0151"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(ROOT)
spec=importlib.util.spec_from_file_location(
 "mmmn_0151_fixture",Path(__file__).with_name("windows_upgrade_0140_to_0151.py"))
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
def srt(bad,short=False):
 return "\n".join(
  str(i+1)+"\n"+stamp(i*8)+" --> "+stamp((i+1)*8)+"\n"+
   (WRONG if bad else PHRASES[i//10])+"\n" for i in range(4 if short else 40))

def main():
 exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
 assert exe.is_file()
 with fixture.Session(exe) as app, sync_playwright() as tool:
  browser=tool.chromium.launch(channel="msedge",headless=True,
    args=["--disable-background-networking","--disable-gpu"])
  # Preserve one genuine browser profile across both cases; browser.new_page()
  # silently creates a fresh isolated context with no previous localStorage.
  context=browser.new_context()
  try:
   for bad,short in ((True,False),(False,True),(False,False)):
    page=context.new_page()
    dialogs=[];errors=[]
    page.on("dialog",lambda dialog:(dialogs.append(dialog.message),dialog.accept()))
    page.on("pageerror",lambda error:errors.append(str(error)))
    try:
     for attempt in range(3):
      try:
       page.goto(app.url,wait_until="domcontentloaded",timeout=45000)
       page.locator(".shell").wait_for(state="visible",timeout=15000)
       break
      except Exception as exc:
       print("Edge startup retry",attempt+1,str(exc)[:180],flush=True)
       if attempt==2:raise
       time.sleep(1)
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
     c["audioAssetId"]="synthetic-original-voice-0151"
     c["videoAssetId"]=None
     c["undoHistory"]=[];c["redoHistory"]=[]
     project["visualRequirements"]=[]
     project["assets"]=[a for a in project.get("assets",[])
       if a.get("id")!="synthetic-original-voice-0151"]
     project["assets"].append({"id":"synthetic-original-voice-0151",
        "type":"audio/wav","name":"synthetic-voice.wav","size":1024})
     prepared=json.dumps(project,ensure_ascii=False)
     app.api("save_project_state",{"json":prepared})
     # Reset BOTH stores between wrong-ASR and matching-ASR scenarios.
     # Native disk save alone leaves previous browser localStorage alive.
     page.evaluate("(data) => localStorage.setItem('mmmn-studio-state',data)",prepared)
     page.reload(wait_until="domcontentloaded")
     page.locator(".shell").wait_for(state="visible",timeout=30000)
     page.locator('[data-tab="timeline"]').first.click()
     raw=srt(bad,short)
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
      result=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]||{}""")
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
     expected_cues=0 if bad or short else 40
     assert len(result.get("subtitleCues") or [])==expected_cues,(
       "Hallucinated Burmese SRT was accepted" if bad or short else "Matching SRT was rejected",
       len(result.get("subtitleCues") or []))
     assert result["recordedSeconds"]==320
     assert len(result["scenes"])>=1
     assert not errors,errors
     # Browser UI state can be ahead of its authenticated native file.
     # A success requires real disk persistence without test-side saving.
     persisted=False
     for _ in range(50):
      try:
       disk=json.loads(app.api("load_project_state"))["chapters"][0]
       if disk.get("scenePolicy")=="major-only-conservative" and (
             disk.get("subtitleCues") or [])==(result.get("subtitleCues") or []):
        persisted=True
        break
      except Exception:pass
      time.sleep(.2)
     if not persisted:
      diagnostics=page.evaluate("""() => ({
        native:window.__qa_native_commands||[],
        errors:window.__qa_native_errors||[]
      })""")
      raise AssertionError("UI changed but native disk did not persist: "+str(diagnostics))
     page.reload(wait_until="domcontentloaded")
     page.locator(".shell").wait_for(state="visible",timeout=30000)
     reread=json.loads(app.api("load_project_state"))["chapters"][0]
     assert reread["subtitleCues"]==result["subtitleCues"]
     # The read-only SRT timing audit must work as a real clickable Edge action.
     page.locator('[data-tab="timeline"]').first.click()
     before_audit=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]""")
     audit=page.locator('[data-action="audit-current-srt"]').first
     assert audit.is_visible(),"Missing 0.15.1 SRT Timing Audit button"
     before_dialogs=len(dialogs)
     audit.click()
     assert len(dialogs)>before_dialogs and 'SRT / အသံ' in dialogs[-1],dialogs
     after_audit=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]""")
     assert before_audit==after_audit,"Audit button unexpectedly changed chapter data"
     print("PASS: 0.15.1 real Edge read-only SRT Timing Audit button",flush=True)
     print("PASS: 0.15.1 installed Edge "+
         ("REJECTED grossly WRONG Burmese ASR" if bad
          else "REJECTED matching but TRUNCATED SRT timing" if short
          else "ACCEPTED full matching SRT as REVIEW-REQUIRED")+
         "; original 320s and save/reload preserved",flush=True)
    finally:page.close()
  finally:browser.close()

if __name__=="__main__":main()
