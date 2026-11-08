"""Incremental 0.14.3 Windows: reserve concurrent imports and enforce per-chunk disk safety.

This runs only on the audited extracted source after the 0.14.1 and 0.14.2
patches. Abort on unexpected upstream changes rather than silently packaging.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()

def replace(rel,old,new):
    path=root/rel
    content=path.read_text(encoding="utf-8")
    matches=content.count(old)
    if matches!=1:
        raise ValueError(f"{rel}: source safety anchor expected once, got {matches}: {old[:80]!r}")
    path.write_text(content.replace(old,new),encoding="utf-8")
    print("WINDOWS 0.14.3 HARDENED:",rel,flush=True)

replace("portable/studio_server.py",
    "        if free < total + reserve:\n",
    """        # Existing uploads reserve their *remaining* bytes on this drive.
        # Without this, two imports can each pass an independent preflight,
        # exhausting space even though each declared size individually fits.
        pending=0
        for previous in (self.root/'imports').glob('*.json'):
            if previous.is_symlink():
                raise ValueError('Unsafe pending import metadata symlink')
            state=json.loads(previous.read_text(encoding='utf-8'))
            previous_part=self.root/'imports'/f'{previous.stem}.partial'
            if previous_part.is_symlink():
                raise ValueError('Unsafe pending import partial symlink')
            if not isinstance(state.get('total'),int) or state['total']<=0 or not previous_part.is_file():
                raise ValueError('Damaged pending import metadata; abort the import before retrying')
            pending+=max(0,state['total']-previous_part.stat().st_size)
        if free < total + pending + reserve:
""")
replace("portable/studio_server.py",
    """        part = self.root/'imports'/f'{id}.partial'
        with part.open('r+b') as f:
""",
    """        part = self.root/'imports'/f'{id}.partial'
        if part.is_symlink():
            raise ValueError('Unsafe media import partial symlink')
        # Disk space can change *after* the initial capacity check, especially
        # with other apps writing files. Never write the next chunk if doing
        # so could consume the safety headroom for novels and recovery.
        headroom=max(128*1024**2,min(meta['total']//20,1024**3))
        if shutil.disk_usage(self.root).free < len(data)+headroom:
            raise ValueError('Not enough free disk space for the next media chunk; original files preserved')
        with part.open('r+b') as f:
""")

for rel in ("version.txt","package.json","src-tauri/Cargo.toml",
            "src-tauri/tauri.conf.json","tests/release-safety-v013.test.mjs",
            "tests/windows-final-artifact-gate.test.mjs",
            ".github/workflows/windows-installer-upgrade-lab.yml",
            "tests/windows_installer_probe.py",
            "tests/windows_installer_probe_test.py"):
    path=root/rel
    content=path.read_text(encoding="utf-8")
    if "0.14.2" not in content and "installer-lab-0142-" not in content:
        raise ValueError(f"Missing verified 0.14.2 release source: {rel}")
    path.write_text(content.replace("0.14.2","0.14.3").replace(
        "installer-lab-0142-","installer-lab-0143-"),encoding="utf-8")

gate=root/"tests"/"windows-final-artifact-gate.test.mjs"
original=gate.read_text(encoding="utf-8")
if r"0\.14\.2" not in original:
    raise ValueError("Cannot locate strict 0.14.2 artifact regex witness")
gate.write_text(original.replace(r"0\.14\.2",r"0\.14\.3"),encoding="utf-8")

tests=r'''"""Windows 0.14.3: real pending-import reservations and chunk safety."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import hashlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'portable'))
from studio_server import Studio

MiB=1024**2
class StreamingCapacity(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='mmmn-0143-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.app=Studio(self.root,'synthetic-only-test-token')
    def test_concurrent_import_reservation_prevents_overcommit(self):
        with patch('studio_server.shutil.disk_usage',
                   return_value=SimpleNamespace(total=1000*MiB,free=500*MiB)):
            self.app.begin_media_import('first0001','wav',300*MiB)
            with self.assertRaisesRegex(ValueError,'Not enough free disk space'):
                self.app.begin_media_import('second001','wav',150*MiB)
        self.assertFalse((self.root/'imports'/'second001.partial').exists())
        self.assertFalse((self.root/'imports'/'second001.json').exists())
    def test_abort_releases_reservation(self):
        with patch('studio_server.shutil.disk_usage',
                   return_value=SimpleNamespace(total=1000*MiB,free=500*MiB)):
            self.app.begin_media_import('first0001','wav',300*MiB)
            self.app.abort_media_import('first0001')
            self.app.begin_media_import('second001','wav',150*MiB)
        self.assertTrue((self.root/'imports'/'second001.partial').is_file())
    def test_space_drop_refuses_chunk_before_writing(self):
        data=b'RIFF'+bytes(range(28))
        self.app.begin_media_import('chunk0001','wav',len(data))
        target=self.root/'imports'/'chunk0001.partial'
        with patch('studio_server.shutil.disk_usage',
                   return_value=SimpleNamespace(total=1000*MiB,free=128*MiB)):
            with self.assertRaisesRegex(ValueError,'Not enough free disk space'):
                self.app.import_media_chunk('chunk0001',0,hashlib.sha256(data).hexdigest(),data)
        self.assertEqual(target.stat().st_size,0)
    def test_normal_chunk_still_succeeds_without_data_change(self):
        data=b'RIFF'+bytes(range(28))
        self.app.begin_media_import('chunk0001','wav',len(data))
        digest=hashlib.sha256(data).hexdigest()
        self.assertEqual(self.app.import_media_chunk('chunk0001',0,digest,data),len(data))
        self.assertEqual(self.app.finalize_media_import('chunk0001')['sha256'],digest)
        self.assertEqual(self.app.media('chunk0001','wav').read_bytes(),data)
    def test_partial_symlink_cannot_overwrite_another_file(self):
        original=self.root/'important-synthetic-file.txt'
        original.write_bytes(b'ORIGINAL FILE')
        self.app.begin_media_import('chunk0001','wav',5)
        partial=self.root/'imports'/'chunk0001.partial'
        partial.unlink()
        try:
            partial.symlink_to(original)
        except (OSError,NotImplementedError):
            self.skipTest('Windows symlink privileges unavailable')
        data=b'abcde'
        with self.assertRaisesRegex(ValueError,'symlink'):
            self.app.import_media_chunk('chunk0001',0,hashlib.sha256(data).hexdigest(),data)
        self.assertEqual(original.read_bytes(),b'ORIGINAL FILE')

if __name__=='__main__':
    unittest.main()
'''
target=root/"tests"/"windows_streaming_capacity_test.py"
if target.exists():
    raise ValueError("0.14.3 streaming safety tests already exist; stop repeated patch")
target.write_text(tests,encoding="utf-8")
print("WINDOWS 0.14.3 PATCH COMPLETE: five new tests and version metadata",flush=True)
