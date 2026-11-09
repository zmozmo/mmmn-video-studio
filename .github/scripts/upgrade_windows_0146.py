"""Windows 0.14.6 — conservative MAJOR scene auto-draft (offline).

Installs the independent tested major-scene.mjs module into the real
Windows UI, without removing any 0.14.5 safety, save, speech, timing
or rendering logic. Only meaningful scene shifts cause image changes.
This is rule-based evidence; it MUST NOT claim semantic AI or perfect
voice-to-word recognition.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def replace(path,old,new):
    p=root/path
    text=p.read_text(encoding="utf-8")
    if text.count(old)!=1:
        raise ValueError(f"{path}: expected one anchor, got {text.count(old)}: {old[:88]}")
    p.write_text(text.replace(old,new),encoding="utf-8")
    print("WINDOWS 0.14.6 MAJOR-SCENE PATCH:",path,flush=True)

module=root/"web/major-scene.mjs"
if not module.is_file() or "export function consolidateMajorScenes" not in module.read_text(encoding="utf-8"):
    raise ValueError("Missing audited conservative scene module — no release permitted")
tests=root/"tests/major-scene.test.mjs"
if not tests.is_file() or "ordinary" not in tests.read_text(encoding="utf-8"):
    raise ValueError("Missing independent major scene regression tests — no release permitted")

replace("web/app.js",
        "import {makeOfflineDraft} from './auto-edit.mjs';",
        "import {makeOfflineDraft} from './auto-edit.mjs';\n"
        "import {consolidateMajorScenes} from './major-scene.mjs';")

replace("web/app.js",
        '<button class="btn" data-action="auto-edit-draft">✨ Auto Draft (SRT / Pause + ပုံ)</button>',
        '<button class="btn primary" data-action="major-only-scene-plan">'
        '🎬 အရေးကြီး Scene မှသာ ပုံပြောင်း (Auto Draft)</button>'
        '<button class="btn" data-action="auto-edit-draft">'
        '✨ Existing Auto Draft (SRT / Pause + ပုံ)</button>')

replace("web/app.js",
        '<button class="btn" data-action="generate-scenes">Auto Scenes (Resets edits)</button>',
        '<button class="btn primary" data-action="major-only-scene-plan">'
        '🎬 အရေးကြီးမှသာ ပုံပြောင်းမယ်</button>'
        '<button class="btn" data-action="generate-scenes">'
        'Auto Scenes (Resets edits)</button>')

# Avoid an inaccurate promise that this deterministic evidence is full
# Burmese ASR or model-level semantic story comprehension.
replace("web/app.js",
        'Auto Suggest က မြန်မာစာလုံးတူညီမှုအလိုက် ပုံ ID ကို အကြံပြုတာသာ ဖြစ်ပြီး AI က ဇာတ်လမ်းအဓိပ္ပာယ်အပြည့်အစုံ နားလည်တာမဟုတ်ပါ။',
        'Auto Major Scenes က မိုးရွာတယ်ဆိုတာနဲ့မပြောင်းဘဲ '
        'နေရာကြီးပြောင်းခြင်း၊ မိုးသည်းပြီးမှောင်မိုက်ခြင်း၊ '
        'အရေးကြီးအဖြစ်အပျက်တို့မှာသာ နောက်ခံပြောင်းရန် အကြံပြုပါတယ်။ '
        'Offline စည်းမျဉ်းနဲ့ SRT/အသံရပ်နားချက်ကို သုံးထားပြီး '
        'အပြည့်အဝ AI ဇာတ်လမ်းနားလည်မှု မဟုတ်ပါ။')

# New non-destructive user opt-in: use existing SRT timing if available,
# otherwise query the already installed FFmpeg pause analyzer. Neither
# path fabricates a word-accurate speech recognition transcript.
new_action=r'''  case 'major-only-scene-plan':{
    const existing=c.scenes?.length?c:{...c,scenes:makeScenes(c,project.settings)};
    let inputChapter=existing;
    let pauseEvidence=false;
    if(!(c.subtitleCues||[]).length && window.__MMMN_TRIAL__ &&
       (c.videoAssetId||c.audioAssetId) && Number(c.recordedSeconds)>0){
      const recording=(project.assets||[]).find(a=>a.id===(c.videoAssetId||c.audioAssetId));
      if(recording){
        try {
          toast('အသံရပ်နားချိန်များကို စက်ထဲမှာပဲ စစ်နေပါတယ်…');
          const plan=await window.__TAURI__.core.invoke('analyze_narration_pauses',{
            chapterNumber:c.number,chapterId:c.id,sourceVideoId:recording.id,
            sourceVideoExt:recording.name.split('.').at(-1).toLowerCase(),
            recordedSeconds:c.recordedSeconds,
            scenes:existing.scenes.map(sc=>({
              id:sc.id,text:sc.text,start:sc.start,
              duration:sc.duration,alignment:sc.alignment
            }))
          });
          const timed=applyPauseTimingPlan(existing,plan);
          inputChapter={...existing,scenes:timed.scenes};
          pauseEvidence=timed.proposed>0;
        } catch(error){
          toast('အသံရပ်နားချိန်ကို အတိအကျမရပါ။ မူလအချိန်ခန့်မှန်းချက်ကိုပဲ သုံးမယ်။ '+error.message,true);
        }
      }
    }
    try {
      const draft=makeOfflineDraft(inputChapter,
        project.visualRequirements||[],project.assets||[]);
      const planned=consolidateMajorScenes(draft.scenes,{minHoldSeconds:75});
      const info=planned.report;
      const timing=(c.subtitleCues||[]).length?'SRT (review required)':
        pauseEvidence?'Audio pauses (estimated, review required)':
        'စာသားအရှည် ခန့်မှန်းချက်သာ — Audio နဲ့စစ်ရန်';
      const msg='အရေးကြီးတဲ့ Scene မှသာ ပုံပြောင်းမယ်။\n\n'+
        'မူလ Scene: '+info.originalScenes+
        '\nအကြံပြုနောက်ခံပုံပြောင်းမယ့် Scene: '+info.majorScenes+
        '\nမပြောင်းဘဲ ပုံအဟောင်းထားမယ့် Boundary: '+info.heldBoundaries+
        '\nManual Lock မထိ: '+info.manualBoundariesProtected+
        '\nအချိန်အထောက်အထား: '+timing+
        '\n\nဒီဟာက မြန်မာစာအကြောင်းအရာကို AI အပြည့်အဝနားလည်တာမဟုတ်ပါ။'+
        '\nပုံတွေကို အလိုအလျောက်မဖန်တီးပါ။ ရွေးထားတာတွေကို မဖြစ်မနေပြန်စစ်ရမယ်။'+
        '\nမူရင်းအသံ၊ စာမူ၊ Google Drive မပြင်ပါ။'+
        '\n\nအကြံပြုထားတဲ့ Draft ကို Save လုပ်မလား?';
      if(!confirm(msg))return;
      checkpoint(c,'Major-visual-only offline auto draft');
      c.scenes=planned.scenes;
      c.scenePolicy='major-only-conservative';
      c.alignmentSummary='Major-only draft: '+info.majorScenes+' image scenes of '+
        info.originalScenes+' original; '+timing+'; all picture choices require review.';
      save();
      await render();
      toast('အရေးကြီးတဲ့အခါမှသာ ပုံပြောင်းမယ့် Draft ကို သိမ်းထားပါပြီ။ Review ပြန်စစ်ပါ။');
    } catch(error){
      toast('Major-only Scene Draft မသိမ်းပါ: '+error.message,true);
    }
    return;
  }
'''
replace("web/app.js","  case 'auto-edit-draft':{",new_action+"  case 'auto-edit-draft':{")

# Version metadata and existing retained test witnesses. The increment
# occurs AFTER 0145 patch, and does NOT recreate 0144 storage patch.
replace("web/app.js",
        "MMMN Windows Offline Studio • v0.14.5",
        "MMMN Windows Offline Studio • v0.14.6")
replace("tests/windows_atomic_save_0144_test.py",
        "Windows Offline Studio • v0.14.5",
        "Windows Offline Studio • v0.14.6")
replace("tests/windows_long_probe_0145_test.py",
        "MMMN Windows Offline Studio • v0.14.5",
        "MMMN Windows Offline Studio • v0.14.6")

for rel in ("version.txt","package.json","src-tauri/Cargo.toml",
            "src-tauri/tauri.conf.json",
            "tests/release-safety-v013.test.mjs",
            "tests/windows-final-artifact-gate.test.mjs",
            ".github/workflows/windows-installer-upgrade-lab.yml",
            "tests/windows_installer_probe.py",
            "tests/windows_installer_probe_test.py"):
    p=root/rel
    raw=p.read_text(encoding="utf-8")
    if "0.14.5" not in raw and "installer-lab-0145-" not in raw:
        raise ValueError("0.14.5 version witness missing: "+rel)
    p.write_text(raw.replace("0.14.5","0.14.6").replace(
        "installer-lab-0145-","installer-lab-0146-"),encoding="utf-8")

gate=root/"tests/windows-final-artifact-gate.test.mjs"
raw=gate.read_text(encoding="utf-8")
if r"0\.14\.5" not in raw:
    raise ValueError("0.14.5 strict version regex absent")
gate.write_text(raw.replace(r"0\.14\.5",r"0\.14\.6"),encoding="utf-8")

ui=(root/"web/app.js").read_text(encoding="utf-8")
for marker in ("major-only-scene-plan","consolidateMajorScenes",
               "Manual Lock မထိ","scenePolicy='major-only-conservative'"):
    if marker not in ui:raise ValueError("Missing major-scene UI integration: "+marker)
print("WINDOWS 0.14.6 PATCH COMPLETE — major-scene UI, conservative timing + visual planning, manual edits preserved",flush=True)
