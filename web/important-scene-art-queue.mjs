/**
 * MMMN 0.15.7 — private offline proposed image-generation queue, NOT generator.
 *
 * Never expands the visual scene count. Only previously planned *important*
 * narrative changes with missing images can become review requests. Manual
 * author confirmation is required before a local engine receives any text.
 * Ordinary rain/arrivals/dialogue stay on their existing background.
 */
const changed = new Set([
 'location-change','major-mood-shift','major-reveal',
 'major-confrontation','major-entrance','time-shift',
 'manual-marker','author-marker'
]);
const locks = s=>Boolean(s?.visualLocked||s?.manualLocked||
 s?.alignment==='manual-locked'||s?.imageMatchStatus==='manual-confirmed'||
 s?.imageMatchStatus==='manual-review');
const clean=v=>Array.from(String(v??'').normalize('NFC')
 .replace(/[\x00-\x1f\x7f]/gu,' ').replace(/\s+/gu,' ').trim()).slice(0,320).join('');
function verifiedPlan(chapter,assets) {
 if(chapter?.scenePolicy!=='major-only-conservative')
  throw Error('Only a reviewed conservative important-scene plan is supported');
 if(!Array.isArray(chapter.scenes)||chapter.scenes.length<1||chapter.scenes.length>1000)
  throw Error('No valid important-scene timeline');
 if(!Array.isArray(assets)||assets.length>5000)
  throw Error('Invalid private media library');
 let end=0;const sceneIds=new Set();
 for(const s of chapter.scenes){
  if(!s||typeof s.id!=='string'||s.id.length>64||
    !/^[A-Za-z0-9_-]+$/.test(s.id)||sceneIds.has(s.id)||
    typeof s.start!=='number'||typeof s.duration!=='number'||
    !Number.isFinite(s.start)||!Number.isFinite(s.duration)||
    s.start<0||s.duration<.25||s.duration>3600||
    Math.abs(s.start-end)>.6)
    throw Error('Unsafe or non-monotonic scene timeline');
  sceneIds.add(s.id);end=s.start+s.duration;
 }
 const ids=new Set();
 for(const a of assets){
  if(typeof a?.id!=='string'||a.id.length>120||ids.has(a.id))
   throw Error('Invalid or duplicated media asset identifier');
  ids.add(a.id);
 }
 return end;
}
/**
 * Local preview ONLY. No image model calls, writes, automatic approvals or
 * time shifts. This intentionally returns unresolved beats, not fake art.
 */
export function proposePrivateMajorArtQueue(chapter,assets=[],opts={}) {
 const seconds=verifiedPlan(chapter,assets);
 const maxCandidates=opts.maxCandidates??12;
 if(!Number.isInteger(maxCandidates)||maxCandidates<1||maxCandidates>24)
  throw Error('Private art queue must cap new artwork to 1–24 important beats');
 const ids=new Set(assets.filter(a=>a.nativeStored===true&&
  /^image\/(?:png|jpeg|webp|bmp)$/i.test(a.type||'')).map(a=>a.id));
 const rows=[];
 const summary={visibleScenes:0,alreadyLinkedOrLocked:0,
  ordinaryBeatHolds:0,technicalSameImageHolds:0,
  missingImportantImages:0,eligibleLocalArtRequests:0,
  overflowImportantBeats:0,sceneTimesChanged:0,
  automaticNetworkRequests:0,automaticImageGenerations:0,
  automaticImageApprovals:0,originalAssetsModified:0,
  privateReviewOnly:true};
 for(const s of chapter.scenes){
  if(s.technicalContinuation){summary.technicalSameImageHolds++;continue;}
  summary.visibleScenes++;
  const linked=typeof s.assetId==='string'&&s.assetId!=='';
  if(linked||locks(s)){
   summary.alreadyLinkedOrLocked++;
   rows.push({sceneId:s.id,status:linked&&!ids.has(s.assetId)?
    'preserve-existing-unavailable-media':'preserve-author-decision',
    userApprovalRequired:false,proposedPrompt:null});
   continue;
  }
  if(!changed.has(s.majorSceneKind)){
   summary.ordinaryBeatHolds++;
   rows.push({sceneId:s.id,status:'hold-current-background',
    userApprovalRequired:false,proposedPrompt:null});
   continue;
  }
  summary.missingImportantImages++;
  if(summary.eligibleLocalArtRequests>=maxCandidates){
   summary.overflowImportantBeats++;
   rows.push({sceneId:s.id,status:'queue-limit-review-later',
    userApprovalRequired:true,proposedPrompt:null});
   continue;
  }
  const phrase=clean(s.imageRequirementText||s.text||'');
  // No ungrounded auto-invented visual prompts and no private source upload.
  if(phrase.length<18){
   rows.push({sceneId:s.id,status:'not-enough-authored-visual-evidence',
    userApprovalRequired:true,proposedPrompt:null});
   continue;
  }
  summary.eligibleLocalArtRequests++;
  rows.push({sceneId:s.id,status:'private-local-generation-review',
   sceneStart:s.start,sceneDuration:s.duration,
   reason:clean(s.majorSceneReason||s.majorSceneKind),
   proposedPrompt:'Myanmar historical novel background, cinematic 16:9 composition; '+
     'only depict what this scene explicitly describes: '+phrase+
     '; no text, captions, logos or watermarks.',
   userApprovalRequired:true,
   engineRequestSubmitted:false,
   imageApproved:false});
 }
 return {rows,summary,seconds,networkCalls:0,mediaWrites:0,
  chaptersMutated:false,automaticallyGeneratedImages:0};
}
