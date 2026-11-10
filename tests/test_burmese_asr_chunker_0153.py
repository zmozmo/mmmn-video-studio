import unittest,importlib.util,math,os,tempfile
from unittest.mock import patch
from pathlib import Path
spec=importlib.util.spec_from_file_location("asr",
    Path(__file__).resolve().parents[1]/"scripts"/"burmese_asr_chunker_0153.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ChunkTests(unittest.TestCase):
 def test_90_minutes_complete_cover(self):
  chunks=m.split_duration(5400,[])
  self.assertEqual(chunks[0]["start"],0)
  self.assertEqual(chunks[-1]["end"],5400)
  self.assertGreater(len(chunks),100)
  self.assertLessEqual(max(x["end"]-x["start"] for x in chunks),28.001)
  self.assertTrue(all(a["end"]==b["start"] for a,b in zip(chunks,chunks[1:])))
 def test_prefer_actual_speech_pause(self):
  rows=m.split_duration(80,[15,37,55,70])
  self.assertEqual(rows[0]["end"],15)
  self.assertTrue(rows[0]["pause_aligned"])
 def test_force_cut_clearly_marked(self):
  rows=m.split_duration(81,[])
  self.assertTrue(any(not x["pause_aligned"] for x in rows))
 def test_short_audio(self):
  self.assertEqual(m.split_duration(3,[]),[{"start":0.0,"end":3,"pause_aligned":False}])
 def test_reject_bad_or_overlong(self):
  for value in [-1,0,float("nan"),float("inf"),5401]:
   with self.assertRaises(ValueError):m.split_duration(value,[])
 def test_no_empty_srt(self):
  with self.assertRaises(ValueError):m.srt_from_segments([{"start":0,"end":10}],[""])
 def test_myanmar_srt_format(self):
  text=m.srt_from_segments([{"start":0,"end":3.5}],
    ["ဦးဘသိန်း ရွာဟောင်းသို့ ရောက်ခဲ့သည်။"])
  self.assertIn("00:00:00,000 --> 00:00:03,500",text)
  self.assertIn("ဦးဘသိန်း",text)
 def test_no_invented_words(self):
  with self.assertRaises(ValueError):m.srt_from_segments([
    {"start":0,"end":3}],["English only no recognized Burmese"])
 def test_srt_does_not_change_source_segments(self):
  original=[{"start":0,"end":8.0,"pause_aligned":False}]
  before=[dict(x) for x in original]
  m.srt_from_segments(original,["ရွာဟောင်းအကြောင်း"])
  self.assertEqual(original,before)
 def test_srt_raises_when_segments_do_not_match_predictions(self):
  with self.assertRaises(ValueError):m.srt_from_segments([{"start":0,"end":10}],[])
 def test_ffmpeg_failure_does_not_generate_fake_audio(self):
  with self.assertRaises((OSError,RuntimeError)):m.run_program(["this-never-exists-mmmn"],timeout=1)
 def test_missing_local_model_is_safe_no_download(self):
  with self.assertRaises(FileNotFoundError):
   m.load_model_only_from_disk("/no/such/private/model/folder")
 def test_packaged_studio_ffmpeg_is_exposed_to_local_model_only(self):
  with tempfile.TemporaryDirectory() as tmp:
   exe=Path(tmp)/("ffmpeg.exe" if os.name=="nt" else "ffmpeg")
   exe.write_bytes(b"dummy, only used to test PATH selection")
   with patch.dict(os.environ,{"PATH":"ORIGINAL_OS_PATH"}):
    actual=m.expose_local_ffmpeg_to_embedded_transcriber(str(exe))
    self.assertEqual(actual,str(Path(tmp).resolve()))
    self.assertEqual(os.environ["PATH"].split(os.pathsep)[0],str(Path(tmp).resolve()))
    self.assertIn("ORIGINAL_OS_PATH",os.environ["PATH"])
 def test_never_downloads_when_local_ffmpeg_is_missing(self):
  with self.assertRaises(FileNotFoundError):
   m.expose_local_ffmpeg_to_embedded_transcriber("/should-not-exist-mmmn-ffmpeg/ffmpeg.exe")
if __name__=="__main__":unittest.main()
