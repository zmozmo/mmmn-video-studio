"""MMM Windows 0.15.1 - audit full narration/SRT timing before using automated cues.

Apply only after verified 0.15.0 patch chain. No cloud, media writes or
silent overwrite of corrected user SRT. The audit is NOT proof of exact
Myanmar speech recognition or word alignment.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def replace(rel,old,new):
    p=root/rel
    s=p.read_text(encoding='utf-8')
    if s.count(old)!=1:
        raise ValueError(f'{rel}: expected one patch anchor, found {s.count(old)}: {old[:90]}')
    p.write_text(s.replace(old,new),encoding='utf-8')
    print('PATCH 0.15.1:',rel,flush=True)

audit=root/'web/narration-timing-audit.mjs'
tests=root/'tests/narration-timing-audit.test.mjs'
if not audit.is_file() or 'export function auditNarrationTiming' not in audit.read_text(encoding='utf-8'):
    raise ValueError('Missing audited local narration-timing library')
if not tests.is_file() or '90 minute narration' not in tests.read_text(encoding='utf-8'):
    raise ValueError('Missing 90-minute narration-timing regression tests')

replace('web/app.js',
  "import {assessBurmeseTranscript} from './burmese-transcript-agreement.mjs';",
  "import {assessBurmeseTranscript} from './burmese-transcript-agreement.mjs';\n"+
  "import {auditNarrationTiming} from './narration-timing-audit.mjs';")
replace('web/app.js',
  '<button class="btn primary" data-action="audio-first-major-plan">',
  '<button class="btn" data-action="audit-current-srt">🕒 အသံ / SRT အချိန်ကွက်လပ် စစ်ရန်</button>\n'
  '<button class="btn primary" data-action="audio-first-major-plan">')
replace('web/app.js',
  "case 'audio-first-major-plan':\n  case 'major-only-scene-plan':{",
  """case 'audit-current-srt':{
    // Read-only timeline check for user-reviewed/imported SRT too.
    const report=auditNarrationTiming(c.recordedSeconds,c.subtitleCues||[]);
    const coverage=typeof report.observedCoverage==='number'?
      (report.observedCoverage*100).toFixed(1)+'%':'မရှိသေး';
    const gap=typeof report.longestGapSeconds==='number'?
      report.longestGapSeconds.toFixed(1)+'s':'မသိ';
    const tail=typeof report.trailingGapSeconds==='number'?
      report.trailingGapSeconds.toFixed(1)+'s':'မသိ';
    alert('SRT / အသံ အချိန်တိုက်စစ်ချက် ('+report.status+')\\n'+
      'SRT: '+(report.cueCount||0)+' ကြောင်း\\n'+
      'အသံဖုံးလွှမ်းမှု: '+coverage+'\\n'+
      'အကြီးဆုံးကွက်လပ်: '+gap+'\\n'+
      'နောက်ဆုံးကွက်လပ်: '+tail+'\\n'+
      'မှတ်ချက်: '+report.reason+'\\n\\n'+
      'ဒီစစ်ချက်က မြန်မာအသံကို တိတိကျကျမှတ်မိတယ်လို့ မဆိုလိုပါ။ '+
      'စာလုံး၊ အသံနဲ့ ပုံပြောင်းချိန်တွေကို လူကိုယ်တိုင် ပြန်စစ်ပါ။');
    return;
  }
  case 'audio-first-major-plan':
  case 'major-only-scene-plan':{""")
replace('web/app.js',
  '            const speechAgreement=assessBurmeseTranscript(originalEvidence,cues);',
  '            const speechAgreement=assessBurmeseTranscript(originalEvidence,cues);\n'
  '            const timelineAudit=auditNarrationTiming(c.recordedSeconds,cues);')
replace('web/app.js',
  """            }else if(checked.warnings.length){
              toast('SRT Timing မကိုက်သေးပါ။ မူလ SRT ကို မပြင်ဘဲ Pause Timing ကို ဆက်သုံးမယ်။',true);""",
  """            }else if(!timelineAudit.safeForDraft){
              toast('SRT စာသားတူပေမယ့် အသံအချိန်လွှမ်းခြုံမှု မလုံလောက်သေးပါ။ '+
                'အချိန်ကွက်လပ်များကြောင့် ဒီ SRT ကို ပုံပြောင်းချိန် Draft အတွက် '+
                'မသုံးဘဲ Pause Timing ကိုသာ သုံးမယ်။',true);
            }else if(checked.warnings.length){
              toast('SRT Timing မကိုက်သေးပါ။ မူလ SRT ကို မပြင်ဘဲ Pause Timing ကို ဆက်သုံးမယ်။',true);""")

replace('web/app.js','MMMN Windows Offline Studio • v0.15.0',
                       'MMMN Windows Offline Studio • v0.15.1')
replace('tests/windows_atomic_save_0144_test.py','Windows Offline Studio • v0.15.0',
                       'Windows Offline Studio • v0.15.1')
replace('tests/windows_long_probe_0145_test.py','MMMN Windows Offline Studio • v0.15.0',
                       'MMMN Windows Offline Studio • v0.15.1')
for rel in ('version.txt','package.json','src-tauri/Cargo.toml',
            'src-tauri/tauri.conf.json','tests/release-safety-v013.test.mjs',
            'tests/windows-final-artifact-gate.test.mjs',
            '.github/workflows/windows-installer-upgrade-lab.yml',
            'tests/windows_installer_probe.py','tests/windows_installer_probe_test.py'):
    p=root/rel
    s=p.read_text(encoding='utf-8')
    if '0.15.0' not in s and 'installer-lab-0150-' not in s:
        raise ValueError(f'Old 0.15.0 version marker missing: {rel}')
    p.write_text(s.replace('0.15.0','0.15.1').replace(
        'installer-lab-0150-','installer-lab-0151-'),encoding='utf-8')
p=root/'tests/windows-final-artifact-gate.test.mjs'
s=p.read_text(encoding='utf-8')
if r'0\.15\.0' not in s:raise ValueError('Old escaped version marker missing')
p.write_text(s.replace(r'0\.15\.0',r'0\.15\.1'),encoding='utf-8')
ui=(root/'web/app.js').read_text(encoding='utf-8')
for witness in ("case 'audit-current-srt':","auditNarrationTiming(c.recordedSeconds,cues)",
    "timelineAudit.safeForDraft","MMMN Windows Offline Studio • v0.15.1"):
    if witness not in ui:raise ValueError('Audio audit integration not present: '+witness)
print('WINDOWS 0.15.1 PATCH PASS: fail-closed SRT coverage + read-only audit UI',flush=True)
