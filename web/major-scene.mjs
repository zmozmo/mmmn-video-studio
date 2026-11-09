/**
 * Conservative, offline-only **major visual scene** planner.
 *
 * This is transparent, explainable text-evidence scoring, NOT a Burmese
 * language understanding model, NOT speech recognition and NOT an image
 * generator. Scene timing must come from existing SRT evidence, pause hints,
 * or clearly labelled estimates. A mere rain/girl mention cannot trigger a
 * new background. Manual photo/timing decisions always survive.
 *
 * See specs/0146-major-scenes.md. No network, no private-data collection.
 */

const has = (s, re) => re.test(s);
const MAX_RENDER_SCENE_SECONDS=3600; // native per-scene encoding safety limit
const protect = s => Boolean(s?.visualLocked || s?.manualLocked ||
  s?.alignment === 'manual-locked' ||
  s?.imageMatchStatus === 'manual-confirmed' ||
  (s?.imageMatchStatus === 'manual-review' && s?.assetId));

const ARRIVAL = /(ရောက်ရှိ|ရောက်သွား|ရောက်လာ|ဝင်ရောက်|ဝင်သွား|ထွက်ခွာ|ပြောင်းရွှေ့|ကူးပြောင်း|သို့သွား|သို့ရောက်|ထဲဝင်|arrived|entered|traveled|moved to)/iu;
const DISTINCT_PLACE = /(သင်္ချိုင်း|ရွာဟောင်း|တောအုပ်|တောင်ကြော|ကျတ်ကုန်း|ဂူ|ဘုရားပုထိုး|အိမ်အို|သစ်တော|မြို့ဟောင်း|လှိုဏ်ဂူ|အိမ်ထဲ|အပြင်ဘက်|cemetery|graveyard|forest|temple|cave|abandoned village)/iu;
const SEVERE_WEATHER = /(မိုး(အလွန်|အရမ်း|အတော်|သည်းထန်|အပြင်းအထန်)|မိုးကြီးသည်း|မိုးသည်း|မုန်တိုင်း|storm|torrential|downpour)/iu;
const STRONG_DARKNESS = /(အမှောင်ဖုံး|အမှောင်ကျ|မှောင်မိုက်|ညနေမှောင်|မည်းမှောင်|မမြင်ရ|တိတ်ဆိတ်မှောင်|pitch.dark|blackout)/iu;
const DANGER = /(ကြောက်မက်|အန္တရာယ်|ထိတ်လန့်|ထွက်ပြေး|ခြောက်လှန့်|လမ်းပျောက်|မမြင်နိုင်|သေဆုံး|အော်ဟစ်|terror|danger|terrified)/iu;
const REVEAL = /(လျှို့ဝှက်ချက်|အမှန်တရား|ပဟေဠိ|ဖြစ်ရပ်မှန်|သဲလွန်စအဖြေ|revelation|secret revealed|true identity)/iu;
const REVEAL_ACTION = /(ပေါ်လွင်|ဖော်ထုတ်|သိရှိ|ဖွင့်ဟ|သဘောပေါက်|ထုတ်ပြော|သိလိုက်|ဖွင့်ပြ|uncovered|discovered|revealed)/iu;
const CONFLICT = /(တိုက်ခိုက်|ဝိုင်းဝန်း|လိုက်ဖမ်း|ဓားဆွဲ|အနိုင်အရှုံး|ပြင်းထန်စွာရင်ဆိုင်|ချောင်းမြောင်းတိုက်|attacked|ambush|confrontation)/iu;
const TURNING = /(အကြီးအကျယ်|မမျှော်လင့်|အသက်အန္တရာယ်|အသက်လုပြေး|အပြင်းအထန်|နောက်ဆုံးအကြိမ်|ထိတ်လန့်|critical|life.threatening)/iu;
const ENTRANCE = /(ပေါ်လာ|ထွက်ပေါ်|နီးကပ်လာ|ဝင်လာ|ရပ်လိုက်|ထွက်လာ|appeared|approached|entered)/iu;
const MAIN_CHARACTER = /(မိန်းကလေး|ဦးဘသိန်း|ရန်သူ|မင်းသား|မင်းသမီး|အဖြူဝတ်|ဝိညာဉ်|သရဲ|stranger|apparition)/iu;
const DAY = /(နေ့ခင်း|နေ့လယ်|နံနက်|မနက်ခင်း|daytime|morning)/iu;
const NIGHT = /(ညအချိန်|ညဉ့်နက်|ညနေမှောင်|ညမိုးချုပ်|ညအမှောင်|midnight|nightfall)/iu;
const EXPLICIT = /^(?:\s*(?:\[SCENE\]|\[MAJOR SCENE\]|\[ဇာတ်ဝင်ခန်း\]|\*\*\s*SCENE CHANGE))/iu;

