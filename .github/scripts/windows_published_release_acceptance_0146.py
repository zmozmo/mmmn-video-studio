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

EXPECTED_VERSION = "0.14.6"

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
                    responses=[]
                    outbounds=[]
                    dialogs=[]
                    def accept_dialog(dialog):
                        dialogs.append(dialog.message)
                        dialog.accept()
                    page.on("pageerror",lambda err: errors.append("JS: "+str(err)[:600]))
                    page.on("console",lambda msg: errors.append("CONSOLE: "+msg.text[:600]) if msg.type=="error" else None)
                    page.on("request",lambda req: outbounds.append(req.url) if not (req.url.startswith(url) or req.url.startswith("blob:") or req.url.startswith("data:")) else None)
                    page.on("response",lambda res: responses.append((res.status,res.url)) if '/__api/' in res.url else None)
                    page.on("dialog",accept_dialog)
                    try:
                        page.goto(url,wait_until="domcontentloaded",timeout=40000)
                        page.locator(".shell").wait_for(state="visible",timeout=30000)
                        assert "Project Dashboard" in page.locator("#app").inner_text()
                        print("PASS: published Windows installer opens REAL Edge GUI",flush=True)
                        storage=page.evaluate("""async () => await window.__TAURI__.core.invoke('project_storage_info')""")
                        assert isinstance(storage.get('freeBytes'),int) and storage['freeBytes'] > 0, storage
                        assert storage.get('totalBytes',0)>=storage['freeBytes'], storage
                        page.locator('[data-tab="updates"]').first.click()
                        page.locator('[data-action="refresh-storage"]').click()
                        assert "Disk free:" in page.locator("#app").inner_text(timeout=10000)
                        print("PASS: installed app reports available Windows disk space in UI",flush=True)
                        initial_state=page.evaluate("""() => JSON.parse(localStorage.getItem('mmmn-studio-state'))""")
                        initial_scenes=initial_state['chapters'][0]['scenes']
                        assert len(initial_scenes)>=2, "Need populated demo storyboard to check scene retention"

                        # A real user edit must be durable on disk and survive a browser reload.
                        page.locator('[data-tab="manuscript"]').first.click()
                        field=page.locator("#chapter-text")
                        field.wait_for(state="visible")
                        original=field.input_value()
                        marker="MMMN-ACCEPTANCE-SYNTHETIC-EDIT-2026"
                        field.fill(original+"\n"+marker)
                        page.locator('[data-action="save-text"]').click()
                        projectfile=localdata/"project-state.json"
                        try:
                            expect_file_contains(projectfile,marker,seconds=12)
                        except AssertionError as error:
                            bridge=page.evaluate("""() => ({
                                hasBridge: !!window.__TAURI__,
                                hasInvoke: typeof window.__TAURI__?.core?.invoke,
                                trial: window.__MMMN_TRIAL__,
                                toast: document.querySelector('#toast')?.textContent,
                                selected: document.querySelector('#chapter-text')?.value?.slice(-120),
                                localStorageHasMarker: (localStorage.getItem('mmmn-studio-state')||'').includes('MMMN-ACCEPTANCE-SYNTHETIC-EDIT-2026')
                            })""")
                            items=[str(p.relative_to(localdata)) for p in localdata.rglob("*") if p.is_file()]
                            raise AssertionError(f"{error}, bridge={bridge}, responses={responses[-20:]}, errors={errors[-10:]}, files={items[-20:]}")

                        page.reload(wait_until="domcontentloaded")
                        page.locator(".shell").wait_for(state="visible",timeout=30000)
                        page.locator('[data-tab="manuscript"]').first.click()
                        assert marker in page.locator("#chapter-text").input_value()
                        retained=json.loads(projectfile.read_text(encoding="utf-8"))
                        assert retained["chapters"][0]["scenes"]==initial_scenes, "Manuscript save deleted or changed storyboard timing/image choices"
                        print("PASS: manuscript save preserved ALL pre-existing scenes and assignments",flush=True)
                        print("PASS: real UI text editing + native disk persistence + restart reload",flush=True)

                        # Import real WAV bytes through the browser's file picker.
                        page.locator('[data-tab="timeline"]').first.click()
                        # New installed Smart Scene control must be visible in
                        # REAL Edge from exact downloaded 0.14.6 EXE.
                        major_button=page.locator('[data-action="major-only-scene-plan"]')
                        assert major_button.count()>=1, "Major-only scene selector not installed"
                        assert major_button.first.is_visible()
                        print("PASS: installed native Edge UI exposes conservative Major Scene Auto Draft",flush=True)
                        verify_major=page.evaluate("""async () => {
                            const {consolidateMajorScenes}=await import('./major-scene.mjs');
                            const scenes=[
                              {id:'s0',text:'သူတို့ စကားပြောနေကြသည်။',start:0,duration:80,assetId:'a'},
                              {id:'s1',text:'မိုးရွာနေသည်။',start:80,duration:80,assetId:'b'},
                              {id:'s2',text:'မိုးသည်းထန်၍ ညနေမှောင်မိုက်လာသည်။',start:160,duration:80,assetId:'c'},
                              {id:'s3',text:'မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။',start:240,duration:80,assetId:'d'}
                            ];
                            const result=consolidateMajorScenes(scenes);
                            return {count:result.scenes.length,
                              starts:result.scenes.map(s=>s.start),
                              assets:result.scenes.map(s=>s.assetId),
                              duration:result.report.narrationSeconds,
                              reviewRequired:result.report.reviewRequired};
                        }""")
                        assert verify_major == {
                            "count":2,"starts":[0,160],"assets":["a","c"],
                            "duration":320,"reviewRequired":True
                        },verify_major
                        print("PASS: actual installed Edge imports conservative module; rain/girl held, dark severe storm switches once; 320s unchanged",flush=True)

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
                        deadline=time.monotonic()+40
                        while time.monotonic()<deadline:
                            if any("Verified Full Backup created" in msg for msg in dialogs):break
                            if any("Full Backup failed" in msg for msg in dialogs):
                                raise AssertionError("UI reports failed native backup: "+str(dialogs))
                            page.wait_for_timeout(250)
                        else:raise AssertionError("UI full backup never completed: "+str(dialogs))
                        snapshots=list((localdata/"snapshots").glob("snapshot-*"))
                        assert snapshots and projectfile.is_file() and stored[0].is_file()
                        print("PASS: UI full-media backup COMPLETED and preserved project/audio",flush=True)
                        backed_up_scenes=json.loads(projectfile.read_text(encoding="utf-8"))["chapters"][0]["scenes"]

                        # A saved folder is not enough: the app must independently
                        # verify the backup hashes through its user-facing control.
                        page.locator('[data-action="verify-native-backup"]').click()
                        deadline=time.monotonic()+35
                        while time.monotonic()<deadline:
                            if any("Backup VERIFIED:" in msg for msg in dialogs):break
                            if any("Backup verification FAILED" in msg for msg in dialogs):
                                raise AssertionError("Native SHA-256 backup verification failed: "+str(dialogs))
                            page.wait_for_timeout(250)
                        else:raise AssertionError("UI backup SHA-256 verification never completed: "+str(dialogs))
                        print("PASS: user-facing full backup SHA-256 verification",flush=True)

                        # Security: forged or missing localhost API tokens must never
                        # allow untrusted callers to overwrite the saved manuscript.
                        import urllib.error
                        baseline_hash = hashlib.sha256(projectfile.read_bytes()).hexdigest()
                        rogue = json.dumps(
                            {'json': 'MMMN-UNAUTHORIZED-WRITE-REJECTION'},
                            ensure_ascii=False).encode('utf-8')
                        for token_headers in ({}, {'X-MM-Token': 'forged-qa-token'}):
                            headers = {'Content-Type': 'application/json', **token_headers}
                            request = urllib.request.Request(
                                url + '__api/save_project_state', data=rogue,
                                headers=headers, method='POST')
                            try:
                                with urllib.request.urlopen(request, timeout=10) as response:
                                    raise AssertionError(
                                        'Unauthenticated API write accepted: ' + str(response.status))
                            except urllib.error.HTTPError as error:
                                assert error.code in (400, 401, 403), (
                                    'Unexpected unauthorized response: ' + str(error.code))
                        assert hashlib.sha256(projectfile.read_bytes()).hexdigest() == baseline_hash, (
                            'Unauthorized API request modified persistent manuscript')
                        print('PASS: missing and forged API tokens rejected without data mutation', flush=True)

                        # Integrity fault injection: corrupt one SYNTHETIC full-backup
                        # media file, prove the backup is rejected, then put original
                        # bytes back. Never mutate actual user files or snapshots.
                        latest_snapshot = max(
                            (p for p in snapshots if p.is_dir()),
                            key=lambda p: p.stat().st_mtime)
                        snapshot_media = [
                            p for p in (latest_snapshot / 'media').rglob('*') if p.is_file()]
                        assert snapshot_media, 'Full backup must contain copied synthetic media'
                        copied_recording = snapshot_media[0]
                        assert not copied_recording.is_symlink(), 'Backup must not contain media symlink'
                        clean_bytes = copied_recording.read_bytes()
                        source_hash = hashlib.sha256(stored[0].read_bytes()).hexdigest()
                        project_hash = hashlib.sha256(projectfile.read_bytes()).hexdigest()
                        try:
                            copied_recording.write_bytes(clean_bytes + b'MMMN-QA-CORRUPTION')
                            tampered = page.evaluate('''async (id) => {
                                try {
                                    const result = await window.__TAURI__.core.invoke('verify_local_backup', {id});
                                    return {ok:true, result};
                                } catch (error) {
                                    return {ok:false, error:String(error)};
                                }
                            }''', latest_snapshot.name)
                            assert not (
                                tampered.get('ok') and
                                isinstance(tampered.get('result'), dict) and
                                tampered['result'].get('verified') is True), (
                                'CORRUPTED BACKUP FALSELY VERIFIED: ' + repr(tampered))
                            assert hashlib.sha256(projectfile.read_bytes()).hexdigest() == project_hash
                            assert hashlib.sha256(stored[0].read_bytes()).hexdigest() == source_hash
                        finally:
                            copied_recording.write_bytes(clean_bytes)
                        repaired = page.evaluate('''async (id) =>
                            await window.__TAURI__.core.invoke('verify_local_backup', {id})''',
                            latest_snapshot.name)
                        assert repaired.get('verified') is True, (
                            'Repaired full backup failed verification: ' + repr(repaired))
                        print('PASS: corrupted full backup rejected, original recovered and reverified', flush=True)

                        # Only vetted local folders can be launched by user action.
                        for action in ("open-local-backups","open-local-project"):
                            with page.expect_response(lambda r: "/__api/open_local_folder" in r.url,timeout=15000) as opening:
                                page.locator('[data-action="'+action+'"]').click()
                            assert opening.value.status==200, f"Could not open Windows Explorer for {action}"
                        page.locator('[data-tab="export"]').first.click()
                        with page.expect_response(lambda r: "/__api/open_local_folder" in r.url,timeout=15000) as opening:
                            page.locator('[data-action="open-local-exports"]').click()
                        assert opening.value.status==200, "Could not open saved MP4 folder"
                        print("PASS: Explorer opens Backup, Project and Export folders from UI",flush=True)
                        # Reject arbitrary browser-supplied paths; the backend is
                        # strictly limited to these three trusted folders.
                        rejected=page.evaluate("""async () => {
                            try { await window.__TAURI__.core.invoke('open_local_folder',{kind:'../../Windows/System32'});return false; }
                            catch(e) { return true; }
                        }""")
                        assert rejected, "Local folder API accepted arbitrary filesystem paths"
                        print("PASS: rejected unsafe browser-supplied folder traversal",flush=True)

                        # Recreate an accidental manuscript edit after the verified
                        # full-media backup, then restore the real snapshot through UI.
                        page.locator('[data-tab="manuscript"]').first.click()
                        field=page.locator("#chapter-text")
                        mutation="MMMN-AFTER-BACKUP-ACCIDENTAL-EDIT"
                        field.fill(field.input_value()+"\n"+mutation)
                        page.locator('[data-action="save-text"]').click()
                        expect_file_contains(projectfile,mutation,seconds=16)
                        page.locator('[data-tab="updates"]').first.click()
                        page.locator('[data-action="restore-native-backup"]').click()
                        deadline=time.monotonic()+65
                        while time.monotonic()<deadline:
                            if any("Restore finished." in msg for msg in dialogs):break
                            if any("Restore stopped:" in msg for msg in dialogs):
                                raise AssertionError("UI restored backup failed: "+str(dialogs))
                            page.wait_for_timeout(300)
                        else:raise AssertionError("UI snapshot restore did not complete: "+str(dialogs))
                        restored=json.loads(projectfile.read_text(encoding="utf-8"))
                        assert mutation not in restored["chapters"][0]["text"], "Restore did not undo accidental edits"
                        assert marker in restored["chapters"][0]["text"], "Restored snapshot lost saved manuscript"
                        assert restored["chapters"][0]["scenes"]==backed_up_scenes, "Restore lost the backed-up narration-aligned storyboard"
                        saved_audio_id=restored["chapters"][0].get("audioAssetId")
                        assert saved_audio_id, "Restored narration link missing"
                        matches=list((localdata/"media").glob(saved_audio_id+".*"))
                        assert len(matches)==1
                        assert hashlib.sha256(matches[0].read_bytes()).digest()==hashlib.sha256(audio.read_bytes()).digest(), "Restore corrupted audio recording"
                        print("PASS: full GUI backup restore recovered manuscript, all scenes and verified original WAV audio",flush=True)

                        # The app must not silently make outbound web requests during core use.
                        # blob:/data: URLs are local in-memory browser media, not network.
                        assert not outbounds, "Offline local mode requested remote connections: "+str(outbounds[:5])
                        serious=[message for message in errors if not message.startswith("CONSOLE: Failed to load resource:")]
                        assert not serious, "Browser runtime errors: "+str(serious[:8])
                        print("PASS: no outbound network request or browser runtime error",flush=True)
                        print("WINDOWS PUBLISHED RELEASE ACCEPTANCE PASS",flush=True)
                    finally:
                        print("BACKEND API RESPONSES:",responses[-22:],flush=True)
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
