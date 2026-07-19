# Deliverable Index

## Included and executed

`outputs/smoke/` contains a completed end-to-end run:

- `metrics.json`
- `history.csv`
- deterministic train/validation/test manifests
- trained `best_model.pt`
- Figures 1–11
- output contact sheets

## Full paper execution path

- `run_paper.sh`
- `scripts/run_pipeline.py`
- `scripts/download_all_data.py`
- `scripts/prepare_tdd.py`
- `scripts/validate_dataset.py`
- `configs/paper.yaml`

The full run path is:

```text
TDD download
→ pairing preparation
→ validation
→ 512×512 U-Net training
→ checkpoint
→ Dice/IoU
→ Figures 1–11
```

## Current blocker recorded transparently

`outputs/paper/README.md` records why an exact TDD run is not bundled yet: the current execution runtime has no approved Tufts download or Kaggle credentials, and the official TDD access process may require download permission.

## Main documentation

- `README.md`
- `docs/RUNBOOK.md`
- `docs/DATASETS.md`
- `docs/REPRODUCIBILITY_REPORT.md`
- `docs/SOURCES.md`
