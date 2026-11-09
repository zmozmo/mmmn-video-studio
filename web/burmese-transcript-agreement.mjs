/**
 * Myanmar narration SRT-to-original-manuscript overlap gate.
 *
 * An offline speech model can output perfectly formatted SRT timestamps but
 * completely wrong words. Do not allow such text to silently drive pictures.
 *
 * This is a conservative text agreement CHECK, not ASR confidence, transcript
 * certification or exact word/time alignment. Always review output manually.
 * No network, storage, model downloads, personal telemetry, or source mutation.
 */
const MAX_TEXT=1_000_000;
const n=7;
const minBook=70;
const minSpeech=30;

function myanmarOnly(value){
  const text=String(value??'').normalize('NFC');
  return Array.from(text.matchAll(/\p{Script=Myanmar}/gu),m=>m[0]).join('');
}

function grams(s){
  const result=new Set;
  const chars=Array.from(s);
  for(let i=0;i+n<=chars.length;i++)result.add(chars.slice(i,i+n).join(''));
  return result;
}

export function assessBurmeseTranscript(manuscript, cues){
  if(!Array.isArray(cues)||cues.length===0||cues.length>20000)
    return {status:'insufficient',reason:'no validated timestamped speech cues',
      autoAccepted:false,reviewRequired:true};
  if(String(manuscript??'').length>MAX_TEXT)
    return {status:'insufficient',reason:'manuscript is too large for a reliable local comparison',
      autoAccepted:false,reviewRequired:true};
  const speech=cues.map(x=>String(x?.text??'')).join(' ');
  if(speech.length>MAX_TEXT)
    return {status:'insufficient',reason:'generated speech transcript is too large',
      autoAccepted:false,reviewRequired:true};
  const book=myanmarOnly(manuscript),spoken=myanmarOnly(speech);
  if(Array.from(book).length<minBook || Array.from(spoken).length<minSpeech){
    return {status:'insufficient',reason:'too little Myanmar script evidence to compare',
      observedOverlap:null,autoAccepted:false,reviewRequired:true};
  }
  const bookGrams=grams(book),speechGrams=grams(spoken);
  if(bookGrams.size===0||speechGrams.size<8)
    return {status:'insufficient',reason:'insufficient distinct Myanmar syllable sequences',
      observedOverlap:null,autoAccepted:false,reviewRequired:true};
  let shared=0;
  for(const gr of speechGrams)if(bookGrams.has(gr))shared++;
  const overlap=shared/speechGrams.size;
  let auditable=0,perCueMatch=0;
  for(const cue of cues){
    const chars=myanmarOnly(cue?.text);
    const gs=grams(chars);
    if(gs.size<4)continue;
    auditable++;
    let ok=false;
    for(const g of gs){if(bookGrams.has(g)){ok=true;break;}}
    if(ok)perCueMatch++;
  }
  const cueRatio=auditable?perCueMatch/auditable:0;
  // These are deterministic safeguards against gross hallucinations, NOT
  // learned model probabilities. The model must prove useful text overlap.
  const supported=shared>=12&&overlap>=.27&&auditable>=2&&cueRatio>=.45;
  return {
    status:supported?'supported':'unsupported',
    reason:supported?
      'generated Burmese text has substantial overlap with the original manuscript; human review still required':
      'generated Burmese text does not sufficiently match the original novel; ignore ASR timing',
    observedOverlap:+overlap.toFixed(4),
    matchingDistinctSequences:shared,
    examinedDistinctSequences:speechGrams.size,
    cueCoverage:+cueRatio.toFixed(4),
    auditableCues:auditable,
    autoAccepted:false,
    reviewRequired:true,
    safeToProposeAfterHumanReview:supported
  };
}
