# Paper Output Fidelity Specification

Target publication: Rohini Joshi, **“Segmentation of Teeth in Panoramic X-ray Image Using U-net Algorithm,” IEEE AIIoT 2024**, DOI `10.1109/AIIoT58432.2024.10574786`.

## Acceptance objective

The delivery must reproduce the paper workflow and output set using the Tufts Dental Database (TDD), not a substitute dataset.

Reported numerical targets:

- Dice: approximately **0.88** (evaluation screenshot approximately 0.8837)
- IoU: approximately **0.79** (evaluation screenshot approximately 0.7986)
- BCE loss, Adam optimizer, learning rate `0.001`, paper pseudocode `50` epochs

## Required figures

1. U-Net architecture schematic
2. Proposed-system workflow
3. Panoramic radiograph with corresponding expert tooth mask
4. IoU concept illustration
5. Training/validation Dice curve (paper caption calls this “accuracy,” but plotted metric is Dice)
6. Training/validation IoU curve
7. Panoramic test radiograph
8. Predicted binary mask, contour extraction, and connected components
9. Final segmentation comparison/overlay
10. Tooth/component bounding boxes and pixel measurements
11. Contour overlay on the radiograph

## Exactness policy

- Figures 1, 2, and 4 can be recreated deterministically in content.
- Figures 3 and 7–11 should use the same TDD source image IDs as the publication whenever those IDs can be recovered; otherwise the closest verified TDD examples must be documented.
- Figures 5–6 must be generated from actual training history, never hand-drawn to imitate the paper.
- Numerical proximity to the paper is reported automatically by `scripts/compare_to_paper.py`.
- Exact point-for-point identity is not claimed unless the authors’ original split, random seed, checkpoint, preprocessing parameters, and training log are available.

## Paper-mode completion gate

A run is user-deliverable only if:

1. TDD provenance validation finds at least 900 paired radiograph/tooth-mask IDs.
2. Train/validation/test manifests are frozen and included.
3. Training completes and a best checkpoint exists.
4. Dice, IoU, and loss are finite.
5. All eleven figure files exist.
6. `PAPER_COMPARISON.md` is generated.
7. `scripts/acceptance_check.py --output-dir outputs/paper --require-paper-data` passes.

Smoke outputs are pipeline-validation artifacts only and must never be delivered as the paper reproduction.
