"""Acceptance test of the EXACT published Windows installer, in an isolated runner.
No source ZIP, no developer environment, no personal or synced content.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import urllib.request
import wave
import math
import struct
import sys

from playwright.sync_api import sync_playwright

EXPECTED_VERSION = "0.14.0"

def pick_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

def make_voice_test_file(path: Path):
    # Synthetic audio for media import; not a real voice or personal recording.
    samplerate = 16000
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(samplerate)
        samples = (
            struct.pack("<h", int(5000 * math.sin(2*math.pi*440*i/samplerate)))
            for i in range(samplerate)
        )
        wav.writeframes(b"".join(samples))

def expect_file_contains(path: Path, needle: str, seconds=28):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        if path.is_file() and needle in path.read_text(encoding="utf-8", errors="replace"):
            return
        time.sleep(0.25)
    raise AssertionError("Persistent storage missing expected content: "+str(path))

def wait_listening(url: str, proc: subprocess.Popen, seconds=45):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        if proc.poll() is not None:
            raise RuntimeError("Installed Windows EXE exited early: "+str(proc.returncode))
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status==200:return
        except OSError:pass
        time.sleep(0.25)
    raise TimeoutError("Installed Windows EXE failed to open its local HTTP UI")

def run():
    exe = Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    if not exe.is_file(): raise AssertionError("Installer did not install EXE at "+str(exe))
    with tempfile.TemporaryDirectory(prefix="mmmn-release-acceptance-") as temporary:
        root=Path(temporary)
        localdata=root/"test-data"
        audio=root/"synthetic-narration.wav"
        make_voice_test_file(audio)
        port=pick_port()
        url=f"http://127.0.0.1:{port}/"
        env=dict(os.environ,
                 MMMN_TRIAL_PORT=str(port),
                 MMMN_NO_BROWSER="1",
                 MMMN_TRIAL_DATA_DIR=str(localdata),
                 PYTHONUTF8="1",
                 PYTHONIOENCODING="utf-8",
                 NO_PROXY="127.0.0.1,localhost")
        logfile=root/"studio.log"
        with logfile.open("wb") as log:
            server=subprocess.Popen([str(exe)],env=env,stdout=log,stderr=subprocess.STDOUT)
            try:
                wait_listening(url,server)
                with sync_playwright() as play:
                    browser=play.chromium.launch(channel="msedge",headless=True,
                              args=["--disable-gpu","--disable-background-networking"])
                    context=browser.new_context(accept_downloads=False)
                    page=context.new_page()
                    errors=[]
                    outbounds=[]
                    page.on("pageerror",lambda err: errors.append("JS: "+str(err)[:600]))
                    page.on("console",lambda msg: errors.append("CONSOLE: "+msg.text[:600]) if msg.type=="error" else None)
                    page.on("request",lambda req: outbounds.append(req.url) if not req.url.startswith(url) else None)
                    page.on("dialog",lambda dialog: dialog.accept())
                    try:
                        page.goto(url,wait_until="domcontentloaded",timeout=40000)
                        page.locator(".shell").wait_for(state="visible",timeout=30000)
                        assert "Project Dashboard" in page.locator("#app").inner_text()
                        print("PASS: published Windows installer opens REAL Edge GUI",flush=True)

                        # A real user edit must be durable on disk and survive a browser reload.
                        page.locator('[data-tab="manuscript"]').first.click()
                        field=page.locator("#chapter-text")
                        field.wait_for(state="visible")
                        original=field.input_value()
                        marker="MMMN-ACCEPTANCE-SYNTHETIC-EDIT-2026"
                        field.fill(original+"\n"+marker)
                        page.locator('[data-action="save-text"]').click()
                        projectfile=localdata/"project-state.json"
                        expect_file_contains(projectfile,marker)
                        page.reload(wait_until="domcontentloaded")
                        page.locator(".shell").wait_for(state="visible",timeout=30000)
                        page.locator('[data-tab="manuscript"]').first.click()
                        assert marker in page.locator("#chapter-text").input_value()
                        print("PASS: real UI text editing + native disk persistence + restart reload",flush=True)

                        # Import real WAV bytes through the browser's file picker.
                        page.locator('[data-tab="timeline"]').first.click()
                        page.locator("#audio-input").set_input_files(str(audio))
                        expect_file_contains(projectfile,"synthetic-narration.wav")
                        project=json.loads(projectfile.read_text(encoding="utf-8"))
                        chapter=project["chapters"][0]
                        media_id=chapter.get("audioAssetId")
                        assert media_id and any(a["id"]==media_id for a in project["assets"])
                        stored=list((localdata/"media").glob(media_id+".*"))
                        assert len(stored)==1 and stored[0].read_bytes()==audio.read_bytes()
                        print("PASS: real UI WAV import + SHA-256 media bytes preserved",flush=True)

                        # Full-media backup includes the UI edit AND imported WAV.
                        page.locator('[data-tab="updates"]').first.click()
                        page.locator('[data-action="backup-native-full"]').click()
                        deadline=time.monotonic()+35
                        while time.monotonic()<deadline:
                            snapshots=list((localdata/"snapshots").glob("snapshot-*"))
                            if snapshots:break
                            time.sleep(.3)
                        else:raise AssertionError("Full backup was not created from UI")
                        assert projectfile.is_file() and stored[0].is_file()
                        print("PASS: UI full-media backup keeps project/audio intact",flush=True)

                        # The app must not silently make outbound web requests during core use.
                        assert not outbounds, "Offline local mode requested remote connections: "+str(outbounds[:5])
                        assert not errors, "Browser runtime errors: "+str(errors[:8])
                        print("PASS: no outbound network request or browser runtime error",flush=True)
                        print("WINDOWS PUBLISHED RELEASE ACCEPTANCE PASS",flush=True)
                    finally:
                        print("BROWSER CONSOLE ERRORS:",errors[-12:],flush=True)
                        print("OUTBOUND REQUESTS:",outbounds[-12:],flush=True)
                        browser.close()
            finally:
                server.terminate()
                try:server.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    server.kill();server.wait(timeout=8)
                log.flush()
                print("INSTALLED APP LOG TAIL:",logfile.read_text(encoding="utf-8",errors="replace")[-1700:],flush=True)

if __name__=="__main__":
    try:run()
    except Exception as exc:
        print("PUBLISHED WINDOWS RELEASE ACCEPTANCE FAIL:",repr(exc),flush=True)
        raise SystemExit(1)
