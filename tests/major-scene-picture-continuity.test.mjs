import test from 'node:test';
import assert from 'node:assert/strict';
import {analyzeMajorScenePictureContinuity as inspect,
 keepExistingMajorScenePicture as keep} from '../web/major-scene-picture-continuity.mjs';
const shot=(id,start,duration,assetId=null,extras={})=>
  ({id,start,duration,text:'မူရင်းဇာတ်ကြောင်းစာသား',assetId,...extras});
const chapter=shots=>({scenePolicy:'major-only-conservative',number:1,
 recordedSeconds:shots.reduce((x,s)=>x+s.duration,0),scenes:shots,
 subtitleCues:[{start:0,end:8,text:'မူရင်းစာသား'}],audioAssetId:'voice-original'});
const pic=(id,nativeStored=true)=>({id,type:'image/png',name:id+'.png',nativeStored});
test('missing major background continues the same already imported photo',()=>{
 const c=chapter([shot('a',0,80,'grave'),shot('b',80,100),shot('c',180,90)]);
 const assets=[pic('grave')],report=inspect(c,assets);
 assert.equal(report.report.continuableUnassigned,2);
 assert.equal(report.report.visibleMajorScenes,3);
 assert.equal(report.report.currentVisiblePictureChanges,0);
 const fixed=keep(c,assets,true);
 assert.deepEqual(fixed.scenes.map(x=>x.assetId),['grave','grave','grave']);
 assert.equal(fixed.createdImages,0);
 assert.equal(fixed.addedSceneBoundaries,0);
 assert.equal(fixed.changedTimestamps,0);
});
test('normal strong new photo is never overwritten by continuity guard',()=>{
 const c=chapter([shot('a',0,80,'grave'),shot('b',80,100,'storm'),
   shot('c',180,90)]);
 const fixed=keep(c,[pic('grave'),pic('storm')],true);
 assert.deepEqual(fixed.scenes.map(s=>s.assetId),['grave','storm','storm']);
 assert.equal(inspect(c,[pic('grave'),pic('storm')]).report.currentVisiblePictureChanges,1);
});
test('manual blank lock is never filled and breaks old photo propagation',()=>{
 const c=chapter([shot('a',0,80,'grave'),
   shot('blank',80,100,null,{visualLocked:true}),
   shot('c',180,90)]);
 const fixed=keep(c,[pic('grave')],true);
 assert.deepEqual(fixed.scenes.map(x=>x.assetId),['grave',null,null]);
 assert.equal(fixed.continuationsApplied,0);
 assert.equal(inspect(c,[pic('grave')]).report.manualUnassigned,1);
});
test('existing manually approved image remains intact despite unavailable media',()=>{
 const c=chapter([shot('a',0,80,'gone',{visualLocked:true}),
   shot('b',80,80)]);
 const result=inspect(c,[pic('other')]);
 assert.equal(result.report.unresolvedMissingOrNonlocal,2); // existing missing photo and following unassigned scene
 assert.equal(keep(c,[pic('other')],true).scenes[0].assetId,'gone');
});
test('never copy a metadata-only unimported image across scenes',()=>{
 const c=chapter([shot('a',0,100,'notNative'),shot('b',100,100)]);
 const r=inspect(c,[pic('notNative',false)]);
 assert.equal(r.report.continuableUnassigned,0);
 assert.equal(r.report.unresolvedMissingOrNonlocal,2);
});
test('no image at opening cannot invent a new image',()=>{
 const c=chapter([shot('a',0,50),shot('b',50,60)]);
 const r=inspect(c,[]);
 assert.equal(r.report.openingMissing,1);
 assert.equal(r.report.continuableUnassigned,0);
});
test('90-minute voice keeps ONE photo through required 3600s encoder split',()=>{
 const c=chapter([shot('a',0,3600,'realPhoto'),
   shot('b',3600,1800,null,{technicalContinuation:true})]);
 const p=inspect(c,[pic('realPhoto')]);
 assert.equal(p.report.durationSeconds,5400);
 assert.equal(p.report.visibleMajorScenes,1);
 assert.equal(p.report.technicalContinuations,1);
 assert.equal(p.rows[1].status,'carry-same-picture-across-encoder-split');
 const applied=keep(c,[pic('realPhoto')],true);
 assert.deepEqual(applied.scenes.map(x=>x.assetId),['realPhoto','realPhoto']);
 assert.deepEqual(applied.scenes.map(x=>x.duration),[3600,1800]);
});
test('wrong second asset in technical same-image continuation must fail closed',()=>{
 const c=chapter([shot('a',0,3600,'a'),
   shot('b',3600,100,'b',{technicalContinuation:true})]);
 const r=inspect(c,[pic('a'),pic('b')]);
 assert.equal(r.report.unsafeTechnicalMismatches,1);
 assert.equal(r.report.canApply,false);
 assert.throws(()=>keep(c,[pic('a'),pic('b')],true),/technical encoder split/);
});
test('no approval means NO change',()=>{
 const c=chapter([shot('a',0,100,'a'),shot('b',100,100)]);
 assert.throws(()=>keep(c,[pic('a')],false),/confirmation/);
});
test('all original media, cues and timelines remain untouched',()=>{
 const c=chapter([shot('a',0,90,'a'),shot('b',90,50)]),
  files=[pic('a')],before=structuredClone({c,files});
 const r=keep(c,files,true);
 assert.deepEqual({c,files},before);
 assert.equal(r.scenes[1].text,c.scenes[1].text);
 assert.deepEqual(r.scenes.map(s=>s.start),[0,90]);
 assert.equal(r.scenes[1].imageMatchStatus,'same-imported-picture-review');
 assert.equal(r.authorMustReview,true);
});
test('repeat operation has no further changes (idempotent)',()=>{
 const c=chapter([shot('a',0,80,'a'),shot('b',80,80)]);
 const first=keep(c,[pic('a')],true);
 const next=keep({...c,scenes:first.scenes},[pic('a')],true);
 assert.equal(next.continuationsApplied,0);
 assert.deepEqual(next.scenes,first.scenes);
});
test('unsafe timeline, NaN, duration, duplicate IDs all refuse',()=>{
 const c=chapter([shot('a',0,90,'a'),shot('a',90,90)]);
 assert.throws(()=>inspect(c,[pic('a')]),/Unsafe/);
 assert.throws(()=>inspect(chapter([shot('a',20,20)]),[]),/Unsafe/);
 assert.throws(()=>inspect(chapter([shot('a',0,4000)]),[]),/Unsafe/);
 assert.throws(()=>inspect(chapter([shot('a',0,NaN)]),[]),/Unsafe/);
});
test('legacy storyboard cannot receive automated image repair',()=>{
 const c=chapter([shot('a',0,80,'a')]);c.scenePolicy='legacy';
 assert.throws(()=>inspect(c,[pic('a')]),/major-only/i);
});
test('audio and video are NOT valid imported images even if marked native',()=>{
 const c=chapter([shot('a',0,90,'bad'),shot('b',90,90)]);
 const r=inspect(c,[{id:'bad',type:'video/mp4',nativeStored:true}]);
 assert.equal(r.report.continuableUnassigned,0);
});
test('read-only inspection has zero network, creation or storage mutations',()=>{
 const c=chapter([shot('a',0,100,'a'),shot('b',100,100)]);
 const before=structuredClone(c);
 const r=inspect(c,[pic('a')]);
 assert.deepEqual(c,before);
 assert.equal(r.report.networkCalls,0);
 assert.equal(r.report.assetsCreated,0);
 assert.equal(r.report.changesApplied,0);
 assert.equal(r.report.manualApprovalRequired,true);
});
test('a lost standalone picture does not silently fall back to an old image',()=>{
 const c=chapter([shot('a',0,80,'good'),shot('b',80,80,'missing'),
   shot('c',160,80)]);
 const fixed=keep(c,[pic('good')],true);
 assert.deepEqual(fixed.scenes.map(x=>x.assetId),['good','missing',null]);
});
