import test from 'node:test';
import assert from 'node:assert/strict';
import {proposeLocalMajorArtwork as propose,
 applyConfirmedLocalMajorArtwork as apply} from '../web/local-major-artwork-match.mjs';
const scene=(id,start,duration,text,extra={})=>({id,start,duration,text,
 assetId:null,...extra});
const chapter=(scenes,extra={})=>({scenePolicy:'major-only-conservative',scenes,...extra});
const art=(id,name)=>({id,name,type:'image/png',nativeStored:true});
test('one existing graveyard picture can be proposed for one actual major scene',()=>{
 const c=chapter([scene('a',0,90,'သင်္ချိုင်းထဲသို့ ဝင်ရောက်ကြသည်။')]);
 const p=propose(c,[art('cem','သင်္ချိုင်း_ည.png')]);
 assert.equal(p.report.uniqueLabelCandidates,1);
 assert.equal(p.rows[0].match.assetId,'cem');
 assert.equal(p.report.originalScenesChanged,0);
});
test('rain mention alone never chooses or switches an image',()=>{
 const p=propose(chapter([scene('a',0,150,'မိုးရွာနေသည်။')]),[art('r','rain.png')]);
 assert.equal(p.report.uniqueLabelCandidates,0);
});
test('two equal local cemetery photographs are ambiguous',()=>{
 const p=propose(chapter([scene('a',0,90,'သင်္ချိုင်းဝင်ပေါက်')]),
 [art('p1','graveyard-first.png'),art('p2','graveyard-second.png')]);
 assert.equal(p.report.ambiguousCandidates,1);
 assert.equal(p.report.uniqueLabelCandidates,0);
});
test('already assigned art is NEVER overwritten even when labels disagree',()=>{
 const c=chapter([scene('a',0,70,'သင်္ချိုင်းဝင်ပေါက်',{assetId:'authorChoice'})]);
 const r=apply(c,[art('photo','graveyard.png')],true);
 assert.equal(r.scenes[0].assetId,'authorChoice');
 assert.equal(r.appliedCandidates,0);
});
test('manual lock protects image and time',()=>{
 const c=chapter([scene('a',0,90,'သင်္ချိုင်းအနီး',{visualLocked:true})]);
 const r=apply(c,[art('s','graveyard.png')],true);
 assert.equal(r.scenes[0].assetId,null);
 assert.equal(r.scenes[0].start,0);
});
test('requires explicit author confirmation, never silently assigning a photo',()=>{
 const c=chapter([scene('a',0,90,'သင်္ချိုင်းအနီး')]);
 assert.throws(()=>apply(c,[art('s','graveyard.png')],false),/confirmation/);
});
test('confirmed proposal stays suggestion, never falsely mark photo manually approved',()=>{
 const c=chapter([scene('a',0,90,'သင်္ချိုင်းအနီး')]);
 const r=apply(c,[art('s','graveyard.png')],true);
 assert.equal(r.scenes[0].imageMatchStatus,'suggested-review');
 assert.equal(r.imagesApprovedAutomatically,0);
 assert.equal(r.authorMustReview,true);
});
test('same photo continues across technical renderer segment after matching',()=>{
 const c=chapter([scene('a',0,3600,'သင်္ချိုင်းထဲရှိ လူများ'),
  scene('b',3600,1800,'ဇာတ်လမ်းဆက်သည်',{technicalContinuation:true})]);
 const r=apply(c,[art('x','graveyard.jpg')],true);
 assert.equal(r.scenes[0].assetId,'x');
 assert.equal(r.scenes[1].assetId,'x');
 assert.equal(r.newSceneBoundaries,0);
});
test('unapproved ordinary storyboard cannot receive local automatic image selection',()=>{
 assert.throws(()=>propose(chapter([scene('a',0,90,'သင်္ချိုင်း')],{scenePolicy:'legacy'}),[]),/Major-only/);
});
test('refuse broken timestamp gaps instead of assigning an image',()=>{
 const c=chapter([scene('a',0,60,'သင်္ချိုင်း'),scene('b',120,60,'တောအုပ်')]);
 assert.throws(()=>propose(c,[art('x','graveyard.png')]),/discontinuous/);
});
test('original chapter and original user artwork metadata never mutate',()=>{
 const c=chapter([scene('a',0,120,'ရွာဟောင်းသို့ရောက်ရှိ')]);
 const imgs=[art('v','old village.png')];
 const before=structuredClone({c,imgs});
 propose(c,imgs);apply(c,imgs,true);
 assert.deepEqual({c,imgs},before);
});
test('video/audio assets cannot be guessed as an imported picture',()=>{
 const c=chapter([scene('a',0,75,'ရွာဟောင်း')]);
 const p=propose(c,[{id:'v',type:'video/mp4',name:'old village.mp4'},
  {id:'aud',type:'audio/mpeg',name:'old village.mp3'}]);
 assert.equal(p.report.uniqueLabelCandidates,0);
});
test('ordinary character entrance inside scene is not a new scene boundary',()=>{
 const c=chapter([scene('a',0,80,'သင်္ချိုင်း'),
   scene('b',80,120,'မိန်းကလေး ပေါ်လာပြီး စကားပြောသည်။')]);
 const p=propose(c,[art('g','graveyard.png')]);
 assert.equal(p.report.uniqueLabelCandidates,1);
 assert.equal(p.report.visibleMajorScenes,2);
 assert.equal(p.report.picturesGenerated,0);
});
test('no network requests or fabricated image files',()=>{
 const p=propose(chapter([scene('a',0,70,'တောအုပ်')]),[art('f','forest.png')]);
 assert.equal(p.report.networkCalls,0);
 assert.equal(p.report.picturesDownloaded,0);
 assert.equal(p.report.picturesGenerated,0);
});

test('metadata-only picture without verified native import is not auto-selected',()=>{
 const c=chapter([scene('a',0,100,'သင်္ချိုင်းလမ်းကို ရောက်ရှိ')]);
 const p=propose(c,[{id:'not-uploaded',name:'graveyard.png',type:'image/png',nativeStored:false}]);
 assert.equal(p.report.uniqueLabelCandidates,0);
 assert.equal(p.report.missingPictures,1);
});
test('media marked as nativeStored with manual photo lock stays protected',()=>{
 const c=chapter([scene('a',0,75,'သင်္ချိုင်းအဝင်',{assetId:'manual-photo',visualLocked:true})]);
 const p=propose(c,[art('other','graveyard.png')]);
 assert.equal(p.report.uniqueLabelCandidates,0);
});
