# Full Paper Run Status

## Current execution state

- **Smoke run:** COMPLETED and bundled under `outputs/smoke/`.
- **Paper-mode code path:** IMPLEMENTED.
- **Exact TDD full run:** NOT EXECUTED IN THIS BUILD because the target 1,000-image Tufts Dental Database could not be retrieved from this execution runtime without external dataset authorization/credentials.

This is not a compute problem. It is a dataset-access problem.

The repository includes automated acquisition support for the Kaggle mirror `iftakharh/tufts-dental-datasetcustomized` plus an authorized local archive route.

## Full-run command

```bash
./run_paper.sh
```

or:

```bash
python scripts/run_pipeline.py paper --download
```

Once TDD is acquired, this command performs acquisition, normalization, pairing validation, deterministic splits, 512×512 U-Net training, checkpoint saving, Dice/IoU evaluation, and Figures 1–11 generation.

No synthetic or alternate dataset is labeled as TDD.
