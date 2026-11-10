import test from 'node:test';
import assert from 'node:assert/strict';
import {buildMajorSceneTimingEvidence as run} from '../web/major-scene-timing-evidence.mjs';
const numeral=i=>String(i).replace(/[0-9]/g,n=>'၀၁၂၃၄၅၆၇၈၉'[+n]);
const texts=Array.from({length:12},(_,i)=>
 'အပိုင်း'+numeral(i+1)+' ဦးဘသိန်းသည် ရွာဟောင်းလမ်းအတိုင်း သင်္ချိုင်းဆီသွားကာ အကြောင်းရင်းကို စုံစမ်းခဲ့သည်။');
const cues=texts.map((text,i)=>({start:20*i,end:20*(i+1),text}));
const shots=[
 {id:'one',start:0,duration:80,text:texts[0],assetId:'keep-1'},
 {id:'two',start:80,duration:80,text:texts[4],assetId:'keep-2'},
 {id:'three',start:160,duration:80,text:texts[8],assetId:'keep-3'}
];
const chapter=o=>({scenePolicy:'major-only-conservative',text:texts.join(' '),
  recordedSeconds:240,subtitleCues:cues,scenes:shots,...o});
test('unique matching Myanmar text provides review-only cue suggestions',()=>{
 const r=run(chapter());
 assert.equal(r.summary.manuscriptAgreement,'supported');
 assert.equal(r.summary.audioCoverage,'supported');
 assert.deepEqual(r.rows.map(x=>x.suggestedCueStart),[0,80,160]);
 assert.equal(r.summary.changesToProject,0);
 assert.equal(r.automaticallyChangesProject,false);
});
test('bad Burmese model text gives NO candidate timings',()=>{
 const wrong=cues.map((c,i)=>({...c,text:
 'မြို့နယ်အစိုးရအဖွဲ့အစည်း စာရင်းဇယား စီးပွားရေးလုပ်ငန်းများ '+numeral(i)}));
 const r=run(chapter({subtitleCues:wrong}));
 assert.equal(r.summary.uniqueTextAnchors,0);
});
test('matching but truncated transcript gives NO timing',()=>{
 const r=run(chapter({subtitleCues:cues.slice(0,3)}));
 assert.equal(r.summary.uniqueTextAnchors,0);
 assert.equal(r.summary.audioCoverage,'unsupported');
});
test('repeated narration with same phrase is ambiguous, not silently timed',()=>{
 const copy=structuredClone(cues);
 copy[8].text=copy[0].text;
 const r=run(chapter({subtitleCues:copy,text:copy.map(c=>c.text).join(' ')}));
 assert.equal(r.rows[0].status,'ambiguous');
 assert.equal(r.rows[0].suggestedCueStart,null);
});
test('SRT reversed/overlapped cannot suggest timestamps',()=>{
 const copy=structuredClone(cues);
 copy[3].start=-10;
 assert.equal(run(chapter({subtitleCues:copy})).summary.uniqueTextAnchors,0);
});
test('too short text does not invent a match',()=>{
 const copy=structuredClone(shots);
 copy[0].text='မိုး';
 assert.equal(run(chapter({scenes:copy})).rows[0].status,'too-short');
});
test('no SRT produces report with safe unresolved labels',()=>{
 const r=run(chapter({subtitleCues:[]}));
 assert.equal(r.summary.audioCoverage,'insufficient');
 assert.equal(r.summary.uniqueTextAnchors,0);
 assert.equal(r.rows[0].suggestedCueStart,null);
});
test('technical continuation does not request a fresh photo',()=>{
 const copy=structuredClone(shots);
 copy[1].technicalContinuation=true;
 const r=run(chapter({scenes:copy}));
 assert.equal(r.summary.visibleMajorScenes,2);
 assert.equal(r.summary.technicalContinuationsIgnored,1);
});
test('manual locked scenes and original SRT are untouched',()=>{
 const copy=structuredClone(shots);
 copy[1].visualLocked=true;
 copy[1].alignment='manual-locked';
 const c=chapter({scenes:copy}),before=structuredClone(c);
 run(c);
 assert.deepEqual(c,before);
});
test('private manuscript safety warning is mandatory',()=>{
 const r=run(chapter());
 assert.match(r.markdown,/UNPUBLISHED/);
 assert.match(r.markdown,/REVIEW ONLY/);
 assert.equal(r.summary.imagesGenerated,0);
 assert.equal(r.summary.networkRequests,0);
});
test('never run on a legacy unreviewed storyboard',()=>{
 assert.throws(()=>run(chapter({scenePolicy:'ordinary-auto'})),/Major-only/);
});
test('non-contiguous and overlong scenes fail closed',()=>{
 const broken=structuredClone(shots);broken[1].start=90;
 assert.throws(()=>run(chapter({scenes:broken})),/Unsafe/);
 assert.throws(()=>run(chapter({scenes:[{...shots[0],duration:4000}]})),/Unsafe/);
});
test('chapter data remains byte identical after repeated review',()=>{
 const c=chapter(),before=JSON.stringify(c);
 run(c);run(c);
 assert.equal(JSON.stringify(c),before);
});
