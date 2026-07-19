from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/(ROOT.name+"_deliverable.zip")
if OUT.exists(): OUT.unlink()
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in ROOT.rglob("*"):
        if p.is_file(): z.write(p,p.relative_to(ROOT.parent))
print(OUT)
