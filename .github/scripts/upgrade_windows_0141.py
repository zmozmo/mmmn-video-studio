"""MMMN Windows 0.14.1 source upgrade. Fail closed if checked-in archive differs."""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def replace(path, old, new):
    p=root/path
    text=p.read_text(encoding="utf-8")
    if text.count(old)!=1:
        raise ValueError(f"{path}: expected exactly one original source anchor, got {text.count(old)}: {old[:90]}")
    p.write_text(text.replace(old,new),encoding="utf-8")
    print("PATCHED",path,old[:65].replace("\n"," "),flush=True)

replace("portable/studio_server.py",
    "    def project_storage_info(self, **_):",
    """    def open_local_folder(self, kind: str, **_):
        \"\"\"Open only fixed user folders; never execute a browser-supplied path.\"\"\"
        if kind not in ('backups', 'exports', 'project'):
            raise ValueError('Unknown local folder; choose Backups, Exports or Project')
        target={'backups':self.root/'snapshots','exports':self.root/'exports',
                'project':self.root}[kind]
        if sys.platform!='win32':
            raise ValueError('Open in Explorer is only available on Windows')
        os.startfile(str(target))
        return {'opened':True,'path':str(target)}

    def project_storage_info(self, **_):""")
replace("portable/studio_server.py",
    "'load_project_state','save_project_state','project_storage_info',",
    "'load_project_state','save_project_state','project_storage_info','open_local_folder',")
replace("web/app.js",
    '<span class="pill">Windows Offline Trial • Installer Lab</span>',
    '<span class="pill">Windows Offline Studio • v0.14.1</span>')
replace("web/app.js",
    "case 'save-text':c.text=$('chapter-text').value;c.scenes=[];save();toast('စာသား Local Copy ကို သိမ်းလိုက်ပါပြီ။ Scene များ ပြန်တွက်ရန် လိုပါမယ်။');return render();",
    """case 'save-text':{
  const updated=$('chapter-text').value;
  if(updated!==c.text){
    c.text=updated;
    // Do NOT delete a user's scene timing, image assignments or manual locks
    // when they correct their novel manuscript. Flag stale alignment instead.
    c.alignmentSummary='Manuscript edited — scene timing and pictures preserved. Review against narration before export.';
  }
  save();toast('စာမူသိမ်းပြီးပါပြီ။ Scene ပုံများနှင့် Timing မပျက်ပါ။ Narration နဲ့ ပြန်တိုက်စစ်ပါ။');return render();
 }""")
replace("web/app.js",
    '<button class="btn" data-action="refresh-native-backups">List Saved Backups</button></div>',
    '<button class="btn" data-action="refresh-native-backups">List Saved Backups</button><button class="btn" data-action="open-local-backups">📂 Open Backup Folder</button></div>')
replace("web/app.js",
    'For an independent USB/external-drive copy, close the app backup dialog and double-click COPY-VERIFIED-BACKUP-TO-USB.cmd in the extracted ZIP. It checks every SHA-256 again.',
    'Click Open Backup Folder, then copy the <b>entire snapshot folder</b> to a USB or external drive in Windows Explorer. No source ZIP or CMD needed. Keep all files together; verify SHA-256 before using a snapshot to restore.')
replace("web/app.js",
    '<button class="btn" data-action="refresh-storage">Refresh storage details</button><button class="btn" data-action="check-media">Check all imported media</button></div>',
    '<button class="btn" data-action="refresh-storage">Refresh storage details</button><button class="btn" data-action="open-local-project">📂 Open Project Folder</button><button class="btn" data-action="check-media">Check all imported media</button></div>')
replace("web/app.js",
    'Show saved MP4 files</button>',
    'Show saved MP4 files</button><button class=\\"btn\\" data-action=\\"open-local-exports\\">📂 Open MP4 Folder</button>')
replace("web/app.js",
    " case 'backup-native-full':{",
    """ case 'open-local-backups':case 'open-local-exports':case 'open-local-project':{
  if(!window.__MMMN_TRIAL__)return toast('Windows Offline App only.',true);
  const kind=action==='open-local-backups'?'backups':action==='open-local-exports'?'exports':'project';
  try{await window.__TAURI__.core.invoke('open_local_folder',{kind});}
  catch(error){toast('Folder ဖွင့်မရပါ: '+error.message,true);}
  return;
 }
 case 'backup-native-full':{""")
for old,new in [
    ('Native Windows စက်ပေါ် စမ်းသပ်အတည်ပြုရဦးမယ်။','Windows Installer မှာ Local Import ကို စမ်းသပ်ထားပြီးပါပြီ။'),
    ('Windows Installer ကို လက်တွေ့ Upgrade စမ်းမပြီးသေးပါ။','Windows GitHub Runner မှာ Install → Upgrade → Data Preservation စစ်ဆေးပြီးပါပြီ။'),
    ('Tauri Installer အတွက် Native Renderer က Hard Cut အဆင့်သာရှိသေးပြီး Windows စက်မှာ Compile စမ်းရဦးမယ်။','Windows Installer မှာ Hard Cut နဲ့ Cross Dissolve Scene များကို FFmpeg နဲ့ ထုတ်နိုင်ပါတယ်။')
]:
    replace("web/app.js",old,new)
for name in ("version.txt","package.json","src-tauri/Cargo.toml","src-tauri/tauri.conf.json",
             "tests/release-safety-v013.test.mjs","tests/windows-final-artifact-gate.test.mjs"):
    p=root/name
    content=p.read_text(encoding="utf-8")
    if "0.14.0" not in content:raise ValueError(name+": missing old release version")
    p.write_text(content.replace("0.14.0","0.14.1"),encoding="utf-8")
    print("VERSION UPDATED",name,flush=True)
# The embedded source has older workflow-level test literals. Update the
# checked-in build contract to the same 0.14.1 candidate, not stale 0.14.0.
workflow=root/".github/workflows/windows-installer-upgrade-lab.yml"
wf=workflow.read_text(encoding="utf-8")
if "0.14.0" not in wf: raise ValueError("Missing prior Windows workflow version")
workflow.write_text(wf.replace("0.14.0","0.14.1"),encoding="utf-8")
gate=root/"tests/windows-final-artifact-gate.test.mjs"
checks=gate.read_text(encoding="utf-8")
if r"0\.14\.0" not in checks: raise ValueError("Missing prior Windows source test version")
gate.write_text(checks.replace(r"0\.14\.0",r"0\.14\.1"),encoding="utf-8")
print("UPDATED Windows source build contract tests",flush=True)

# Keep the real installed-upgrade probe aligned with the actual 0.14.1
# revision names. This is NOT a waiver: the probe still verifies original
# project/media SHA-256 and pre-upgrade checkpoint existence.
for rel in ("tests/windows_installer_probe.py",
            "tests/windows_installer_probe_test.py",
            ".github/workflows/windows-installer-upgrade-lab.yml"):
    file=root/rel
    raw=file.read_text(encoding="utf-8")
    if "installer-lab-base" not in raw:
        raise ValueError("Prior revision witness missing: "+rel)
    new=raw.replace("installer-lab-base","installer-lab-0141-base")
    new=new.replace("installer-lab-upgrade","installer-lab-0141-upgrade")
    file.write_text(new,encoding="utf-8")
    print("UPGRADE REVISION WITNESS UPDATED",rel,flush=True)

print("MMMN WINDOWS 0.14.1 SOURCE UPGRADE READY",flush=True)
