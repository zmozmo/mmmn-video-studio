"""Windows 0.15.4: optional REAL local Burmese CPU ASR companion pack.

- The Windows app stays offline and keeps existing Whisper fallback unchanged.
- Only a complete locally installed additive pack becomes the preferred ASR.
- Uses existing background worker and cancellation, never uploads recordings.
- Generated SRT remains unapproved and must pass existing Myanmar manuscript,
  full-audio timing and manual consent before it influences picture timing.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
def once(rel,before,after):
    file=root/rel
    original=file.read_text(encoding='utf-8')
    if original.count(before)!=1:
        raise ValueError(f'{rel}: expected one 0.15.2 source anchor, got {original.count(before)}: {before[:85]}')
    file.write_text(original.replace(before,after),encoding='utf-8')
    print('PATCH 0.15.4',rel,flush=True)

server=root/'portable/studio_server.py'
s=server.read_text(encoding='utf-8')
needle="    def offline_speech_status(self, **_):"
if s.count(needle)!=1:raise ValueError('Missing native speech status function anchor')
new_methods=r'''    def _burmese_asr_addon(self):
        """Find the complete optional LOCAL add-on; never fetch missing files."""
        folder=self.root/'addons'/'BurmeseASR'
        exe=folder/'mmmn-burmese-asr.exe'
        model=folder/'model'
        required=('model.safetensors','model.py','transcribe.py',
                  'vocab.json','cmvn.json','config.json','preprocessor_config.json')
        if not exe.is_file() or exe.is_symlink() or not model.is_dir() or model.is_symlink():
            return None
        if any(not (model/f).is_file() or (model/f).is_symlink() for f in required):
            return None
        if (model/'model.safetensors').stat().st_size<80_000_000:
            return None
        if not self.ffmpeg or not Path(self.ffmpeg).is_file():
            return None
        ffprobe=Path(self.ffmpeg).with_name('ffprobe.exe')
        if not ffprobe.is_file():
            cmd=shutil.which('ffprobe.exe') or shutil.which('ffprobe')
            ffprobe=Path(cmd) if cmd else ffprobe
        if not ffprobe.is_file():
            return None
        return exe,model,ffprobe

    def _transcribe_burmese_addon(self, chapterNumber, video, _cancel=None, _progress=None):
        """Create an isolated REVIEW-ONLY SRT with local CPU model and original audio intact."""
        pack=self._burmese_asr_addon()
        if not pack:
            raise ValueError('Offline Burmese add-on pack is unavailable')
        executable,model,ffprobe=pack
        from tempfile import TemporaryDirectory
        with TemporaryDirectory(prefix='burmese-local-',dir=self.root/'transcripts') as folder:
            generated=Path(folder)/'candidate.srt'
            cmd=[str(executable),'--input',str(video),
                 '--model-dir',str(model),'--output',str(generated),
                 '--ffmpeg',str(self.ffmpeg),'--ffprobe',str(ffprobe)]
            if _progress:
                _progress('Recognizing private Burmese voice locally in bounded segments (unapproved SRT)')
            try:
                done=self._run_speech_step(cmd,24*3600,_cancel)
            except subprocess.TimeoutExpired as error:
                raise ValueError('Local Burmese model recognition timed out') from error
            if done.returncode or not generated.is_file():
                raise ValueError('Offline Burmese recognition failed: '+done.stderr[-480:])
            text=generated.read_text(encoding='utf-8-sig')
            if len(text.encode('utf-8'))>MAX_JSON or not re.search(
                r'\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}',text):
                raise ValueError('Local model output has no usable SRT timestamps')
            if _cancel is not None and _cancel.is_set():
                raise ValueError('Offline Burmese transcription cancelled')
            destination=self.root/'transcripts'/f'chapter-{chapterNumber}-{secrets.token_hex(6)}.srt'
            pending=Path(folder)/'review-only.pending'
            pending.write_text(text,encoding='utf-8')
            if _cancel is not None and _cancel.is_set():
                raise ValueError('Offline Burmese transcription cancelled')
            if destination.exists():
                raise FileExistsError('Never overwrite an existing reviewed SRT')
            pending.replace(destination)
            return {'srt':text,'file':destination.name,
                    'modelName':'myanmar-asr-cpu-conformer',
                    'humanReviewRequired':True,'source':'local Burmese CPU optional addon; chunk-level approximate time'}

'''
s=s.replace(needle,new_methods+needle)
anchor="""        """+"\"\"\"User-supplied whisper.cpp and multilingual model; never downloads files.\"\"\""+"""
"""
if s.count(anchor)!=1:raise ValueError('Speech-status docstring anchor missing')
s=s.replace(anchor,anchor+"""        # Prefer a complete, previously installed, zero-network Burmese CPU pack.
        local_pack=self._burmese_asr_addon()
        if local_pack:
            return {'ready':True,'problems':[],
                    'toolsFolder':str(local_pack[0].parent),
                    'modelsFolder':str(local_pack[1]),
                    'modelName':'myanmar-asr-cpu-conformer',
                    'engine':'myanmar-cpu-addon; entirely local; subtitles always need manual review'}
