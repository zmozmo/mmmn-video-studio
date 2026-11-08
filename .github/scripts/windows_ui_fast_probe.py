"""Fast Windows source-level browser diagnostic. No installation and no user data."""
from __future__ import annotations
import json, os, pathlib, shutil, socket, subprocess, sys, tempfile, time, urllib.request, zipfile
from playwright.sync_api import sync_playwright

def port_number():
    with socket.socket() as s:
        s.bind(("127.0.0.1",0))
        return s.getsockname()[1]

def main():
    zip_path=pathlib.Path("public-safe-windows-source.zip").resolve()
    with tempfile.TemporaryDirectory(prefix="mmmn-ui-quick-") as directory:
        scratch=pathlib.Path(directory)
        with zipfile.ZipFile(zip_path) as arc:arc.extractall(scratch/"src")
        roots=list((scratch/"src").rglob("portable/studio_server.py"))
        if len(roots)!=1: raise RuntimeError("Cannot find source server: "+str(roots))
        root=roots[0].parent.parent
        subprocess.run([sys.executable, str(pathlib.Path(os.environ['GITHUB_WORKSPACE'])/'.github/scripts/fix_windows_mime.py'),str(root)],check=True)
        port=port_number()
        host=f"http://127.0.0.1:{port}"
        env=dict(os.environ,MMMN_TRIAL_PORT=str(port),MMMN_TRIAL_DATA_DIR=str(scratch/"data"),MMMN_NO_BROWSER="1",NO_PROXY="127.0.0.1,localhost")
        logfile=scratch/"server.txt"
        with logfile.open("wb") as logs:
            server=subprocess.Popen([sys.executable,"portable/studio_server.py","--no-browser","--port",str(port)],cwd=str(root),env=env,stdout=logs,stderr=subprocess.STDOUT)
            try:
                for _ in range(100):
                    try:
                        with urllib.request.urlopen(host,timeout=1) as response:
                            if response.status==200:break
                    except OSError:pass
                    if server.poll()!=None:raise RuntimeError("Server closed: "+str(server.returncode))
                    time.sleep(.2)
                else: raise RuntimeError("Server failed to start")
                for asset in ("/","/app.js","/__bridge.js","/core.mjs","/resources/starter-project.json"):
                    with urllib.request.urlopen(host+asset,timeout=8) as response:
                        print("URL CHECK",asset,response.status,response.headers.get("Content-Type"),len(response.read()),flush=True)
                with sync_playwright() as play:
                    for channel in ("msedge",):
                        browser=play.chromium.launch(channel=channel,headless=True,args=["--disable-gpu","--no-proxy-server","--no-first-run"])
                        page=browser.new_page()
                        events=[]
                        page.on("request",lambda req:events.append("REQUEST "+req.method+" "+req.url))
                        page.on("response",lambda res:events.append("RESPONSE "+str(res.status)+" "+res.url+" "+str(res.headers.get("content-type"))))
                        page.on("requestfailed",lambda req:events.append("FAILED "+req.url+" "+str(req.failure)))
                        page.on("console",lambda msg:events.append("CONSOLE "+msg.type+" "+msg.text[:700]))
                        page.on("pageerror",lambda ex:events.append("PAGEERROR "+str(ex)[:800]))
                        try:
                            page.goto(host+"/",wait_until="domcontentloaded",timeout=30000)
                            page.locator(".shell").wait_for(state="visible",timeout=20000)
                            print("FAST UI PASS",page.locator("h1").first.inner_text()[:160],flush=True)
                        except Exception as exc:
                            print("FAST UI FAIL:",repr(exc),flush=True)
                            print("BROWSER EVENTS:\n"+"\n".join(events[-120:]),flush=True)
                            print("WEB:\n"+page.locator("body").inner_text(timeout=3000)[:1000],flush=True)
                            print("PAGE STATE:",json.dumps(page.evaluate("""() => ({
                                location: location.href, state: document.readyState,
                                scripts: [...document.scripts].map(x=>({src:x.src,type:x.type})),
                                bridge: !!window.__TAURI__, trial: !!window.__MMMN_TRIAL__,
                                app: document.querySelector('#app')?.innerHTML?.slice(0,250),
                                resourceCount: performance.getEntriesByType('resource').length,
                                resources: performance.getEntriesByType('resource').map(x=>x.name).slice(-20)
                            })""")),flush=True)
                            try: page.screenshot(path=str(pathlib.Path(os.environ.get("GITHUB_WORKSPACE","."))/"fast-ui-debug.png"),full_page=True)
                            except Exception as screenshot_error:print("Screenshot failed:",screenshot_error)
                            raise
                        finally:browser.close()
            finally:
                server.terminate()
                try:server.wait(timeout=5)
                except subprocess.TimeoutExpired:server.kill()
                logs.flush()
                print("SERVER LOG:\n"+logfile.read_text(errors="replace")[-4000:],flush=True)

if __name__=="__main__":
    try:main()
    except Exception as exc: print("FAST-UI FAILURE:",repr(exc),flush=True);raise SystemExit(1)
