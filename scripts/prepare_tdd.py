#!/usr/bin/env python3
"""
Normalize a downloaded TDD tree into:
    data/tdd/images/
    data/tdd/masks/

The TDD mirror layout has varied across redistributions. This script:
- recursively indexes image files,
- classifies likely radiographs vs tooth masks by path/name keywords,
- matches by normalized filename stem,
- verifies mask-like candidates,
- writes a pairing report before copying.

It fails instead of guessing if pairing confidence is poor.
"""
from __future__ import annotations
import argparse, csv, re, shutil
from collections import defaultdict
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EXTS={".png",".jpg",".jpeg",".tif",".tiff",".bmp"}
MASK_WORDS=("mask","teeth","tooth","seg","label","annotation","groundtruth","ground_truth","gt")
RAD_WORDS=("radiograph","xray","x-ray","panoramic","image","images","original")

def clean_stem(p: Path) -> str:
    s=p.stem.lower()
    for t in ("_mask","-mask"," mask","_teeth","-teeth"," teeth","_tooth","-tooth","_segmentation","-segmentation","_seg","-seg","_label","-label","_groundtruth","-groundtruth","_ground_truth","-ground_truth","_gt","-gt"):
        s=s.replace(t,"")
    return re.sub(r"[^a-z0-9]","",s)

def path_score(p: Path, words) -> int:
    s=str(p).lower(); return sum(1 for w in words if w in s)

def mask_likeness(p: Path) -> float:
    try:
        im=Image.open(p).convert("L"); a=np.asarray(im.resize((128,64))); u=np.unique(a); binaryish=float(np.mean((a<20)|(a>235))); return max(binaryish,1.0 if len(u)<=16 else 0.0)
    except Exception: return 0.0

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",default="data/tdd_download"); ap.add_argument("--dest",default="data/tdd"); ap.add_argument("--min-pairs",type=int,default=100); ap.add_argument("--copy",action="store_true",default=True); args=ap.parse_args()
    source=(ROOT/args.source if not Path(args.source).is_absolute() else Path(args.source)); dest=(ROOT/args.dest if not Path(args.dest).is_absolute() else Path(args.dest))
    if not source.exists(): raise SystemExit(f"Source not found: {source}")
    files=[p for p in source.rglob("*") if p.is_file() and p.suffix.lower() in EXTS]
    if not files: raise SystemExit(f"No image files found in {source}")
    groups=defaultdict(list)
    for p in files: groups[clean_stem(p)].append(p)
    pairs=[]
    for stem,ps in groups.items():
        if len(ps)<2: continue
        ranked_masks=sorted(ps,key=lambda p:(path_score(p,MASK_WORDS),mask_likeness(p)),reverse=True); mp=ranked_masks[0]; candidates=[p for p in ps if p!=mp]
        if not candidates: continue
        ip=max(candidates,key=lambda p:(path_score(p,RAD_WORDS),-mask_likeness(p))); ml=mask_likeness(mp)
        if ip!=mp and ml>=0.70: pairs.append((stem,ip,mp,ml))
    if len(pairs)<args.min_pairs:
        likely_masks=[p for p in files if path_score(p,MASK_WORDS)>0 and mask_likeness(p)>=0.70]; likely_imgs=[p for p in files if p not in likely_masks]; mask_by={clean_stem(p):p for p in likely_masks}; fallback=[]
        for ip in likely_imgs:
            k=clean_stem(ip)
            if k in mask_by: fallback.append((k,ip,mask_by[k],mask_likeness(mask_by[k])))
        if len(fallback)>len(pairs): pairs=fallback
    report=ROOT/"outputs"/"tdd_pairing_report.csv"; report.parent.mkdir(parents=True,exist_ok=True)
    with report.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["stem","image","mask","mask_likeness"])
        for row in pairs: w.writerow([row[0],row[1],row[2],f"{row[3]:.4f}"])
    if len(pairs)<args.min_pairs: raise SystemExit(f"Only {len(pairs)} confident image/mask pairs detected (minimum {args.min_pairs}). Pairing report: {report}")
    for d in [dest/"images",dest/"masks"]:
        if d.exists(): shutil.rmtree(d)
        d.mkdir(parents=True,exist_ok=True)
    for idx,(stem,ip,mp,_) in enumerate(sorted(pairs,key=lambda x:x[0])):
        base=f"{idx:04d}"; shutil.copy2(ip,dest/"images"/f"{base}{ip.suffix.lower()}"); shutil.copy2(mp,dest/"masks"/f"{base}{mp.suffix.lower()}")
    print(f"Prepared {len(pairs)} TDD image/mask pairs in {dest}"); print("Pairing report:",report)

if __name__=="__main__": main()
