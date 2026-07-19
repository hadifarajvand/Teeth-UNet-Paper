#!/usr/bin/env python3
"""Download and prepare all datasets INSIDE this repository.

Targets are always relative to the repository root:
  data/bootstrap_synthetic/   -> generated smoke dataset
  data/tdd_download/          -> raw downloaded Tufts material (temporary/source)
  data/tdd/                   -> prepared paper dataset used by configs/paper.yaml
  data/open_reference_download/ -> optional open reference raw material

The script never silently substitutes a different dataset for TDD.

Examples:
  python scripts/download_datasets.py --dataset all
  python scripts/download_datasets.py --dataset tdd
  python scripts/download_datasets.py --dataset smoke
  python scripts/download_datasets.py --dataset tdd --archive /path/to/tdd.zip
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*parts: str) -> None:
    cmd = [str(x) for x in parts]
    print("\n>>>", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def has_files(path: Path) -> bool:
    return path.is_dir() and any(path.iterdir())


def ensure_smoke(force: bool) -> None:
    root = ROOT / "data/bootstrap_synthetic"
    if force and root.exists():
        shutil.rmtree(root)
    images, masks = root / "images", root / "masks"
    if has_files(images) and has_files(masks):
        print(f"[ok] Smoke dataset already exists: {root.relative_to(ROOT)}")
        return
    run(sys.executable, "scripts/generate_bootstrap_dataset.py", "--root", "data/bootstrap_synthetic", "--count", "48")
    if not (has_files(images) and has_files(masks)):
        raise SystemExit("Smoke dataset generation failed.")
    print(f"[ok] Smoke dataset prepared in: {root.relative_to(ROOT)}")


def ensure_tdd(force: bool, archive: str | None) -> None:
    prepared = ROOT / "data/tdd"
    raw = ROOT / "data/tdd_download"

    if force:
        if prepared.exists():
            shutil.rmtree(prepared)
        if raw.exists():
            shutil.rmtree(raw)

    images, masks = prepared / "images", prepared / "masks"
    if not (has_files(images) and has_files(masks)):
        cmd = [sys.executable, "scripts/download_all_data.py", "--dataset", "tdd"]
        if archive:
            cmd += ["--archive", archive]
        run(*cmd)

        # Normalize the downloaded/raw TDD tree into data/tdd/images + data/tdd/masks.
        run(sys.executable, "scripts/prepare_tdd.py", "--source", "data/tdd_download", "--dest", "data/tdd")

    # Strict dataset checks used before every paper run.
    run(sys.executable, "scripts/validate_dataset.py", "--root", "data/tdd")
    run(sys.executable, "scripts/verify_tdd_provenance.py", "--root", "data/tdd", "--min-pairs", "900")
    print("[ok] TDD is downloaded, normalized and validated inside data/tdd/")


def ensure_open_reference(force: bool) -> None:
    out = ROOT / "data/open_reference_download"
    if force and out.exists():
        shutil.rmtree(out)
    run(sys.executable, "scripts/download_all_data.py", "--dataset", "open-reference", *( ["--force"] if force else [] ))
    print("[ok] Optional open-reference raw data is under data/open_reference_download/")


def main() -> None:
    ap = argparse.ArgumentParser(description="Download datasets directly into this repository's data/ directory.")
    ap.add_argument("--dataset", choices=["smoke", "tdd", "open-reference", "all"], default="all")
    ap.add_argument("--archive", help="Optional authorized local Tufts/TDD archive.")
    ap.add_argument("--force", action="store_true", help="Delete existing target data and download/regenerate again.")
    args = ap.parse_args()

    (ROOT / "data").mkdir(exist_ok=True)

    if args.dataset in ("smoke", "all"):
        ensure_smoke(args.force)
    if args.dataset in ("tdd", "all"):
        ensure_tdd(args.force, args.archive)
    if args.dataset in ("open-reference", "all"):
        ensure_open_reference(args.force)

    print("\nDataset setup complete.")
    print(f"Repository root: {ROOT}")
    print("Paper dataset path: data/tdd/")
    print("Smoke dataset path: data/bootstrap_synthetic/")


if __name__ == "__main__":
    main()
