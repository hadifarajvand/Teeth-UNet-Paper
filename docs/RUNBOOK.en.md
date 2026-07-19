# Reproduction Runbook

**Language:** [فارسی / Persian](RUNBOOK.md) | **English**

This repository has two separated execution modes:

1. **Smoke mode** — fast end-to-end validation using the generated bootstrap dataset.
2. **Paper mode** — full reproduction pipeline using the real Tufts Dental Database (TDD).

No unrelated fallback dataset is silently relabeled as TDD.

## 1. Environment setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

GPU is recommended for the 512×512 paper run.

## 2. Download datasets into the cloned repository

Primary command:

```bash
python scripts/download_datasets.py --dataset all
```

Shell wrapper:

```bash
bash download_datasets.sh --dataset all
```

Target directories are always inside this repository:

```text
data/bootstrap_synthetic/
data/tdd_download/
data/tdd/images/
data/tdd/masks/
data/open_reference_download/
```

### TDD only

```bash
python scripts/download_datasets.py --dataset tdd
```

This performs:

```text
acquisition
→ extraction
→ image/mask matching
→ normalization into data/tdd/
→ validation
→ >=900-pair TDD provenance gate
```

### Authorized local TDD archive

```bash
python scripts/download_datasets.py \
  --dataset tdd \
  --archive /absolute/path/to/tufts-dental-database.zip
```

### Force clean re-download

```bash
python scripts/download_datasets.py --dataset tdd --force
```

### Smoke dataset only

```bash
python scripts/download_datasets.py --dataset smoke
```

### Optional open-reference data

```bash
python scripts/download_datasets.py --dataset open-reference
```

## 3. TDD acquisition chain

The repository attempts legitimate sources in sequence:

1. full-TDD Kaggle mirror `iftakharh/tufts-dental-datasetcustomized`;
2. KaggleHub / Kaggle CLI / direct Kaggle API;
3. official Tufts radiograph archive through the hybrid fallback;
4. active radiograph fallback `manarmaged/tufts-radiographs`;
5. verified TDD tooth masks from a public Tufts-derived repository;
6. strict pairing by original numeric ID;
7. minimum 900 matched pairs required.

If Kaggle authentication is required, configure the normal Kaggle API credentials and rerun the same command.

## 4. Smoke simulation

```bash
bash run_smoke.sh
```

or:

```bash
python scripts/run_pipeline.py smoke
```

Outputs:

```text
outputs/smoke/
├── metrics.json
├── history.csv
├── train_manifest.csv
├── validation_manifest.csv
├── test_manifest.csv
├── checkpoints/best_model.pt
└── figures/figure_01...figure_11
```

Smoke metrics validate execution only; they are not paper-reproduction metrics.

## 5. Full paper simulation

```bash
bash run_paper.sh
```

or:

```bash
python scripts/run_pipeline.py paper --download
```

The runner performs:

```text
download TDD into repository/data/
→ normalize to data/tdd/images + data/tdd/masks
→ validate dataset
→ verify >=900 TDD pairs/provenance
→ freeze deterministic manifests
→ train 512×512 U-Net
→ evaluate Dice / IoU / loss
→ save best checkpoint
→ generate Figures 1–11
→ generate PAPER_COMPARISON.md
→ final acceptance check
```

If TDD is already prepared:

```bash
python scripts/run_pipeline.py paper --skip-prepare
```

## 6. Run both modes

```bash
bash run_all.sh
```

or:

```bash
python scripts/run_pipeline.py both --download
```

## 7. Paper configuration hypothesis

From the published pseudocode:

- U-Net
- Binary Cross Entropy
- Adam
- learning rate `0.001`
- 50 epochs
- paper-mode input `512×512`

Reported targets:

```text
Dice ≈ 0.88
IoU  ≈ 0.79
```

The publication does not disclose enough information for bit-for-bit reproduction of exact split IDs, original seed, original checkpoint, complete augmentation parameters, and all preprocessing/post-processing choices.

## 8. Paper outputs

```text
outputs/paper/
├── metrics.json
├── history.csv
├── train_manifest.csv
├── validation_manifest.csv
├── test_manifest.csv
├── PAPER_COMPARISON.md
├── checkpoints/best_model.pt
└── figures/
    ├── figure_01_unet_architecture.png
    ├── ...
    └── figure_11_contour_overlay.png
```

## 9. Acceptance gate

A paper run is user-deliverable only when:

- >=900 real TDD image/mask pairs pass validation;
- train/validation/test manifests exist;
- training completes and best checkpoint exists;
- Dice, IoU, and loss are finite;
- all 11 figures exist;
- `PAPER_COMPARISON.md` exists;
- final acceptance check passes.

```bash
python scripts/acceptance_check.py \
  --output-dir outputs/paper \
  --require-paper-data
```

## 10. Package the deliverable

```bash
python scripts/package_deliverable.py
```

Raw medical datasets are downloaded locally into `data/` and ignored by Git by default, preventing accidental publication of large/controlled medical-image files.
