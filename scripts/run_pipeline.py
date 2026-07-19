#!/usr/bin/env python3
"""Unified runner for smoke, paper, or both execution modes."""
from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(cmd):
    print("\n>>>"," ".join(str(x) for x in cmd),flush=True)
    subprocess.run([str(x) for x in cmd],cwd=ROOT,check=True)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("mode",choices=["smoke","paper","both"]); ap.add_argument("--download",action="store_true"); ap.add_argument("--archive"); ap.add_argument("--skip-prepare",action="store_true"); args=ap.parse_args()
    if args.mode in ("smoke","both"):
        smoke_images=ROOT/"data/bootstrap_synthetic/images"; smoke_masks=ROOT/"data/bootstrap_synthetic/masks"
        prepared=smoke_images.is_dir() and smoke_masks.is_dir() and any(smoke_images.iterdir()) and any(smoke_masks.iterdir())
        if not prepared: run([sys.executable,"scripts/generate_bootstrap_dataset.py","--root","data/bootstrap_synthetic","--count","48"])
        run([sys.executable,"scripts/reproduce_all.py","--config","configs/smoke.yaml"])
    if args.mode in ("paper","both"):
        if args.download or args.archive:
            cmd=[sys.executable,"scripts/download_all_data.py","--dataset","tdd"]
            if args.archive: cmd += ["--archive",args.archive]
            run(cmd)
        if not args.skip_prepare:
            imgdir=ROOT/"data/tdd/images"; maskdir=ROOT/"data/tdd/masks"; prepared=imgdir.is_dir() and maskdir.is_dir() and any(imgdir.iterdir()) and any(maskdir.iterdir())
            if not prepared: run([sys.executable,"scripts/prepare_tdd.py"])
        run([sys.executable,"scripts/validate_dataset.py","--root","data/tdd"])
        run([sys.executable,"scripts/reproduce_all.py","--config","configs/paper.yaml"])

if __name__=="__main__": main()
