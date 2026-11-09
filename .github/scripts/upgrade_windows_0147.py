"""Windows 0.14.7: major-only artwork brief and optional audio-first SRT draft.

Apply only after all verified 0.14.1–0.14.6 patches. Never delete a
user's manual picture/time locks, never invent illustrations, never send
narration or manuscript to a cloud service. Local whisper.cpp MODEL and
CLI are optional and MUST already be present to use auto transcription.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def replace(rel,old,new):
    p=root/rel
    s=p.read_text(encoding="utf-8")
    if s.count(old)!=1:
        raise ValueError("Expected exactly one 0.14.6 UI witness in "+rel+
                         ", found "+str(s.count(old))+": "+old[:90])
    p.write_text(s.replace(old,new),encoding="utf-8")
    print("PATCH 0.14.7",rel,flush=True)

module=root/"web/major-artwork-brief.mjs"
tests=root/"tests/major-artwork-brief.test.mjs"
if not module.is_file() or "buildMajorArtworkBrief" not in module.read_text(encoding="utf-8"):
    raise ValueError("Important-artwork brief module not installed")
if not tests.is_file() or "technical continuation" not in tests.read_text(encoding="utf-8"):
    raise ValueError("Important-artwork brief regression tests missing")

replace("web/app.js",
        "import {consolidateMajorScenes} from './major-scene.mjs';",
        "import {consolidateMajorScenes} from './major-scene.mjs';\n"
        "import {buildMajorArtworkBrief} from './major-artwork-brief.mjs';")

# Audio-first is OPTIONAL: no bundled ASR model and no silent downloads.
# It falls back to existing pause/SRT timing if speech model is missing.
replace("web/app.js",
        '<button class="btn primary" data-action="major-only-scene-plan">'
        '🎬 အရေးကြီး Scene မှသာ ပုံပြောင်း (Auto Draft)</button>',
        '<button class="btn primary" data-action="audio-first-major-plan">'
        '🎧 အသံဖတ်ပြချက်နဲ့ အရေးကြီး Scene (Offline Model ရှိမှ)</button>'
        '<button class="btn" data-action="major-only-scene-plan">'
        '🎬 အရေးကြီး Scene မှသာ ပုံပြောင်း (Auto Draft)</button>')

replace("web/app.js",
        '<button class="btn" data-action="export-missing">⬇ Missing Image CSV</button>',
        '<button class="btn" data-action="export-missing">⬇ Missing Image CSV</button>'
        '<button class="btn primary" data-action="export-major-picture-brief">'
        '🖼 အရေးကြီး Scene ပုံလိုအပ်ချက်သာ ထုတ်ရန်</button>')

new_cases=r'''  case 'export-major-picture-brief':{
    try{
      const summary=buildMajorArtworkBrief(c,project.assets||[],{title:project.title});
      if(!confirm('အရေးကြီး Scene '+summary.majorBeats+' ခုအတွက်သာ ပုံစာရင်းထုတ်မယ်။\n'+
        'ရှိပြီးသားပုံ: '+summary.linkedPictures+
        '\nပုံအသစ်လိုနေသော Scene: '+summary.missingPictures+
        '\nအတွင်းပိုင်း Renderer Scene ကို မတွက်ပါ: '+summary.skippedTechnicalContinuations+
        '\n\nဒီဖိုင်ထဲမှာ မထုတ်ဝေသေးတဲ့ စာမူအပိုင်းများ ပါနိုင်ပါတယ်။'+
        '\nစက်ထဲမှာသာ သိမ်းပြီး Public GitHub မတင်ပါနဲ့။ ဆက်လုပ်မလား?'))return;
      download(new Blob([summary.markdown],
        {type:'text/markdown;charset=utf-8'}),
        'MMMN-ch'+String(c.number).padStart(2,'0')+'-MAJOR-IMAGES-ONLY.md');
      toast('အရေးကြီး Scene '+summary.majorBeats+' ခုအတွက် ပုံလိုအပ်ချက်ဖိုင် ထုတ်ပြီးပါပြီ။');
    }catch(error){
      toast('ပုံလိုအပ်ချက် မထုတ်နိုင်ပါ: '+error.message,true);
    }
    return;
  }
'''
replace("web/app.js",
        "case 'major-only-scene-plan':{",
        new_cases+"""case 'audio-first-major-plan':
  case 'major-only-scene-plan':{
    // New optional AUDIO-first path. This is real local whisper.cpp only
    // when the caller has provided its executable and a multilingual model.
    // No cloud calls and no forced overwrite of edited/corrected SRT.
    let newLocalCues=null;
    if(action==='audio-first-major-plan' && !(c.subtitleCues||[]).length &&
       window.__MMMN_TRIAL__ && (c.videoAssetId||c.audioAssetId) &&
       Number(c.recordedSeconds)>0){
      const recording=(project.assets||[]).find(a=>a.id===(c.videoAssetId||c.audioAssetId));
      if(recording){
        try{
          const state=await window.__TAURI__.core.invoke('offline_speech_status');
          if(!state?.ready){
            toast('Whisper.cpp Offline Model မရှိသေးပါ။ အသံရပ်နားချက်အလိုက် '
              +'ခန့်မှန်း Scene Draft ကို ဆက်လုပ်မယ်။',true);
          } else if(confirm('Local Multilingual Speech Model တွေ့ပါတယ်။ '
              +'ဖတ်ပြအသံကို စက်ထဲမှာပဲ မြန်မာ SRT အဖြစ် ပြောင်းမယ်။ '
              +'အချိန်ကြာနိုင်ပြီး မြန်မာစာမှန်မမှန် ပြန်စစ်ဖို့လိုပါတယ်။ '
              +'မလုပ်ချင်ရင် Cancel နှိပ်ပြီး Pause Timing နဲ့ ဆက်လုပ်မယ်။')){
            toast('Offline Myanmar Speech-to-Text လုပ်နေပါတယ်…');
            const generated=await window.__TAURI__.core.invoke('transcribe_narration',{
              chapterNumber:c.number,sourceVideoId:recording.id,
              sourceVideoExt:recording.name.split('.').at(-1).toLowerCase()
            });
            const cues=parseSRT(generated.srt||'');
            if(!cues.length)throw Error('Offline Speech-to-Text မှ SRT စာသားမရပါ');
            const checked=subtitleDiagnostics(cues,c.recordedSeconds);
            if(checked.warnings.length){
              toast('SRT Timing မကိုက်သေးပါ။ မူလ SRT ကို မပြင်ဘဲ Pause Timing ကို ဆက်သုံးမယ်။',true);
            }else{
              newLocalCues=cues;
              toast('Offline Myanmar SRT '+cues.length+' ကြောင်း စက်ထဲမှာရပါပြီ။ '
                +'စာလုံးမှားနိုင်၍ Preview ပြန်စစ်ပါ။');
            }
          }
        }catch(error){
          toast('Offline အသံမှစာပြောင်းခြင်း မအောင်မြင်ပါ: '+error.message+
            '။ Pause Timing ကိုပဲ သုံးမယ်။',true);
        }
      }
    }
    const working=newLocalCues?{...c,subtitleCues:newLocalCues}:c;""")

replace("web/app.js",
        "const existing=c.scenes?.length?c:{...c,scenes:makeScenes(c,project.settings)};",
        "const existing=working.scenes?.length?working:"
        "{...working,scenes:makeScenes(working,project.settings)};")
replace("web/app.js",
        "if(!(c.subtitleCues||[]).length && window.__MMMN_TRIAL__ &&",
        "if(!(working.subtitleCues||[]).length && window.__MMMN_TRIAL__ &&")
replace("web/app.js",
        "const timing=(c.subtitleCues||[]).length?'SRT (review required)':",
        "const timing=(working.subtitleCues||[]).length?"
        "'Offline Myanmar SRT / imported SRT (must proofread)':")
replace("web/app.js",
        "checkpoint(c,'Major-visual-only offline auto draft');\n      c.scenes=planned.scenes;",
        "checkpoint(c,'Major-visual-only offline auto draft');\n"
        "      if(newLocalCues)c.subtitleCues=newLocalCues;\n"
        "      c.scenes=planned.scenes;")

replace("web/app.js",
        "MMMN Windows Offline Studio • v0.14.6",
        "MMMN Windows Offline Studio • v0.14.7")
replace("tests/windows_atomic_save_0144_test.py",
        "Windows Offline Studio • v0.14.6",
        "Windows Offline Studio • v0.14.7")
replace("tests/windows_long_probe_0145_test.py",
        "MMMN Windows Offline Studio • v0.14.6",
        "MMMN Windows Offline Studio • v0.14.7")

for rel in ("version.txt","package.json","src-tauri/Cargo.toml",
            "src-tauri/tauri.conf.json",
            "tests/release-safety-v013.test.mjs",
            "tests/windows-final-artifact-gate.test.mjs",
            ".github/workflows/windows-installer-upgrade-lab.yml",
            "tests/windows_installer_probe.py",
            "tests/windows_installer_probe_test.py"):
    p=root/rel
    raw=p.read_text(encoding="utf-8")
    if "0.14.6" not in raw and "installer-lab-0146-" not in raw:
        raise ValueError("0.14.6 version witness missing: "+rel)
    p.write_text(raw.replace("0.14.6","0.14.7").replace(
        "installer-lab-0146-","installer-lab-0147-"),encoding="utf-8")

gate=root/"tests/windows-final-artifact-gate.test.mjs"
raw=gate.read_text(encoding="utf-8")
if r"0\.14\.6" not in raw:
    raise ValueError("0.14.6 strict version regex missing")
gate.write_text(raw.replace(r"0\.14\.6",r"0\.14\.7"),encoding="utf-8")

final=(root/"web/app.js").read_text(encoding="utf-8")
for witness in ("buildMajorArtworkBrief","export-major-picture-brief",
                "audio-first-major-plan","offline_speech_status",
                "transcribe_narration","if(newLocalCues)c.subtitleCues=newLocalCues"):
    if witness not in final:raise ValueError("Windows 0.14.7 UI witness missing: "+witness)
print("Windows 0.14.7 patch COMPLETE: important picture brief + optional local voice-to-SRT on one-click Smart Draft",flush=True)
