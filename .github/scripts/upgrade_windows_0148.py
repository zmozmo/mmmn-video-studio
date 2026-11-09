"""Windows 0.14.8: safe cancellable offline speech transcription for long novels.

Applies after source patches 0.14.1 ... 0.14.7. Changes only the local
speech-processing control flow; preserves original project, speech media,
reviewed subtitles, 0.14.7 image brief, and all MP4/backup security.
The optional user-provided multilingual model/CLI is NOT bundled.
"""
from pathlib import Path
import re
import sys

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()

def once(rel,old,new):
    p=root/rel
    s=p.read_text(encoding="utf-8")
    if s.count(old)!=1:
        raise ValueError(f"{rel}: expected exactly one anchor, got {s.count(old)}: {old[:110]!r}")
    p.write_text(s.replace(old,new),encoding="utf-8")
    print("PATCH 0.14.8:",rel,flush=True)

server=root/"portable/studio_server.py"
s=server.read_text(encoding="utf-8")
def serve(old,new):
    global s
    if s.count(old)!=1:
        raise ValueError(f"studio_server: expected exactly one patch anchor, got {s.count(old)}: {old[:110]!r}")
    s=s.replace(old,new)

helper=r'''    @staticmethod
    def _run_speech_step(args, timeout, cancel=None):
        """Run trusted local FFmpeg/whisper process with bounded cooperative cancel.

        Never use shell=True, don't keep captured output in a project,
        and kill stalled children on cancellation/timeout/error.
        """
        command=[str(x) for x in args]
        if not command or not 1 <= float(timeout) <= 24*3600:
            raise ValueError('Invalid local speech subprocess request')
        if cancel is not None and cancel.is_set():
            raise ValueError('Offline transcription cancelled')
        flags=getattr(subprocess,'CREATE_NO_WINDOW',0) if os.name=='nt' else 0
        child=subprocess.Popen(command,stdin=subprocess.DEVNULL,
             stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
             encoding='utf-8',errors='replace',creationflags=flags)
        deadline=time.monotonic()+float(timeout)
        try:
            while True:
                if cancel is not None and cancel.is_set():
                    raise ValueError('Offline transcription cancelled')
                remaining=deadline-time.monotonic()
                if remaining<=0:
                    raise subprocess.TimeoutExpired(command,timeout)
                try:
                    out,err=child.communicate(timeout=min(1.0,remaining))
                    return subprocess.CompletedProcess(command,child.returncode,out,err)
                except subprocess.TimeoutExpired:
                    continue
        finally:
            if child.poll() is None:
                child.kill()
                try:child.communicate(timeout=5)
                except subprocess.TimeoutExpired:pass

    def start_transcription_job(self, chapterNumber:int, sourceVideoId:str,
                                sourceVideoExt:str, **_):
        """Return immediately; actual offline transcription runs in a worker."""
        if not isinstance(chapterNumber,int) or not 1 <= chapterNumber <= 1000:
            raise ValueError('Invalid chapter number')
        if sourceVideoExt not in NARRATION_EXTS:
            raise ValueError('Unsupported narration extension')
        media=self.media(sourceVideoId,sourceVideoExt)
        if not media.is_file() or media.is_symlink():
            raise ValueError('Original narration missing')
        if not self.offline_speech_status()['ready']:
            raise ValueError('Optional local Whisper CLI/model not ready')
        with self._jobs_lock:
            jobs=getattr(self,'_speech_jobs',None)
            if jobs is None:
                self._speech_jobs={}
                self._active_speech_job=None
                jobs=self._speech_jobs
            old=jobs.get(self._active_speech_job)
            if old and old['status'] in ('queued','running','cancelling'):
                raise ValueError('An offline transcription is already in progress')
            job_id='speech-'+secrets.token_hex(12)
            cancel=threading.Event()
            jobs[job_id]=dict(id=job_id,status='queued',phase='Queued for local speech analysis',
                              result=None,error=None,_cancel=cancel)
            self._active_speech_job=job_id
            # Bound memory; completed transcripts can be retained as local files.
            for old_id in list(jobs)[:-8]:
                if old_id!=job_id and jobs[old_id]['status'] in ('complete','failed','cancelled'):
                    jobs.pop(old_id,None)
        def progress(phase):
            with self._jobs_lock:
                if not cancel.is_set():
                    jobs[job_id].update(status='running',phase=phase)
        def worker():
            try:
                progress('Preparing offline 16kHz speech audio')
                result=self.transcribe_narration(
                    chapterNumber=chapterNumber,
                    sourceVideoId=sourceVideoId,
                    sourceVideoExt=sourceVideoExt,
                    _cancel=cancel,_progress=progress)
                with self._jobs_lock:
                    if cancel.is_set():
                        jobs[job_id].update(status='cancelled',phase='Cancelled safely',result=None)
                    else:
                        jobs[job_id].update(status='complete',phase='Local SRT needs human review',
                                            result=result)
            except Exception as exc:
                with self._jobs_lock:
                    if cancel.is_set():
                        jobs[job_id].update(status='cancelled',phase='Cancelled safely',result=None)
                    else:
                        jobs[job_id].update(status='failed',phase='Speech analysis failed safely',
                                            error=str(exc)[:800])
            finally:
                with self._jobs_lock:
                    if self._active_speech_job==job_id:
                        self._active_speech_job=None
        threading.Thread(target=worker,name='mmmn-offline-speech-'+job_id,
                         daemon=True).start()
        return self.get_transcription_job_status(id=job_id)

    def get_transcription_job_status(self,id:str,**_):
        if not isinstance(id,str) or not re.fullmatch(r'speech-[a-f0-9]{24}',id):
            raise ValueError('Invalid offline speech job ID')
        with self._jobs_lock:
            job=getattr(self,'_speech_jobs',{}).get(id)
            if not job:raise ValueError('Unknown offline speech job')
            return {key:val for key,val in job.items() if not key.startswith('_')}

    def cancel_transcription_job(self,id:str,**_):
        if not isinstance(id,str) or not re.fullmatch(r'speech-[a-f0-9]{24}',id):
            raise ValueError('Invalid offline speech job ID')
        with self._jobs_lock:
            job=getattr(self,'_speech_jobs',{}).get(id)
            if not job:raise ValueError('Unknown offline speech job')
            if job['status'] in ('queued','running','cancelling'):
                job['_cancel'].set()
                job.update(status='cancelling',phase='Stopping local Whisper safely')
        return self.get_transcription_job_status(id=id)

'''
serve("    def offline_speech_status(self, **_):",helper+"    def offline_speech_status(self, **_):")
serve("    def transcribe_narration(self, chapterNumber:int, sourceVideoId:str,\n                             sourceVideoExt:str, **_):",
      "    def transcribe_narration(self, chapterNumber:int, sourceVideoId:str,\n                             sourceVideoExt:str, _cancel=None, _progress=None, **_):")

