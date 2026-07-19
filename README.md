# IEEE AIIoT 2024 — U-Net Teeth Segmentation Reimplementation

Reimplementation target:

**Rohini Joshi, “Segmentation of Teeth in Panoramic X-ray Image Using U-net Algorithm,” IEEE AIIoT 2024.**

This repository is a reproducible delivery package with two strictly separated execution modes.

## 1. Smoke simulation — executed and verified

```bash
./run_smoke.sh
```

Pipeline:

```text
bootstrap data → U-Net training → Dice/IoU → checkpoint
→ prediction → morphology → connected components → contours
→ pixel measurements → Figures 1–11
```

Executed smoke metrics committed as text records:

- Dice: `0.9171192049980164`
- IoU: `0.846945196390152`
- Loss: `0.43136271834373474`

The downloadable user-deliverable ZIP contains the executed smoke checkpoint and all 11 generated PNG figures. The GitHub source repository can regenerate them deterministically with the smoke runner.

**Smoke results validate the software only. They are not represented as the IEEE paper's TDD reproduction.**

## 2. Full paper simulation — Tufts Dental Database

One command:

```bash
./run_paper.sh
```

Equivalent:

```bash
python scripts/run_pipeline.py paper --download
```

The acquisition chain is autonomous and refuses to silently substitute another dental dataset:

1. cited full-TDD Kaggle mirror `iftakharh/tufts-dental-datasetcustomized`;
2. official Tufts radiograph archive `https://tdd.ece.tufts.edu/Tufts_Dental_Database/Radiographs.zip`;
3. active radiograph fallback `manarmaged/tufts-radiographs`;
4. verified real TDD tooth masks from `gopimeruva/Dental_Xray_Anamoly_Detection/TUFTS-project/Segmentation/teeth_mask/`;
5. strict pairing by original numeric image ID;
6. minimum `900` matched-pair provenance gate.

Then:

```text
acquire TDD
→ normalize image/mask pairs
→ verify provenance
→ freeze deterministic manifests
→ train 512×512 U-Net
→ evaluate Dice/IoU
→ save best checkpoint
→ generate Figures 1–11
→ compare against paper targets
→ acceptance gate
```

An authorized local archive is also supported:

```bash
python scripts/run_pipeline.py paper --archive /absolute/path/to/tdd.zip
```

## Paper configuration hypothesis

From the candidate paper's published pseudocode:

- U-Net
- Binary Cross Entropy
- Adam
- learning rate `0.001`
- `50` epochs

Paper mode defaults to 512×512 input. The publication does not disclose the exact original split IDs, seed, checkpoint, complete augmentation parameters, or every preprocessing/post-processing choice; therefore exact point-for-point identity cannot be claimed without those author-side assets.

Reported paper targets:

- Dice ≈ `0.88` (evaluation screenshot ≈ `0.8837`)
- IoU ≈ `0.79` (evaluation screenshot ≈ `0.7986`)

## Paper-mode acceptance gate

`outputs/paper/` is user-deliverable only when all are true:

1. at least 900 verified TDD radiograph/tooth-mask pairs;
2. train/validation/test manifests saved;
3. completed training and best checkpoint;
4. finite loss, Dice, and IoU;
5. all 11 required figures present;
6. `PAPER_COMPARISON.md` generated;
7. `scripts/acceptance_check.py --output-dir outputs/paper --require-paper-data` passes.

## Key commands

```bash
# environment
pip install -r requirements.txt

# smoke
make smoke

# full paper run
make paper

# everything
make all
```

## Documentation

- `docs/RUNBOOK.md` — operational procedure.
- `docs/DATASETS.md` — data provenance.
- `docs/TDD_ACQUISITION.md` — autonomous exact-data acquisition chain.
- `docs/PAPER_OUTPUT_SPEC.md` — figure/metric fidelity contract.
- `docs/REPRODUCIBILITY_REPORT.md` — reported vs inferred configuration.
- `USER_DELIVERABLE_STATUS.md` — exact current delivery status.

## Scientific integrity

A run on synthetic data or a different panoramic dataset is **not** a reproduction of the paper. The repository deliberately fails rather than relabeling another dataset as TDD or fabricating paper-identical figures/metrics.
