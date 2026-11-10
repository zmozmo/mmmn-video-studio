"""0.15.0: strict offline Burmese SRT chronology, evidence, explicit draft consent.
Applies only after the 0.14.9 Windows patch; never edits original media.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def replace(rel,old,new):
    path=root/rel
    data=path.read_text(encoding='utf-8')
    if data.count(old)!=1:raise ValueError(f'{rel}: expected unique anchor, got {data.count(old)}')
    path.write_text(data.replace(old,new),encoding='utf-8')
    print('PATCH 0.15.0:',rel,flush=True)

agreement=root/'web/burmese-transcript-agreement.mjs'
test=root/'tests/burmese-transcript-chronology.test.mjs'
if not agreement.is_file() or 'manuscriptOrderCoverage' not in agreement.read_text(encoding='utf-8'):
    raise ValueError('Chronology-aware Burmese agreement guard missing')
if not test.is_file() or 'shuffled backwards' not in test.read_text(encoding='utf-8'):
    raise ValueError('Chronology regression suite missing')
replace('web/app.js',
"""            const originalEvidence=[
              String(c.text||''),...(c.scenes||[]).map(s=>String(s.text||''))
            ].join(' ');""",
"""            // Prefer the original chapter manuscript; do not inflate evidence
            // by concatenating duplicated derived scene excerpts.
            const originalEvidence=String(c.text||'').trim() ||
              (c.scenes||[]).map(s=>String(s.text||'')).join(' ');""")
replace('web/app.js',
"""            }else{
              newLocalCues=cues;""",
"""            }else if(confirm(
              'မြန်မာ SRT ကို မူရင်းစာမူနဲ့ တိုက်စစ်ထားပေမယ့် '+
              'စာလုံးနဲ့ အချိန်အတိအကျ မှန်ကြောင်း အာမမခံပါ။ '+
              'ပုံပြောင်းချိန် Draft အတွက်သာ ယာယီသုံးမလား? '+
              'မသုံးလိုရင် Cancel နှိပ်ပါ။ မူရင်းအသံ၊ စာမူ၊ SRT မပြောင်းပါ။')){
              newLocalCues=cues;""")
replace('web/app.js','MMMN Windows Offline Studio • v0.14.9',
                       'MMMN Windows Offline Studio • v0.15.0')
replace('tests/windows_atomic_save_0144_test.py','Windows Offline Studio • v0.14.9',
                       'Windows Offline Studio • v0.15.0')
replace('tests/windows_long_probe_0145_test.py','MMMN Windows Offline Studio • v0.14.9',
                       'MMMN Windows Offline Studio • v0.15.0')
for rel in ('version.txt','package.json','src-tauri/Cargo.toml',
            'src-tauri/tauri.conf.json','tests/release-safety-v013.test.mjs',
            'tests/windows-final-artifact-gate.test.mjs',
            '.github/workflows/windows-installer-upgrade-lab.yml',
            'tests/windows_installer_probe.py','tests/windows_installer_probe_test.py'):
    path=root/rel
    data=path.read_text(encoding='utf-8')
    if '0.14.9' not in data and 'installer-lab-0149-' not in data:
        raise ValueError(f'Expected 0.14.9 marker: {rel}')
    path.write_text(data.replace('0.14.9','0.15.0').replace(
       'installer-lab-0149-','installer-lab-0150-'),encoding='utf-8')
path=root/'tests/windows-final-artifact-gate.test.mjs'
data=path.read_text(encoding='utf-8')
if r'0\.14\.9' not in data:raise ValueError('Old regex gate missing')
path.write_text(data.replace(r'0\.14\.9',r'0\.15\.0'),encoding='utf-8')
result=(root/'web/app.js').read_text(encoding='utf-8')
for marker in ('manuscriptOrderCoverage','မြန်မာ SRT ကို မူရင်းစာမူနဲ့',
               'MMMN Windows Offline Studio • v0.15.0'):
    if marker=='manuscriptOrderCoverage':
        if marker not in agreement.read_text(encoding='utf-8'):raise ValueError(marker)
    elif marker not in result:raise ValueError(marker)
print('0.15.0 PATCH PASS: stricter cue chronology and draft-use consent',flush=True)
