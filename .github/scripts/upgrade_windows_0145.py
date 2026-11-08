"""Windows 0.14.5: fix 90/120-minute MP4 verification timeout without skipping frame count.

Apply AFTER verified incremental patches 0.14.1, .2, .3, .4.
90/120-minute synthetic public EXE acceptance proved that 0.14.4 encoded
the video but failed during FFprobe -count_frames due to hard-coded 180s.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()

def replace_once(rel,old,new):
    file=root/rel
    s=file.read_text(encoding="utf-8")
    count=s.count(old)
    if count!=1:
        raise ValueError(f"{rel}: expected one exact anchor; got {count}: {old[:85]!r}")
    file.write_text(s.replace(old,new),encoding="utf-8")
    print("WINDOWS 0.14.5 PATCH:",rel,flush=True)

server=root/"portable/studio_server.py"
source=server.read_text(encoding="utf-8")
anchor="""    RENDER_FPS = 30

    # Cache only reproducible ENCODED VIDEO SCENES"""
replacement="""    RENDER_FPS = 30

    @staticmethod
    def full_export_probe_timeout(seconds):
        # Count every actual H.264 frame to catch incomplete novel videos.
        # Decoding 162,000+ frames on Windows takes longer than the old fixed
        # 180 seconds, even after the MP4 itself was encoded successfully.
        # Limit the verification time but scale fairly for long novel videos.
        import math
        if not isinstance(seconds,(int,float)) or not math.isfinite(seconds) or seconds<=0:
            raise ValueError('Invalid MP4 duration for final frame verification')
        return max(180,min(3600,int(seconds*0.25)+120))

    # Cache only reproducible ENCODED VIDEO SCENES"""
if source.count(anchor)!=1:
    raise ValueError("Expected one RENDER_FPS/scene-cache anchor")
source=source.replace(anchor,replacement)
start=source.index("    def render_chapter_command(")
end=source.index("\n\nALLOWED =",start)
render=source[start:end]
if render.count("timeout=180)")!=1:
    raise ValueError("Expected one fixed 180s FFprobe verification timeout inside renderer")
render=render.replace("timeout=180)",
    "timeout=self.full_export_probe_timeout(recordedSeconds))")
source=source[:start]+render+source[end:]
if "self.full_export_probe_timeout(recordedSeconds)" not in render:
    raise ValueError("Final full-MP4 verification timeout patch not applied")
server.write_text(source,encoding="utf-8")
print("WINDOWS 0.14.5: full MP4 FFprobe frame-count verification now length-aware",flush=True)

# Retain original 0.14.4 source-safety regressions, update only the
# installed UI version witness. Original 0.14.4 source patch stays unchanged.
replace_once("web/app.js",
             "MMMN Windows Offline Studio • v0.14.4",
             "MMMN Windows Offline Studio • v0.14.5")
replace_once("tests/windows_atomic_save_0144_test.py",
             "Windows Offline Studio • v0.14.4",
             "Windows Offline Studio • v0.14.5")

for rel in ("version.txt","package.json","src-tauri/Cargo.toml",
            "src-tauri/tauri.conf.json","tests/release-safety-v013.test.mjs",
            "tests/windows-final-artifact-gate.test.mjs",
            ".github/workflows/windows-installer-upgrade-lab.yml",
            "tests/windows_installer_probe.py","tests/windows_installer_probe_test.py"):
    p=root/rel
    s=p.read_text(encoding="utf-8")
    if "0.14.4" not in s and "installer-lab-0144-" not in s:
        raise ValueError("0.14.4 version witness missing: "+rel)
    p.write_text(s.replace("0.14.4","0.14.5").replace(
        "installer-lab-0144-","installer-lab-0145-"),encoding="utf-8")
gate=root/"tests/windows-final-artifact-gate.test.mjs"
text=gate.read_text(encoding="utf-8")
if r"0\.14\.4" not in text:
    raise ValueError("Strict version 0.14.4 regex witness not found")
gate.write_text(text.replace(r"0\.14\.4",r"0\.14\.5"),encoding="utf-8")

unit=r'''"""Version 0.14.5: long-duration MP4 verification timeouts."""
from pathlib import Path
import inspect
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"portable"))
from studio_server import Studio

class FullNovelVerificationTimeoutTest(unittest.TestCase):
    def test_short_video_keeps_bounded_quick_verification(self):
        self.assertEqual(Studio.full_export_probe_timeout(1),180)
        self.assertEqual(Studio.full_export_probe_timeout(15),180)
    def test_15_minute_video_has_proportional_checking_window(self):
        self.assertGreater(Studio.full_export_probe_timeout(900),180)
    def test_full_novel_90_minutes_gets_sufficient_checking_time(self):
        self.assertGreaterEqual(Studio.full_export_probe_timeout(5400),1000)
    def test_two_hour_resilience_has_larger_probe_window(self):
        self.assertGreater(Studio.full_export_probe_timeout(7200),
                           Studio.full_export_probe_timeout(5400))
    def test_probe_timeout_is_always_finite_bounded(self):
        self.assertLessEqual(Studio.full_export_probe_timeout(43200),3600)
        with self.assertRaises(ValueError):
            Studio.full_export_probe_timeout(float("nan"))
    def test_renderer_keeps_independent_full_frame_count_validation(self):
        source=inspect.getsource(Studio.render_chapter_command)
        self.assertIn("'-count_frames'",source)
        self.assertIn("timeout=self.full_export_probe_timeout(recordedSeconds)",source)
        self.assertNotIn("timeout=180)",source)
    def test_version_witness_in_installed_ui(self):
        ui=(Path(__file__).resolve().parents[1]/"web/app.js").read_text(encoding="utf-8")
        self.assertIn("MMMN Windows Offline Studio • v0.14.5",ui)

if __name__=="__main__":unittest.main()
'''
target=root/"tests/windows_long_probe_0145_test.py"
if target.exists():
    raise ValueError("0.14.5 regression test already exists")
target.write_text(unit,encoding="utf-8")
print("WINDOWS 0.14.5 PATCH COMPLETE; length-scaled FFprobe + seven regression cases",flush=True)
