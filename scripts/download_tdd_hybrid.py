#!/usr/bin/env python3
"""Hybrid Tufts Dental Database acquisition fallback.

Assembles original Tufts components by numeric image ID:
  1) radiographs: official Tufts archive first, then active Kaggle mirror fallback;
  2) tooth masks: verified public TDD-derived `Segmentation/teeth_mask` directory.

Requires >=900 matched IDs. Never substitutes a different dental dataset.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, urllib.request, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OFFICIAL_RADIOGRAPHS='https://tdd.ece.tufts.edu/Tufts_Dental_Database/Radiographs.zip'
RAD_DATASET='manarmaged/tufts-radiographs'
MASK_REPO='https://github.com/gopimeruva/Dental_Xray_Anamoly_Detection.git'
EXTS={'.jpg','.jpeg','.png','.tif','.tiff','.bmp'}

def download_official(dest: Path):
    dest.mkdir(parents=True,exist_ok=True); z=dest/'Radiographs.zip'
    print('[hybrid] official Tufts radiographs:',OFFICIAL_RADIOGRAPHS)
    req=urllib.request.Request(OFFICIAL_RADIOGRAPHS,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=240) as r, z.open('wb') as f: shutil.copyfileobj(r,f)
    if not zipfile.is_zipfile(z): raise RuntimeError('Official Tufts response is not a ZIP archive')
    out=dest/'official'; out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(z) as f: f.extractall(out)
    return out

def download_kaggle(dataset: str, dest: Path) -> Path:
    dest.mkdir(parents=True,exist_ok=True)
    try:
        import kagglehub
        p=Path(kagglehub.dataset_download(dataset)); print('[hybrid] kagglehub:',p); return p
    except Exception as e: print('[hybrid] kagglehub failed:',e)
    if shutil.which('kaggle'):
        try:
            subprocess.run(['kaggle','datasets','download','-d',dataset,'-p',str(dest),'--unzip'],check=True); return dest
        except Exception as e: print('[hybrid] kaggle CLI failed:',e)
    owner,slug=dataset.split('/',1); url=f'https://www.kaggle.com/api/v1/datasets/download/{owner}/{slug}'; z=dest/'radiographs.zip'
    print('[hybrid] direct Kaggle API:',url)
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=240) as r, z.open('wb') as f: shutil.copyfileobj(r,f)
    if not zipfile.is_zipfile(z): raise RuntimeError('Kaggle response is not a ZIP archive')
    out=dest/'extracted'; out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(z) as f: f.extractall(out)
    return out

def acquire_radiographs(work: Path, dataset: str):
    try: return download_official(work/'official_download'), 'official Tufts Radiographs.zip'
    except Exception as e: print('[hybrid] official archive failed:',e)
    return download_kaggle(dataset,work/'kaggle_download'), dataset

def clone_masks(dest: Path) -> Path:
    if dest.exists(): shutil.rmtree(dest)
    subprocess.run(['git','clone','--depth','1','--filter=blob:none','--sparse',MASK_REPO,str(dest)],check=True)
    subprocess.run(['git','-C',str(dest),'sparse-checkout','set','TUFTS-project/Segmentation/teeth_mask'],check=True)
    p=dest/'TUFTS-project/Segmentation/teeth_mask'
    if not p.is_dir(): raise RuntimeError(f'Mask directory not found: {p}')
    return p

def numeric_stem(p: Path):
    return str(int(p.stem)) if p.stem.isdigit() else None

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default='data/tdd_download/hybrid'); ap.add_argument('--min-pairs',type=int,default=900); ap.add_argument('--radiographs-dataset',default=RAD_DATASET); args=ap.parse_args()
    out=ROOT/args.out if not Path(args.out).is_absolute() else Path(args.out); work=out.parent/'_hybrid_work'
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True,exist_ok=True)
    rad_root,rad_source=acquire_radiographs(work,args.radiographs_dataset); mask_root=clone_masks(work/'mask_repo')
    masks={numeric_stem(p):p for p in mask_root.rglob('*') if p.is_file() and p.suffix.lower() in EXTS and numeric_stem(p)}
    radiographs={}
    for p in rad_root.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in EXTS: continue
        k=numeric_stem(p)
        if not k or any(x in str(p).lower() for x in ('mask','segmentation','label','annotation')): continue
        radiographs.setdefault(k,p)
    keys=sorted(set(radiographs)&set(masks),key=lambda x:int(x)); print(f'[hybrid] radiographs={len(radiographs)} masks={len(masks)} matched={len(keys)}')
    if len(keys)<args.min_pairs: raise SystemExit(f'Hybrid TDD validation failed: {len(keys)} matched IDs; require >= {args.min_pairs}.')
    if out.exists(): shutil.rmtree(out)
    rdest=out/'Radiographs'; mdest=out/'Segmentation/teeth_mask'; rdest.mkdir(parents=True); mdest.mkdir(parents=True)
    for k in keys:
        ip,mp=radiographs[k],masks[k]; shutil.copy2(ip,rdest/f'{k}{ip.suffix}'); shutil.copy2(mp,mdest/f'{k}{mp.suffix}')
    provenance={'dataset':'Tufts Dental Database hybrid acquisition','radiographs_source':rad_source,'masks_source':MASK_REPO,'masks_path':'TUFTS-project/Segmentation/teeth_mask','matched_pairs':len(keys),'first_ids':keys[:20],'note':'Paired strictly by original numeric ID; no alternate dental dataset substituted.'}
    (out/'HYBRID_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)); print('[hybrid] SUCCESS:',out)
if __name__=='__main__': main()
