import base64,io,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from fastsdcpu_art_bridge_0157 import (
 create_review_art,validated_prompt,validated_scene_id,validate_image,_decode,_request
)
def jpeg():
 buf=io.BytesIO()
 Image.new("RGB",(512,512),(40,60,80)).save(buf,format="JPEG")
 return buf.getvalue()
def local_reply(port,payload,timeout):
 assert port==8000 and payload["image_width"]==512
 assert payload["number_of_images"]==1
 assert payload["use_openvino"] is True
 return {"images":[base64.b64encode(jpeg()).decode()],"error":"","latency":1.2}
class ArtBridgeSafety(unittest.TestCase):
 def setUp(self):self.temp=tempfile.TemporaryDirectory()
 def tearDown(self):self.temp.cleanup()
 def run_local(self,**kwargs):
  return create_review_art("Dark storm at an ancient Myanmar cemetery","major_cemetery",
    self.temp.name,approved=True,request_func=local_reply,**kwargs)
 def test_one_local_review_only_jpeg_and_manifest(self):
  r=self.run_local()
  self.assertTrue(r["image"].exists())
  self.assertTrue(r["manifest"].exists())
  meta=json.loads(r["manifest"].read_text())
  self.assertEqual(meta["status"],"PRIVATE_UNAPPROVED_REVIEW_ONLY")
  self.assertTrue(meta["requiresManualScenePictureApproval"])
  self.assertFalse(meta["originalAssetsModified"])
  self.assertFalse(meta["newSceneCreated"])
  self.assertEqual(meta["sha256"],r["sha256"])
 def test_never_overwrite_existing_review_art(self):
  first=self.run_local()
  second=self.run_local()
  self.assertNotEqual(first["image"],second["image"])
  self.assertEqual(first["image"].read_bytes(),second["image"].read_bytes())
 def test_explicit_consent_required_before_local_generation(self):
  calls=[]
  def forbidden(*args):calls.append(args);raise AssertionError("No request allowed")
  with self.assertRaises(PermissionError):
   create_review_art("Dark storm at an ancient Myanmar cemetery","s",
      self.temp.name,approved=False,request_func=forbidden)
  self.assertEqual(calls,[])
 def test_local_output_directory_symlink_rejected(self):
  p=Path(self.temp.name)/"outside";p.mkdir()
  s=Path(self.temp.name)/"link"
  try:s.symlink_to(p,target_is_directory=True)
  except OSError:self.skipTest("Symlinks not supported")
  with self.assertRaises(ValueError):
   create_review_art("Dark storm at an ancient Myanmar cemetery","s",s,
    approved=True,request_func=local_reply)
 def test_scene_traversal_disallowed(self):
  for val in ("../hack","local/path","\\Windows","", "😀"):
   with self.assertRaises(ValueError):validated_scene_id(val)
 def test_missing_or_too_long_prompt_disallowed(self):
  for val in ("short","x"*2000):
   with self.assertRaises(ValueError):validated_prompt(val)
 def test_wrong_model_image_format_rejected(self):
  for payload in ({"images":["AAAA"],"error":""},
       {"images":[],"error":""},{"images":["###"],"error":""},
       {"images":[base64.b64encode(b"\x89PNG").decode()],"error":""}):
   with self.assertRaises(ValueError):_decode(payload)
 def test_huge_model_json_or_image_rejected(self):
  with self.assertRaises(ValueError):_decode({"images":["X"*10_000_000],"error":""})
  with self.assertRaises(ValueError):validate_image(b"\xff\xd8\xff"+b"\x00"*4_000_001+b"\xff\xd9")
 def test_corrupt_and_tiny_jpeg_rejected(self):
  im=io.BytesIO()
  Image.new("RGB",(1,1)).save(im,format="JPEG")
  with self.assertRaises(ValueError):validate_image(im.getvalue())
  with self.assertRaises(ValueError):validate_image(jpeg()[:120]+b"\xff\xd9")
 def test_model_errors_fail_closed_without_files(self):
  def bad(*args):return {"images":[],"error":"model missing"}
  with self.assertRaises(RuntimeError):
   create_review_art("Dark storm at an ancient Myanmar cemetery","s",
     self.temp.name,approved=True,request_func=bad)
  self.assertEqual(list(Path(self.temp.name).iterdir()),[])
 def test_no_external_endpoint_or_proxy(self):
  with self.assertRaises(ValueError):_request(80,{},5)
  with self.assertRaises(ValueError):_request(65536,{},5)
  with self.assertRaises(RuntimeError):_request(65432,{},5)
 def test_invalid_long_timeout_rejected(self):
  with self.assertRaises(ValueError):self.run_local(timeout=9999)
 def test_original_asset_bytes_unchanged(self):
  source=Path(self.temp.name)/"original-novel-photo.jpg"
  source.write_bytes(b"ORIGINAL-PRIVATE-PHOTO-HASH-DO-NOT-CHANGE")
  before=source.read_bytes()
  self.run_local()
  self.assertEqual(source.read_bytes(),before)
 def test_localhost_fastsd_http_json_contract_with_fake_server(self):
  from http.server import BaseHTTPRequestHandler,HTTPServer
  from threading import Thread
  received=[]
  class Server(BaseHTTPRequestHandler):
   def do_POST(self):
    body=self.rfile.read(int(self.headers["Content-Length"]))
    received.append((self.path,json.loads(body)))
    output=json.dumps(local_reply(8000,received[-1][1],4)).encode()
    self.send_response(200)
    self.send_header("Content-Type","application/json")
    self.send_header("Content-Length",str(len(output)))
    self.end_headers();self.wfile.write(output)
   def log_message(self,*args):pass
  srv=HTTPServer(("127.0.0.1",0),Server)
  t=Thread(target=srv.serve_forever,daemon=True);t.start()
  try:
   payload={"prompt":"Night cemetery","number_of_images":1,
    "use_openvino":True,"image_width":512}
   reply=_request(srv.server_port,payload,10)
   self.assertEqual(received[0][0],"/api/generate")
   self.assertEqual(received[0][1],payload)
   self.assertTrue(validate_image(_decode(reply)))
  finally:srv.shutdown();srv.server_close();t.join(5)
if __name__=="__main__":unittest.main()
