# Reproduction Runbook

This repository supports **two explicitly separated execution modes**:

1. **Smoke mode** — fast, zero-credential, end-to-end validation using the bundled synthetic dental-style dataset.
2. **Paper mode** — full U-Net reproduction using the real Tufts Dental Database (TDD) tooth images/masks.

No fallback dataset is silently substituted for TDD.

---

## 1. Environment setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

GPU is strongly recommended for the 512×512 paper run.

Verify:

```bash
python - <<'PY'
import torch
print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
PY
```

---

# 2. Smoke simulation

This requires no external dataset or credentials.

```bash
./run_smoke.sh
```

or:

```bash
python scripts/run_pipeline.py smoke
```

Pipeline:

```text
bundled synthetic pairs
→ deterministic split
→ compact U-Net training
→ Dice + IoU
→ prediction masks
→ morphology / connected components / contours
→ Figures 1–11
→ checkpoint + metrics + manifests
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

The smoke scores prove execution only. They are **not** paper-reproduction scores.

---

# 3. Acquire the full paper dataset (TDD)

The paper identifies the **Tufts Dental Database**, approximately 1,000 panoramic radiographs with expert tooth masks.

The repository uses this acquisition priority:

### Route A — Kaggle mirror, automated

Later peer-reviewed work cites:

```text
iftakharh/tufts-dental-datasetcustomized
```

Run:

```bash
python scripts/download_all_data.py --dataset tdd
```

The downloader tries, in order:

1. `kagglehub`
2. Kaggle CLI
3. Kaggle public archive API

For Kaggle credentials, use either the normal Kaggle API token setup or environment-supported authentication.

Typical Kaggle token setup:

```bash
mkdir -p ~/.kaggle
cp /path/to/kaggle.json ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json
```

Then rerun:

```bash
python scripts/download_all_data.py --dataset tdd
```

### Route B — Official Tufts access

The official TDD source may require a dataset access/download-permission request.

After receiving an authorized archive:

```bash
python scripts/download_all_data.py --dataset tdd --archive /absolute/path/to/tufts-dental-database.zip
```

### Route C — Already downloaded data

Place the dataset under any temporary folder, then prepare it:

```bash
python scripts/prepare_tdd.py --source /path/to/extracted/tdd --dest data/tdd
```

Canonical final layout:

```text
data/tdd/
├── images/
│   ├── 0000.jpg
│   └── ...
└── masks/
    ├── 0000.png
    └── ...
```

---

# 4. Normalize and validate TDD

If the automated downloader placed raw files in `data/tdd_download/`:

```bash
python scripts/prepare_tdd.py
```

Then:

```bash
python scripts/validate_dataset.py --root data/tdd
```

Do **not** start paper training unless pairing validation succeeds.

The preparation script writes:

```text
outputs/tdd_pairing_report.csv
```

Inspect this report if the number of detected pairs is unexpectedly low.

---

# 5. Full paper simulation

One command:

```bash
./run_paper.sh
```

Equivalent:

```bash
python scripts/run_pipeline.py paper --download
```

If TDD is already prepared:

```bash
python scripts/run_pipeline.py paper --skip-prepare
```

If you have a local authorized archive:

```bash
python scripts/run_pipeline.py paper --archive /path/to/tdd.zip
```

The full run performs:

```text
TDD acquisition
→ TDD preparation
→ image/mask pairing validation
→ deterministic train/validation/test manifests
→ 512×512 U-Net
→ BCE loss
→ Adam optimizer
→ lr = 0.001
→ up to 50 epochs
→ best checkpoint
→ Dice / IoU
→ post-processing
→ all 11 paper-style figures
```

Outputs:

```text
outputs/paper/
├── metrics.json
├── history.csv
├── *_manifest.csv
├── checkpoints/best_model.pt
└── figures/
    ├── figure_01_unet_architecture.png
    ├── ...
    └── figure_11_contour_overlay.png
```

---

# 6. Run smoke + paper together

```bash
./run_all.sh
```

or:

```bash
python scripts/run_pipeline.py both --download
```

Smoke executes first. Paper starts only after TDD is acquired and validated.

---

# 7. Paper target values

The IEEE candidate reports approximately:

```text
Dice ≈ 0.88
IoU  ≈ 0.79
```

The repository does **not** force training to hit those values.

The original paper does not publish enough information for bit-for-bit reproduction of:

- exact split IDs;
- random seed;
- definitive batch size;
- exact augmentation probabilities/ranges;
- exact preprocessing parameters;
- original checkpoint;
- raw training history.

Therefore compare honestly:

```text
paper reported
vs
our TDD execution
vs
absolute difference
vs
relative difference
```

Do not tune solely to match the published decimals.

---

# 8. Figure map

| Figure | Generated from |
|---|---|
| 1 | U-Net architecture schematic |
| 2 | workflow schematic |
| 3 | real radiograph + ground-truth tooth mask |
| 4 | IoU illustration |
| 5 | actual training/validation Dice history |
| 6 | actual training/validation IoU history |
| 7 | test panoramic radiograph |
| 8 | predicted mask + contours + connected components |
| 9 | input / GT / prediction / overlay |
| 10 | boxes and pixel measurements |
| 11 | contour overlay |

Figures 3 and 5–11 are data/run dependent in paper mode.

---

# 9. Dataset downloader scripts

Primary:

```bash
python scripts/download_all_data.py --dataset tdd
```

Optional open-reference dataset, which is **not TDD**:

```bash
python scripts/download_all_data.py --dataset open-reference
```

Download all supported sources:

```bash
python scripts/download_all_data.py --dataset all
```

The open-reference data exists for external checks and debugging only. It must never be reported as the paper's Tufts dataset.

---

# 10. Repackage after a full run

```bash
python scripts/package_deliverable.py
```

This creates a ZIP containing code, runbooks, current outputs, manifests, and any data present in the repository.

For GitHub, large raw datasets/checkpoints should normally be stored using Git LFS or downloaded through the included scripts rather than committed directly.

---

# 11. Definition of done

A full paper execution is complete only when all are true:

- TDD acquisition is confirmed;
- image/mask pairing validation passes;
- paper train/val/test manifests are saved;
- training completes or resumes to completion;
- a best checkpoint exists;
- Dice and IoU are finite;
- all 11 figures exist under `outputs/paper/figures`;
- `outputs/paper/metrics.json` is present;
- the deliverable ZIP passes integrity testing.
