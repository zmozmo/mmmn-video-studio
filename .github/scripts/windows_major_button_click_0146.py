"""Acceptance: CLICK real Major-Scene Draft button in installed 0.14.6 Edge UI.

No user data or cloud. This tests the actual button -> makeOfflineDraft ->
consolidateMajorScenes -> confirmed save/reload flow, not just module import.
"""
import importlib.util
import json
import os
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

ROOT=Path(os.environ["RUNNER_TEMP"])/"mmmn-major-click-qa0146"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(ROOT)
spec=importlib.util.spec_from_file_location(
    "mmmn_fixture_0146",
    Path(__file__).with_name("windows_upgrade_0140_to_0146.py"))
fixture=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

def main():
    installed=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    assert installed.is_file()
    with fixture.Session(installed) as app, sync_playwright() as p:
        browser=p.chromium.launch(channel="msedge",headless=True,
            args=["--disable-gpu","--disable-background-networking"])
        page=browser.new_page()
        console_errors=[]
        dialogs=[]
        page.on("pageerror",lambda error:console_errors.append(str(error)))
        def accept(dialog):
            dialogs.append(dialog.message)
            dialog.accept()
        page.on("dialog",accept)
        try:
            page.goto(app.url,wait_until="domcontentloaded",timeout=45000)
            page.locator(".shell").wait_for(state="visible",timeout=25000)
            original=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state'))""")
            assert original and len(original.get("chapters",[]))>0
            c=original["chapters"][0]
            c["scenes"]=[
              {"id":"beat-a","title":"A","text":"သူတို့ စကားပြောနေကြသည်။",
               "start":0,"duration":80,"assetId":"safe-local-image-A",
               "motion":"still","alignment":"estimated"},
              {"id":"beat-b","title":"B","text":"မိုးရွာနေသည်။",
               "start":80,"duration":80,"assetId":"safe-local-image-B",
               "motion":"still","alignment":"estimated"},
              {"id":"beat-c","title":"C","text":"မိုးသည်းထန်၍ ညနေမှောင်မိုက်လာသည်။",
               "start":160,"duration":80,"assetId":"safe-local-image-C",
               "motion":"still","alignment":"estimated"},
              {"id":"beat-d","title":"D","text":"မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။",
               "start":240,"duration":80,"assetId":"safe-local-image-D",
               "motion":"still","alignment":"estimated"}
            ]
            c["recordedSeconds"]=320
            c["subtitleCues"]=[]
            c["videoAssetId"]=None
            c["audioAssetId"]=None
            c["undoHistory"]=[]
            c["redoHistory"]=[]
            original["visualRequirements"]=[]
            saved=app.api("save_project_state",{"json":json.dumps(original,ensure_ascii=False)})
            page.reload(wait_until="domcontentloaded")
            page.locator(".shell").wait_for(state="visible",timeout=30000)
            page.locator('[data-tab="timeline"]').first.click()
            button=page.locator('[data-action="major-only-scene-plan"]')
            assert button.first.is_visible()
            button.first.click()
            deadline=time.monotonic()+20
            while time.monotonic()<deadline:
                current=json.loads(app.api("load_project_state"))
                ch=current["chapters"][0]
                if ch.get("scenePolicy")=="major-only-conservative":
                    break
                time.sleep(.25)
            else:
                raise AssertionError("Click did not persist the major-only scene draft; dialogs="+str(dialogs))
            assert len(ch["scenes"])==2,ch["scenes"]
            assert [x["start"] for x in ch["scenes"]]==[0,160]
            assert [x["duration"] for x in ch["scenes"]]==[160,160]
            assert [x.get("assetId") for x in ch["scenes"]]==[
                "safe-local-image-A","safe-local-image-C"]
            assert ch["recordedSeconds"]==320
            assert "Major-only draft:" in ch["alignmentSummary"]
            assert any("Save" in d or "Draft" in d for d in dialogs),dialogs
            page.reload(wait_until="domcontentloaded")
            page.locator(".shell").wait_for(state="visible",timeout=30000)
            after=json.loads(app.api("load_project_state"))["chapters"][0]
            assert after["scenes"]==ch["scenes"],"Reload lost selected major scenes"
            assert not console_errors,console_errors
            print("PASS: actual installed 0.14.6 Edge button clicked; four "
                  "narrative beats conservatively saved as two major visual "
                  "scenes at 0s/160s, ordinary rain and girl mention ignored, "
                  "320s unchanged, image choice retained and reload durable",flush=True)
        finally:
            browser.close()

if __name__=="__main__":
    main()
