import test from 'node:test';
import assert from 'node:assert/strict';
import {assessBurmeseTranscript} from '../web/burmese-transcript-agreement.mjs';

const book='ဦးဘသိန်းသည် ရွာဟောင်းသို့ သွားရောက်ပြီး သင်္ချိုင်းအနီးတွင် ရပ်နေသည်။ ထိုညတွင် မိုးအလွန်သည်းထန်စွာ ရွာသွန်းပြီး ကောင်းကင်တစ်ခုလုံး မှောင်မိုက်လာသည်။ သူ့နောက်က ခြေသံအနည်းငယ် ကြားလိုက်ရသောအခါ ဘယ်သူလဲဟု မေးလိုက်သည်။ လျှို့ဝှက်ချက်တစ်ခုကို သတိထားမိပြီး မယ်တော်နတ်ကွန်းဆီသို့ တဖြည်းဖြည်း လျှောက်သွားသည်။';
const cues=(text)=>[{start:0,end:7,text},{start:7,end:14,text},{start:14,end:21,text}];

test('strong agreement still NEVER auto-approves a generated transcript',()=>{
  const result=assessBurmeseTranscript(book,cues('ဦးဘသိန်းသည် ရွာဟောင်းသို့ သွားရောက်ပြီး သင်္ချိုင်းအနီးတွင် ရပ်နေသည်။'));
  assert.equal(result.status,'supported');
  assert.equal(result.autoAccepted,false);
  assert.equal(result.reviewRequired,true);
  assert.equal(result.safeToProposeAfterHumanReview,true);
});
test('wrong Burmese narration text is rejected despite legal SRT timestamps',()=>{
  const wrong='မြန်မာပြည်၏ စီးပွားရေး လေယာဉ်ပျံများအကြောင်း ထုတ်ပြန်ကြေညာချက်ကို နောက်ဆုံးနေ့တွင် ပြုလုပ်သည်။';
  const result=assessBurmeseTranscript(book,cues(wrong));
  assert.equal(result.status,'unsupported');
  assert.equal(result.safeToProposeAfterHumanReview,false);
  assert.equal(result.autoAccepted,false);
});
test('English output from a Burmese recording is insufficient, not silently accepted',()=>{
  const result=assessBurmeseTranscript(book,cues('Hello I cannot recognize Myanmar speech. It is raining'));
  assert.equal(result.status,'insufficient');
  assert.equal(result.autoAccepted,false);
});
test('empty and malformed subtitle cues cannot match',()=>{
  assert.equal(assessBurmeseTranscript(book,[]).status,'insufficient');
  assert.equal(assessBurmeseTranscript(book,'not an array').status,'insufficient');
  assert.equal(assessBurmeseTranscript(book,[{}]).status,'insufficient');
});
test('tiny short novel/short speech cannot claim high semantic alignment',()=>{
  assert.equal(assessBurmeseTranscript('မိုးရွာသည်။',cues('မိုးရွာသည်။')).status,'insufficient');
  assert.equal(assessBurmeseTranscript(book,cues('မိုးရွာသည်။')).status,'insufficient');
});
test('spaces and Myanmar stacked characters are normalized deterministically',()=>{
  const a=assessBurmeseTranscript(book,cues('ဦးဘသိန်းသည် ရွာဟောင်းသို့ သွားရောက်ပြီး သင်္ချိုင်းအနီးတွင် ရပ်နေသည်။'));
  const b=assessBurmeseTranscript(book.replace(/ /gu,'  \n'),cues('ဦးဘသိန်းသည်ရွာဟောင်းသို့သွားရောက်ပြီးသင်္ချိုင်းအနီးတွင်ရပ်နေသည်။'));
  assert.deepEqual([a.status,a.observedOverlap,a.matchingDistinctSequences],
                   [b.status,b.observedOverlap,b.matchingDistinctSequences]);
});
test('long unreliably large text fails closed instead of exhausting memory',()=>{
  assert.equal(assessBurmeseTranscript('က'.repeat(1000002),cues(book)).status,'insufficient');
});
test('many cues with no Burmese evidence cannot be approved',()=>{
  const srt=Array.from({length:35},(_,i)=>({start:i,end:i+1,text:'noise ...'}));
  assert.equal(assessBurmeseTranscript(book,srt).status,'insufficient');
});
test('report includes observed overlap, not a made-up ASR confidence score',()=>{
  const r=assessBurmeseTranscript(book,cues(book.slice(0,160)));
  assert.ok(typeof r.observedOverlap==='number');
  assert.equal(r.autoAccepted,false);
  assert.equal('confidence' in r,false);
});
test('original manuscript and cue arrays are never modified',()=>{
  const a=cues(book.slice(0,160)),copy=structuredClone(a);
  assessBurmeseTranscript(book,a);
  assert.deepEqual(a,copy);
});
test('Latin punctuation and digits alone cannot fake a matched Burmese passage',()=>{
  const fake=cues('00000 ...123   HELLO yes .world.');
  const r=assessBurmeseTranscript(book,fake);
  assert.equal(r.autoAccepted,false);
  assert.equal(r.status,'insufficient');
});
test('repeated matching short phrase is not enough to force approval',()=>{
  const r=assessBurmeseTranscript(book,cues('မိုးရွာသည်။'.repeat(20)));
  assert.equal(r.autoAccepted,false);
  assert.notEqual(r.status,'supported');
});
test('mixed unrelated speech with only one matching cue fails coverage gate',()=>{
  const result=assessBurmeseTranscript(book,[
    {start:0,end:10,text:'ဦးဘသိန်းသည် ရွာဟောင်းသို့ သွားရောက်ပြီး သင်္ချိုင်းအနီးတွင် ရပ်နေသည်။'},
    {start:10,end:20,text:'နိုင်ငံတကာစျေးကွက် ထုတ်ကုန်ပစ္စည်းများ တင်ပို့ရောင်းချခြင်းဆိုင်ရာ စာရင်းဇယားများ'},
    {start:20,end:30,text:'စီးပွားရေးသတင်းထုတ်ပြန်ချက်များနှင့် စက်မှုကုန်ထုတ်စွမ်းအား သုံးသပ်ချက်များ'},
    {start:30,end:40,text:'အာကာသလေ့လာရေးစီမံကိန်းများနှင့် နည်းပညာတိုးတက်မှုအခြေအနေ'}
  ]);
  assert.equal(result.status,'unsupported');
});
