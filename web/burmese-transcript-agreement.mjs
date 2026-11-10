/**
 * Offline Burmese SRT-to-original-manuscript agreement gate.
 * A matching n-gram is NOT proof the words were spoken at that timestamp.
 * All accepted cues remain human-review-only proposals.
 * No files, network, telemetry, model downloads, or source mutation.
 */
const MAX_TEXT = 1_000_000;
const N = 7;
function result(status, reason, extra={}) {
  return {status, reason, autoAccepted:false, reviewRequired:true,
    safeToProposeAfterHumanReview:status==='supported', ...extra};
}
function myanmarOnly(value) {
  return Array.from(String(value??'').normalize('NFC').matchAll(/\p{Script=Myanmar}/gu),m=>m[0]).join('');
}
function grams(s) {
  const found=new Set(), a=Array.from(s);
  for(let i=0; i+N<=a.length; i++) found.add(a.slice(i,i+N).join(''));
  return found;
}
function timesAreSafe(cues) {
  let lastStart=-1,lastEnd=-1;
  for(const cue of cues) {
    if(typeof cue?.start!=='number'||typeof cue?.end!=='number'||
       !Number.isFinite(cue.start)||!Number.isFinite(cue.end)||
       cue.start<0||cue.end<=cue.start||cue.end>48*3600||
       cue.start<lastStart||cue.start<lastEnd-0.15) return false;
    lastStart=cue.start;
    lastEnd=cue.end;
  }
  return true;
}
// Rough narrative-order sanity check. Repeated words may share a book position.
function orderedAnchor(book, spoken, at) {
  const a=Array.from(spoken), width=11;
  if(a.length<width)return -1;
  const indices=[0,Math.floor((a.length-width)/3),
                 Math.floor((a.length-width)*2/3),a.length-width];
  let best=Infinity;
  for(const start of new Set(indices)) {
    const position=book.indexOf(a.slice(start,start+width).join(''),at);
    if(position>=0 && position<best) best=position;
  }
  return best===Infinity?-1:best;
}
export function assessBurmeseTranscript(manuscript,cues) {
  if(!Array.isArray(cues)||cues.length<2||cues.length>20000)
    return result('insufficient','no sufficiently varied timestamped speech cues');
  if(typeof manuscript!=='string'||manuscript.length>MAX_TEXT)
    return result('insufficient','manuscript missing or too large for a safe comparison');
  if(!timesAreSafe(cues))
    return result('unsupported','generated SRT timings are invalid or out of order');
  const texts=[];
  let chars=0;
  for(const cue of cues) {
    if(typeof cue?.text!=='string')return result('insufficient','speech cue text is invalid');
    chars+=cue.text.length;
    if(chars>MAX_TEXT)return result('insufficient','generated transcript is too large');
    texts.push(cue.text);
  }
  const book=myanmarOnly(manuscript);
  const spoken=myanmarOnly(texts.join(' '));
  if(Array.from(book).length<70 || Array.from(spoken).length<30)
    return result('insufficient','too little Myanmar script evidence to compare',{observedOverlap:null});
  const bookGrams=grams(book), speechGrams=grams(spoken);
  if(bookGrams.size===0||speechGrams.size<12)
    return result('insufficient','insufficient distinct Myanmar character sequences',{observedOverlap:null});
  let shared=0;
  for(const gram of speechGrams)if(bookGrams.has(gram))shared++;
  const overlap=shared/speechGrams.size;
  let auditable=0,goodCues=0,orderedCues=0,position=0;
  let examinedChars=0,matchedChars=0;
  for(const cue of cues) {
    const seq=myanmarOnly(cue.text), gs=grams(seq);
    if(gs.size<4) continue;
    auditable++;
    let hits=0;
    for(const gram of gs)if(bookGrams.has(gram))hits++;
    const ratio=hits/gs.size, len=Array.from(seq).length;
    examinedChars+=len;
    if(hits>=3 && ratio>=0.4) {
      goodCues++;
      matchedChars+=len;
      const next=orderedAnchor(book,seq,position);
      if(next>=0) {orderedCues++;position=next;}
    }
  }
  const cueCoverage=auditable?goodCues/auditable:0;
  const orderCoverage=goodCues?orderedCues/goodCues:0;
  const characterCoverage=examinedChars?matchedChars/examinedChars:0;
  // Conservative anti-hallucination thresholds, not an ASR confidence score.
  const supported=shared>=16&&overlap>=.35&&auditable>=2&&
    cueCoverage>=.70&&characterCoverage>=.70&&orderCoverage>=.70&&orderedCues>=2;
  return result(supported?'supported':'unsupported',supported?
    'substantial Burmese manuscript overlap in plausible order; review every word and timestamp':
    'generated speech differs from the manuscript or its narrative order; ignore ASR timing',{
    observedOverlap:+overlap.toFixed(4),matchingDistinctSequences:shared,
    examinedDistinctSequences:speechGrams.size,
    cueCoverage:+cueCoverage.toFixed(4),
    manuscriptOrderCoverage:+orderCoverage.toFixed(4),
    characterCoverage:+characterCoverage.toFixed(4),
    auditableCues:auditable,timestampOrderValid:true
  });
}