serve("""            try:
                audio=subprocess.run(audio_cmd,capture_output=True,text=True,timeout=7200)
            except subprocess.TimeoutExpired as e:
                raise ValueError('Audio extraction timed out') from e""",
"""            if _progress:_progress('Extracting local narration WAV')
            try:
                audio=self._run_speech_step(audio_cmd,7200,_cancel)
            except subprocess.TimeoutExpired as e:
                raise ValueError('Audio extraction timed out') from e""")
serve("""            try:
                done=subprocess.run(cmd,capture_output=True,text=True,timeout=24*3600)
            except subprocess.TimeoutExpired as e:
                raise ValueError('Offline speech recognition timed out') from e""",
"""            if _progress:_progress('Recognizing local speech; exact completion time unavailable')
            try:
                done=self._run_speech_step(cmd,24*3600,_cancel)
            except subprocess.TimeoutExpired as e:
                raise ValueError('Offline speech recognition timed out') from e""")
serve("""            destination=self.root/'transcripts'/f'chapter-{chapterNumber}-{secrets.token_hex(6)}.srt'
            # Never overwrite an earlier corrected transcript.""",
"""            if _cancel is not None and _cancel.is_set():
                raise ValueError('Offline transcription cancelled')
            destination=self.root/'transcripts'/f'chapter-{chapterNumber}-{secrets.token_hex(6)}.srt'
            # Never overwrite an earlier corrected transcript.""")

# Security: expose only the three specific short non-blocking commands.
m=re.search(r'(?m)^ALLOWED\s*=\s*\{',s)
if not m:raise ValueError('Named API allowlist missing; refuse unsafe service patch')
s=s[:m.end()]+"\n    'start_transcription_job', 'get_transcription_job_status', 'cancel_transcription_job',"+s[m.end():]
for witness in ("_run_speech_step","start_transcription_job",
                "get_transcription_job_status","cancel_transcription_job",
                "self._run_speech_step(cmd,24*3600,_cancel)",
                "if _cancel is not None and _cancel.is_set()"):
    if witness not in s:raise ValueError('ASR async API missing '+witness)
server.write_text(s,encoding='utf-8')
print("0.14.8: cancellable local transcription / API allowlist patched",flush=True)

once("web/app.js",
     '<button class="btn primary" data-action="audio-first-major-plan">',
     '<button class="btn" data-action="cancel-offline-speech">⏹ အသံမှစာပြောင်းခြင်း ရပ်ရန်</button>'
     '<button class="btn primary" data-action="audio-first-major-plan">')

