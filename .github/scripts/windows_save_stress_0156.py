"""Independent installed Microsoft Edge test: no silently lost chapter saves."""
import importlib.util,json,os,time
from pathlib import Path
from playwright.sync_api import sync_playwright
RUN=int(os.environ.get("MMMN_STRESS_ATTEMPT","1"))
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(Path(os.environ["RUNNER_TEMP"])/f"mmmn-save-stress-0156-{RUN}")
fixture=Path(__file__).with_name("windows_upgrade_0140_to_0156.py")
spec=importlib.util.spec_from_file_location("mmmn_save_fixture",fixture)
fx=importlib.util.module_from_spec(spec);spec.loader.exec_module(fx)
def stored(app,marker,seconds=16):
 deadline=time.monotonic()+seconds
 while time.monotonic()<deadline:
  try:
   state=json.loads(app.api("load_project_state"))
   if marker in state["chapters"][0]["text"]:return state
  except Exception:pass
  time.sleep(.2)
 raise AssertionError("Lost native manuscript save: "+marker)
def main():
 exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
 assert exe.is_file()
 with fx.Session(exe) as app,sync_playwright() as p:
  browser=p.chromium.launch(channel="msedge",headless=True,
    args=["--disable-background-networking","--disable-gpu"])
  try:
   page=browser.new_page()
   errors=[];responses=[]
   page.on("pageerror",lambda err:errors.append(str(err)))
   page.on("response",lambda res:responses.append(res.status)
    if "/__api/save_project_state" in res.url else None)
   page.goto(app.url,wait_until="domcontentloaded",timeout=45000)
   page.locator(".shell").wait_for(state="visible",timeout=20000)
   page.locator('[data-tab="manuscript"]').first.click()
   field=page.locator("#chapter-text")
   original=field.input_value()
   source=json.loads(app.api("load_project_state"))["chapters"][0]
   for i in range(24):
    marker=f"MMMN-STRESS-SYNTHETIC-{RUN}-{i:02d}"
    field.fill(original+"\n"+marker)
    page.locator('[data-action="save-text"]').first.click()
    s=stored(app,marker)["chapters"][0]
    assert s["scenes"]==source["scenes"],"Storyboard lost after text save"
    assert s.get("audioAssetId")==source.get("audioAssetId"),"Audio reference changed"
    if i in (5,11,17,23):
     # Diagnose unavailable Edge on reload, retry UI only and never repeat data writes.
     for retry in range(3):
      try:
       response=(page.reload(wait_until="domcontentloaded",timeout=45000)
         if retry==0 else page.goto(app.url,wait_until="domcontentloaded",timeout=45000))
       page.locator(".shell").wait_for(state="visible",timeout=15000)
       page.locator('[data-tab="manuscript"]').first.click(timeout=10000)
       field=page.locator("#chapter-text")
       field.wait_for(state="visible",timeout=10000)
       assert marker in field.input_value(),"Reload lost a saved edit"
       break
      except Exception as exc:
       disk=stored(app,marker)["chapters"][0]
       print("DIAG: Edge reload, attempt",retry+1,
         "iteration",i,"status",getattr(response,"status",None) if "response" in locals() else None,
         "url",page.url,"browserErrors",errors[-5:],"saveStatus",responses[-5:],
         "nativeSaved",marker in disk.get("text",""),"error",str(exc)[:500],flush=True)
       if retry==2:
        raise AssertionError("UI failed 3 reload attempts, original disk chapter still persisted") from exc
       page.wait_for_timeout(800)

    if i%6==5:print(f"PASS: run {RUN}, {i+1}/24 native saved/reloaded",flush=True)
   assert not errors,errors
   assert responses and all(code<400 for code in responses),responses
   print(f"PASS: 0.15.6 public EXE REAL Edge saved 24/24 chapters, four reloads, no HTTP 400, run {RUN}",flush=True)
  finally:browser.close()
if __name__=="__main__":main()
