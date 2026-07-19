# Executed Output Summary

The bundled smoke reimplementation completed successfully.

| Metric | Smoke execution | Paper-reported target |
|---|---:|---:|
| Dice | 0.9171 | ~0.88 |
| IoU | 0.8469 | ~0.79 |

**Do not interpret the numerical proximity as reproduction evidence.** The smoke dataset is procedurally generated.
The value of this run is that the complete code path is verified: data loading, U-Net training,
checkpointing, Dice/IoU evaluation, segmentation, connected components, contours, measurements,
and Figures 1–11 export.
