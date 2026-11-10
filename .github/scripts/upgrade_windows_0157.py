"""Windows 0.15.7: important scenes only, PRIVATE read-only local art queue.
No automatic images, network service, approval or scene alterations.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def once(rel,old,new):
 p=root/rel
 s=p.read_text(encoding='utf-8')
 if s.count(old)!=1:raise ValueError(rel+': nonunique patch anchor '+str(s.count(old))+': '+old[:65])
 p.write_text(s.replace(old,new),encoding='utf-8')
 print('WINDOWS 0.15.7 PATCH:',rel,flush=True)
module=root/'web/important-scene-art-queue.mjs'
tests=root/'tests/important-scene-art-queue.test.mjs'
if not module.is_file() or 'proposePrivateMajorArtQueue' not in module.read_text(encoding='utf-8'):
 raise ValueError('Missing reviewed offline important scene art queue module')
if not tests.is_file() or 'runaway photo' not in tests.read_text(encoding='utf-8'):
 raise ValueError('Missing conservative scene-art queue regression suite')
once('web/app.js',
 "import {analyzeMajorScenePictureContinuity,keepExistingMajorScenePicture} from './major-scene-picture-continuity.mjs';",
 "import {analyzeMajorScenePictureContinuity,keepExistingMajorScenePicture} from './major-scene-picture-continuity.mjs';\n"+
 "import {proposePrivateMajorArtQueue} from './important-scene-art-queue.mjs';")
once('web/app.js','<button class="btn" data-action="hold-verified-major-photo">',
 '<button class="btn" data-action="review-important-art-queue">🎨 အရေးကြီး Scene ပုံလိုအပ်ချက် စစ်ရန်</button>\n'+
 '<button class="btn" data-action="hold-verified-major-photo">')
once('web/app.js',"case 'hold-verified-major-photo':{",
 """case 'review-important-art-queue':{
    try{
      // Read-only review, not local model execution or image generation.
      const proposal=proposePrivateMajorArtQueue(c,project.assets||[],{maxCandidates:12});
      const s=proposal.summary;
      const lines=['# MMMN — PRIVATE Important-scene image candidate review',
        '','Chapter: '+c.number,
        'Important images to review: '+s.eligibleLocalArtRequests,
        'Ordinary details keeping the current picture: '+s.ordinaryBeatHolds,
        'Already linked or manually locked: '+s.alreadyLinkedOrLocked,
        'Excess beats postponed: '+s.overflowImportantBeats,'',
        'This is an OFFLINE planning report, NOT an AI generated image.',
        'NEVER publish unpublished novel text in a public repository.',
        'Manual approval and separately installed local model required.',''];
      for(const r of proposal.rows){
        lines.push('## '+r.sceneId+' — '+r.status,'',
          'Original image time: '+(r.sceneStart??'unchanged'),
          'Image prompt (private suggestion ONLY): '+(r.proposedPrompt||'(keep current image)'),
          'Never auto-approve or silently change a locked picture.','');
      }
      const msg='အရေးကြီး Scene ပုံလိုအပ်ချက်\\n'+
        'ပုံအသစ်လိုနိုင်တဲ့ Scene: '+s.eligibleLocalArtRequests+'\\n'+
        'လက်ရှိပုံဆက်ပြရန်: '+s.ordinaryBeatHolds+'\\n'+
        'အတည်ပြု/Lock ပုံမပြောင်း: '+s.alreadyLinkedOrLocked+'\\n\\n'+
        'ဒီခလုတ်က ပုံအသစ်မဖန်တီးပါ။ အထူး Scene တွေအတွက် PRIVATE စစ်ဆေးရန်စာရင်းသာ ထုတ်ပါတယ်။'+
        '\\nစာမူနဲ့ ပုံများကို Cloud တင်ခြင်းမပြုပါ။'+
        '\\n\\nPrivate Markdown စာရင်းထုတ်မလား?';
      if(!confirm(msg))return;
      download(new Blob([lines.join('\\n')],{type:'text/markdown;charset=utf-8'}),
        'MMMN-ch'+String(c.number).padStart(2,'0')+'-MAJOR-ART-REVIEW-PRIVATE.md');
      toast('အရေးကြီး Scene ပုံလိုအပ်ချက် စာရင်းကို Local မှာ ထုတ်ထားပါပြီ။');
    }catch(error){
      toast('Scene ပုံလိုအပ်ချက် မစစ်နိုင်ပါ: '+error.message,true);
    }
    return;
  }
  case 'hold-verified-major-photo':{""")
once('web/app.js','MMMN Windows Offline Studio • v0.15.6',
                  'MMMN Windows Offline Studio • v0.15.7')
once('tests/windows_atomic_save_0144_test.py','Windows Offline Studio • v0.15.6',
      'Windows Offline Studio • v0.15.7')
once('tests/windows_long_probe_0145_test.py','MMMN Windows Offline Studio • v0.15.6',
      'MMMN Windows Offline Studio • v0.15.7')
for rel in ('version.txt','package.json','src-tauri/Cargo.toml',
   'src-tauri/tauri.conf.json','tests/release-safety-v013.test.mjs',
   'tests/windows-final-artifact-gate.test.mjs',
   '.github/workflows/windows-installer-upgrade-lab.yml',
   'tests/windows_installer_probe.py','tests/windows_installer_probe_test.py'):
 p=root/rel
 s=p.read_text(encoding='utf-8')
 if '0.15.6' not in s and 'installer-lab-0156-' not in s:
  raise ValueError('Missing previous version marker: '+rel)
 p.write_text(s.replace('0.15.6','0.15.7').replace(
  'installer-lab-0156-','installer-lab-0157-'),encoding='utf-8')
gate=root/'tests/windows-final-artifact-gate.test.mjs'
s=gate.read_text(encoding='utf-8')
if r'0\.15\.6' not in s:raise ValueError('Missing escaped version witness')
gate.write_text(s.replace(r'0\.15\.6',r'0\.15\.7'),encoding='utf-8')
ui=(root/'web/app.js').read_text(encoding='utf-8')
for marker in ("case 'review-important-art-queue':",
               'proposePrivateMajorArtQueue(c,project.assets',
               'MMMN Windows Offline Studio • v0.15.7'):
 if marker not in ui:raise ValueError('Missing installed UI witness: '+marker)
print('WINDOWS 0.15.7 SOURCE PATCH PASS — private major art review, no network/media edits',flush=True)
