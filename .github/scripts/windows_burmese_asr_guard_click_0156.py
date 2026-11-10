"""Published Windows 0.15.6 real Edge test: bad Burmese ASR MUST NOT steer images.

Two synthetic 320s chapters are used, one with a wrong but valid
timestamped SRT and one with an agreement-matching SRT. No real Whisper
inference is claimed; local API responses are mocked to exercise the REAL
button, real agreement gate, save and reload. No personal assets are used.
"""
import importlib.util, json, os, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(os.environ["RUNNER_TEMP"])/"mmmn-asr-agreement-qa0156"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(ROOT)
spec=importlib.util.spec_from_file_location(
 "mmmn_0156_fixture",Path(__file__).with_name("windows_upgrade_0140_to_0156.py"))
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
     c["audioAssetId"]="synthetic-original-voice-0156"
     c["videoAssetId"]=None
     c["undoHistory"]=[];c["redoHistory"]=[]
     project["visualRequirements"]=[]
     project["assets"]=[a for a in project.get("assets",[])
       if a.get("id")!="synthetic-original-voice-0156"]
     project["assets"].append({"id":"synthetic-original-voice-0156",
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
     assert audit.is_visible(),"Missing 0.15.6 SRT Timing Audit button"
     before_dialogs=len(dialogs)
     audit.click()
     assert len(dialogs)>before_dialogs and 'SRT / အသံ' in dialogs[-1],dialogs
     after_audit=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]""")
     assert before_audit==after_audit,"Audit button unexpectedly changed chapter data"
     # NEW 0.15.6: real Edge PRIVATE local scene/SRT report download.
     # This action may not alter either browser project or backed-up native state.
     before_report=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]""")
     before_disk=json.loads(app.api("load_project_state"))["chapters"][0]
     report_button=page.locator('[data-action="export-major-timing-evidence"]').first
     assert report_button.is_visible(),"Missing 0.15.6 scene/SRT evidence report button"
     dialog_start=len(dialogs)
     with page.expect_download(timeout=30000) as expected:
      report_button.click()
     downloaded=expected.value
     assert downloaded.suggested_filename.endswith("-SCENE-SRT-REVIEW-PRIVATE.md"),downloaded.suggested_filename
     content=Path(downloaded.path()).read_text(encoding="utf-8")
     assert "PRIVATE LOCAL REVIEW" in content and "UNPUBLISHED" in content,content[:250]
     assert len(dialogs)>dialog_start and "အရေးကြီး Scene" in dialogs[-1],dialogs
     after_report=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]""")
     after_disk=json.loads(app.api("load_project_state"))["chapters"][0]
     assert before_report==after_report,"Read-only report changed user's browser chapter"
     assert before_disk==after_disk,"Read-only report changed user's native disk chapter"
     if not bad and not short:
      # Use a REAL native-imported PNG, not a metadata-only/nonexistent photo.
      image_id="actual-graveyard-png-0156"
      app.upload(image_id,"png",fixture.PNG)
      photo_file=fixture.DATA/"media"/(image_id+".png")
      real_image_sha=fixture.sha(photo_file)
      fresh=json.loads(app.api("load_project_state"))
      chapter=fresh["chapters"][0]
      original_cues=chapter.get("subtitleCues")
      original_text=chapter.get("text")
      chapter["scenePolicy"]="major-only-conservative"
      chapter["scenes"]=[{"id":"test-major-graveyard",
        "start":0,"duration":320,"text":"သင်္ချိုင်းထဲသို့ ဝင်ရောက်လာကြသည်။",
        "assetId":None,"alignment":"estimated","motion":"still"}]
      fresh["assets"].append({"id":image_id,"name":"graveyard.png",
        "type":"image/png","nativeStored":True})
      ready=json.dumps(fresh,ensure_ascii=False)
      app.api("save_project_state",{"json":ready})
      page.evaluate("(data) => localStorage.setItem('mmmn-studio-state', data)",ready)
      page.reload(wait_until="domcontentloaded")
      page.locator(".shell").wait_for(state="visible",timeout=30000)
      page.locator('[data-tab="timeline"]').first.click()
      find=page.locator('[data-action="match-local-major-images"]').first
      assert find.is_visible(),"0.15.6 real local imported-artwork match button missing"
      before_changes=len(dialogs)
      find.click()
      assert len(dialogs)>before_changes,"Explicit user confirmation dialog missing"
      for _ in range(80):
       candidate=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]||{}""")
       if candidate.get("scenes",[{}])[0].get("assetId")==image_id:break
       time.sleep(.2)
      else:
       raise AssertionError("Matching imported actual photo never applied via real Edge button")
      selected=candidate["scenes"][0]
      assert selected["imageMatchStatus"]=="suggested-review",selected
      assert selected["start"]==0 and selected["duration"]==320
      assert candidate.get("text")==original_text
      assert candidate.get("subtitleCues")==original_cues
      assert fixture.sha(photo_file)==real_image_sha
      persisted=json.loads(app.api("load_project_state"))["chapters"][0]
      assert persisted["scenes"][0]["assetId"]==image_id,"UI image changed but disk did not"
      assert persisted["scenes"][0]["imageMatchStatus"]=="suggested-review"
      assert persisted.get("subtitleCues")==original_cues
      assert persisted.get("text")==original_text
      page.reload(wait_until="domcontentloaded")
      page.locator(".shell").wait_for(state="visible",timeout=30000)
      reloaded=json.loads(app.api("load_project_state"))["chapters"][0]
      assert reloaded["scenes"][0]["assetId"]==image_id
      # 0.15.6: test the NEW actual Edge button on TWO scenes. An unassigned
      # subsequent major beat must keep the verified local photo, never blank,
      # while preserving original subtitle cues and image SHA on native disk.
      carry=json.loads(app.api("load_project_state"))
      carry_ch=carry["chapters"][0]
      carry_ch["scenePolicy"]="major-only-conservative"
      carry_ch["scenes"]=[
       {"id":"preserve-opening-image","start":0,"duration":160,
        "text":"သင်္ချိုင်းအနီးမှာ ရပ်နေသည်။","assetId":image_id,
        "alignment":"estimated","motion":"still"},
       {"id":"missing-new-image","start":160,"duration":160,
        "text":"မိုးရွာနေစဉ် စကားပြောပြီး နောက်ခံပုံအသစ် မရသေးပါ။",
        "assetId":None,"alignment":"estimated","motion":"still"}]
      revised=json.dumps(carry,ensure_ascii=False)
      app.api("save_project_state",{"json":revised})
      page.evaluate("(data) => localStorage.setItem('mmmn-studio-state',data)",revised)
      page.reload(wait_until="domcontentloaded")
      page.locator(".shell").wait_for(state="visible",timeout=30000)
      page.locator('[data-tab="timeline"]').first.click()
      hold=page.locator('[data-action="hold-verified-major-photo"]').first
      assert hold.is_visible(),"Missing real Windows 0.15.6 picture continuity button"
      prev_dialogs=len(dialogs)
      hold.click()
      assert len(dialogs)>prev_dialogs,"0.15.6 continuity requires explicit confirmation"
      for _ in range(80):
       staged=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state')||'{}').chapters?.[0]||{}""")
       if staged.get("scenes",[{},{}])[1].get("assetId")==image_id:break
       time.sleep(.2)
      else:
       raise AssertionError("Real Edge 0.15.6 continuity button did not carry prior image")
      assert len(staged["scenes"])==2
      assert [i["start"] for i in staged["scenes"]]==[0,160]
      assert [i["duration"] for i in staged["scenes"]]==[160,160]
      assert staged["scenes"][1]["imageMatchStatus"]=="same-imported-picture-review"
      assert staged.get("text")==original_text
      assert staged.get("subtitleCues")==original_cues
      assert fixture.sha(photo_file)==real_image_sha
      for _ in range(50):
       native=json.loads(app.api("load_project_state"))["chapters"][0]
       if native["scenes"][1].get("assetId")==image_id:break
       time.sleep(.2)
      else:
       raise AssertionError("Photo continuity changed only browser storage, not native disk")
      assert native["scenes"][1]["imageMatchStatus"]=="same-imported-picture-review"
      assert native["scenes"][0]["assetId"]==image_id
      assert native.get("subtitleCues")==original_cues
      assert fixture.sha(photo_file)==real_image_sha
      print("PASS: 0.15.6 REAL Edge two 160s major beats reused ONE existing local photo with explicit confirmation, no black image, no scene split, original media and SRT intact",flush=True)
      print("PASS: 0.15.6 REAL Edge local native-imported cemetery picture matched ONE MAJOR scene, explicit confirmation, no new timeline boundaries, 320s original and SRT unchanged, photo SHA unchanged, saved/reloaded",flush=True)
     print("PASS: 0.15.6 REAL Edge private evidence report exported without ANY chapter mutation",flush=True)
     print("PASS: 0.15.6 real Edge read-only SRT Timing Audit button",flush=True)
     print("PASS: 0.15.6 installed Edge "+
         ("REJECTED grossly WRONG Burmese ASR" if bad
          else "REJECTED matching but TRUNCATED SRT timing" if short
          else "ACCEPTED full matching SRT as REVIEW-REQUIRED")+
         "; original 320s and save/reload preserved",flush=True)
    finally:page.close()
  finally:browser.close()

if __name__=="__main__":main()