# The original synchronous call could stall a 90-minute novel for hours.
once("web/app.js",
"""            const generated=await window.__TAURI__.core.invoke('transcribe_narration',{
              chapterNumber:c.number,sourceVideoId:recording.id,
              sourceVideoExt:recording.name.split('.').at(-1).toLowerCase()
            });""",
"""            const request={
              chapterNumber:c.number,sourceVideoId:recording.id,
              sourceVideoExt:recording.name.split('.').at(-1).toLowerCase()
            };
            const started=await window.__TAURI__.core.invoke('start_transcription_job',request);
            window.__MMMN_ACTIVE_SPEECH_JOB__=started.id;
            let state=started,checks=0;
            try{
              while(['queued','running','cancelling'].includes(state.status)){
                await new Promise(resolve=>setTimeout(resolve,1000));
                state=await window.__TAURI__.core.invoke('get_transcription_job_status',{id:started.id});
                if(++checks%30===0)toast('Offline အသံမှစာပြောင်းခြင်း: '+state.phase+
                  '။ စကားလုံးအလိုက်အချိန် မတိကျနိုင်ပါ။');
              }
            } finally{
              if(window.__MMMN_ACTIVE_SPEECH_JOB__===started.id){
                window.__MMMN_ACTIVE_SPEECH_JOB__=null;
              }
            }
            if(state.status==='cancelled')throw Error('Offline transcription cancelled');
            if(state.status!=='complete'||!state.result?.srt){
              throw Error(state.error||'Offline Speech-to-Text အောင်မြင်မှုမရှိပါ');
            }
            const generated=state.result;""")

once("web/app.js",
"""        }catch(error){
          toast('Offline အသံမှစာပြောင်းခြင်း မအောင်မြင်ပါ: '+error.message+
            '။ Pause Timing ကိုပဲ သုံးမယ်။',true);
        }""",
"""        }catch(error){
          if(String(error.message).includes('cancelled')){
            toast('အသံမှစာပြောင်းခြင်း ရပ်ပြီးပါပြီ။ မူရင်းစာမူ/SRT မပြောင်းပါ။');
            return;
          }
          toast('Offline အသံမှစာပြောင်းခြင်း မအောင်မြင်ပါ: '+error.message+
            '။ Pause Timing ကိုပဲ သုံးမယ်။',true);
        }""")

once("web/app.js",
     "case 'audio-first-major-plan':",
     """case 'cancel-offline-speech':{
    const active=window.__MMMN_ACTIVE_SPEECH_JOB__;
    if(!active){toast('လက်ရှိ အသံမှစာပြောင်းနေခြင်း မရှိပါ။');return;}
    try{
      await window.__TAURI__.core.invoke('cancel_transcription_job',{id:active});
      toast('Offline Speech-to-Text ရပ်ရန် အမိန့်ပို့ပြီးပါပြီ။');
    }catch(error){toast('Speech Cancel မအောင်မြင်ပါ: '+error.message,true);}
    return;
  }
  case 'audio-first-major-plan':""")

once("web/app.js","MMMN Windows Offline Studio • v0.14.7",
                   "MMMN Windows Offline Studio • v0.14.8")
once("tests/windows_atomic_save_0144_test.py",
     "Windows Offline Studio • v0.14.7","Windows Offline Studio • v0.14.8")
once("tests/windows_long_probe_0145_test.py",
     "MMMN Windows Offline Studio • v0.14.7","MMMN Windows Offline Studio • v0.14.8")

for rel in ("version.txt","package.json","src-tauri/Cargo.toml",
            "src-tauri/tauri.conf.json","tests/release-safety-v013.test.mjs",
            "tests/windows-final-artifact-gate.test.mjs",
            ".github/workflows/windows-installer-upgrade-lab.yml",
            "tests/windows_installer_probe.py",
            "tests/windows_installer_probe_test.py"):
    p=root/rel
    source=p.read_text(encoding="utf-8")
    if "0.14.7" not in source and "installer-lab-0147-" not in source:
        raise ValueError('0.14.7 metadata witness missing: '+rel)
    p.write_text(source.replace("0.14.7","0.14.8").replace(
                 "installer-lab-0147-","installer-lab-0148-"),encoding="utf-8")
gate=root/"tests/windows-final-artifact-gate.test.mjs"
source=gate.read_text(encoding="utf-8")
if r'0\.14\.7' not in source:
    raise ValueError('Strict 0.14.7 release gate witness missing')
gate.write_text(source.replace(r'0\.14\.7',r'0\.14\.8'),encoding="utf-8")

ui=(root/"web/app.js").read_text(encoding="utf-8")
for key in ("cancel-offline-speech","start_transcription_job",
            "get_transcription_job_status","cancel_transcription_job",
            "Offline transcription cancelled"):
    if key not in ui:raise ValueError('Speech cancellable UI path missing: '+key)
print("WINDOWS 0.14.8 PATCH COMPLETE: asynchronous cancellable local transcription; original media and reviewed SRT protected",flush=True)
