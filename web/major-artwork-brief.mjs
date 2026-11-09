/**
 * Major-only artwork brief. Fully local, based only on already planned
 * major visible scenes. No image generation, no network and no fake AI claims.
 */
const safe=(v,max=380)=>Array.from(String(v??'').replace(/\s+/gu,' ').trim()).slice(0,max).join('');
const escapeMd=s=>safe(s,600).replace(/[|\x60]/g,' ').replace(/[\r\n]/g,' ');
const section=(label,value)=>'- '+label+': '+value;

function valid(chapter){
  if(!chapter || chapter.scenePolicy!=='major-only-conservative')
    throw Error('Run and review Major-only Auto Draft first.');
  const scenes=chapter.scenes;
  if(!Array.isArray(scenes)||!scenes.length||scenes.length>1000)
    throw Error('No major visual scenes available.');
  let end=0;
  for(let i=0;i<scenes.length;i++){
    const a=Number(scenes[i].start),d=Number(scenes[i].duration);
    if(!Number.isFinite(a)||!Number.isFinite(d)||d<=0||d>3600||
       Math.abs(a-end)>.6)throw Error('Unsafe timeline at scene '+i);
    end=a+d;
  }
  return {scenes,seconds:end};
}

export function buildMajorArtworkBrief(chapter,assets=[],options={}){
  const plan=valid(chapter);
  if(!Array.isArray(assets))throw Error('Local artwork library unavailable.');
  const images=new Map(assets.filter(a=>a&&typeof a.id==='string'&&
    a.type?.startsWith('image/')).map(a=>[a.id,a]));
  const rows=[];
  let skipped=0,linked=0,missing=0;
  const ch=String(chapter.number||0).padStart(2,'0');
  for(const scene of plan.scenes){
    if(scene.technicalContinuation){skipped++;continue;}
    const image=scene.assetId?images.get(scene.assetId):null;
    const exists=!!image,idx=rows.length+1;
    const requested=scene.imageRequirementId||
       ('MS-'+ch+'-'+String(idx).padStart(3,'0'));
    const row={
      id:String(scene.id||'beat-'+idx),
      requestedId:String(requested),
      start:Number(scene.start),
      duration:Number(scene.duration),
      evidence:safe(scene.imageRequirementText||scene.text||'',440),
      reason:String(scene.majorSceneReason||'opening picture or manually preserved scene'),
      kind:String(scene.majorSceneKind||'review-needed'),
      assetId:exists?image.id:null,
      assetName:exists?image.name:null,
      assignedButMissing:!!(scene.assetId&&!exists),
      confirmed:scene.imageMatchStatus==='manual-confirmed',
      needsArtwork:!exists
    };
    if(exists)linked++;else missing++;
    rows.push(row);
  }
  if(!rows.length)throw Error('No visible story beats available.');
  const lines=[
    '# '+safe(options.title||chapter.title||'MMMN')+' — Important-Scenes-Only Image Brief',
    '',
    'Chapter: '+String(chapter.number||'unknown'),
    'Major visual beats: '+rows.length,
    'Local pictures linked: '+linked,
    'Pictures still needed: '+missing,
    'Renderer-only same-image continuations omitted: '+skipped,
    'Original narration runtime: '+plan.seconds.toFixed(3)+' seconds',
    '',
    '## Rules','','- One image per important visible scene, not per rain word, dialogue turn or minor entrance.',
    '- A long quiet passage can hold the original photo. Technical renderer segments are not new artwork.',
    '- Keep location, clothing and recurring-character continuity based strictly on the real novel.',
    '- Use a 16:9 master with central subjects to support vertical crops. No captions/logos/watermarks.',
    '- This document does NOT create, upload or download images. Import photos from local folders.',
    '- The brief may include unpublished manuscript excerpts; never post it to a public repository.',''
  ];
  for(const [i,row] of rows.entries()){
    const status=row.needsArtwork?'MISSING — make/find an image':
      (row.confirmed?'LOCAL PHOTO LINKED — confirmed':'LOCAL PHOTO LINKED — review');
    lines.push('## '+(i+1)+'. '+escapeMd(row.requestedId)+' — '+status,'',
      section('Narration time',row.start.toFixed(3)+' seconds; visual hold '+row.duration.toFixed(3)+' seconds'),
      section('Why picture can change',escapeMd(row.reason)),
      section('Scene kind',escapeMd(row.kind)),
      section('Author text or visual requirement',escapeMd(row.evidence)||'(Author should fill this)'),
      section('Local artwork',row.assetName?escapeMd(row.assetName):'(not found)'),
      section('Suggested new filename',escapeMd(row.requestedId)+'.png'),'',
      'Illustration guidance: depict ONLY the major location/action supported by the author text above, keeping characters and setting consistent; do not invent new events.','');
  }
  return {
    markdown:lines.join('\n'),rows,
    majorBeats:rows.length,linkedPictures:linked,missingPictures:missing,
    skippedTechnicalContinuations:skipped,
    narrationSeconds:Number(plan.seconds.toFixed(3)),
    generatedImages:0,networkRequests:0,requiresHumanReview:true
  };
}
