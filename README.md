# IEEE AIIoT 2024 — U-Net Teeth Segmentation Reimplementation

Reimplementation target:

**Rohini Joshi, “Segmentation of Teeth in Panoramic X-ray Image Using U-net Algorithm,” IEEE AIIoT 2024.**

This repository is designed as a reproducible delivery package with two execution modes.

## 1. Smoke simulation — bundled and already executed

```bash
./run_smoke.sh
```

Uses the bundled synthetic dental-style dataset only to verify the complete pipeline:

```text
data → U-Net → training → Dice/IoU → prediction
→ morphology → connected components → contours
→ pixel measurements → Figures 1–11
```

Actual executed smoke outputs are in:

```text
outputs/smoke/
```

The shipped smoke checkpoint, metrics, history, manifests, and 11 figures are real outputs of the included code.

**Smoke metrics are not claimed as paper reproduction metrics.**

## 2. Full paper simulation — Tufts Dental Database

One command:

```bash
./run_paper.sh
```

Equivalent:

```bash
python scripts/run_pipeline.py paper --download
```

The script attempts to acquire the target TDD dataset from the published Kaggle mirror:

```text
iftakharh/tufts-dental-datasetcustomized
```

Then automatically:

```text
download TDD
→ normalize images/masks
→ validate pairing
→ freeze split manifests
→ train 512×512 U-Net
→ evaluate Dice/IoU
→ save checkpoint
→ generate Figures 1–11
```

If you obtained the official TDD archive manually:

```bash
python scripts/run_pipeline.py paper --archive /absolute/path/to/tdd.zip
```

If TDD is already prepared:

```bash
python scripts/run_pipeline.py paper --skip-prepare
```

## Full dataset acquisition

Primary:

```bash
python scripts/download_all_data.py --dataset tdd
```

The downloader tries:

1. `kagglehub`
2. Kaggle CLI
3. Kaggle public archive API
4. an explicitly supplied authorized local archive

It never silently substitutes another dataset.

## Run everything

```bash
./run_all.sh
```

This runs smoke first, then attempts the full TDD paper run.

## Paper configuration hypothesis

From the candidate paper’s published pseudocode:

- U-Net
- Binary Cross Entropy
- Adam
- learning rate `0.001`
- `50` epochs

Paper mode defaults to 512×512 input. The paper does not publish all details required for bit-identical reproduction, including exact split IDs, seed, original checkpoint, complete augmentation parameters, and several preprocessing choices.

## Output layout

```text
outputs/
├── smoke/        # executed and bundled
└── paper/        # populated after successful TDD run
```

Each completed run contains:

```text
metrics.json
history.csv
train_manifest.csv
validation_manifest.csv
test_manifest.csv
checkpoints/best_model.pt
figures/
  figure_01_unet_architecture.png
  ...
  figure_11_contour_overlay.png
```

## Documentation

- `docs/RUNBOOK.md` — complete operational procedure.
- `docs/DATASETS.md` — dataset provenance and acquisition.
- `docs/REPRODUCIBILITY_REPORT.md` — what is exact vs inferred.
- `outputs/paper/README.md` — current exact-paper-run status.
- `DELIVERABLE_INDEX.md` — pack inventory.

## Important scientific honesty

A completed run on a different dataset is **not** a full reproduction of the paper. The full paper run is considered complete only when the actual Tufts Dental Database is acquired and `outputs/paper/` is generated from it.
