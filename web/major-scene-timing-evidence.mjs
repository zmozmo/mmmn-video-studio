/**
 * Read-only local Burmese evidence for important-scene SRT timestamps.
 * A unique text match only suggests where to LISTEN; it is not alignment.
 * Never changes scene times, existing pictures, subtitles, or source files.
 */
import {auditNarrationTiming} from './narration-timing-audit.mjs';
import {assessBurmeseTranscript} from './burmese-transcript-agreement.mjs';
const mm=v=>Array.from(String(v??'').normalize('NFC').matchAll(/\p{Script=Myanmar}/gu),m=>m[0]).join('');
const safe=(v,max=180)=>Array.from(String(v??'').replace(/[\r\n\t|]/gu,' ').replace(/\s+/gu,' ').trim()).slice(0,max).join('');
const time=v=>Number.isFinite(v)?v.toFixed(2)+'s':'unavailable';
function check(chapter){
 if(!chapter||chapter.scenePolicy!=='major-only-conservative')throw Error('Major-only draft required');
 const scenes=chapter.scenes;
 if(!Array.isArray(scenes)||!scenes.length||scenes.length>1000)throw Error('Unsafe major-scene timeline');
 let end=0;
 for(const s of scenes){
  if(typeof s?.start!=='number'||typeof s?.duration!=='number'||
     !Number.isFinite(s.start)||!Number.isFinite(s.duration)||
     s.start<0||s.duration<.25||s.duration>3600||
     Math.abs(s.start-end)>.6)throw Error('Unsafe or discontinuous scene timeline');
  end=s.start+s.duration;
 }
 return {scenes,end};
}
function uniqueCue(cues,sceneText){
 const phrase=mm(sceneText).slice(0,32);
 if(phrase.length<20)return {status:'too-short'};
 let hits=0,idx=-1;
 for(let i=0;i<cues.length;i++){
  if(mm(cues[i]?.text).includes(phrase)){
   hits++;idx=i;
   if(hits>1)break;
  }
 }
 if(hits===0)return {status:'unmatched'};
 if(hits>1)return {status:'ambiguous'};
 return {status:'unique-text-only',index:idx,start:cues[idx].start};
}
export function buildMajorSceneTimingEvidence(chapter){
 const {scenes,end}=check(chapter);
 const cues=Array.isArray(chapter.subtitleCues)?chapter.subtitleCues:[];
 const timing=auditNarrationTiming(chapter.recordedSeconds,cues);
 const transcript=assessBurmeseTranscript(
   typeof chapter.text==='string'?chapter.text:'',cues);
 const safeTranscript=timing.status==='supported'&&transcript.status==='supported';
 const rows=[];
 let candidates=0,unresolved=0,ambiguous=0,skipped=0;
 for(const scene of scenes){
  if(scene.technicalContinuation){skipped++;continue;}
  const match=safeTranscript?uniqueCue(cues,scene.text):
    {status:'unverified-transcript'};
  const accepted=match.status==='unique-text-only';
  if(accepted)candidates++;
  else {unresolved++;if(match.status==='ambiguous')ambiguous++;}
  rows.push({
   sceneId:safe(scene.id||'scene',70),currentStart:scene.start,
   duration:scene.duration,status:match.status,
   suggestedCueStart:accepted?match.start:null,
   suggestedCueIndex:accepted?match.index:null,
   manuallyApproved:false,readOnly:true,
   excerpt:safe(scene.text||'',100),
   reason:safe(scene.majorSceneReason||'Opening image or protected scene',100)
  });
 }
 const summary={
  visibleMajorScenes:rows.length,uniqueTextAnchors:candidates,
  unresolvedScenes:unresolved,ambiguousMatches:ambiguous,
  technicalContinuationsIgnored:skipped,
  storySeconds:end,recordedSeconds:chapter.recordedSeconds,
  manuscriptAgreement:transcript.status,audioCoverage:timing.status,
  imagesGenerated:0,changesToProject:0,networkRequests:0,
  wordAlignmentCertified:false,humanReviewMandatory:true
 };
 const lines=['# MMMN Major Scene/SRT Evidence — PRIVATE LOCAL REVIEW',
  '','Unique text matches: '+candidates+' / '+rows.length,
  'Manuscript agreement: '+transcript.status,
  'Full narration coverage: '+timing.status,
  'Original audio duration: '+time(Number(chapter.recordedSeconds)),
  '',
  'WARNING: Word alignment NOT certified. Matching text gives only a listening hint.',
  'Never automatically move scene/photo timestamps from this evidence.',
  'May contain UNPUBLISHED novel text. Do not upload to public GitHub.',
  'No original narration, approved SRT, scene lock or image was modified.',''];
 for(const [i,row] of rows.entries()){
  lines.push('## '+(i+1)+'. '+row.sceneId,'',
   '- Existing scene: '+time(row.currentStart)+' / '+time(row.duration),
   '- Match: '+row.status,
   '- Candidate audio cue (REVIEW ONLY): '+
     (row.suggestedCueStart===null?'NO SAFE MATCH':time(row.suggestedCueStart)),
   '- Why visible image: '+row.reason,
   '- Original novel excerpt: '+row.excerpt,
   '- Action: listen locally and manually confirm picture switch time.','');
 }
 return {rows,summary,markdown:lines.join('\n'),
   readOnly:true,offline:true,automaticallyChangesProject:false};
}
