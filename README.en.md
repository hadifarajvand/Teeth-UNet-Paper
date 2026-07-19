# IEEE AIIoT 2024 — U-Net Teeth Segmentation Reimplementation

**Language:** [فارسی / Persian](README.md) | **English**

Target paper:

**Rohini Joshi, “Segmentation of Teeth in Panoramic X-ray Image Using U-net Algorithm,” IEEE AIIoT 2024.**

This repository is a reproducible, user-deliverable implementation with two separated modes:

- **Smoke mode:** fast end-to-end software validation with a bundled/generated synthetic dataset.
- **Paper mode:** full Tufts Dental Database (TDD) acquisition, preparation, validation, training, evaluation, and Figures 1–11 generation.

> The repository never silently substitutes another dental dataset and calls it TDD.

## 1. Clone and install

```bash
git clone https://github.com/hadifarajvand/Teeth-UNet-Paper.git
cd Teeth-UNet-Paper

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Download datasets directly into this repository

The main dataset command is:

```bash
./download_datasets.sh --dataset all
```

Equivalent Python command:

```bash
python scripts/download_datasets.py --dataset all
```

All downloaded/generated data is stored under this repository's `data/` directory:

```text
data/
├── bootstrap_synthetic/        # smoke dataset
├── tdd_download/               # raw/source TDD download material
├── tdd/                        # normalized paper dataset used by training
│   ├── images/
│   └── masks/
└── open_reference_download/    # optional external/reference dataset
```

### Download only the paper dataset (TDD)

```bash
./download_datasets.sh --dataset tdd
```

This command automatically performs:

```text
TDD acquisition
→ extraction
→ image/mask pairing
→ normalization into data/tdd/
→ dataset validation
→ >=900-pair provenance validation
```

### Download/generate only the smoke dataset

```bash
./download_datasets.sh --dataset smoke
```

### Download the optional open-reference dataset

```bash
./download_datasets.sh --dataset open-reference
```

### Force a clean re-download

```bash
./download_datasets.sh --dataset tdd --force
```

### Use an authorized local TDD archive

```bash
./download_datasets.sh \
  --dataset tdd \
  --archive /absolute/path/to/tufts-dental-database.zip
```

## 3. TDD acquisition chain

The downloader tries legitimate Tufts/TDD routes and fails explicitly rather than substituting unrelated data:

1. cited full-TDD Kaggle mirror: `iftakharh/tufts-dental-datasetcustomized`;
2. KaggleHub / Kaggle CLI / direct Kaggle API;
3. official Tufts radiograph archive through the hybrid fallback;
4. active Tufts radiograph mirror: `manarmaged/tufts-radiographs`;
5. verified real TDD tooth masks from a public Tufts-derived repository;
6. strict matching by original numeric image ID;
7. minimum **900 matched image/mask pairs** required before a paper run is accepted.

For Kaggle-authenticated access, configure your normal Kaggle API credentials before running the downloader.

## 4. Smoke simulation

```bash
./run_smoke.sh
```

or:

```bash
python scripts/run_pipeline.py smoke
```

Pipeline:

```text
bootstrap dataset
→ U-Net training
→ Dice / IoU
→ checkpoint
→ prediction
→ morphology
→ connected components
→ contours / measurements
→ Figures 1–11
```

Previously executed smoke validation metrics:

- Dice: `0.9171192049980164`
- IoU: `0.846945196390152`
- Loss: `0.43136271834373474`

These numbers validate the software pipeline only. They are **not** claimed as the paper's TDD results.

## 5. Full paper simulation

The simplest command is:

```bash
./run_paper.sh
```

Equivalent:

```bash
python scripts/run_pipeline.py paper --download
```

The runner now performs the complete chain itself:

```text
download TDD into repository/data/
→ normalize to data/tdd/images + data/tdd/masks
→ validate dataset
→ validate >=900 TDD pairs/provenance
→ freeze deterministic manifests
→ train 512×512 U-Net
→ evaluate loss, Dice and IoU
→ save best checkpoint
→ generate Figures 1–11
→ compare against paper targets
→ run final acceptance gate
```

## 6. Run smoke + paper

```bash
./run_all.sh
```

or:

```bash
python scripts/run_pipeline.py both --download
```

## 7. Paper configuration reproduced from the publication

Primary paper-mode hypothesis:

- U-Net
- Binary Cross Entropy
- Adam
- learning rate: `0.001`
- epochs: `50`
- paper-mode input: `512×512`

Reported paper targets:

- Dice ≈ `0.88` (evaluation screenshot ≈ `0.8837`)
- IoU ≈ `0.79` (evaluation screenshot ≈ `0.7986`)

The publication does not provide every author-side detail required for bit-for-bit identity, such as the exact split IDs, original random seed, checkpoint, complete augmentation configuration, and all preprocessing/post-processing parameters. Therefore the repository reports paper-faithful reproduction honestly and does not fabricate exact equality.

## 8. Outputs

Smoke outputs:

```text
outputs/smoke/
├── metrics.json
├── history.csv
├── train_manifest.csv
├── validation_manifest.csv
├── test_manifest.csv
├── checkpoints/best_model.pt
└── figures/
    ├── figure_01_unet_architecture.png
    ├── ...
    └── figure_11_contour_overlay.png
```

Paper outputs after a successful real-TDD run:

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

## 9. Paper-mode acceptance gate

`outputs/paper/` is user-deliverable only when all conditions pass:

1. at least 900 verified TDD radiograph/tooth-mask pairs;
2. train/validation/test manifests saved;
3. training completed and best checkpoint exists;
4. finite loss, Dice and IoU;
5. all 11 required figures exist;
6. `PAPER_COMPARISON.md` exists;
7. final acceptance checker passes.

Manual verification command:

```bash
python scripts/acceptance_check.py \
  --output-dir outputs/paper \
  --require-paper-data
```

## 10. Useful commands

```bash
# install
pip install -r requirements.txt

# download all datasets into repository/data/
./download_datasets.sh --dataset all

# only TDD
./download_datasets.sh --dataset tdd

# smoke
make smoke

# full paper
make paper

# both
make all
```

## Documentation

- `README.md` — primary Persian README.
- `README.en.md` — English README.
- `docs/RUNBOOK.md` — operational runbook.
- `docs/DATASETS.md` — data provenance.
- `docs/TDD_ACQUISITION.md` — TDD acquisition chain.
- `docs/PAPER_OUTPUT_SPEC.md` — figure/metric fidelity contract.
- `docs/REPRODUCIBILITY_REPORT.md` — reported vs inferred configuration.
- `USER_DELIVERABLE_STATUS.md` — exact current delivery status.
