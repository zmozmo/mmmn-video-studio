import test from 'node:test';
import assert from 'node:assert/strict';
import {buildMajorArtworkBrief} from '../web/major-artwork-brief.mjs';

const scene=(id,start,duration,text,changes={})=>({
 id,start,duration,text,assetId:null,majorSceneKind:'review-needed',
 majorSceneReason:'major setting or atmosphere',...changes
});
const chapter=(scenes,rest={})=>({
 number:2,title:'ဇာတ်ဝင်ခန်း',scenePolicy:'major-only-conservative',scenes,...rest
});
const art=(id,name)=>({id,name,type:'image/png'});
const run=(scenes,assets=[],opts={})=>buildMajorArtworkBrief(chapter(scenes,opts),assets);

test('only real major visible beats appear in image brief',()=>{
 const rows=run([
  scene('a',0,80,'ရိုးရိုးအကြောင်း'),
  scene('b',80,140,'မိုးသည်း၍ ညနေမှောင်မိုက်သည်။',
    {majorSceneKind:'major-mood-shift'}),
  scene('c',220,100,'သင်္ချိုင်းထဲသို့ ဝင်ရောက်သည်။',
    {majorSceneKind:'location-change'})]);
 assert.equal(rows.majorBeats,3);
 assert.equal(rows.missingPictures,3);
 assert.equal(rows.narrationSeconds,320);
 assert.match(rows.markdown,/MS-02-001.png/);
 assert.match(rows.markdown,/MS-02-003.png/);
});
test('technical continuation is NOT a new image request',()=>{
 const x=run([
  scene('a',0,3600,'စာမူဆက်သွားသည်', {assetId:'p'}),
  scene('b',3600,1800,'စာမူဆက်သွားသည်', {assetId:'p',technicalContinuation:true})
 ],[art('p','main.png')]);
 assert.equal(x.majorBeats,1);
 assert.equal(x.linkedPictures,1);
 assert.equal(x.skippedTechnicalContinuations,1);
 assert.equal(x.narrationSeconds,5400);
 assert.doesNotMatch(x.markdown,/## 2\./);
});
test('existing local photo is reported as linked, not missing',()=>{
 const x=run([scene('a',0,90,'တောအုပ်', {assetId:'p'})],[art('p','forest.png')]);
 assert.equal(x.missingPictures,0);
 assert.equal(x.linkedPictures,1);
 assert.match(x.markdown,/forest.png/);
});
test('phantom asset ID is still flagged missing',()=>{
 const x=run([scene('a',0,90,'တောအုပ်', {assetId:'no-real-file'})]);
 assert.equal(x.missingPictures,1);
 assert.equal(x.rows[0].assignedButMissing,true);
});
test('unrelated video/mp3 assets do not count as pictures',()=>{
 const x=run([scene('a',0,90,'မြို့ဟောင်း', {assetId:'n'})],
 [{id:'n',type:'audio/mpeg',name:'narration.mp3'}]);
 assert.equal(x.missingPictures,1);
});
test('export refuses unapproved ordinary auto draft',()=>{
 assert.throws(()=>buildMajorArtworkBrief({number:1,scenePolicy:'legacy',scenes:[
  scene('a',0,30,'မိုးရွာသည်')]}),/Major-only/);
});
test('gapped timeline rejected instead of fake art plan',()=>{
 assert.throws(()=>run([scene('a',0,20,'a'),scene('b',40,20,'b')]),/Unsafe/);
});
test('overlong native scene rejected and requires renderer split',()=>{
 assert.throws(()=>run([scene('a',0,5400,'long')]),/Unsafe/);
});
test('review prompts do not invent narrator/character attributes',()=>{
 const x=run([scene('a',0,50,'ဦးဘသိန်း သင်္ချိုင်းတွင် အိပ်မက်မက်သည်။')]);
 assert.match(x.markdown,/ဦးဘသိန်း/);
 assert.doesNotMatch(x.markdown,/red-haired|blonde|red dress|royal crown/);
 assert.match(x.markdown,/do not invent new events/);
});
test('manual confirmation flag remains visible but still needs human review',()=>{
 const x=run([scene('a',0,80,'setting',{assetId:'p',imageMatchStatus:'manual-confirmed'})],
 [art('p','chosen.png')]);
 assert.match(x.markdown,/confirmed/);
 assert.equal(x.requiresHumanReview,true);
});
test('read-only generator never modifies supplied chapter or image library',()=>{
 const scenes=[scene('a',0,120,'စာမူ', {assetId:'p'})],assets=[art('p','one.png')];
 const c=chapter(scenes);
 const before=structuredClone({c,assets});
 run(scenes,assets);
 assert.deepEqual({c,assets},before);
});
test('report never claims creating images or contacting Google Drive',()=>{
 const x=run([scene('a',0,90,'test')]);
 assert.equal(x.generatedImages,0);
 assert.equal(x.networkRequests,0);
 assert.match(x.markdown,/does NOT create, upload or download images/);
});
