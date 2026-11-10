"""MMMN 0.15.7 RESEARCH ONLY — private localhost FastSDCPU artwork candidate.

NOT bundled in Windows Studio, NOT tested on author's Intel 16GB laptop.
No model installation, no remote prompt API, no automatic scene approval.
The installed optional FastSDCPU server MUST be preconfigured with its model
already cached, ideally with HF_HUB_OFFLINE=1 and TRANSFORMERS_OFFLINE=1,
and bound to 127.0.0.1, not 0.0.0.0 (FastSD default can expose LAN).
This client only connects to 127.0.0.1; it cannot control the server's own
outbound network connections or whether it downloads uncached model weights.
"""
import argparse,base64,binascii,hashlib,io,json,os,re,secrets,sys,tempfile,unicodedata
import urllib.error,urllib.request
from pathlib import Path
from PIL import Image,UnidentifiedImageError

MAX_REPLY_BYTES=8_000_000
MAX_JPEG_BYTES=4_000_000
MAX_PROMPT_CHARS=1400
MIN_DIM=256
MAX_DIM=1536

def validated_prompt(value):
    if not isinstance(value,str):raise ValueError("Text prompt must be a string")
    prompt=unicodedata.normalize("NFC",value).strip()
    if len(prompt)<15 or len(prompt)>MAX_PROMPT_CHARS:
        raise ValueError("Artwork prompt must be 15-1400 characters")
    if any(ord(c)<32 and c not in "\n\t" for c in prompt):
        raise ValueError("Control characters are not permitted in prompts")
    return prompt

def validated_scene_id(value):
    if not isinstance(value,str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}",value):
        raise ValueError("Scene id must be 1-64 safe ASCII characters")
    return value

def validate_image(raw):
    if not isinstance(raw,bytes) or len(raw)<100 or len(raw)>MAX_JPEG_BYTES:
        raise ValueError("Unreasonable encoded JPEG size")
    if not raw.startswith(b"\xff\xd8\xff") or not raw.endswith(b"\xff\xd9"):
        raise ValueError("Model returned non-JPEG output")
    try:
        with Image.open(io.BytesIO(raw)) as im:
            if im.format!="JPEG" or im.width<MIN_DIM or im.height<MIN_DIM or im.width>MAX_DIM or im.height>MAX_DIM:
                raise ValueError("Unexpected generated image dimensions or format")
            im.verify()
        with Image.open(io.BytesIO(raw)) as im:
            im.load()
    except (UnidentifiedImageError,OSError,ValueError,Image.DecompressionBombError) as exc:
        raise ValueError("Invalid, corrupt or unreasonably sized generated JPEG") from exc
    return raw

def _request(port,payload,timeout):
    if not isinstance(port,int) or not 1024<=port<=65535:
        raise ValueError("Only a safe local port is allowed")
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    url="http://127.0.0.1:"+str(port)+"/api/generate"
    request=urllib.request.Request(url,
        data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type":"application/json","Accept":"application/json"},
        method="POST")
    try:
        with opener.open(request,timeout=timeout) as res:
            if res.status!=200:raise RuntimeError("Local model HTTP status "+str(res.status))
            blob=res.read(MAX_REPLY_BYTES+1)
            if len(blob)>MAX_REPLY_BYTES:raise ValueError("Model output exceeds safe maximum")
            return json.loads(blob.decode("utf-8"))
    except (urllib.error.URLError,TimeoutError) as exc:
        raise RuntimeError("Local FastSD CPU model server is unavailable") from exc

def _decode(response):
    if not isinstance(response,dict):raise ValueError("Invalid local model response")
    if response.get("error"):raise RuntimeError("Local model generation returned an error")
    images=response.get("images")
    if not isinstance(images,list) or len(images)!=1 or not isinstance(images[0],str):
        raise ValueError("Expected exactly one JPEG from the local model")
    encoded=images[0]
    if len(encoded)>MAX_REPLY_BYTES:raise ValueError("Oversized base64 response")
    if encoded.startswith("data:image/jpeg;base64,"):
        encoded=encoded.split(",",1)[1]
    try:
        binary=base64.b64decode(encoded,validate=True)
    except (binascii.Error,ValueError) as exc:
        raise ValueError("Invalid base64 image") from exc
    return validate_image(binary)

def create_review_art(prompt,scene_id,output_dir,*,approved=False,port=8000,
                      request_func=_request,timeout=480):
    if approved is not True:raise PermissionError("User must explicitly request private local image generation")
    prompt=validated_prompt(prompt)
    scene_id=validated_scene_id(scene_id)
    if not isinstance(output_dir,(str,Path)):raise ValueError("Local directory required")
    folder=Path(output_dir).resolve()
    if folder.is_symlink():raise ValueError("Refusing symlink output directory")
    folder.mkdir(parents=True,exist_ok=True)
    if not folder.is_dir():raise ValueError("Output directory unavailable")
    if not 5<=timeout<=900:raise ValueError("Invalid local inference timeout")
    payload={"prompt":prompt,"diffusion_task":"text_to_image",
             "use_openvino":True,"image_width":512,"image_height":512,
             "inference_steps":1,"guidance_scale":1.0,"number_of_images":1,
             "use_safety_checker":True}
    # No external hostname accepted; all network requests from THIS bridge
    # always target IPv4 loopback. A separately running model may not be
    # offline unless configured independently.
    raw=_decode(request_func(port,payload,timeout))
    digest=hashlib.sha256(raw).hexdigest()
    # No silent writes to the user's existing photo library or art. Create a
    # fresh preview candidate with an unambiguous scene/token identifier.
    name="MMMN-art-review-"+scene_id+"-"+secrets.token_hex(8)+".jpg"
    image=folder/name
    manifest=image.with_suffix(".json")
    try:
        with image.open("xb") as out:
            out.write(raw);out.flush();os.fsync(out.fileno())
        metadata={
          "status":"PRIVATE_UNAPPROVED_REVIEW_ONLY",
          "sceneId":scene_id,"photo":image.name,
          "sha256":digest,"bytes":len(raw),
          "modelService":"FastSDCPU on 127.0.0.1",
          "locallyGeneratedCandidate":True,
          "newSceneCreated":False,
          "originalAssetsModified":False,
          "requiresManualScenePictureApproval":True,
          "potentialModelServerOutboundDownloadsNotVerified":True
        }
        with manifest.open("x",encoding="utf-8") as f:
            json.dump(metadata,f,ensure_ascii=False,indent=2)
            f.flush();os.fsync(f.fileno())
    except BaseException:
        image.unlink(missing_ok=True)
        manifest.unlink(missing_ok=True)
        raise
    return {"image":image,"manifest":manifest,"sha256":digest,"reviewOnly":True}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scene-id",required=True)
    p.add_argument("--prompt",required=True)
    p.add_argument("--output-dir",required=True)
    p.add_argument("--port",type=int,default=8000)
    p.add_argument("--timeout",type=int,default=480)
    p.add_argument("--approve-local-generation",action="store_true")
    args=p.parse_args()
    result=create_review_art(args.prompt,args.scene_id,args.output_dir,
        approved=args.approve_local_generation,port=args.port,timeout=args.timeout)
    print("LOCAL UNAPPROVED ART CANDIDATE:",result["image"])
    print("PRIVATE SHA256:",result["sha256"])
    print("Listen and review scene, do not automatically assign art to chapter.")

if __name__=="__main__":main()
