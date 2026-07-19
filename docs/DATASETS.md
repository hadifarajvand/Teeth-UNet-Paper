# Dataset Sources and Acquisition

## Target dataset: Tufts Dental Database (TDD)

The candidate IEEE paper states that it uses the Tufts Dental Database.

The canonical TDD publication/documentation describes:
- approximately 1,000 panoramic dental radiographs;
- expert labeling of teeth and abnormalities;
- tooth masks among the released components.

The original database publication states that researchers obtain download permission through the Tufts project site:

```text
https://tdd.ece.tufts.edu/
```

A later peer-reviewed paper explicitly cites this Kaggle redistribution:

```text
https://www.kaggle.com/datasets/iftakharh/tufts-dental-datasetcustomized
```

Repository downloader:

```bash
python scripts/download_all_data.py --dataset tdd
```

The script tries KaggleHub, Kaggle CLI, direct Kaggle archive access, or an explicitly supplied authorized archive.

### Authorized archive route

```bash
python scripts/download_all_data.py --dataset tdd --archive /path/to/tufts-dental-database.zip
python scripts/prepare_tdd.py
python scripts/validate_dataset.py --root data/tdd
```

Canonical prepared layout:

```text
data/tdd/
├── images/
└── masks/
```

## Optional open reference dataset

The repository also documents a separate 116-image panoramic dataset associated with the Helli/Abdi line of work.

It is **not TDD** and must not be reported as the paper dataset.

Sources include:
- Mendeley Data identifier `hxt48yk462`;
- Hugging Face dataset `SerdarHelli/SegmentationOfTeethPanoramicXRayImages`.

Use only for external validation/debugging:

```bash
python scripts/download_all_data.py --dataset open-reference
```

## Bundled smoke dataset

`data/bootstrap_synthetic/` is procedurally generated and contains no patient data.

Purpose:
- verify installation;
- verify U-Net training;
- verify metrics;
- verify checkpointing;
- verify all 11 figure generators.

It is never used as evidence that the IEEE paper's numerical results were reproduced.
