"""Windows 0.14.8: local speech subprocess, async job and cancellation tests."""
import sys
import threading
import time
import types
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'portable'))
from studio_server import Studio

class SafeOfflineSpeechJobs(unittest.TestCase):
    def instance(self,slow=False):
        s=Studio.__new__(Studio)
        s._jobs_lock=threading.RLock()
        s._media_for_test=Path(__file__)
        s.media=types.MethodType(lambda self,mid,ext:self._media_for_test,s)
        s.offline_speech_status=types.MethodType(lambda self,**kw:{'ready':True},s)
        def fake(self,chapterNumber,sourceVideoId,sourceVideoExt,_cancel=None,_progress=None,**_):
            if _progress:_progress('Synthetic test process, no real user audio')
            if slow:
                for _ in range(300):
                    if _cancel.is_set():raise ValueError('Offline transcription cancelled')
                    time.sleep(.02)
            return {'srt':'1\n00:00:00,000 --> 00:00:01,000\nမြန်မာစာ\n',
                    'humanReviewRequired':True}
        s.transcribe_narration=types.MethodType(fake,s)
        return s

    def wait(self,studio,id):
        for _ in range(250):
            state=studio.get_transcription_job_status(id=id)
            if state['status'] in ('complete','cancelled','failed'):return state
            time.sleep(.02)
        self.fail('Speech job never completed/cancelled')

    def test_local_process_completes_without_shell(self):
        p=Studio._run_speech_step([sys.executable,'-c','print("clean speech")'],15)
        self.assertEqual(p.returncode,0)
        self.assertIn('clean speech',p.stdout)

    def test_pre_cancelled_subprocess_never_launches(self):
        event=threading.Event();event.set()
        with self.assertRaisesRegex(ValueError,'cancelled'):
            Studio._run_speech_step([sys.executable,'-c','print("not launched")'],5,event)

    def test_cancel_stops_live_child_without_waiting_for_long_timeout(self):
        event=threading.Event()
        threading.Timer(.4,event.set).start()
        t=time.monotonic()
        with self.assertRaisesRegex(ValueError,'cancelled'):
            Studio._run_speech_step([sys.executable,'-c','import time;time.sleep(60)'],90,event)
        self.assertLess(time.monotonic()-t,4)

    def test_subprocess_timeout_kills_child(self):
        with self.assertRaises(Exception):
            Studio._run_speech_step([sys.executable,'-c','import time;time.sleep(30)'],1)

    def test_complete_job_returns_review_required_srt(self):
        s=self.instance()
        x=s.start_transcription_job(chapterNumber=1,sourceVideoId='synthetic_1',
                                    sourceVideoExt='wav')
        result=self.wait(s,x['id'])
        self.assertEqual(result['status'],'complete')
        self.assertTrue(result['result']['humanReviewRequired'])
        self.assertIn('မြန်မာစာ',result['result']['srt'])
        self.assertIsNone(result['error'])

    def test_cancelled_job_never_returns_partial_srt(self):
        s=self.instance(slow=True)
        x=s.start_transcription_job(chapterNumber=1,sourceVideoId='synthetic_1',
                                    sourceVideoExt='wav')
        cancelled=s.cancel_transcription_job(id=x['id'])
        self.assertIn(cancelled['status'],('cancelling','cancelled'))
        final=self.wait(s,x['id'])
        self.assertEqual(final['status'],'cancelled')
        self.assertIsNone(final['result'])

    def test_prevent_concurrent_transcription_overwriting_same_reviewed_srt(self):
        s=self.instance(slow=True)
        x=s.start_transcription_job(chapterNumber=1,sourceVideoId='synthetic_1',
                                    sourceVideoExt='wav')
        with self.assertRaisesRegex(ValueError,'already in progress'):
            s.start_transcription_job(chapterNumber=2,sourceVideoId='synthetic_2',
                                      sourceVideoExt='wav')
        s.cancel_transcription_job(id=x['id'])
        self.wait(s,x['id'])

    def test_unknown_job_id_rejected(self):
        s=self.instance()
        for op in (s.get_transcription_job_status,s.cancel_transcription_job):
            with self.assertRaisesRegex(ValueError,'Invalid'):
                op(id='../secret')
            with self.assertRaisesRegex(ValueError,'Unknown'):
                op(id='speech-'+'0'*24)

    def test_invalid_source_request_rejected(self):
        s=self.instance()
        with self.assertRaisesRegex(ValueError,'Unsupported'):
            s.start_transcription_job(chapterNumber=1,sourceVideoId='something',sourceVideoExt='txt')
        with self.assertRaisesRegex(ValueError,'Invalid'):
            s.start_transcription_job(chapterNumber=0,sourceVideoId='synthetic_1',sourceVideoExt='wav')

if __name__=='__main__':
    unittest.main()
