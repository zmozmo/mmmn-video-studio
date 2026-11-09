import test from 'node:test';
import assert from 'node:assert/strict';
import {consolidateMajorScenes,detectMajorVisualBeat} from '../web/major-scene.mjs';

const mk=(parts,seconds=80)=>parts.map((text,i)=>({
  id:'scene-'+i,text,title:'Scene '+(i+1),start:i*seconds,duration:seconds,
  assetId:'photo-'+i,imageMatchStatus:'suggested-review',alignment:'estimated'
}));
const compact=(x,opts)=>consolidateMajorScenes(x,opts);

test('mere rain and new girl mentions NEVER rotate images',()=>{
  const a=mk(['ရွာကနေ့လယ်ခင်း။','မိုးရွာလာသည်။','မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။','ဇာတ်ကောင်နှစ်ယောက် စကားပြောကြသည်။']);
  const out=compact(a);
  assert.equal(out.scenes.length,1);
  assert.equal(out.scenes[0].assetId,'photo-0');
  assert.equal(out.scenes[0].duration,320);
  assert.equal(out.report.heldBoundaries,3);
  assert.equal(out.report.imagesGenerated,0);
});
test('intense rain AND thick darkness justify ONE major atmospheric change',()=>{
  const a=mk(['သာမန်နေ့လယ်','မိုးသည်းထန်လာပြီး ညနေမှောင်မိုက်ကာ လမ်းမမြင်ရတော့။','မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။']);
  const out=compact(a);
  assert.equal(out.scenes.length,2);
  assert.deepEqual(out.scenes.map(x=>x.start),[0,80]);
  assert.deepEqual(out.scenes.map(x=>x.duration),[80,160]);
  assert.equal(out.scenes[1].majorSceneKind,'major-mood-shift');
});
test('new character alone is not an image switch',()=>{
  const a=mk(['အိမ်နောက်မှာ ထိုင်နေကြသည်။','အဖြူဝတ်မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။']);
  assert.equal(compact(a).scenes.length,1);
});
test('explicit arrival at a different major location is a change',()=>{
  const a=mk(['အိမ်ထဲတွင် နေကြသည်။','ဦးဘသိန်းက ရွာဟောင်းအနီးရှိ သင်္ချိုင်းထဲသို့ ဝင်ရောက်လာသည်။']);
  const out=compact(a);
  assert.equal(out.scenes.length,2);
  assert.equal(out.scenes[1].majorSceneKind,'location-change');
});
test('location mention without travel or arrival does not cause a change',()=>{
  assert.equal(compact(mk(['သူ ထိုင်နေသည်။','သူက တောအုပ်အကြောင်း ပြောပြသည်။'])).scenes.length,1);
});
test('big plot secret REVEALED triggers change, secret mention alone does not',()=>{
  const plain=mk(['မနက်ခင်း','သူက လျှို့ဝှက်ချက်အကြောင်း ပြောသည်။']);
  assert.equal(compact(plain).scenes.length,1);
  const major=mk(['မနက်ခင်း','နှစ်ပေါင်းများစွာ ဖုံးကွယ်ထားတဲ့ လျှို့ဝှက်ချက်ကို ဖော်ထုတ်လိုက်သည်။']);
  assert.equal(compact(major).scenes[1].majorSceneKind,'major-reveal');
});
test('dangerous climax confrontation can trigger',()=>{
  const a=mk(['တိတ်ဆိတ်နေ၏။','ရန်သူတို့ ဝိုင်းဝန်းတိုက်ခိုက်ပြီး အသက်အန္တရာယ် ကျရောက်လာသည်။']);
  assert.equal(compact(a).scenes[1].majorSceneKind,'major-confrontation');
});
test('a major beat shortly after another is held, not flickered',()=>{
  const a=[
    {id:'1',start:0,duration:20,text:'အိမ်၌။',assetId:'a'},
    {id:'2',start:20,duration:30,text:'သင်္ချိုင်းထဲသို့ ဝင်ရောက်သွားသည်။',assetId:'b'},
    {id:'3',start:50,duration:50,text:'မိုးသည်းထန်စွာရွာပြီး ညနေမှောင်မိုက်သည်။',assetId:'c'}
  ];
  const out=compact(a);
  assert.equal(out.scenes.length,1);
  assert.equal(out.scenes[0].duration,100);
});
test('minimum hold cannot force periodic switching in quiet long-form narration',()=>{
  const a=mk(Array(30).fill('အခြေအနေက မပြောင်းလဲဘဲ စကားပြောဆိုမှုသာ ဆက်သွားသည်။'),100);
  assert.equal(compact(a).scenes.length,1);
});
test('author-marked major beat overrides cooldown after 20 seconds only',()=>{
  const a=[{id:'0',start:0,duration:25,text:'စာမူအစ။'},
    {id:'1',start:25,duration:15,text:'[SCENE] အထူးနေရာ။',assetId:'x'}];
  const result=compact(a);
  assert.equal(result.scenes.length,2);
  assert.equal(result.scenes[1].majorSceneKind,'author-marker');
});
test('manual timing lock keeps precise start, duration and asset assignment',()=>{
  const a=mk(['စကားပြောနေကြသည်။','မိုးရွာလာသည်။','မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။'],60);
  a[1]={...a[1],alignment:'manual-locked',imageMatchStatus:'manual-confirmed',visualLocked:true};
  const input=structuredClone(a);
  const out=compact(a);
  assert.deepEqual(a,input,'planner must NOT mutate originals');
  assert.equal(out.scenes.length,3);
  assert.equal(out.scenes[1].start,60);
  assert.equal(out.scenes[1].duration,60);
  assert.equal(out.scenes[1].assetId,'photo-1');
  assert.ok(out.report.manualBoundariesProtected>=1);
});
test('confirmed image remains protected even on ordinary mention',()=>{
  const a=mk(['အိမ်၌။','မိုးရွာသည်။'],90);
  a[1].imageMatchStatus='manual-confirmed';
  assert.equal(compact(a).scenes.length,2);
});
test('no images means no hallucinated image ID',()=>{
  const a=mk(['တိတ်ဆိတ်သည်။','အိမ်အိုထဲသို့ ဝင်ရောက်သည်။'],100).map(x=>({...x,assetId:null}));
  const out=compact(a);
  assert.equal(out.scenes.length,2);
  assert.equal(out.scenes[0].assetId,null);
  assert.equal(out.scenes[1].assetId,null);
});
test('unsafe noncontiguous timestamps must fail closed',()=>{
  assert.throws(()=>compact([{id:'1',start:0,duration:50},{id:'2',start:70,duration:15}]),/discontinuous/);
});
test('nan/negative timeline must fail closed',()=>{
  assert.throws(()=>compact([{id:'1',start:0,duration:-1}]),/Unsafe/);
});
test('full narration duration is preserved, starts stay monotonic',()=>{
  const a=mk(['မနက်ခင်း','မိုးသည်းထန်၍ ညနေမှောင်မိုက်သည်။','မိန်းကလေး ပေါ်လာသည်။',
    'အိမ်ထဲကနေ တောအုပ်သို့ ရောက်ရှိလာသည်။','သူတို့ ဆက်လက်စကားပြောကြသည်။'],100);
  const result=compact(a);
  const total=result.scenes.reduce((n,s)=>n+s.duration,0);
  assert.equal(total,500);
  for(let i=1;i<result.scenes.length;i++)assert.equal(result.scenes[i].start,
    result.scenes[i-1].start+result.scenes[i-1].duration);
  assert.equal(result.report.narrationSeconds,500);
});
test('output explicitly remains unapproved and does not claim semantic AI/transcription',()=>{
  const out=compact(mk(['မိုးရွာလာသည်။','မိုးသည်းထန်၍ ညနေမှောင်မိုက်လာသည်။']));
  assert.equal(out.report.automaticImageApproval,false);
  assert.equal(out.report.semanticAI,false);
  assert.equal(out.report.offline,true);
  assert.equal(out.report.reviewRequired,true);
});