""")
anchor="""        if not status['ready']:
            raise ValueError('Offline transcription not ready: '+'; '.join(status['problems']))
"""
if s.count(anchor)!=1:raise ValueError('Native transcription status anchor missing')
s=s.replace(anchor,anchor+"""        if status.get('engine','').startswith('myanmar-cpu-addon'):
            return self._transcribe_burmese_addon(
                chapterNumber,video,_cancel=_cancel,_progress=_progress)
""")
for k in ('def _burmese_asr_addon(self)','def _transcribe_burmese_addon',
          'myanmar-cpu-addon','return self._transcribe_burmese_addon('):
    if k not in s:raise ValueError('Missing optional Burmese model backend: '+k)
server.write_text(s,encoding='utf-8')

once('web/app.js',
     "Whisper.cpp Offline Model မရှိသေးပါ။",
     "Offline Burmese / Whisper Model မရှိသေးပါ။")
once('web/app.js',
     "Local Multilingual Speech Model တွေ့ပါတယ်။",
     "Local Burmese / Multilingual Speech Model တွေ့ပါတယ်။")
once('web/app.js','MMMN Windows Offline Studio • v0.15.2',
     'MMMN Windows Offline Studio • v0.15.4')
once('tests/windows_atomic_save_0144_test.py',
     'Windows Offline Studio • v0.15.2','Windows Offline Studio • v0.15.4')
once('tests/windows_long_probe_0145_test.py',
     'MMMN Windows Offline Studio • v0.15.2','MMMN Windows Offline Studio • v0.15.4')
for rel in ('version.txt','package.json','src-tauri/Cargo.toml',
            'src-tauri/tauri.conf.json','tests/release-safety-v013.test.mjs',
            'tests/windows-final-artifact-gate.test.mjs',
            '.github/workflows/windows-installer-upgrade-lab.yml',
            'tests/windows_installer_probe.py','tests/windows_installer_probe_test.py'):
    p=root/rel
    raw=p.read_text(encoding='utf-8')
    if '0.15.2' not in raw and 'installer-lab-0152-' not in raw:
        raise ValueError('Missing pinned previous release version witness: '+rel)
    p.write_text(raw.replace('0.15.2','0.15.4').replace(
        'installer-lab-0152-','installer-lab-0154-'),encoding='utf-8')
gate=root/'tests/windows-final-artifact-gate.test.mjs'
raw=gate.read_text(encoding='utf-8')
if r'0\.15\.2' not in raw:raise ValueError('Escaped version witness absent')
gate.write_text(raw.replace(r'0\.15\.2',r'0\.15\.4'),encoding='utf-8')
print('WINDOWS 0.15.4: optional offline Burmese CPU pack backend wired, all source checks PASS',flush=True)
