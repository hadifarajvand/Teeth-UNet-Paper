# Tufts Dental Database Acquisition Chain

The repository uses a strict, ordered acquisition chain and never silently substitutes a different dental dataset.

## Route 1 — cited full-TDD Kaggle mirror

Dataset slug:

```text
iftakharh/tufts-dental-datasetcustomized
```

This mirror is cited as a 1,000-image Tufts dental dataset with teeth segmentation in later peer-reviewed literature.

## Route 2 — official Tufts radiographs + verified TDD tooth masks

Original radiograph archive path published in peer-reviewed literature:

```text
https://tdd.ece.tufts.edu/Tufts_Dental_Database/Radiographs.zip
```

Verified public TDD-derived tooth-mask source:

```text
https://github.com/gopimeruva/Dental_Xray_Anamoly_Detection
TUFTS-project/Segmentation/teeth_mask/
```

The repository contains real mask files across the numeric ID range; IDs `1.jpg`, `95.jpg`, and `1000.jpg` were independently verified during construction of this reproduction pack.

`python scripts/download_tdd_hybrid.py`:

1. attempts the official Tufts radiograph archive;
2. falls back to active Kaggle `manarmaged/tufts-radiographs` if needed;
3. sparse-clones only the verified `teeth_mask` directory;
4. pairs radiographs and masks strictly by original numeric ID;
5. refuses to succeed with fewer than 900 matched IDs;
6. writes `HYBRID_PROVENANCE.json`.

## Route 3 — authorized local Tufts archive

```bash
python scripts/run_pipeline.py paper --archive /path/to/authorized-tdd.zip
```

## One-command paper acquisition/run

```bash
./run_paper.sh
```

or:

```bash
python scripts/run_pipeline.py paper --download
```

The full-paper GitHub workflows use the same acquisition chain and commit either the validated paper outputs or explicit upstream-host acquisition evidence.
