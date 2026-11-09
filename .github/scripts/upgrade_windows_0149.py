"""Windows 0.14.9: reject offline Burmese ASR hallucinations before planning photos.

Applies only AFTER all 0.14.1–0.14.8 patches. Never overwrite existing
human-corrected SRT or decide scenes from unverified model output. Local
manuscript/ASR overlap is a conservative anti-hallucination gate, NOT
language understanding or certified ASR accuracy.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def replace(rel,old,new):
    p=root/rel
    s=p.read_text(encoding='utf-8')
    if s.count(old)!=1:
        raise ValueError(f'{rel}: expected unique patch anchor; saw {s.count(old)}: {old[:110]}')
    p.write_text(s.replace(old,new),encoding='utf-8')
    print('PATCH 0.14.9:',rel,flush=True)

module=root/'web/burmese-transcript-agreement.mjs'
tests=root/'tests/burmese-transcript-agreement.test.mjs'
if not module.is_file() or 'assessBurmeseTranscript' not in module.read_text(encoding='utf-8'):
    raise ValueError('No verified offline Myanmar transcript overlap module')
if not tests.is_file() or "wrong Burmese narration" not in tests.read_text(encoding='utf-8'):
    raise ValueError('Missing real anti-hallucination regression test suite')

replace('web/app.js',
 "import {buildMajorArtworkBrief} from './major-artwork-brief.mjs';",
 "import {buildMajorArtworkBrief} from './major-artwork-brief.mjs';\n"
 "import {assessBurmeseTranscript} from './burmese-transcript-agreement.mjs';")

replace('web/app.js',
 "            const checked=subtitleDiagnostics(cues,c.recordedSeconds);\n"
 "            if(checked.warnings.length){",
 """            const checked=subtitleDiagnostics(cues,c.recordedSeconds);
            // Transcription can be timestamp-perfect but 100% wrong Burmese.
            // Comparing only to the author's own local manuscript makes it
            // fail closed, never leaking content to a network service.
            const originalEvidence=[
              String(c.text||''),...(c.scenes||[]).map(s=>String(s.text||''))
            ].join(' ');
            const speechAgreement=assessBurmeseTranscript(originalEvidence,cues);
            if(speechAgreement.status!=='supported'){
              toast('မြန်မာအသံမှထွက်လာတဲ့ SRT က မူရင်းဝတ္ထုစာသားနဲ့ '
                +'မကိုက်ညီသေးပါ ('+speechAgreement.status+'). '
                +'ဒီ SRT ကို ပုံပြောင်းချိန်အတွက် မသုံးပါ။ '
                +'မှန်ကန်တဲ့ SRT ကို ကိုယ်တိုင်ပြင်ပြီး Import လုပ်နိုင်ပါတယ်။',true);
            }else if(checked.warnings.length){""")

replace('web/app.js',
 "MMMN Windows Offline Studio • v0.14.8",
 "MMMN Windows Offline Studio • v0.14.9")
replace('tests/windows_atomic_save_0144_test.py',
 "Windows Offline Studio • v0.14.8","Windows Offline Studio • v0.14.9")
replace('tests/windows_long_probe_0145_test.py',
 "MMMN Windows Offline Studio • v0.14.8",
 "MMMN Windows Offline Studio • v0.14.9")

for rel in ("version.txt","package.json","src-tauri/Cargo.toml",
            "src-tauri/tauri.conf.json","tests/release-safety-v013.test.mjs",
            "tests/windows-final-artifact-gate.test.mjs",
            ".github/workflows/windows-installer-upgrade-lab.yml",
            "tests/windows_installer_probe.py","tests/windows_installer_probe_test.py"):
    p=root/rel
    s=p.read_text(encoding='utf-8')
    if "0.14.8" not in s and "installer-lab-0148-" not in s:
        raise ValueError(f'No old 0.14.8 version witness: {rel}')
    p.write_text(s.replace("0.14.8","0.14.9").replace(
                 "installer-lab-0148-","installer-lab-0149-"),encoding='utf-8')
p=root/"tests/windows-final-artifact-gate.test.mjs"
s=p.read_text(encoding='utf-8')
if r'0\.14\.8' not in s:raise ValueError('Missing strict prior version regex witness')
p.write_text(s.replace(r'0\.14\.8',r'0\.14\.9'),encoding='utf-8')

result=(root/'web/app.js').read_text(encoding='utf-8')
for x in ('assessBurmeseTranscript(originalEvidence,cues)',
          "speechAgreement.status!=='supported'",
          'မူရင်းဝတ္ထုစာသားနဲ့','MMMN Windows Offline Studio • v0.14.9'):
    if x not in result:raise ValueError('0.14.9 reject-bad-ASR witness absent: '+x)
print('WINDOWS 0.14.9 PATCH COMPLETE — erroneous Burmese ASR cannot automatically drive visuals or overwrite reviewed SRT',flush=True)
