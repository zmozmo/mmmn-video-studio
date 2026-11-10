"""Windows 0.15.2: offline read-only scene/SRT evidence export.
Applies after 0.15.1. No automated scene time edits, no private uploads.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def replace(rel,old,new):
    p=root/rel
    s=p.read_text(encoding='utf-8')
    if s.count(old)!=1:
        raise ValueError(f'{rel}: patch anchor count {s.count(old)}: {old[:70]}')
    p.write_text(s.replace(old,new),encoding='utf-8')
    print('PATCH 0.15.2:',rel,flush=True)
module=root/'web/major-scene-timing-evidence.mjs'
tests=root/'tests/major-scene-timing-evidence.test.mjs'
if not module.is_file() or 'buildMajorSceneTimingEvidence' not in module.read_text(encoding='utf-8'):
    raise ValueError('Missing audited local SRT scene evidence module')
if not tests.is_file() or 'ambiguous' not in tests.read_text(encoding='utf-8'):
    raise ValueError('Missing ambiguous Burmese text regression tests')

replace('web/app.js',
 "import {auditNarrationTiming} from './narration-timing-audit.mjs';",
 "import {auditNarrationTiming} from './narration-timing-audit.mjs';\n"+
 "import {buildMajorSceneTimingEvidence} from './major-scene-timing-evidence.mjs';")
replace('web/app.js',
 '<button class="btn primary" data-action="export-major-picture-brief">',
 '<button class="btn" data-action="export-major-timing-evidence">'
 '🧭 အရေးကြီး Scene / SRT အချိန်တိုက်စစ်ချက်</button>\n'
 '<button class="btn primary" data-action="export-major-picture-brief">')
replace('web/app.js',"case 'export-major-picture-brief':{",
 """case 'export-major-timing-evidence':{
    try{
      const report=buildMajorSceneTimingEvidence(c);
      const s=report.summary;
      const msg='အရေးကြီး Scene / SRT အချိန်တိုက်စစ်ချက်\\n'+
        'အရေးကြီး Scene: '+s.visibleMajorScenes+'\\n'+
        'စာသားတစ်နေရာတည်းကိုက်: '+s.uniqueTextAnchors+'\\n'+
        'မကိုက်/ထပ်နေ: '+s.unresolvedScenes+'\\n'+
        'စာမူနှင့် SRT စစ်ချက်: '+s.manuscriptAgreement+'\\n'+
        'အသံအချိန်ပြည့် စစ်ချက်: '+s.audioCoverage+'\\n\\n'+
        'စာသားတူတာနဲ့ အသံစကားလုံးအချိန်တိကျကြောင်း မဆိုလိုပါ။ '+
        'ဒီစာရင်းကို နားထောင်ပြီး ကိုယ်တိုင်ပြန်စစ်ရမယ်။ '+
        'မူရင်းအသံ၊ SRT၊ ပုံ၊ Manual Lock၊ Scene Timing ကို မပြင်ပါ။'+
        '\\nမထုတ်ဝေရသေးတဲ့ ဝတ္ထုစာသား ပါနိုင်လို့ PRIVATE အဖြစ်သာ သိမ်းပါ။'+
        '\\n\\nLocal Review ဖိုင်ထုတ်မလား?';
      if(!confirm(msg))return;
      download(new Blob([report.markdown],{type:'text/markdown;charset=utf-8'}),
        'MMMN-ch'+String(c.number).padStart(2,'0')+'-SCENE-SRT-REVIEW-PRIVATE.md');
      toast('Scene / SRT Local Review ဖိုင် ထုတ်ပြီးပါပြီ။');
    }catch(error){
      toast('Scene / SRT Review မထုတ်နိုင်ပါ: '+error.message,true);
    }
    return;
  }
  case 'export-major-picture-brief':{""")
replace('web/app.js','MMMN Windows Offline Studio • v0.15.1',
  'MMMN Windows Offline Studio • v0.15.2')
replace('tests/windows_atomic_save_0144_test.py','Windows Offline Studio • v0.15.1',
  'Windows Offline Studio • v0.15.2')
replace('tests/windows_long_probe_0145_test.py','MMMN Windows Offline Studio • v0.15.1',
  'MMMN Windows Offline Studio • v0.15.2')
for rel in ('version.txt','package.json','src-tauri/Cargo.toml',
            'src-tauri/tauri.conf.json','tests/release-safety-v013.test.mjs',
            'tests/windows-final-artifact-gate.test.mjs',
            '.github/workflows/windows-installer-upgrade-lab.yml',
            'tests/windows_installer_probe.py','tests/windows_installer_probe_test.py'):
    p=root/rel
    s=p.read_text(encoding='utf-8')
    if '0.15.1' not in s and 'installer-lab-0151-' not in s:
        raise ValueError('0.15.1 version witness missing: '+rel)
    p.write_text(s.replace('0.15.1','0.15.2').replace(
        'installer-lab-0151-','installer-lab-0152-'),encoding='utf-8')
gate=root/'tests/windows-final-artifact-gate.test.mjs'
s=gate.read_text(encoding='utf-8')
if r'0\.15\.1' not in s:raise ValueError('Escaped version witness missing')
gate.write_text(s.replace(r'0\.15\.1',r'0\.15\.2'),encoding='utf-8')
ui=(root/'web/app.js').read_text(encoding='utf-8')
for witness in ("case 'export-major-timing-evidence':",
                'buildMajorSceneTimingEvidence(c)',
                'MMMN Windows Offline Studio • v0.15.2'):
    if witness not in ui:raise ValueError('Missing UI integration: '+witness)
print('Windows 0.15.2 source patch PASS; read-only SRT/major-image review',flush=True)
