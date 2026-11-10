import test from 'node:test';
import assert from 'node:assert/strict';
import {proposePrivateMajorArtQueue as run} from '../web/important-scene-art-queue.mjs';
const draft=(o={})=>({scenePolicy:'major-only-conservative',scenes:[
 {id:'scene_1',start:0,duration:100,majorSceneKind:'manual-marker',
  text:'သင်္ချိုင်းက ရွာဟောင်းတံခါးနားတွင် အမှောင်ထုကို အနည်းငယ် မြင်ရသည်။'},
 {id:'scene_2',start:100,duration:100,majorSceneKind:'hold',
  text:'မိုးရွာနေတယ်လို့ အနည်းငယ်ပြောသော်လည်း နောက်ခံမပြောင်းပါ။'},
 {id:'scene_3',start:200,duration:100,majorSceneKind:'major-mood-shift',
  text:'မိုးသည်းထန်သည်နှင့် ညနေမှောင်သွားသော သင်္ချိုင်းမြင်ကွင်း။'}
],...o});
test('only significant missing images reach local review queue',()=>{
 const r=run(draft());
 assert.equal(r.summary.visibleScenes,3);
 assert.equal(r.summary.eligibleLocalArtRequests,2);
 assert.equal(r.summary.ordinaryBeatHolds,1);
 assert.equal(r.summary.automaticNetworkRequests,0);
 assert.equal(r.summary.automaticImageGenerations,0);
 assert.equal(r.rows[1].proposedPrompt,null);
});
test('locked scene remains unchanged and receives no generation prompt',()=>{
 const c=draft();c.scenes[2].visualLocked=true;c.scenes[2].assetId=null;
 const prev=structuredClone(c);
 const r=run(c);
 assert.equal(r.rows[2].status,'preserve-author-decision');
 assert.deepEqual(c,prev);
});
test('previously assigned local or missing media is never overwritten',()=>{
 const c=draft();c.scenes[0].assetId='original_author_photo';
 const r=run(c,[]);
 assert.equal(r.rows[0].status,'preserve-existing-unavailable-media');
 assert.equal(r.rows[0].proposedPrompt,null);
});
test('renderer technical continuation is never a new image',()=>{
 const c=draft();
 c.scenes[1].technicalContinuation=true;
 assert.equal(run(c).summary.technicalSameImageHolds,1);
});
test('explicit author wording required; no invented story content',()=>{
 const c=draft();c.scenes[0].text='မိုး';
 const r=run(c);
 assert.equal(r.rows[0].status,'not-enough-authored-visual-evidence');
 assert.equal(r.rows[0].proposedPrompt,null);
});
test('cap stops runaway photo generation on huge chapters',()=>{
 const many=Array.from({length:30},(_,i)=>({
 id:'major_'+i,start:i*10,duration:10,majorSceneKind:'location-change',
 text:'ထူးခြားသောမြို့ဟောင်းသို့ ဝင်ရောက်ပြီး အလွန်ကြီးမားသောအရာကို တွေ့လိုက်သည်။'
 }));
 const r=run(draft({scenes:many}),[],{maxCandidates:3});
 assert.equal(r.summary.eligibleLocalArtRequests,3);
 assert.equal(r.summary.overflowImportantBeats,27);
 assert.equal(r.summary.automaticImageGenerations,0);
});
test('reject abusive or malformed scene identifier and timestamps',()=>{
 const c=draft();c.scenes[1].id='../private';
 assert.throws(()=>run(c),/Unsafe/);
 c.scenes[1].id='safe';c.scenes[1].start=150;
 assert.throws(()=>run(c),/Unsafe/);
});
test('duplicate media identifiers are fail closed',()=>{
 assert.throws(()=>run(draft(),[{id:'x'},{id:'x'}]),/duplicated/);
});
test('no reviewed major-only plan rejects unrelated automatic slideshow',()=>{
 assert.throws(()=>run(draft({scenePolicy:'ordinary-auto'})),/conservative/);
});
test('local-only image output queue preserves source and manual timing locks',()=>{
 const c=draft(),before=JSON.stringify(c);
 const q=run(c);assert.equal(q.mediaWrites,0);
 assert.equal(q.chaptersMutated,false);
 assert.equal(JSON.stringify(c),before);
 assert.ok(q.rows[0].proposedPrompt.includes('only depict'));
});
test('invalid limits refused',()=>{
 assert.throws(()=>run(draft(),[],{maxCandidates:1000}),/cap/);
});
