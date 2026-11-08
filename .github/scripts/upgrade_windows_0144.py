"""MMMN Windows 0.14.4: atomic save, symlink-aware import finalization and clear UI.

Apply strictly after audited Windows 0.14.1 -> 0.14.2 -> 0.14.3.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()

def replace(rel,old,new):
    path=root/rel
    original=path.read_text(encoding='utf-8')
    count=original.count(old)
    if count!=1:
        raise ValueError(f'{rel}: source anchor expected exactly once, found {count}: {old[:95]!r}')
    path.write_text(original.replace(old,new),encoding='utf-8')
    print('WINDOWS 0.14.4 SAFE PATCH:',rel,flush=True)

# The old predictable project-state.pending.json was opened with 'w', which
# followed a pre-existing symlink and might change an unrelated local file.
# Create an unpredictable EXCLUSIVE staging file, only once validation and
# recovery checks are complete; clean up even if os.replace fails.
replace('portable/studio_server.py',
    """        path = self.root / 'project-state.json'
        stage = self.root / 'project-state.pending.json'
        # Windows CRT _commit()/os.fsync() needs a writable descriptor.
        # Write, flush and sync the staging file before the atomic replace.
        with stage.open('w', encoding='utf-8') as f:
            f.write(json)
            f.flush()
            os.fsync(f.fileno())
        if path.is_file():""",
    """        path = self.root / 'project-state.json'
        if path.is_symlink() or any((self.root / name).is_symlink()
                for name in ('project-state.previous.json','project-state.older.json')):
            raise ValueError('Unsafe project or recovery symlink; no files overwritten')
        # Check original and recovery before creating any temporary new data.
        if path.is_file():""")
replace('portable/studio_server.py',
    """        os.replace(stage, path)
        return None""",
    """        stage = self.root / f'project-state.pending-{secrets.token_hex(12)}.json'
        try:
            # Exclusive create is required: never follow an existing link or
            # truncate an attacker-selected previous pending file.
            with stage.open('x', encoding='utf-8') as f:
                f.write(json)
                f.flush()
                os.fsync(f.fileno())
            os.replace(stage, path)
        finally:
            stage.unlink(missing_ok=True)
        return None""")

# Do not read a forged import metadata symlink or convert a partial symlink
# into an imported media asset. A Windows rename refuses target collisions,
# unlike os.replace, which can overwrite an existing file during a race.
replace('portable/studio_server.py',
    """        meta = json.loads((self.root/'imports'/f'{id}.json').read_text())
        if offset+len(data)>meta['total']:""",
    """        meta_path=self.root/'imports'/f'{id}.json'
        if meta_path.is_symlink():
            raise ValueError('Unsafe media import metadata symlink')
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        if offset+len(data)>meta['total']:""")
replace('portable/studio_server.py',
    """        metadata=self.root/'imports'/f'{id}.json'
        meta=json.loads(metadata.read_text())
        target=self.media(id,meta['ext'])
        part=self.root/'imports'/f'{id}.partial'
        size, sha=self.checksum(part)""",
    """        metadata=self.root/'imports'/f'{id}.json'
        if metadata.is_symlink():
            raise ValueError('Unsafe media import metadata symlink')
        meta=json.loads(metadata.read_text(encoding='utf-8'))
        target=self.media(id,meta['ext'])
        part=self.root/'imports'/f'{id}.partial'
        if part.is_symlink():
            raise ValueError('Unsafe media import partial symlink')
        size, sha=self.checksum(part)""")
replace('portable/studio_server.py',
    """        os.replace(part,target)
        metadata.unlink()""",
    """        # On Windows os.rename does not replace existing destinations.
        # Keep the original if a new file appears after the collision check.
        os.rename(part,target)
        metadata.unlink()""")

# Remove historical, misleading statements from the actual installed UI.
replace('web/app.js',
    '<span class="pill">Windows Offline Studio • v0.14.1</span>',
    '<span class="pill">MMMN Windows Offline Studio • v0.14.4</span>')
replace('web/app.js',
    'Local Windows Trial',
    'Windows Offline Installer')
replace('web/app.js',
    'Windows GitHub Runner မှာ Install → Upgrade → Data Preservation စစ်ဆေးပြီးပါပြီ။',
    'Windows 0.14.4 ကို GitHub Windows Runner တွင် Build → Install → Upgrade → MP4 Render → Uninstall အစအဆုံး စမ်းသပ်ပြီးမှ Release တင်ပါမည်။')
replace('web/app.js',
    'Click Open Backup Folder, then copy the <b>entire snapshot folder</b> to a USB or external drive in Windows Explorer. No source ZIP or CMD needed. Keep all files together; verify SHA-256 before using a snapshot to restore.',
    'အရင် Create + Verify Full Backup နှိပ်ပါ။ ထို့နောက် Open Backup Folder နှိပ်ပြီး snapshot folder တစ်ခုလုံးကို USB / အခြား Drive ထဲ Windows Explorer ဖြင့် ကူးပါ။ ZIP ဖြည်ရန်၊ CMD သုံးရန် မလိုပါ။ USB ပေါ်မှ Restore မလုပ်မီ မူရင်း Project Folder ထဲ snapshot folder ပြန်ထည့်ပြီး SHA-256 Verify လုပ်ပါ။')

# Preserve every pre-existing pinned release safety witness, updated together.
for rel in ("version.txt","package.json","src-tauri/Cargo.toml",
            "src-tauri/tauri.conf.json","tests/release-safety-v013.test.mjs",
            "tests/windows-final-artifact-gate.test.mjs",
            ".github/workflows/windows-installer-upgrade-lab.yml",
            "tests/windows_installer_probe.py","tests/windows_installer_probe_test.py"):
    p=root/rel
    content=p.read_text(encoding='utf-8')
    if "0.14.3" not in content and "installer-lab-0143-" not in content:
        raise ValueError('Cannot locate 0.14.3 version witness: '+rel)
    p.write_text(content.replace('0.14.3','0.14.4').replace(
        'installer-lab-0143-','installer-lab-0144-'),encoding='utf-8')
gate=root/'tests'/'windows-final-artifact-gate.test.mjs'
content=gate.read_text(encoding='utf-8')
if r'0\.14\.3' not in content:
    raise ValueError('Strict version regex for 0.14.3 not found')
gate.write_text(content.replace(r'0\.14\.3',r'0\.14\.4'),encoding='utf-8')

unit=r'''"""Windows 0.14.4: atomic manuscript save and import symlink regression tests."""
from pathlib import Path
from unittest.mock import patch
import hashlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'portable'))
from studio_server import Studio

class AtomicStorageTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='mmmn-safe0144-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.app=Studio(self.root,'synthetic-test-only')
        self.first='{"title":"synthetic original","chapters":[],"assets":[]}'
        self.second='{"title":"synthetic second","chapters":[],"assets":[]}'
    def test_save_works_and_recovery_is_preserved(self):
        self.app.save_project_state(self.first)
        self.app.save_project_state(self.second)
        self.assertEqual(self.app.load_project_state(),self.second)
        self.assertEqual((self.root/'project-state.previous.json').read_text(),self.first)
    def test_predictable_old_pending_file_is_never_overwritten(self):
        sentinel=self.root/'project-state.pending.json'
        sentinel.write_bytes(b'PREVIOUS-UNRELATED-BYTES')
        self.app.save_project_state(self.first)
        self.assertEqual(sentinel.read_bytes(),b'PREVIOUS-UNRELATED-BYTES')
        self.assertEqual(list(self.root.glob('project-state.pending-*.json')),[])
    def test_failed_atomic_replace_cleans_staging(self):
        self.app.save_project_state(self.first)
        with patch('studio_server.os.replace',side_effect=OSError('synthetic disk error')):
            with self.assertRaisesRegex(OSError,'synthetic disk error'):
                self.app.save_project_state(self.second)
        self.assertEqual(self.app.load_project_state(),self.first)
        self.assertEqual(list(self.root.glob('project-state.pending-*.json')),[])
    def test_recovery_symlink_refused_without_overwriting_target(self):
        self.app.save_project_state(self.first)
        target=self.root/'important-synthetic-data.txt'
        target.write_bytes(b'UNRELATED')
        backup=self.root/'project-state.previous.json'
        try:
            backup.symlink_to(target)
        except (OSError,NotImplementedError):
            self.skipTest('Symlink privilege unavailable')
        with self.assertRaisesRegex(ValueError,'symlink'):
            self.app.save_project_state(self.second)
        self.assertEqual(target.read_bytes(),b'UNRELATED')
        self.assertEqual(self.app.load_project_state(),self.first)
    def test_import_media_finalization_preserves_exact_bytes(self):
        raw=b'RIFF'+bytes(range(32))
        digest=hashlib.sha256(raw).hexdigest()
        self.app.begin_media_import('audio0144001','wav',len(raw))
        self.app.import_media_chunk('audio0144001',0,digest,raw)
        result=self.app.finalize_media_import('audio0144001')
        self.assertEqual(result['sha256'],digest)
        self.assertEqual(self.app.media('audio0144001','wav').read_bytes(),raw)
    def test_finalize_refuses_symlink_partial(self):
        outside=self.root/'important-synthetic-data.txt'
        outside.write_bytes(b'UNRELATED')
        self.app.begin_media_import('audio0144001','wav',len(b'UNRELATED'))
        partial=self.root/'imports'/'audio0144001.partial'
        partial.unlink()
        try:
            partial.symlink_to(outside)
        except (OSError,NotImplementedError):
            self.skipTest('Symlink privilege unavailable')
        with self.assertRaisesRegex(ValueError,'symlink'):
            self.app.finalize_media_import('audio0144001')
        self.assertEqual(outside.read_bytes(),b'UNRELATED')
        self.assertFalse(self.app.media('audio0144001','wav').exists())
    def test_finalize_refuses_metadata_symlink(self):
        self.app.begin_media_import('audio0144001','wav',5)
        meta=self.root/'imports'/'audio0144001.json'
        outside=self.root/'other-synthetic-metadata.json'
        outside.write_text('{"ext":"wav","total":5}')
        meta.unlink()
        try:
            meta.symlink_to(outside)
        except (OSError,NotImplementedError):
            self.skipTest('Symlink privilege unavailable')
        with self.assertRaisesRegex(ValueError,'symlink'):
            self.app.finalize_media_import('audio0144001')
        self.assertTrue(outside.exists())
    def test_chunk_refuses_metadata_symlink(self):
        self.app.begin_media_import('audio0144001','wav',5)
        meta=self.root/'imports'/'audio0144001.json'
        outside=self.root/'other-synthetic-metadata.json'
        outside.write_text('{"ext":"wav","total":5}')
        meta.unlink()
        try:
            meta.symlink_to(outside)
        except (OSError,NotImplementedError):
            self.skipTest('Symlink privilege unavailable')
        raw=b'abcde'
        with self.assertRaisesRegex(ValueError,'symlink'):
            self.app.import_media_chunk('audio0144001',0,hashlib.sha256(raw).hexdigest(),raw)
        self.assertEqual((self.root/'imports'/'audio0144001.partial').stat().st_size,0)
    def test_version_ui_avoids_legacy_install_instructions(self):
        html=(Path(__file__).resolve().parents[1]/'web'/'app.js').read_text(encoding='utf-8')
        self.assertIn('Windows Offline Studio • v0.14.4',html)
        self.assertNotIn('COPY-VERIFIED-BACKUP-TO-USB.cmd',html)
        self.assertNotIn('Windows Installer ကို လက်တွေ့ Upgrade စမ်းမပြီးသေးပါ။',html)

if __name__=='__main__':
    unittest.main()
'''
target=root/'tests'/'windows_atomic_save_0144_test.py'
if target.exists():raise ValueError('0.14.4 test already present; refuse duplicate patch')
target.write_text(unit,encoding='utf-8')
print('MMMN WINDOWS 0.14.4 PATCH COMPLETE; nine new regression tests',flush=True)
