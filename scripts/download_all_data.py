#!/usr/bin/env python3
"""
Dataset acquisition for the teeth-segmentation reproduction.

Priority for --dataset tdd:
1) Existing prepared data/tdd/images + data/tdd/masks.
2) KaggleHub public dataset mirror.
3) Kaggle CLI.
4) Direct Kaggle public API archive endpoint.
5) User-supplied local archive (--archive).

The target mirror cited by later peer-reviewed literature:
    iftakharh/tufts-dental-datasetcustomized

The official TDD source may require a download-permission request:
    https://tdd.ece.tufts.edu/

This script NEVER substitutes a different dataset while claiming it is TDD.
"""
from __future__ import annotations
import argparse, shutil, subprocess, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_KAGGLE = "iftakharh/tufts-dental-datasetcustomized"
MENDELEY_REFERENCE = "https://prod-dcd-datasets-cache-zipfiles.s3.eu-west-1.amazonaws.com/hxt48yk462-1.zip"
HF_PARQUET = (
    "https://huggingface.co/datasets/SerdarHelli/"
    "SegmentationOfTeethPanoramicXRayImages/resolve/main/data/"
    "train-00000-of-00001-f8e051e737d32f09.parquet"
)

def has_prepared_pairs(root: Path) -> bool:
    return (root/"images").is_dir() and (root/"masks").is_dir() and any((root/"images").iterdir()) and any((root/"masks").iterdir())

def extract_archive(path: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z: z.extractall(out)
    else: shutil.unpack_archive(str(path), str(out))

def try_kagglehub(dataset: str, out: Path) -> bool:
    try: import kagglehub
    except Exception: return False
    try:
        print(f"[download] Trying kagglehub: {dataset}")
        p = Path(kagglehub.dataset_download(dataset)); print(f"[download] kagglehub cache: {p}")
        if p.is_dir(): shutil.copytree(p, out, dirs_exist_ok=True)
        elif p.is_file(): extract_archive(p, out)
        return True
    except Exception as e:
        print(f"[download] kagglehub failed: {e}"); return False

def try_kaggle_cli(dataset: str, out: Path) -> bool:
    if shutil.which("kaggle") is None: return False
    try:
        out.mkdir(parents=True, exist_ok=True)
        cmd=["kaggle","datasets","download","-d",dataset,"-p",str(out),"--unzip"]
        print("[download] Trying Kaggle CLI:"," ".join(cmd)); subprocess.run(cmd,check=True); return True
    except Exception as e:
        print(f"[download] Kaggle CLI failed: {e}"); return False

def try_direct_kaggle(dataset: str, out: Path) -> bool:
    owner, slug = dataset.split("/",1); url=f"https://www.kaggle.com/api/v1/datasets/download/{owner}/{slug}"
    try:
        print(f"[download] Trying direct Kaggle public API: {url}"); out.mkdir(parents=True,exist_ok=True); tmp=out/"dataset.zip"
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=120) as r, open(tmp,"wb") as f: shutil.copyfileobj(r,f)
        if not zipfile.is_zipfile(tmp): raise RuntimeError("Downloaded response is not a ZIP archive; Kaggle authentication may be required.")
        extract_archive(tmp,out); tmp.unlink(missing_ok=True); return True
    except Exception as e:
        print(f"[download] Direct Kaggle API failed: {e}"); return False

def download_url(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True,exist_ok=True); req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=120) as r, open(dest,"wb") as f: shutil.copyfileobj(r,f)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--dataset",choices=["tdd","open-reference","all"],default="tdd"); ap.add_argument("--kaggle-dataset",default=DEFAULT_KAGGLE); ap.add_argument("--archive"); ap.add_argument("--force",action="store_true"); args=ap.parse_args()
    if args.dataset in ("tdd","all"):
        prepared=ROOT/"data/tdd"; raw=ROOT/"data/tdd_download"
        if has_prepared_pairs(prepared) and not args.force: print("[download] TDD already prepared:",prepared)
        else:
            if args.force and raw.exists(): shutil.rmtree(raw)
            raw.mkdir(parents=True,exist_ok=True); ok=False
            if args.archive:
                arc=Path(args.archive).expanduser().resolve()
                if not arc.exists(): raise SystemExit(f"Archive not found: {arc}")
                extract_archive(arc,raw); ok=True
            if not ok: ok=try_kagglehub(args.kaggle_dataset,raw)
            if not ok: ok=try_kaggle_cli(args.kaggle_dataset,raw)
            if not ok: ok=try_direct_kaggle(args.kaggle_dataset,raw)
            if not ok:
                raise SystemExit("TDD acquisition failed. Configure Kaggle credentials, obtain TDD from https://tdd.ece.tufts.edu/, or place paired files under data/tdd/images and data/tdd/masks. No alternate dataset has been silently substituted for TDD.")
            print("[download] Raw TDD material saved under:",raw)
    if args.dataset in ("open-reference","all"):
        out=ROOT/"data/open_reference_download"; out.mkdir(parents=True,exist_ok=True); zip_path=out/"hxt48yk462-1.zip"
        try:
            if not zip_path.exists() or args.force: download_url(MENDELEY_REFERENCE,zip_path)
            extract_archive(zip_path,out/"mendeley")
        except Exception as e: print("[download] Mendeley open-reference download failed:",e)
        try:
            pq=out/"teeth_masks.parquet"
            if not pq.exists() or args.force: download_url(HF_PARQUET,pq)
        except Exception as e: print("[download] Hugging Face open-reference download failed:",e)

if __name__ == "__main__": main()
