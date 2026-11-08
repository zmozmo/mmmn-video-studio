"""Pin JavaScript module MIME on Windows, where mimetypes reports .mjs as text/plain.

Source ZIP is SHA-256 verified first. This exact reviewed patch is used for native
packaging and for the rapid UI test. Never silently patch an unrecognized source.
"""
import pathlib
import sys

OLD = "return self.reply(200,content,mimetypes.guess_type(path.name)[0] or 'application/octet-stream')"
NEW = ("return self.reply(200,content, "
       "'text/javascript; charset=utf-8' if path.suffix.lower() in ('.js', '.mjs') "
       "else (mimetypes.guess_type(path.name)[0] or 'application/octet-stream'))")

def main(root: pathlib.Path):
    path=root/"portable"/"studio_server.py"
    raw=path.read_text(encoding="utf-8")
    if NEW in raw:
        if OLD in raw:raise RuntimeError("Ambiguous MIME source, patch rejected")
        print("WINDOWS MODULE MIME: already corrected",flush=True)
        return
    if raw.count(OLD)!=1:raise RuntimeError("Unexpected source MIME response, patch rejected")
    result=raw.replace(OLD,NEW)
    if result.count(NEW)!=1:raise RuntimeError("MIME patch did not apply uniquely")
    path.write_text(result,encoding="utf-8")
    print("WINDOWS MODULE MIME: .js/.mjs use text/javascript; strict Edge module loading enabled",flush=True)

if __name__=="__main__":
    main(pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path.cwd())
