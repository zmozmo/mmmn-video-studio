/**
 * MMMN: conservative, 100%-offline matching of EXISTING imported pictures
 * to already-approved MAJOR scene boundaries based on author-supplied labels.
 *
 * This is not AI image recognition, image generation or web scraping.
 * Does NOT create new scene boundaries or interpret arbitrary brief mentions.
 * Manual image/timing locks and previously linked art are never changed.
 */
const GROUPS=[
 ['graveyard',true,/သင်္ချိုင်း|cemetery|graveyard/iu],
 ['old-village',true,/ရွာဟောင်း|ရွာပျက်|abandoned.village|old.village/iu],
 ['cave',true,/လှိုဏ်ဂူ|ဂူထဲ|ဂူဝ|cave|cavern/iu],
 ['forest',true,/တောအုပ်|သစ်တော|forest|jungle/iu],
 ['temple',true,/ဘုရား|စေတီ|temple|pagoda|shrine/iu],
 ['old-house',true,/အိမ်အို|အိမ်ဟောင်း|old.house|abandoned.house/iu],
 ['river',true,/မြစ်|ချောင်းကမ်း|river|stream/iu],
 ['mountains',true,/တောင်ကြော|တောင်တန်း|mountain|ridge/iu],
 ['storm',false,/မိုးသည်း|မုန်တိုင်း|storm|downpour|thunderstorm/iu],
 ['darkness',false,/ညနေမှောင်|မှောင်မိုက်|အမှောင်ဖုံး|darkness|pitch.dark|nightfall/iu],
 ['morning',false,/နံနက်|မနက်ခင်း|morning|sunrise/iu],
 ['fog',false,/မြူဆိုင်း|မြူနှင်း|fog|mist/iu]
];
const marked=s=>!!(s?.visualLocked||s?.manualLocked||
  s?.alignment==='manual-locked'||s?.imageMatchStatus==='manual-confirmed');
const tagged=text=>new Set(GROUPS.filter(x=>x[2].test(String(text??'').normalize('NFC'))).map(x=>x[0]));
const specific=new Set(GROUPS.filter(x=>x[1]).map(x=>x[0]));
function safe(chapter,assets){
 if(chapter?.scenePolicy!=='major-only-conservative')throw Error('Major-only storyboard must be reviewed first');
 if(!Array.isArray(chapter.scenes)||chapter.scenes.length<1||chapter.scenes.length>1000)
  throw Error('Unsafe or missing important-scene plan');
 if(!Array.isArray(assets)||assets.length>5000)throw Error('Unsafe or missing local image asset metadata');
 let end=0;
 for(const s of chapter.scenes){
  if(typeof s?.start!=='number'||typeof s?.duration!=='number'||
   !Number.isFinite(s.start)||!Number.isFinite(s.duration)||
   s.start<0||s.duration<.25||s.duration>3600||Math.abs(s.start-end)>.6)
   throw Error('Unsafe/discontinuous original storyboard');
  end=s.start+s.duration;
 }
 return end;
}
function bestImage(scene,images){
 const sceneText=[scene.imageRequirementText,scene.text,
   scene.title].filter(Boolean).join(' ');
 const sceneTags=tagged(sceneText);
 const options=[];
 for(const a of images){
  const assetTags=tagged([a.name,a.description,
   ...(Array.isArray(a.tags)?a.tags:[])].filter(Boolean).join(' '));
  const common=[...sceneTags].filter(t=>assetTags.has(t));
  if(!common.some(t=>specific.has(t)))continue;
  const score=common.reduce((n,t)=>n+(specific.has(t)?4:2),0);
  if(score<4)continue;
  options.push({assetId:a.id,name:String(a.name||'').slice(0,130),
    score,labels:common});
 }
 options.sort((a,b)=>b.score-a.score||a.assetId.localeCompare(b.assetId));
 if(!options.length)return {status:'no-grounded-local-image'};
 if(options.length>1&&options[0].score-options[1].score<3)
  return {status:'ambiguous-image-labels',possible:options.length};
 return {status:'unique-local-label-match',assetId:options[0].assetId,
  assetName:options[0].name,labels:options[0].labels,
  score:options[0].score};
}
export function proposeLocalMajorArtwork(chapter,assets){
 const seconds=safe(chapter,assets);
 const seen=new Set(),images=[];
 for(const a of assets){
  if(!a||typeof a.id!=='string'||a.id.length>120||
     !String(a.type||'').startsWith('image/')||seen.has(a.id))continue;
  seen.add(a.id);images.push(a);
 }
 const rows=[];let candidates=0,kept=0,ambiguous=0,missing=0,continuations=0;
 for(const sc of chapter.scenes){
  if(sc.technicalContinuation){continuations++;continue;}
  let outcome;
  if(sc.assetId||marked(sc)){
   outcome={status:'existing-or-locked-picture'};
   kept++;
  }else{
   outcome=bestImage(sc,images);
   if(outcome.status==='unique-local-label-match')candidates++;
   else if(outcome.status==='ambiguous-image-labels')ambiguous++;
   else missing++;
  }
  rows.push({sceneId:sc.id,start:sc.start,
    currentAssetId:sc.assetId??null,match:outcome,
    authorApprovalRequired:true,readonly:true});
 }
 return {rows,report:{
  visibleMajorScenes:rows.length,
  existingOrLockedImagesKept:kept,
  uniqueLabelCandidates:candidates,
  ambiguousCandidates:ambiguous,
  missingPictures:missing,
  technicalSamePhotoContinuations:continuations,
  narrationSeconds:seconds,
  originalScenesChanged:0,
  picturesDownloaded:0,picturesGenerated:0,networkCalls:0,
  automaticImageApproval:false,requiresHumanReview:true,offline:true
 }};
}
export function applyConfirmedLocalMajorArtwork(chapter,assets,approved){
 if(approved!==true)throw Error('Explicit author confirmation is required before any image choice');
 const proposal=proposeLocalMajorArtwork(chapter,assets);
 const byScene=new Map(proposal.rows.filter(r=>r.match.status==='unique-local-label-match')
  .map(r=>[r.sceneId,r.match.assetId]));
 let selected=0,lastPhoto=null;
 const next=chapter.scenes.map(scene=>{
  if(scene.technicalContinuation){
   // Renderer-only continuation retains same already-visible image.
   return !marked(scene)&&!scene.assetId&&lastPhoto?
    {...scene,assetId:lastPhoto,imageMatchStatus:'suggested-review'}:{...scene};
  }
  if(scene.assetId||marked(scene)){
   lastPhoto=scene.assetId??null;
   return {...scene};
  }
  const image=byScene.get(scene.id);
  if(!image){lastPhoto=scene.assetId??null;return {...scene};}
  selected++;lastPhoto=image;
  return {...scene,assetId:image,imageMatchStatus:'suggested-review',
    localArtworkReviewRequired:true,localMatchBasis:'imported-picture-name-and-tags'};
 });
 return {scenes:next,appliedCandidates:selected,
  imagesApprovedAutomatically:0,authorMustReview:true,
  originalsUnchanged:true,newSceneBoundaries:0};
}
