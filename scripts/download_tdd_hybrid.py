#!/usr/bin/env python3
"""Hybrid Tufts Dental Database acquisition fallback.

This does NOT substitute another dental dataset.
It assembles two public Tufts-derived sources by the original numeric image ID:
  - radiographs: Kaggle dataset `manarmaged/tufts-radiographs`
  - tooth masks: public Tufts project repository
    `gopimeruva/Dental_Xray_Anamoly_Detection`, path
    `TUFTS-project/Segmentation/teeth_mask/`

The script requires >=900 matching radiograph/mask stems before succeeding.
Raw medical images are not committed to this repository; provenance is written locally.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys, tempfile, urllib.request, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RAD_DATASET='manarmaged/tufts-radiographs'
MASK_REPO='https://github.com/gopimeruva/Dental_Xray_Anamoly_Detection.git'
EXTS={'.jpg','.jpeg','.png','.tif','.tiff','.bmp'}

def download_kaggle(dataset: str, dest: Path) -> Path:
    dest.mkdir(parents=True,exist_ok=True)
    try:
        import kagglehub
        p=Path(kagglehub.dataset_download(dataset))
        print('[hybrid] kagglehub:',p)
        return p
    except Exception as e:
        print('[hybrid] kagglehub failed:',e)
    if shutil.which('kaggle'):
        try:
            subprocess.run(['kaggle','datasets','download','-d',dataset,'-p',str(dest),'--unzip'],check=True)
            return dest
        except Exception as e:
            print('[hybrid] kaggle CLI failed:',e)
    owner,slug=dataset.split('/',1)
    url=f'https://www.kaggle.com/api/v1/datasets/download/{owner}/{slug}'
    z=dest/'radiographs.zip'
    print('[hybrid] direct Kaggle API:',url)
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=180) as r, z.open('wb') as f:
        shutil.copyfileobj(r,f)
    if not zipfile.is_zipfile(z): raise RuntimeError('Kaggle response is not a ZIP archive')
    with zipfile.ZipFile(z) as f: f.extractall(dest/'extracted')
    return dest/'extracted'

def clone_masks(dest: Path) -> Path:
    if dest.exists(): shutil.rmtree(dest)
    # Sparse clone downloads only the TDD tooth-mask directory.
    subprocess.run(['git','clone','--depth','1','--filter=blob:none','--sparse',MASK_REPO,str(dest)],check=True)
    subprocess.run(['git','-C',str(dest),'sparse-checkout','set','TUFTS-project/Segmentation/teeth_mask'],check=True)
    p=dest/'TUFTS-project/Segmentation/teeth_mask'
    if not p.is_dir(): raise RuntimeError(f'Mask directory not found after clone: {p}')
    return p

def numeric_stem(p: Path):
    s=p.stem
    return str(int(s)) if s.isdigit() else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='data/tdd_download/hybrid')
    ap.add_argument('--min-pairs',type=int,default=900)
    ap.add_argument('--radiographs-dataset',default=RAD_DATASET)
    args=ap.parse_args()
    out=ROOT/args.out if not Path(args.out).is_absolute() else Path(args.out)
    work=out.parent/'_hybrid_work'
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True,exist_ok=True)

    rad_root=download_kaggle(args.radiographs_dataset,work/'radiographs_download')
    mask_root=clone_masks(work/'mask_repo')

    masks={numeric_stem(p):p for p in mask_root.rglob('*') if p.is_file() and p.suffix.lower() in EXTS and numeric_stem(p)}
    # Radiograph source may contain nested folders. Prefer numeric image files and reject obvious masks/labels.
    radiographs={}
    for p in rad_root.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in EXTS: continue
        k=numeric_stem(p)
        if not k: continue
        low=str(p).lower()
        if any(x in low for x in ('mask','segmentation','label','annotation')): continue
        radiographs.setdefault(k,p)

    keys=sorted(set(radiographs)&set(masks),key=lambda x:int(x))
    print(f'[hybrid] radiographs={len(radiographs)} masks={len(masks)} matched={len(keys)}')
    if len(keys)<args.min_pairs:
        raise SystemExit(f'Hybrid TDD validation failed: only {len(keys)} matched numeric IDs; require >= {args.min_pairs}.')

    if out.exists(): shutil.rmtree(out)
    rdest=out/'Radiographs'; mdest=out/'Segmentation/teeth_mask'
    rdest.mkdir(parents=True,exist_ok=True); mdest.mkdir(parents=True,exist_ok=True)
    for k in keys:
        ip=radiographs[k]; mp=masks[k]
        shutil.copy2(ip,rdest/f'{k}{ip.suffix}')
        shutil.copy2(mp,mdest/f'{k}{mp.suffix}')

    provenance={
      'dataset':'Tufts Dental Database hybrid acquisition',
      'radiographs_source':args.radiographs_dataset,
      'masks_source':MASK_REPO,
      'masks_path':'TUFTS-project/Segmentation/teeth_mask',
      'matched_pairs':len(keys),
      'first_ids':keys[:20],
      'note':'Sources were paired strictly by original numeric ID. No alternate dental dataset was substituted.'
    }
    (out/'HYBRID_PROVENANCE.json').write_text(json.dumps(provenance,indent=2))
    print('[hybrid] SUCCESS:',out)

if __name__=='__main__': main()
