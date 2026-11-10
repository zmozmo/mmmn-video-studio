/**
 * MMMN: deterministic local narration-to-SRT timeline coverage audit.
 * Checks clock integrity only, NOT Myanmar recognition or word alignment.
 * Does not access network, files, user telemetry or mutate provided data.
 */
const limit=4*3600;
function outcome(status,reason,extra={}) {
  return {status,reason,safeForDraft:status==='supported',
    humanReviewRequired:true,semanticUnderstanding:false,
    wordAccurate:false,offline:true,...extra};
}
export function auditNarrationTiming(recordedSeconds,cues){
  const total=Number(recordedSeconds);
  if(!Number.isFinite(total)||total<=0||total>limit)
    return outcome('insufficient','invalid or missing original narration duration');
  if(!Array.isArray(cues)||cues.length<3||cues.length>20000)
    return outcome('insufficient','not enough timestamped SRT cues for an automatic draft',
      {cueCount:Array.isArray(cues)?cues.length:0});
  let covered=0,lastEnd=0,lastStart=-1,longestGap=0;
  let maxCue=0,validCues=0;
  for(let i=0;i<cues.length;i++){
    const cue=cues[i],start=cue?.start,end=cue?.end;
    if(typeof start!=='number'||typeof end!=='number'||
       !Number.isFinite(start)||!Number.isFinite(end)||
       start<0||end<=start||end>total+.5||
       start<lastStart||start<lastEnd-.15)
      return outcome('unsupported','unsafe SRT time order, overlap or out-of-range cue',
        {cueCount:cues.length,firstBadCue:i+1});
    if(typeof cue.text!=='string'||cue.text.trim().length===0)
      return outcome('unsupported','SRT cue text missing',{cueCount:cues.length,firstBadCue:i+1});
    const length=end-start;
    if(length>120)
      return outcome('unsupported','one generated SRT cue is implausibly long',
        {cueCount:cues.length,firstBadCue:i+1});
    const gap=Math.max(0,start-lastEnd);
    longestGap=Math.max(longestGap,gap);
    covered+=Math.max(0,end-Math.max(start,lastEnd));
    maxCue=Math.max(maxCue,length);
    lastEnd=Math.max(lastEnd,end);
    lastStart=start;
    validCues++;
  }
  const first=cues[0].start,tail=Math.max(0,total-lastEnd);
  const coverage=covered/total;
  const allowedGap=Math.max(30,Math.min(120,total*.08));
  const allowedEdge=Math.max(12,Math.min(90,total*.06));
  const audit={
    cueCount:validCues,narrationSeconds:+total.toFixed(3),
    coveredSpeechSeconds:+covered.toFixed(3),
    observedCoverage:+coverage.toFixed(4),
    longestGapSeconds:+longestGap.toFixed(3),
    beginningGapSeconds:+first.toFixed(3),
    trailingGapSeconds:+tail.toFixed(3),
    maxCueSeconds:+maxCue.toFixed(3),
    audioUnchanged:true,srtUnchanged:true
  };
  // Safety gates, not estimates of speech-recognition confidence.
  const ok=coverage>=.40&&
    longestGap<=allowedGap&&first<=allowedEdge&&tail<=allowedEdge&&
    maxCue<=Math.max(45,Math.min(120,total*.10));
  return outcome(ok?'supported':'unsupported',ok?
    'SRT spans most of the original audio without major timing holes; proofread word placement':
    'SRT leaves major narration gaps, implausible cue lengths or incomplete audio coverage',audit);
}
