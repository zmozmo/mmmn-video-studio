"""Windows GitHub Actions: assert that the installed native EXE actually renders its GUI.
The source smoke used a fixed Chromium virtual-time budget and sometimes dumped the
initial loading HTML before native bridge/network promises completed. This uses a
real browser, waits for the editor, and prints useful browser-console diagnostics.
"""
import argparse
import os
import pathlib
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from playwright.sync_api import sync_playwright

def unused_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--exe",required=True)
    args=parser.parse_args()
    exe=pathlib.Path(args.exe).resolve()
    if not exe.is_file(): raise FileNotFoundError(exe)
    with tempfile.TemporaryDirectory(prefix="mmmn-win-browser-") as folder:
        root=pathlib.Path(folder)
        port=unused_port()
        url=f"http://127.0.0.1:{port}/"
        env=dict(os.environ,MMMN_TRIAL_PORT=str(port),MMMN_NO_BROWSER="1",MMMN_TRIAL_DATA_DIR=str(root/"data"))
        with (root/"exe.log").open("wb") as output:
            server=subprocess.Popen([str(exe)],env=env,stdout=output,stderr=subprocess.STDOUT)
            try:
                for _ in range(200):
                    if server.poll() is not None:
                        raise RuntimeError(f"Installed EXE exited early: {server.returncode}")
                    try:
                        with urllib.request.urlopen(url,timeout=1) as response:
                            if response.status==200: break
                    except OSError: pass
                    time.sleep(0.25)
                else: raise RuntimeError("Installed EXE never served editor")
                with sync_playwright() as p:
                    edge=p.chromium.launch(channel="msedge",headless=True,args=["--disable-gpu","--disable-background-networking"])
                    context=edge.new_context(accept_downloads=False)
                    page=context.new_page()
                    diagnostics=[]
                    page.on("console",lambda m: diagnostics.append("console "+m.type+": "+m.text[:500]) if m.type=="error" else None)
                    page.on("pageerror",lambda e: diagnostics.append("JS EXCEPTION: "+str(e)[:1000]))
                    page.on("response",lambda r: diagnostics.append("HTTP "+str(r.status)+" "+r.url) if r.status>=400 else None)
                    try:
                        page.goto(url,wait_until="domcontentloaded",timeout=45000)
                        page.locator(".shell").wait_for(state="visible",timeout=60000)
                        text=page.locator("#app").inner_text(timeout=10000)
                        for marker in ("Project Dashboard","Video Timeline"):
                            if marker not in text: raise AssertionError("Missing editor control: "+marker)
                        if "Error:" in text[:180]: raise AssertionError("Editor error state")
                        print("WINDOWS EDGE UI SMOKE PASS: real installed EXE, rendered editor, isolated data",flush=True)
                    except Exception:
                        print("PAGE TEXT:",page.locator("body").inner_text(timeout=5000)[-2000:],file=sys.stderr)
                        print("BROWSER DIAGNOSTICS:",*diagnostics[-25:],sep="\n",file=sys.stderr)
                        raise
                    finally:
                        edge.close()
            finally:
                server.terminate()
                try:server.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    server.kill();server.wait(timeout=8)
                output.flush()
                print("INSTALLED EXE LOG:",(root/"exe.log").read_text(errors="replace")[-1200:],flush=True)

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print("WINDOWS EDGE UI SMOKE FAIL:",repr(exc),file=sys.stderr)
        raise SystemExit(1)
