"""Windows 0.15.5 — conservative local imported-picture proposals for major scenes.

Never generate/download art, never insert an extra image switch, preserve
original narration, manually chosen art, timing locks and data backups.
Only user-imported nativeStored images with unique grounded scene labels
are candidates; every proposal requires a separate explicit confirmation.
Apply after all pinned 0.14.1 -> 0.15.4 native patches.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def once(rel,before,after):
 p=root/rel
 s=p.read_text(encoding='utf-8')
 if s.count(before)!=1:
  raise ValueError(f'{rel}: required 0.15.4 source anchor not unique ({s.count(before)}): {before[:75]}')
 p.write_text(s.replace(before,after),encoding='utf-8')
 print('WINDOWS 0.15.5 PATCH',rel,flush=True)
module=root/'web/local-major-artwork-match.mjs'
tests=root/'tests/local-major-artwork-match.test.mjs'
if not module.is_file() or 'applyConfirmedLocalMajorArtwork' not in module.read_text(encoding='utf-8'):
 raise ValueError('Conservative local imagery audit module missing')
if not tests.is_file() or 'metadata-only picture' not in tests.read_text(encoding='utf-8'):
 raise ValueError('Native Stored only picture label guards missing')
once('web/app.js',
 "import {buildMajorSceneTimingEvidence} from './major-scene-timing-evidence.mjs';",
 "import {buildMajorSceneTimingEvidence} from './major-scene-timing-evidence.mjs';\n"+
 "import {proposeLocalMajorArtwork,applyConfirmedLocalMajorArtwork} from './local-major-artwork-match.mjs';")
once('web/app.js',
 '<button class="btn primary" data-action="export-major-picture-brief">',
 '<button class="btn" data-action="match-local-major-images">🖼️ အရေးကြီး Scene အတွက် ရှိပြီးပုံများ စစ်ရွေးရန်</button>\n'
 '<button class="btn primary" data-action="export-major-picture-brief">')
once('web/app.js',
 "case 'export-major-timing-evidence':{",
 """case 'match-local-major-images':{
    try{
      const match=proposeLocalMajorArtwork(c,project.assets||[]);
      const s=match.report;
      if(!s.uniqueLabelCandidates){
        toast('အရေးကြီး Scene တွေနဲ့ တိတိကျကျကိုက်တဲ့ Import လုပ်ပြီးသားပုံ မတွေ့ပါ။ '
          +'စာသား/ပုံနာမည်စစ်ပြီး လိုအပ်တဲ့ပုံကို ကိုယ်တိုင်ရွေးနိုင်ပါတယ်။');
        return;
      }
      const ok=confirm(
        'အရေးကြီး Scene အတွက် Import လုပ်ပြီးသားပုံများ စစ်ဆေးချက်\\\\n'+
        'တစ်နေရာတည်း ကိုက်တဲ့ပုံ: '+s.uniqueLabelCandidates+'\\\\n'+
        'ပုံတူများ မသေချာ: '+s.ambiguousCandidates+'\\\\n'+
        'လိုအပ်နေသောပုံ: '+s.missingPictures+'\\\\n'+
        'ရှိပြီး/Manual Lock: '+s.existingOrLockedImagesKept+'\\\\n'+
        'နောက်ခံပုံအသစ် ဖန်တီးမည်: 0\\\\n'+
        'Scene အသစ် ဖြည့်မည်: 0\\\\n\\\\n'+
        'ရှိပြီးသားပုံနာမည်/Tag ကိုသာ စစ်ပြီး ရွေးပေးတဲ့ အကြံပြုချက်ပါ။ '+
        'ဓာတ်ပုံအကြောင်းအရာကို AI က မမြင်နိုင်ပါ။'+
        ' မူရင်းအသံ၊ Manual Lock၊ ပုံအတည်ပြုချက်၊ မူလ Scene Timing မပြင်ပါ။'+
        '\\\\nအကြံပြုထားတဲ့ပုံကို Review လုပ်ရန်အဖြစ် သုံးမလား?');
      if(!ok)return;
      const selected=applyConfirmedLocalMajorArtwork(c,project.assets||[],true);
      if(!selected.appliedCandidates){toast('အတည်ပြုနိုင်တဲ့ ပုံအကြံပြုချက် မရှိပါ။');return;}
      checkpoint(c,'Offline native-only important scene picture suggestions');
      c.scenes=selected.scenes;
      c.localImageMatchSummary='Offline imported picture labels: '+
        selected.appliedCandidates+' review-only picture proposals; no scene timing changes.';
      save();
      await render();
      toast('အရေးကြီး Scene '+selected.appliedCandidates+
        ' ခုမှာ ရှိပြီးသားပုံကို Review အဖြစ် ရွေးထားပါပြီ။ ပုံတစ်ပုံချင်းစီ ပြန်စစ်ပါ။');
    }catch(error){
      toast('Import လုပ်ပြီးသားပုံ ရွေးချယ်ရန် မအောင်မြင်ပါ: '+error.message,true);
    }
    return;
  }
  case 'export-major-timing-evidence':{""")
once('web/app.js','MMMN Windows Offline Studio • v0.15.4',
 'MMMN Windows Offline Studio • v0.15.5')
once('tests/windows_atomic_save_0144_test.py','Windows Offline Studio • v0.15.4',
 'Windows Offline Studio • v0.15.5')
once('tests/windows_long_probe_0145_test.py','MMMN Windows Offline Studio • v0.15.4',
 'MMMN Windows Offline Studio • v0.15.5')
for rel in ('version.txt','package.json','src-tauri/Cargo.toml',
   'src-tauri/tauri.conf.json','tests/release-safety-v013.test.mjs',
   'tests/windows-final-artifact-gate.test.mjs',
   '.github/workflows/windows-installer-upgrade-lab.yml',
   'tests/windows_installer_probe.py','tests/windows_installer_probe_test.py'):
 p=root/rel
 s=p.read_text(encoding='utf-8')
 if '0.15.4' not in s and 'installer-lab-0154-' not in s:
  raise ValueError('0.15.4 metadata witness missing: '+rel)
 p.write_text(s.replace('0.15.4','0.15.5').replace(
    'installer-lab-0154-','installer-lab-0155-'),encoding='utf-8')
p=root/'tests/windows-final-artifact-gate.test.mjs'
s=p.read_text(encoding='utf-8')
if r'0\.15\.4' not in s:raise ValueError('Strict escaped version witness missing')
p.write_text(s.replace(r'0\.15\.4',r'0\.15\.5'),encoding='utf-8')
ui=(root/'web/app.js').read_text(encoding='utf-8')
for key in ("case 'match-local-major-images':",
            'proposeLocalMajorArtwork(c,project.assets',
            'applyConfirmedLocalMajorArtwork(c,project.assets',
            'MMMN Windows Offline Studio • v0.15.5'):
 if key not in ui:raise ValueError('No real installed UI local picture button: '+key)
print('WINDOWS 0.15.5 SOURCE PATCH PASS: photo label proposals are explicit, local and human-review-only',flush=True)
