#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image

EXTS={'.png','.jpg','.jpeg','.tif','.tiff','.bmp'}

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='data/tdd'); ap.add_argument('--min-pairs',type=int,default=900); args=ap.parse_args()
    root=Path(args.root); imgs={p.stem:p for p in (root/'images').glob('*') if p.suffix.lower() in EXTS}; masks={p.stem:p for p in (root/'masks').glob('*') if p.suffix.lower() in EXTS}
    keys=sorted(set(imgs)&set(masks))
    if len(keys)<args.min_pairs: raise SystemExit(f'FAIL: only {len(keys)} paired samples; expected at least {args.min_pairs} for TDD')
    sample=[]
    for k in keys[:10]:
        with Image.open(imgs[k]) as im, Image.open(masks[k]) as mm:
            sample.append({'id':k,'image_size':im.size,'mask_size':mm.size,'image_sha256':sha256(imgs[k]),'mask_sha256':sha256(masks[k])})
    report={'dataset':'Tufts Dental Database candidate','paired_samples':len(keys),'sample_checks':sample}
    out=Path('outputs/tdd_provenance.json'); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2))
    print(f'PASS: {len(keys)} pairs; provenance written to {out}')
if __name__=='__main__': main()
