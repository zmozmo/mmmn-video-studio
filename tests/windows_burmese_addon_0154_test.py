"""Native backend tests for optional FULLY LOCAL Myanmar ASR addon.

The fake EXE/model exercise routing, fail-closed missing dependencies,
and no original narration modifications. These tests do not claim the
real model is present or accurate.
"""
import importlib.util,subprocess,tempfile,unittest,threading
from pathlib import Path
from unittest.mock import patch

SRC=Path("portable/studio_server.py").resolve()
spec=importlib.util.spec_from_file_location("mmmn_pinned_native_0154",SRC)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class BurmeseASRAddonTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix="mmmn-0154-local-addon-")
  self.addCleanup(self.tmp.cleanup)
  root=Path(self.tmp.name)
  self.studio=mod.Studio.__new__(mod.Studio)
  self.studio.root=root
  self.studio.ffmpeg=str(root/"ffmpeg.exe")
  (root/"ffmpeg.exe").write_bytes(b"synthetic only")
  (root/"ffprobe.exe").write_bytes(b"synthetic only")
  for name in ("transcripts","media","models","tools"):
   (root/name).mkdir(exist_ok=True)
  self.voice=root/"media"/"testvoice.wav"
  self.voice.write_bytes(b"ORIGINAL VOICE MUST BE LEFT UNCHANGED")
  self.original=self.voice.read_bytes()
 def install_fake_addon(self):
  addon=self.studio.root/"addons"/"BurmeseASR"
  model=addon/"model"
  model.mkdir(parents=True)
  (addon/"mmmn-burmese-asr.exe").write_bytes(b"dummy .exe - do not run")
  for file in ("model.py","transcribe.py","vocab.json",
               "cmvn.json","config.json","preprocessor_config.json"):
   (model/file).write_text("{}",encoding="utf8")
  with (model/"model.safetensors").open("wb") as out:
   out.truncate(80_000_002)
  return addon
 def test_model_not_ready_by_default(self):
  self.assertIsNone(self.studio._burmese_asr_addon())
  status=self.studio.offline_speech_status()
  self.assertFalse(status["ready"])
 def test_real_stable_local_folder_detection_no_download(self):
  self.install_fake_addon()
  status=self.studio.offline_speech_status()
  self.assertTrue(status["ready"])
  self.assertTrue(status["engine"].startswith("myanmar-cpu-addon"))
  self.assertEqual(status["modelName"],"myanmar-asr-cpu-conformer")
 def test_no_weights_or_executable_fails_closed(self):
  addon=self.install_fake_addon()
  (addon/"model"/"model.safetensors").unlink()
  self.assertIsNone(self.studio._burmese_asr_addon())
  self.assertFalse(self.studio.offline_speech_status()["ready"])
  with (addon/"model"/"model.safetensors").open("wb") as out:out.truncate(80_000_002)
  (addon/"mmmn-burmese-asr.exe").unlink()
  self.assertIsNone(self.studio._burmese_asr_addon())
 def test_realistic_srt_from_subprocess_is_review_only_and_preserves_wav(self):
  self.install_fake_addon()
  srt="1\n00:00:00,000 --> 00:00:04,000\nဦးဘသိန်းသည် ရွာဟောင်းသို့ သွားသည်။\n"
  commands=[]
  def fake_run(args,timeout,cancel):
   commands.append((args,timeout))
   Path(args[args.index("--output")+1]).write_text(srt,encoding="utf-8")
   return subprocess.CompletedProcess(args,0,"","")
  with patch.object(self.studio,"_run_speech_step",side_effect=fake_run):
   result=self.studio._transcribe_burmese_addon(1,self.voice)
  self.assertEqual(result["srt"],srt)
  self.assertTrue(result["humanReviewRequired"])
  self.assertIn("--model-dir",commands[0][0])
  self.assertIn("--ffmpeg",commands[0][0])
  self.assertIn("--ffprobe",commands[0][0])
  self.assertEqual(self.original,self.voice.read_bytes())
  path=self.studio.root/"transcripts"/result["file"]
  self.assertEqual(path.read_text(encoding="utf-8"),srt)
 def test_failure_never_generates_visible_subtitle_file(self):
  self.install_fake_addon()
  def fail(args,timeout,cancel):
   return subprocess.CompletedProcess(args,1,"","inference failed")
  with patch.object(self.studio,"_run_speech_step",side_effect=fail):
   with self.assertRaisesRegex(ValueError,"recognition failed"):
    self.studio._transcribe_burmese_addon(1,self.voice)
  self.assertEqual(list((self.studio.root/"transcripts").glob("*.srt")),[])
  self.assertEqual(self.voice.read_bytes(),self.original)
 def test_cancellation_never_persists_partial_subtitles(self):
  self.install_fake_addon()
  cancelled=threading.Event()
  def fake_run(args,timeout,cancel):
   Path(args[args.index("--output")+1]).write_text(
    "1\n00:00:00,000 --> 00:00:02,000\nဦးဘသိန်း\n",encoding="utf-8")
   cancelled.set()
   return subprocess.CompletedProcess(args,0,"","")
  with patch.object(self.studio,"_run_speech_step",side_effect=fake_run):
   with self.assertRaisesRegex(ValueError,"cancelled"):
    self.studio._transcribe_burmese_addon(1,self.voice,_cancel=cancelled)
  self.assertEqual(list((self.studio.root/"transcripts").glob("*.srt")),[])
 def test_app_route_uses_same_addon_after_status(self):
  self.install_fake_addon()
  # Native routing; no fake voices submitted to real CPU neural model.
  with patch.object(self.studio,"_transcribe_burmese_addon",
                    return_value={"source":"addon","srt":"REVIEW"}):
   result=self.studio.transcribe_narration(
    chapterNumber=1,sourceVideoId="testvoice",sourceVideoExt="wav")
  self.assertEqual(result["source"],"addon")
  self.assertEqual(self.voice.read_bytes(),self.original)
 def test_bad_source_path_cannot_invoke_optional_model(self):
  self.install_fake_addon()
  with self.assertRaises(ValueError):
   self.studio.transcribe_narration(chapterNumber=1,
    sourceVideoId="../escape",sourceVideoExt="wav")
 def test_no_spurious_files_are_created_by_status(self):
  self.install_fake_addon()
  before=list(self.studio.root.rglob("*.srt"))
  self.studio.offline_speech_status()
  self.assertEqual(before,list(self.studio.root.rglob("*.srt")))

if __name__=="__main__":
 unittest.main()
