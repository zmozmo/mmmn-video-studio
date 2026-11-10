"""0.15.4: independent REAL installed Studio + REAL installed offline Burmese CPU pack.

Only public licensed example speech and synthetic data. Confirms no private
uploads, no changed original audio, project, corrected SRT or manual locks.
"""
import hashlib,importlib.util,json,os,shutil,time
from pathlib import Path
TEST=Path(os.environ["RUNNER_TEMP"])/"mmmn-0154-native-public-asr-e2e"
os.environ["MMMN_UPGRADE_TEST_ROOT"]=str(TEST)
path=Path(__file__).with_name("windows_upgrade_0140_to_0154.py")
spec=importlib.util.spec_from_file_location("mmmn_0154_real_addon_fixture",path)
fx=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)

def main():
    app=Path(os.environ["MMMN_RELEASE_INSTALLED_EXE"])
    assert app.is_file(),"Real published Windows app must be installed"
    bundle=Path(os.environ["LOCALAPPDATA"])/"MMMN-Video-Studio-Trial"/"addons"/"BurmeseASR"
    assert (bundle/"mmmn-burmese-asr.exe").is_file()
    assert (bundle/"model"/"model.safetensors").stat().st_size>80_000_000
    fx.DATA.mkdir(parents=True,exist_ok=True)
    isolated=fx.DATA/"addons"/"BurmeseASR"
    assert not isolated.exists()
    shutil.copytree(bundle,isolated)
    audio=Path(os.environ["MMMN_REAL_BURMESE_PUBLIC_AUDIO"])
    raw=audio.read_bytes()
    assert len(raw)>5000
    digest=hashlib.sha256(raw).hexdigest()
    with fx.Session(app) as session:
        status=session.api("offline_speech_status")
        assert status["ready"] and status["engine"].startswith("myanmar-cpu-addon"),status
        assert status["modelName"]=="myanmar-asr-cpu-conformer"
        mid="public-burmese-real-0154"
        session.upload(mid,"mp3",raw)
        project={"title":"SYNTHETIC REAL CPU QA","chapters":[{"id":"qa-voice","number":1,
          "text":"စစ်ကောင်စီအတွက် လေယာဉ်ဆီရောင်းချဖြန့်ဖြူးပေးနေတဲ့ လူ",
          "audioAssetId":mid,"recordedSeconds":3.13,
          "subtitleCues":[],"scenePolicy":"major-only-conservative",
          "scenes":[{"id":"qa-shot","start":0,"duration":3.13,
            "visualLocked":True,"assetId":None,"text":"ဦးဘသိန်း သွားသည်။"}]}],
          "assets":[{"id":mid,"name":"public.mp3","type":"audio/mpeg","nativeStored":True}]}
        session.api("save_project_state",{"json":json.dumps(project,ensure_ascii=False)})
        local_sha=fx.sha(fx.DATA/"project-state.json")
        wav_sha=fx.sha(fx.DATA/"media"/(mid+".mp3"))
        started=session.api("start_transcription_job",{"chapterNumber":1,
            "sourceVideoId":mid,"sourceVideoExt":"mp3"})
        assert started["id"].startswith("speech-")
        for _ in range(300):
            job=session.api("get_transcription_job_status",{"id":started["id"]})
            if job["status"] in ("complete","failed","cancelled"):break
            time.sleep(1)
        else:
            session.api("cancel_transcription_job",{"id":started["id"]})
            raise AssertionError("Real installed model exceeded five minute QA limit")
        assert job["status"]=="complete",job
        result=job["result"]
        assert result["humanReviewRequired"] is True
        assert result["modelName"]=="myanmar-asr-cpu-conformer"
        assert result["source"].startswith("local Burmese CPU optional addon")
        subtitles=result["srt"]
        assert "-->" in subtitles and any("\u1000"<=c<="\u109f" for c in subtitles)
        assert fx.sha(fx.DATA/"project-state.json")==local_sha
        assert fx.sha(fx.DATA/"media"/(mid+".mp3"))==wav_sha
        saved=json.loads(session.api("load_project_state"))
        assert saved["chapters"][0]["subtitleCues"]==[]
        assert saved["chapters"][0]["scenes"][0]["visualLocked"] is True
        assert hashlib.sha256(audio.read_bytes()).hexdigest()==digest
        assert (fx.DATA/"transcripts"/result["file"]).read_text(encoding="utf-8")==subtitles
        print("PASS: exact PUBLISHED Windows Studio + real INSTALLED Burmese CPU model "+
              "-> private local unapproved SRT. Original audio, project and locks SHA intact.",flush=True)
if __name__=="__main__":
    main()
