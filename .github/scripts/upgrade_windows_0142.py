"""Windows 0.14.2: safe import capacity guard and disk-space reporting."""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def replace(rel,old,new):
    p=root/rel
    data=p.read_text(encoding='utf-8')
    if data.count(old)!=1:
        raise ValueError(f"Expected one old source anchor in {rel}, found {data.count(old)}: {old[:60]}")
    p.write_text(data.replace(old,new),encoding='utf-8')
    print("PATCH 0.14.2",rel,flush=True)

replace("portable/studio_server.py",
    "        return {'path':str(self.root),'projectFile':'project-state.json',",
    """        disk=shutil.disk_usage(self.root)
        return {'path':str(self.root),'projectFile':'project-state.json',
                'freeBytes':disk.free,'totalBytes':disk.total,""")
replace("portable/studio_server.py",
    """        if self.media(id,ext).exists():
            raise ValueError('Media ID is already in use')
        partial = self.root / 'imports' / f'{id}.partial'""",
    """        target=self.media(id,ext)
        if target.exists() or target.is_symlink():
            raise ValueError('Media ID is already in use')
        # Keep enough free space for original novels, recovery and exports.
        # Reject BEFORE the first partial import is created.
        free=shutil.disk_usage(self.root).free
        reserve=max(128*1024**2,min(total//20,1024**3))
        if free < total + reserve:
            raise ValueError('Not enough free disk space for this media import. Free at least '
                             f'{(total+reserve-free+1024**2-1)//(1024**2)} MiB and retry. '
                             'Existing project, recordings and backups were not changed.')
        partial = self.root / 'imports' / f'{id}.partial'""")
replace("portable/studio_server.py",
    "        if target.exists():raise ValueError('Media ID collision; original preserved')",
    """        if target.exists() or target.is_symlink():
            raise ValueError('Media ID collision; original preserved')""")
dollar=chr(36)
replace("web/app.js",
    """</pre><div class="actions"><button class="btn" data-action="refresh-storage">Refresh storage details</button>""",
    """</pre><p class="small muted">Disk free: """+dollar+"""{typeof storageInfo?.freeBytes==='number'?(storageInfo.freeBytes/1073741824).toFixed(1)+' GiB':'Refresh storage details to check free space'} · Large recording imports reserve disk space for projects and backups.</p><div class="actions"><button class="btn" data-action="refresh-storage">Refresh storage details</button>""")
for rel in ("version.txt","package.json","src-tauri/Cargo.toml",
            "src-tauri/tauri.conf.json","tests/release-safety-v013.test.mjs",
            "tests/windows-final-artifact-gate.test.mjs",
            ".github/workflows/windows-installer-upgrade-lab.yml",
            "tests/windows_installer_probe.py",
            "tests/windows_installer_probe_test.py"):
    p=root/rel
    content=p.read_text(encoding='utf-8')
    if "0.14.1" not in content and "installer-lab-0141-" not in content:
        raise ValueError("Expected 0.14.1 base source revision absent: "+rel)
    p.write_text(content.replace("0.14.1","0.14.2")
                             .replace("installer-lab-0141-","installer-lab-0142-"),encoding="utf-8")
    print("RELEASE METADATA 0.14.2",rel,flush=True)
tests=r'''"""Real media-import capacity and symlink safety."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import hashlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'portable'))
from studio_server import Studio

class StorageSafety(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='mmmn-storage-')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.app=Studio(self.root,'synthetic-token')
    def test_insufficient_disk_refuses_before_partial_file(self):
        with patch('studio_server.shutil.disk_usage',return_value=SimpleNamespace(total=1000*1024**2,free=520*1024**2)):
            with self.assertRaisesRegex(ValueError,'Not enough free disk space'):
                self.app.begin_media_import('testaudio001','wav',500*1024**2)
        self.assertFalse((self.root/'imports'/'testaudio001.partial').exists())
        self.assertFalse((self.root/'imports'/'testaudio001.json').exists())
    def test_small_import_still_reserves_headroom(self):
        with patch('studio_server.shutil.disk_usage',return_value=SimpleNamespace(total=1000*1024**2,free=128*1024**2)):
            with self.assertRaisesRegex(ValueError,'Not enough free disk space'):
                self.app.begin_media_import('testaudio001','wav',1)
    def test_good_import_preserves_source_bytes_and_sha(self):
        audio=b'RIFF'+bytes(range(64))
        self.app.begin_media_import('testaudio001','wav',len(audio))
        digest=hashlib.sha256(audio).hexdigest()
        self.assertEqual(self.app.import_media_chunk('testaudio001',0,digest,audio),len(audio))
        self.assertEqual(self.app.finalize_media_import('testaudio001')['sha256'],digest)
        self.assertEqual(self.app.media('testaudio001','wav').read_bytes(),audio)
    def test_symlink_target_not_replaced(self):
        target=self.app.media('testaudio001','wav')
        try:target.symlink_to(self.root/'outside-recording.wav')
        except (OSError,NotImplementedError):self.skipTest('No symlink support')
        with self.assertRaisesRegex(ValueError,'already in use'):
            self.app.begin_media_import('testaudio001','wav',10)
        self.assertTrue(target.is_symlink())
    def test_storage_reports_true_disk_headroom(self):
        with patch('studio_server.shutil.disk_usage',return_value=SimpleNamespace(total=1000,free=123)):
            info=self.app.project_storage_info()
        self.assertEqual(info['freeBytes'],123)
        self.assertEqual(info['totalBytes'],1000)
if __name__=='__main__':unittest.main()
'''
(root/'tests'/'windows_storage_capacity_test.py').write_text(tests,encoding='utf-8')
print("WINDOWS 0.14.2 UPGRADE AND 5 SAFETY TESTS READY",flush=True)