/**
 * A new picture is a rare deliberate visual beat, not a word occurrence.
 * Reasons are exposed for review; confidence is NOT a semantic AI score.
 */
export function detectMajorVisualBeat(text, previousText = '', annotations = {}) {
  if (annotations?.majorVisualChange === true) {
    return {score:10, reason:'author-marked major visual transition', kind:'manual-marker'};
  }
  const current = String(text || '').normalize('NFC');
  const previous = String(previousText || '').normalize('NFC');
  if (EXPLICIT.test(current)) {
    return {score:10, reason:'explicit author scene-break marker', kind:'author-marker'};
  }
  if (has(current, ARRIVAL) && has(current, DISTINCT_PLACE)) {
    return {score:8, reason:'clear arrival or departure at a distinct setting', kind:'location-change'};
  }
  if (has(current, SEVERE_WEATHER) && has(current, STRONG_DARKNESS)) {
    return {score:8, reason:'severe weather transforms the main visual atmosphere', kind:'major-mood-shift'};
  }
  if (has(current, REVEAL) && has(current, REVEAL_ACTION)) {
    return {score:8, reason:'central story revelation or mystery resolves', kind:'major-reveal'};
  }
  if (has(current, CONFLICT) && (has(current, TURNING) || has(current, DANGER))) {
    return {score:8, reason:'important confrontation with clear escalation', kind:'major-confrontation'};
  }
  if (has(current, MAIN_CHARACTER) && has(current, ENTRANCE) &&
      has(current, DANGER) && has(current, TURNING)) {
    return {score:7, reason:'character dominates an escalating pivotal event', kind:'major-entrance'};
  }
  if (has(previous, DAY) && has(current, NIGHT) && has(current, STRONG_DARKNESS)) {
    return {score:7, reason:'explicit daytime-to-nighttime atmosphere transition', kind:'time-shift'};
  }
  // Rain, a single character entrance, a dialogue turn, or a camera detail
  // is not a visual scene transition. It must NOT independently select art.
  return {score:0, reason:'ordinary narration detail; keep current background', kind:'hold'};
}

function validateScenes(scenes) {
  if (!Array.isArray(scenes) || !scenes.length || scenes.length > 1000)
    throw Error('An existing scene timeline (1–1000 shots) is required.');
  let expectedStart = 0;
  scenes.forEach((s, i) => {
    const start=Number(s?.start),duration=Number(s?.duration);
    if (!Number.isFinite(start) || !Number.isFinite(duration) ||
        duration < .25 || duration>MAX_RENDER_SCENE_SECONDS ||
        Math.abs(start-expectedStart)>.6)
      throw Error('Unsafe or discontinuous original scene timeline at index '+i);
    expectedStart += duration;
  });
  return expectedStart;
}

/**
 * Merge adjacent unprotected beats unless evidence supports a major switch.
 *
 * Important invariants:
 * - Never move start/duration of manual-timing/confirmed-image scenes.
 * - Never modify the original array or objects.
 * - Never choose a new image that wasn't already attached to a selected beat.
 * - Keep the full original audio timeline (no cuts, no speed changes).
 * - Never automatically approve images, captions, or SRT.
 * - No maximum time limit forces an unnecessary background switch.
 * - 3600s renderer-safe technical segments preserve the exact same picture.
 */
