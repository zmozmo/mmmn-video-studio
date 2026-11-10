import test from 'node:test';
import assert from 'node:assert/strict';
import {auditNarrationTiming as audit} from '../web/narration-timing-audit.mjs';
const make=(count,span=8)=>Array.from({length:count},(_,i)=>({start:i*span,end:(i+1)*span,
  text:'ဦးဘသိန်းသည် ရွာလမ်းအတိုင်း လျှောက်သွားသည်။'}));
test('40 timestamped cues span 320 second local narration',()=>{
 const r=audit(320,make(40));
 assert.equal(r.status,'supported');assert.equal(r.safeForDraft,true);
 assert.equal(r.observedCoverage,1);assert.equal(r.humanReviewRequired,true);
 assert.equal(r.wordAccurate,false);assert.equal(r.semanticUnderstanding,false);
});
test('true 90 minute complete timeline is acceptable but never auto-approved',()=>{
 const r=audit(5400,make(540,10));
 assert.equal(r.status,'supported');assert.equal(r.cueCount,540);
 assert.equal(r.narrationSeconds,5400);assert.equal(r.humanReviewRequired,true);
});
test('real 90 minute narration with only 1 minute transcript must fail closed',()=>{
 const r=audit(5400,make(6,10));
 assert.equal(r.status,'unsupported');assert.equal(r.safeForDraft,false);
 assert.ok(r.trailingGapSeconds>5300);
});
test('three cues within a 90 minute recording cannot fake full coverage',()=>{
 const r=audit(5400,make(3,10));assert.equal(r.status,'unsupported');
});
test('a missing or infinite audio duration is insufficient',()=>{
 for(const duration of [0,-1,NaN,Infinity,17000,undefined]){
  assert.equal(audit(duration,make(4)).status,'insufficient');
 }
});
test('short unrelated SRT and missing cues never permit auto timing',()=>{
 assert.equal(audit(60,[]).status,'insufficient');
 assert.equal(audit(60,'file').safeForDraft,false);
});
test('nonfinite, negative or out-of-bounds cue time fails closed',()=>{
 for(const val of [-1,NaN,Infinity,1000]){
  const c=make(5);c[1].start=val;
  assert.equal(audit(40,c).status,'unsupported');
 }
});
test('overlapping timestamps are rejected',()=>{
 const c=make(5);c[2].start=10;
 assert.equal(audit(40,c).status,'unsupported');
});
test('narrative 4 minute hole rejects a 10 minute audio',()=>{
 const c=make(50,4);
 const shifted=c.map((x,i)=>i>=20?{...x,start:x.start+240,end:x.end+240}:x);
 const r=audit(600,shifted);
 assert.equal(r.status,'unsupported');
 assert.ok(r.longestGapSeconds>=240);
});
test('missing SRT words are rejected',()=>{
 const c=make(5);c[2].text='  ';
 assert.equal(audit(40,c).status,'unsupported');
});
test('one unreasonably long SRT cue cannot fake narration coverage',()=>{
 const c=[{start:0,end:150,text:'မှတ်တမ်း'},...make(5,10).map(x=>({...x,start:x.start+150,end:x.end+150}))];
 assert.equal(audit(200,c).status,'unsupported');
});
test('moderately silent narration passages are acceptable if well-covered',()=>{
 const c=make(20,8).map((x,i)=>({
  ...x,start:x.start+i*1,end:x.end+i*1
 }));
 const r=audit(179,c);
 assert.equal(r.status,'supported');
 assert.ok(r.observedCoverage>.75);
});
test('original audio and subtitle data are not mutated by the audit',()=>{
 const c=make(40);const before=structuredClone(c);
 const r=audit(320,c);
 assert.deepEqual(c,before);assert.equal(r.audioUnchanged,true);
 assert.equal(r.srtUnchanged,true);
});
test('12 malformed cues fail rather than emit an invented ASR confidence',()=>{
 const c=make(12);c[7].end=c[7].start-1;
 const r=audit(96,c);
 assert.equal(r.status,'unsupported');assert.equal('confidence' in r,false);
});
