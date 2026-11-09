"""Real 0.14.0 -> 0.14.7 Windows in-place upgrade acceptance.

Creates only synthetic data in an isolated GitHub runner directory.
Before: installs/runs REAL old Windows executable, imports WAV and PNG through
authenticated localhost API, saves manuscript/storyboard and a full snapshot.
After: boots REAL updated executable, verifies original SHA256 unchanged, proves
pre-upgrade metadata was checkpointed and snapshot can still be verified.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import re
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request
import wave

ROOT=Path(os.environ["MMMN_UPGRADE_TEST_ROOT"]).resolve()
DATA=ROOT/"user-data"
WITNESS=ROOT/"sha256-witness.json"
PNG=base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/1L8AAAAASUVORK5CYII=")

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as fd:
        for chunk in iter(lambda: fd.read(1048576),b""):h.update(chunk)
    return h.hexdigest()

def port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1",0))
        return sock.getsockname()[1]

class Session:
    def __init__(self,exe):
        self.exe=Path(exe).resolve()
    def __enter__(self):
        self.port=port()
        self.url=f"http://127.0.0.1:{self.port}"
        env=dict(os.environ,MMMN_TRIAL_DATA_DIR=str(DATA),
                 MMMN_TRIAL_PORT=str(self.port),MMMN_NO_BROWSER="1",
                 NO_PROXY="127.0.0.1,localhost",PYTHONUTF8="1",PYTHONIOENCODING="utf-8")
        self.proc=subprocess.Popen([str(self.exe)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(160):
            if self.proc.poll() is not None:
                raise RuntimeError("Installed EXE exited: "+str(self.proc.returncode))
            try:
                raw=urllib.request.urlopen(self.url+"/__bridge.js",timeout=1).read().decode("utf-8")
                match=re.search(r'^const token=(".+?");',raw,re.M)
                if match:
                    self.token=json.loads(match.group(1))
                    return self
            except OSError:pass
            time.sleep(.25)
        raise RuntimeError("Installed Windows version did not serve authenticated offline API")
    def __exit__(self,*_):
        self.proc.terminate()
        try:self.proc.wait(timeout=8)
        except subprocess.TimeoutExpired:self.proc.kill()
    def api(self,command,params=None,binary=None,headers=None):
        payload=binary if binary is not None else json.dumps(params or {},ensure_ascii=False).encode()
        request=urllib.request.Request(self.url+"/__api/"+command,payload,method="POST")
        request.add_header("X-MM-Token",self.token)
        if binary is None:request.add_header("Content-Type","application/json")
        for key,value in (headers or {}).items():request.add_header(key,str(value))
        response=json.loads(urllib.request.urlopen(request,timeout=30).read())
        return response["result"]
    def upload(self,mid,ext,data):
        self.api("begin_media_import",dict(id=mid,ext=ext,total=len(data)))
        for index in range(0,len(data),512*1024):
            part=data[index:index+512*1024]
            self.api("import_media_chunk",binary=part,headers={
                "x-media-id":mid,"x-media-offset":index,
                "x-media-sha256":hashlib.sha256(part).hexdigest()})
        result=self.api("finalize_media_import",{"id":mid})
        assert result["sha256"]==hashlib.sha256(data).hexdigest()

def sample_audio():
    with tempfile.TemporaryFile() as f:
        # wave.open(fileobj) is safe; no personal recordings involved.
        with wave.open(f,"wb") as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000)
            w.writeframes(b"".join(struct.pack("<h",int(3000*math.sin(i*2*math.pi*440/16000)))
                                   for i in range(16000)))
        f.seek(0)
        return f.read()

def before(exe):
    ROOT.mkdir(parents=True,exist_ok=True)
    assert not WITNESS.exists(),"Refusing to overwrite prior upgrade test witness"
    with Session(exe) as app:
        app.upload("upgrade-photo-01","png",PNG)
        app.upload("upgrade-audio-01","wav",sample_audio())
        project={
            "title":"MMMN SYNTHETIC 0.14.0 UPGRADE DATA",
            "chapters":[{"id":"upgrade-chapter","number":1,
               "title":"Synthetic chapter","text":"SAFE SYNTHETIC CHAPTER TO KEEP",
               "audioAssetId":"upgrade-audio-01",
               "scenes":[{"id":"upgrade-scene-1","assetId":"upgrade-photo-01",
                          "duration":1.0,"start":0.0,"motion":"still","manualLocked":True}]}],
            "assets":[{"id":"upgrade-photo-01","name":"synthetic.png","nativeStored":True},
                      {"id":"upgrade-audio-01","name":"synthetic.wav","nativeStored":True}]
        }
        app.api("save_project_state",{"json":json.dumps(project,ensure_ascii=False)})
        snapshot=app.api("create_full_local_backup")
        assert snapshot["verified"] and snapshot["files"]==2
        assert app.api("verify_local_backup",{"id":snapshot["id"]})["verified"]
        tracked=[
            DATA/"project-state.json",
            DATA/"media"/"upgrade-photo-01.png",
            DATA/"media"/"upgrade-audio-01.wav",
            DATA/"snapshots"/snapshot["id"]/"project-state.json",
            DATA/"snapshots"/snapshot["id"]/"manifest.json",
            DATA/"snapshots"/snapshot["id"]/"media"/"upgrade-photo-01.png",
            DATA/"snapshots"/snapshot["id"]/"media"/"upgrade-audio-01.wav"
        ]
        witness={"files":{str(p.relative_to(DATA)):sha(p) for p in tracked},
                 "snapshot":snapshot["id"],"oldRevision":json.loads((DATA/"trial-revision.json").read_text())["revision"]}
        WITNESS.write_text(json.dumps(witness,indent=2),encoding="utf-8")
        print("LEGACY 0.14.0 USER DATA CREATED VIA INSTALLED EXE API, snapshot",snapshot["id"],flush=True)

def after(exe):
    witness=json.loads(WITNESS.read_text(encoding="utf-8"))
    with Session(exe) as app:
        for relative,expected in witness["files"].items():
            path=DATA/relative
            if sha(path)!=expected:raise AssertionError("0.14.7 altered original project/media/backup bytes: "+relative)
        source=app.api("load_project_state")
        project=json.loads(source)
        assert project["title"]=="MMMN SYNTHETIC 0.14.0 UPGRADE DATA"
        assert project["chapters"][0]["scenes"][0]["manualLocked"]
        assert app.api("verify_local_backup",{"id":witness["snapshot"]})["verified"]
        tracker=json.loads((DATA/"trial-revision.json").read_text())
        assert tracker["revision"]=="installer-lab-0147-upgrade",tracker
        assert tracker.get("previousRevision")==witness["oldRevision"],tracker
        checkpoints=list((DATA/"preupgrade-metadata").glob("preupgrade-*.json"))
        assert checkpoints and any(sha(p)==witness["files"]["project-state.json"] for p in checkpoints)
        print("PASS: Installed 0.14.0 -> Installed 0.14.7 in-place update retained 7 original file hashes, manuscript/storyboard/manual lock, verified snapshot and PREUPGRADE METADATA",flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("phase",choices=["before","after"])
    parser.add_argument("--exe",required=True)
    args=parser.parse_args()
    try:
        (before if args.phase=="before" else after)(args.exe)
    except Exception as ex:
        print("STABLE WINDOWS REAL-UPGRADE TEST FAILED:",repr(ex),flush=True)
        raise
