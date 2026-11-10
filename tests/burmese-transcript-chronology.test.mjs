import test from 'node:test';
import assert from 'node:assert/strict';
import {assessBurmeseTranscript as assess} from '../web/burmese-transcript-agreement.mjs';
const chunks=[
  'ဦးဘသိန်းသည် ရွာဟောင်းသို့ သွားရောက်ပြီး သင်္ချိုင်းအနီးတွင် ရပ်နေသည်။',
  'မိုးရွာနေသော်လည်း သူတို့ စကားပြောနေကြသည်။',
  'မိုးသည်းထန်၍ ညနေမှောင်မိုက်လာသည်။ သင်္ချိုင်းလမ်း မမြင်နိုင်တော့ပါ။',
  'မိန်းကလေးတစ်ယောက် ပေါ်လာသည်။ ဦးဘသိန်းက မေးလိုက်သည်။'
];
const book=chunks.join(' ')+' '+chunks.join(' ');
const srt=(chunks)=>chunks.map((text,i)=>({start:i*8,end:(i+1)*8,text}));
test('many ordered repeated real-manuscript cues stay review-only',()=>{
  const cues=Array.from({length:40},(_,i)=>({
    start:i*8,end:(i+1)*8,text:chunks[Math.floor(i/10)]
  }));
  const r=assess(book,cues);
  assert.equal(r.status,'supported');
  assert.equal(r.autoAccepted,false);
  assert.equal(r.reviewRequired,true);
  assert.equal(r.manuscriptOrderCoverage,1);
  assert.equal(r.timestampOrderValid,true);
});
test('same words shuffled backwards do not silently control photos',()=>{
  const r=assess(book,srt([...chunks].reverse()));
  assert.equal(r.status,'unsupported');
  assert.ok(r.observedOverlap>0.5);
  assert.ok(r.manuscriptOrderCoverage<0.70);
  assert.equal(r.safeToProposeAfterHumanReview,false);
});
test('chronologically reversed timestamps reject otherwise perfect Burmese',()=>{
  const cues=srt(chunks); cues[1].start=-1;
  assert.equal(assess(book,cues).status,'unsupported');
});
test('overlapping timestamps reject even when words are perfect',()=>{
  const cues=srt(chunks); cues[1].start=3;
  assert.equal(assess(book,cues).status,'unsupported');
});
test('end before start, NaN, Infinity and extreme duration reject',()=>{
  for(const end of [0,NaN,Infinity,200000]){
    const cues=srt(chunks);cues[0].end=end;
    assert.equal(assess(book,cues).status,'unsupported');
  }
});
test('out-of-order cues reject identical repeated sentences',()=>{
  const cues=srt(chunks);cues[2].start=0;
  assert.equal(assess(book,cues).status,'unsupported');
});
test('mixed false cues can fail even when the overall book overlap is moderate',()=>{
  const r=assess(book,srt([
    chunks[0],chunks[1],
    'နိုင်ငံတကာစျေးကွက် ထုတ်ကုန်ပစ္စည်းများ တင်ပို့ရောင်းချခြင်းဆိုင်ရာ စာရင်းဇယားများ'
  ]));
  assert.equal(r.status,'unsupported');
  assert.ok(r.characterCoverage<.70);
});
test('cue is invalid if it does not contain actual text',()=>{
  const cues=srt(chunks);cues[0].text={};
  assert.equal(assess(book,cues).status,'insufficient');
});
test('a huge cue is bounded and fails closed',()=>{
  const cues=srt(chunks);cues[0].text='က'.repeat(1000001);
  assert.equal(assess(book,cues).status,'insufficient');
});
test('neither book nor cues are mutated',()=>{
  const cues=srt(chunks), copy=structuredClone(cues);
  const r=assess(book,cues);
  assert.equal(r.status,'supported');
  assert.deepEqual(cues,copy);
});