export function consolidateMajorScenes(scenes, options = {}) {
  const total=validateScenes(scenes);
  const minHold=Math.max(20,Math.min(300,Number(options.minHoldSeconds)||75));
  const threshold=7;
  const result=[];
  const decisions=[];
  let held=0,locked=0,major=0,technical=0,lastVisibleChangeStart=0;
  for(let i=0;i<scenes.length;i++){
    const src=scenes[i];
    const beat=detectMajorVisualBeat(src.text,scenes[i-1]?.text,src);
    const next={...src,majorSceneReviewRequired:true};
    if(i===0){
      result.push(next);
      decisions.push({id:src.id,start:src.start,action:'opening-image',reason:'first background',score:0});
      continue;
    }
    const previous=result[result.length-1];
    const isLocked=protect(src)||protect(previous);
    const since=Number(src.start)-lastVisibleChangeStart;
    const allowsSwitch=beat.score>=threshold && (since>=minHold ||
      (beat.score>=9 && since>=20));
    if(isLocked || allowsSwitch) {
      if(isLocked)locked++;else major++;
      if(!isLocked) {
        next.majorSceneReason=beat.reason;
        next.majorSceneKind=beat.kind;
      }
      result.push(next);
      lastVisibleChangeStart=Number(src.start);
      decisions.push({id:src.id,start:src.start,action:isLocked?'preserve-manual':'new-major-background',
        reason:isLocked?'manually locked timing/image':beat.reason,score:beat.score});
    } else if(Number(previous.duration)+Number(src.duration)>MAX_RENDER_SCENE_SECONDS) {
      // Keep one visible photo for the entire passage while creating another
      // internal encoder segment. No invented image or artificial slideshow.
      next.assetId=previous.assetId ?? null;
      next.motion=previous.motion;
      next.imageRequirementId=previous.imageRequirementId ?? null;
      next.imageRequirementText=previous.imageRequirementText || '';
      next.imageMatchStatus=previous.imageMatchStatus;
      next.technicalContinuation=true;
      next.majorSceneReason='same picture; renderer-safe continuation';
      result.push(next);
      technical++;held++;
      decisions.push({id:src.id,start:src.start,action:'continue-same-image',
        reason:'renderer technical split; visual background unchanged',score:0});
    } else {
      // Current shot and original visual choice remain as the background.
      // Unconfirmed alternate assets must not trigger surprise switches.
      previous.duration=+(Number(previous.duration)+Number(src.duration)).toFixed(3);
      previous.text=String(previous.text||'')+'\n'+String(src.text||'');
      previous.majorSceneReviewRequired=true;
      held++;
      decisions.push({id:src.id,start:src.start,action:'hold-image',
        reason:beat.score>=threshold?'major beat too close to previous switch':beat.reason,
        score:beat.score});
    }
  }
  const outputDuration=result.reduce((a,s)=>a+Number(s.duration),0);
  if(Math.abs(outputDuration-total)>.05)
    throw Error('Conservative planning must preserve every narration second.');
  for(let i=1;i<result.length;i++){
    const expected=Number(result[i-1].start)+Number(result[i-1].duration);
    if(Math.abs(result[i].start-expected)>.6)
      throw Error('Conservative planning created an unsafe timestamp gap.');
  }
  for(const source of scenes.filter(protect)) {
    const found=result.find(s=>s.id===source.id);
    if(!found || found.start!==source.start ||
       found.duration!==source.duration || found.assetId!==source.assetId)
      throw Error('A confirmed/manual scene decision would be changed.');
  }
  return {scenes:result,report:{
    originalScenes:scenes.length,majorScenes:result.length-technical,
    renderSegments:result.length,technicalSameImageContinuations:technical,
    heldBoundaries:held,majorSwitches:major,manualBoundariesProtected:locked,
    minimumHoldSeconds:minHold,
    narrationSeconds:+total.toFixed(3),
    timingEvidence:'uses provided chapter timeline; actual audio alignment depends on validated SRT or pause review',
    imagesGenerated:0,automaticImageApproval:false,reviewRequired:true,
    semanticAI:false,offline:true,
    decisions
  }};
}
