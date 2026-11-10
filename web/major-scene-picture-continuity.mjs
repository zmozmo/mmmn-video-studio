/**
 * MMMN Windows 0.15.6 — author-confirmed, offline missing-background guard.
 *
 * NEVER fetches/generates pictures and never adds visual scene boundaries.
 * For an unassigned important scene, it can keep displaying the SAME
 * already-imported verified local picture instead of showing a blank frame.
 * This is not semantic image understanding or an approved new scene picture.
 */
const locked=s=>Boolean(s?.visualLocked||s?.manualLocked||
  s?.alignment==='manual-locked'||s?.imageMatchStatus==='manual-confirmed');
const finite=n=>typeof n==='number'&&Number.isFinite(n);
function verifiedImages(assets){
  if(!Array.isArray(assets)||assets.length>5000)
    throw Error('Invalid local asset metadata');
  const images=new Set(),ids=new Set();
  for(const a of assets){
    if(!a||typeof a.id!=='string'||a.id.length>120||ids.has(a.id))continue;
    ids.add(a.id);
    if(a.nativeStored===true&&typeof a.type==='string'&&
       /^image\/(?:png|jpeg|webp|gif|bmp|svg\+xml)$/i.test(a.type))
      images.add(a.id);
  }
  return images;
}
function checkedScenes(chapter){
  if(chapter?.scenePolicy!=='major-only-conservative')
    throw Error('Run major-only storyboard review first');
  const scenes=chapter.scenes;
  if(!Array.isArray(scenes)||scenes.length<1||scenes.length>1000)
    throw Error('No safe important scene plan');
  let end=0;
  const ids=new Set();
  for(const [i,s] of scenes.entries()){
    if(!s||typeof s.id!=='string'||s.id.length>160||
       ids.has(s.id)||!finite(s.start)||!finite(s.duration)||
       s.start<0||s.duration<.25||s.duration>3600||
       Math.abs(s.start-end)>.6)
      throw Error('Unsafe or discontinuous scene timeline at '+i);
    ids.add(s.id);end=s.start+s.duration;
  }
  return {scenes,seconds:end};
}
function imageId(scene){
  return typeof scene.assetId==='string'&&scene.assetId.length<=120&&scene.assetId?
    scene.assetId:null;
}
export function analyzeMajorScenePictureContinuity(chapter,assets=[]){
  const {scenes,seconds}=checkedScenes(chapter);
  const images=verifiedImages(assets);
  const rows=[];let last=null;
  const count={continuableUnassigned:0,openingMissing:0,manualUnassigned:0,
    unresolvedMissingOrNonlocal:0,unsafeTechnicalMismatches:0,
    technicalContinuations:0,existingImageChoicesPreserved:0,
    currentVisiblePictureChanges:0};
  for(const [i,scene] of scenes.entries()){
    const actual=imageId(scene);
    const protectedChoice=locked(scene);
    const imported=Boolean(actual&&images.has(actual));
    const previouslyVerified=last;
    let status,proposedAssetId=null;
    if(scene.technicalContinuation){
      count.technicalContinuations++;
      // An encoded continuation may NEVER imply a different visual picture.
      if(actual&&previouslyVerified&&actual!==previouslyVerified){
        status='unsafe-technical-image-switch';count.unsafeTechnicalMismatches++;
      }else if(!actual&&!protectedChoice&&previouslyVerified){
        status='carry-same-picture-across-encoder-split';
        proposedAssetId=previouslyVerified;
        count.continuableUnassigned++;
      }else if(actual&&!imported){
        status='technical-image-not-locally-verified';
        count.unresolvedMissingOrNonlocal++;
      }else if(!actual&&protectedChoice){
        status='protected-manual-blank';
        count.manualUnassigned++;
      }else if(!actual){
        status='unresolved-technical-blank';count.unresolvedMissingOrNonlocal++;
      }else{
        status='already-same-picture';count.existingImageChoicesPreserved++;
      }
    }else if(protectedChoice&&!actual){
      status='protected-manual-blank';count.manualUnassigned++;
    }else if(actual){
      // Existing manual/editor selection always takes priority, even if the
      // media file is unavailable. Never silently replace a missing image.
      if(imported){
        status='existing-picture-preserved';count.existingImageChoicesPreserved++;
        if(previouslyVerified&&previouslyVerified!==actual)
          count.currentVisiblePictureChanges++;
      }else{
        status='existing-picture-needs-local-verification';
        count.unresolvedMissingOrNonlocal++;
      }
    }else if(previouslyVerified&&!protectedChoice){
      status='continue-prior-imported-picture';
      proposedAssetId=previouslyVerified;count.continuableUnassigned++;
    }else if(i===0){
      status='opening-image-required';count.openingMissing++;
    }else{
      status='unresolved-missing-picture';count.unresolvedMissingOrNonlocal++;
    }
    // Crucial: a manually locked intentional blank starts a fresh hold; it
    // cannot be filled by a much earlier picture across the lock.
    if(protectedChoice&&!actual)last=null;
    else if(actual)last=imported?actual:null;
    else if(proposedAssetId)last=proposedAssetId;
    else last=null;
    rows.push({sceneId:scene.id,start:scene.start,duration:scene.duration,
      status,existingAssetId:actual,proposedAssetId,
      isTechnicalContinuation:Boolean(scene.technicalContinuation),
      manualProtected:protectedChoice,readOnly:true,approvalRequired:true});
  }
  return {rows,report:{...count,visibleMajorScenes:rows.length-count.technicalContinuations,
    durationSeconds:seconds,changesApplied:0,sceneBoundariesAdded:0,
    assetsCreated:0,imagesDownloaded:0,networkCalls:0,
    canApply:count.unsafeTechnicalMismatches===0&&count.continuableUnassigned>0,
    manualApprovalRequired:true,semanticImageAI:false,offline:true}};
}
export function keepExistingMajorScenePicture(chapter,assets,confirmed){
  if(confirmed!==true)throw Error('Explicit author confirmation required');
  const diagnosis=analyzeMajorScenePictureContinuity(chapter,assets);
  if(diagnosis.report.unsafeTechnicalMismatches)
    throw Error('A technical encoder split unexpectedly changes pictures; review manually');
  const byId=new Map(diagnosis.rows.filter(x=>x.proposedAssetId)
    .map(x=>[x.sceneId,x.proposedAssetId]));
  let kept=0;
  const next=chapter.scenes.map(scene=>{
    const candidate=byId.get(scene.id);
    if(!candidate||locked(scene)||imageId(scene))return {...scene};
    kept++;
    return {...scene,assetId:candidate,
      imageMatchStatus:'same-imported-picture-review',
      localArtworkReviewRequired:true,
      localPhotoContinuity:'same-background-not-new-visual-beat'};
  });
  for(const [i,s] of next.entries()){
    const prior=chapter.scenes[i];
    if(s.start!==prior.start||s.duration!==prior.duration||s.text!==prior.text||
       s.id!==prior.id)throw Error('Narration timing/text must never change');
    if(locked(prior)&&s.assetId!==prior.assetId)
      throw Error('Manual photo/time lock must never change');
  }
  return {scenes:next,continuationsApplied:kept,
    authorMustReview:true,originalsUnchanged:true,
    createdImages:0,addedSceneBoundaries:0,changedTimestamps:0};
}
