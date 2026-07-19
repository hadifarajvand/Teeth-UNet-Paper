# Reproducibility Report

## Current status

| Component | Status |
|---|---|
| Reimplementation code | Complete |
| Smoke dataset | Bundled |
| Smoke execution | Complete |
| Smoke checkpoint | Complete |
| Figures 1–11 smoke outputs | Complete |
| TDD automated downloader | Complete |
| TDD normalizer/pair validator | Complete |
| Full paper runner | Complete |
| Actual 1,000-image TDD bytes | Not acquired in this sandbox |
| Exact TDD full training run | Pending dataset access |

## Why the TDD full run is pending

This environment has neither:
- unrestricted outbound dataset download access, nor
- Kaggle credentials / an approved Tufts archive.

The target database is not replaced by another dataset.

The original TDD publication states that access/download permission is obtained through the Tufts project website. Later peer-reviewed work cites a Kaggle mirror of the 1,000-image dataset. The included downloader supports that mirror automatically when executed in an internet-enabled environment.

## Paper-derived configuration

The candidate paper pseudocode explicitly shows:

```text
Binary Cross Entropy
Adam
learning rate = 0.001
50 epochs
```

Paper mode uses these values as the primary hypothesis and 512×512 input.

## Missing information in the paper

The publication does not fully disclose:

- exact train/validation/test image IDs;
- random seed;
- definitive batch size;
- exact augmentation ranges/probabilities;
- exact normalization/contrast/denoising settings;
- exact threshold/post-processing settings;
- original model checkpoint;
- raw training history.

Therefore even with TDD, this is a method-faithful reproduction unless the authors supply those missing assets.

## Executed smoke result

The bundled smoke run exists only to prove the pipeline works end to end. Its metrics must not be compared as if they were TDD reproduction metrics.

See:

```text
outputs/smoke/metrics.json
outputs/smoke/history.csv
outputs/smoke/figures/
```
