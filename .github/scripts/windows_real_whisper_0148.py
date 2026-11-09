"""Windows 0.14.8 real local CLI+model smoke test, NOT Burmese accuracy certification.

Uses the independently published setup.exe, official SHA256-pinned ggml-org
whisper.cpp Windows CPU binary and ggerganov multilingual ggml-base model.
A short public example.mp3 is provided as a test sample; no private content.
Nothing is uploaded by the app. After downloading test dependencies, all
transcription executes offline via localhost and a local child process.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import time

root=Path(os.environ["RUNNER_TEMP"])/"mmmn-0148-real-local-whisper"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(root)
spec=importlib.util.spec_from_file_location("qa_0148_fixture",
    Path(__file__).with_name("windows_upgrade_0140_to_0148.py"))
fixture=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return h.hexdigest()

def main():
    exe=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    wav=Path(os.environ["MMMN_TEST_ASR_AUDIO"])
    tools=Path(os.environ["MMMN_TEST_ASR_BIN_FOLDER"])
    model=Path(os.environ["MMMN_TEST_ASR_MODEL"])
    assert exe.is_file() and wav.is_file(), "Only installed EXE + public example may be used"
    assert (tools/"whisper-cli.exe").is_file() and model.is_file()
    assert sha(model)=="60ed5bc3dd14eea856493d334349b405782ddcaf0028d4b5df4088345fba2efe"
    fixture.DATA.mkdir(parents=True,exist_ok=True)
    (fixture.DATA/"tools").mkdir(exist_ok=True)
    (fixture.DATA/"models").mkdir(exist_ok=True)
    import shutil
    for item in tools.iterdir():
        if item.is_file():shutil.copy2(item,fixture.DATA/"tools"/item.name)
    shutil.copy2(model,fixture.DATA/"models"/"ggml-base.bin")
    mid="real-public-burmese-clip-0148"
    original=wav.read_bytes()
    input_hash=hashlib.sha256(original).hexdigest()
    with fixture.Session(exe) as app:
        app.upload(mid,"mp3",original)
        status=app.api("offline_speech_status")
        assert status["ready"] and status["modelName"]=="ggml-base.bin",status
        start=time.monotonic()
        job=app.api("start_transcription_job",{
            "chapterNumber":1,"sourceVideoId":mid,"sourceVideoExt":"mp3"})
        job_id=job["id"]
        assert job_id.startswith("speech-"),job
        for _ in range(240):
            job=app.api("get_transcription_job_status",{"id":job_id})
            if job["status"] in ("complete","failed","cancelled"):break
            time.sleep(1)
        else:
            app.api("cancel_transcription_job",{"id":job_id})
            raise AssertionError("Real local ggml-base transcription did not finish within 240s")
        assert job["status"]=="complete",job
        result=job["result"]
        assert result["humanReviewRequired"] is True
        assert result["modelName"]=="ggml-base.bin"
        srt=result["srt"]
        assert re.search(r"\d\d:\d\d:\d\d[,.]\d\d\d\s*-->\s*\d\d:\d\d:\d\d[,.]\d\d\d",srt),repr(srt[:150])
        assert sha(fixture.DATA/"media"/(mid+".mp3"))==input_hash
        print("PASS: REAL official local whisper-cli.exe + REAL ggml-base.bin "
          "on published Windows 0.14.8 EXE, 3s public Burmese sample => "
          "valid timestamped SRT, original audio SHA intact, no cloud inference; "
          f"elapsed {time.monotonic()-start:.1f}s on disposable Windows",
          flush=True)
        print("WARNING: This is a functional pipeline test, NOT an ASR "
          "accuracy/meaning/timing-quality evaluation for full Burmese novels.",
          flush=True)

if __name__=="__main__":
    main()
