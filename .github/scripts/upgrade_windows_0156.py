"""Windows 0.15.6: show the same imported photo through unassigned major shots.

After 0.15.5. No new image, video boundary, outside API, audio edit or
manual scene changes. Only author-confirmed, previously imported, nativeStored
pictures may be carried forward to avoid blank chapter backgrounds.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def once(rel,old,new):
 p=root/rel
 s=p.read_text(encoding='utf-8')
 if s.count(old)!=1:
  raise ValueError(f'{rel}: nonunique patch anchor ({s.count(old)}): {old[:70]}')
 p.write_text(s.replace(old,new),encoding='utf-8')
 print('WINDOWS 0.15.6 PATCH:',rel,flush=True)
module=root/'web/major-scene-picture-continuity.mjs'
tests=root/'tests/major-scene-picture-continuity.test.mjs'
if not module.is_file() or 'keepExistingMajorScenePicture' not in module.read_text(encoding='utf-8'):
 raise ValueError('No 0.15.6 photo continuity module')
if not tests.is_file() or '90-minute voice' not in tests.read_text(encoding='utf-8'):
 raise ValueError('Missing 90m image continuity tests')

once('web/app.js',
 "import {proposeLocalMajorArtwork,applyConfirmedLocalMajorArtwork} from './local-major-artwork-match.mjs';",
 "import {proposeLocalMajorArtwork,applyConfirmedLocalMajorArtwork} from './local-major-artwork-match.mjs';\n"+
 "import {analyzeMajorScenePictureContinuity,keepExistingMajorScenePicture} from './major-scene-picture-continuity.mjs';")
once('web/app.js',
 '<button class="btn" data-action="match-local-major-images">',
 '<button class="btn" data-action="hold-verified-major-photo">🎞️ ပုံမရှိတဲ့ Scene မှာ ယခင်ပုံ ဆက်ပြရန်</button>\n'
 '<button class="btn" data-action="match-local-major-images">')
once('web/app.js',
 "case 'match-local-major-images':{",
 """case 'hold-verified-major-photo':{
    try{
      const audit=analyzeMajorScenePictureContinuity(c,project.assets||[]);
      const s=audit.report;
      const details='နောက်ခံပုံ Continuity / Review စစ်ချက်\\\\n'+
        'အရေးကြီး Scene: '+s.visibleMajorScenes+'\\\\n'+
        'ယခင် Import လုပ်ထားတဲ့ ပုံဆက်ပြနိုင်: '+s.continuableUnassigned+'\\\\n'+
        'အစပုံမရှိ: '+s.openingMissing+'\\\\n'+
        'Manual Blank / Lock: '+s.manualUnassigned+'\\\\n'+
        'စစ်ဆေးရန် ပုံမရှိ/မသိ: '+s.unresolvedMissingOrNonlocal+'\\\\n'+
        'Encoding အပိုင်းတွင် ပုံမတူ: '+s.unsafeTechnicalMismatches+'\\\\n'+
        'အသံအချိန်: '+s.durationSeconds.toFixed(1)+'s\\\\n\\\\n'+
        'ပုံအသစ် ဖန်တီး/Download မလုပ်ပါ။ Scene Timing၊ Audio၊ SRT၊ '+ 
        'Manual Photo Lock၊ ရှိပြီးသား ပုံရွေးချယ်မှုတို့ကို မပြင်ပါ။';
      if(s.unsafeTechnicalMismatches){
        alert(details+'\\\\n\\\\nEncoding အပိုင်းမှာ ပုံပြောင်းမှုရှိနေလို့ အရင် ကိုယ်တိုင် ပြင်ရန်လိုပါသည်။');
        return;
      }
      if(!s.continuableUnassigned){
        alert(details+'\\\\n\\\\nအန္တရာယ်ကင်းစွာ ယခင်ပုံ ဆက်ပြနိုင်မည့် Scene မရှိပါ။');
        return;
      }
      if(!confirm(details+'\\\\n\\\\nရှိပြီးသားပုံကို ဆက်ပြထားပြီး Scene တစ်ခုချင်းစီ ကိုယ်တိုင်ပြန်စစ်မလား?'))return;
      const fixed=keepExistingMajorScenePicture(c,project.assets||[],true);
      if(!fixed.continuationsApplied)return;
      checkpoint(c,'Review-only verified imported picture continuity');
      c.scenes=fixed.scenes;
      c.pictureContinuitySummary='Local prior picture held in '+
        fixed.continuationsApplied+' unassigned scene(s); no new boundary or approval.';
      save();
      await render();
      toast('ပုံမရှိသေးသော Scene '+fixed.continuationsApplied+
        ' ခုမှာ Import လုပ်ပြီးသား ယခင်ပုံကို Review အဖြစ် ဆက်ပြထားပါပြီ။');
    }catch(error){
      toast('နောက်ခံပုံ Continuity စစ်ဆေးမှု မအောင်မြင်ပါ: '+error.message,true);
    }
    return;
  }
  case 'match-local-major-images':{""")
once('web/app.js','MMMN Windows Offline Studio • v0.15.5',
 'MMMN Windows Offline Studio • v0.15.6')
once('tests/windows_atomic_save_0144_test.py','Windows Offline Studio • v0.15.5',
 'Windows Offline Studio • v0.15.6')
once('tests/windows_long_probe_0145_test.py','MMMN Windows Offline Studio • v0.15.5',
 'MMMN Windows Offline Studio • v0.15.6')
for rel in ('version.txt','package.json','src-tauri/Cargo.toml',
   'src-tauri/tauri.conf.json','tests/release-safety-v013.test.mjs',
   'tests/windows-final-artifact-gate.test.mjs',
   '.github/workflows/windows-installer-upgrade-lab.yml',
   'tests/windows_installer_probe.py','tests/windows_installer_probe_test.py'):
 p=root/rel
 s=p.read_text(encoding='utf-8')
 if '0.15.5' not in s and 'installer-lab-0155-' not in s:
  raise ValueError('Old 0.15.5 version marker missing: '+rel)
 p.write_text(s.replace('0.15.5','0.15.6').replace(
  'installer-lab-0155-','installer-lab-0156-'),encoding='utf-8')
gate=root/'tests/windows-final-artifact-gate.test.mjs'
s=gate.read_text(encoding='utf-8')
if r'0\.15\.5' not in s:raise ValueError('Missing previous escaped version')
gate.write_text(s.replace(r'0\.15\.5',r'0\.15\.6'),encoding='utf-8')
ui=(root/'web/app.js').read_text(encoding='utf-8')
for marker in ("case 'hold-verified-major-photo':",
               'analyzeMajorScenePictureContinuity(c,project.assets',
               'keepExistingMajorScenePicture(c,project.assets',
               'MMMN Windows Offline Studio • v0.15.6'):
 if marker not in ui:raise ValueError('Missing installed UI proof: '+marker)
print('WINDOWS 0.15.6 SOURCE PATCH PASS: existing picture only, review first',flush=True)
