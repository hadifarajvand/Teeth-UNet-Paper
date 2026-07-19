# User Deliverable Status

## Delivered

- Full U-Net reproduction codebase.
- Smoke and paper configurations.
- End-to-end runners and operational runbook.
- Automated TDD acquisition chain with official and mirror fallbacks.
- Strict >=900-pair TDD provenance validation.
- Paper-target comparison and final acceptance tooling.
- Executed smoke metrics, history, and deterministic manifests in the repository.
- GitHub workflow definitions for reproducibility environments where Actions are enabled.
- Downloadable delivery ZIP contains the executed smoke checkpoint, all 11 generated smoke figures, original candidate-paper PDF, code, notebook, and documentation.

## Executed smoke verification

- Dice: `0.9171192049980164`
- IoU: `0.846945196390152`
- Loss: `0.43136271834373474`
- Figures: `11/11`

These smoke numbers validate the software pipeline only. They are not represented as the IEEE paper's Tufts Dental Database results.

## Exact paper-run status

The build environment used for this delivery could not retrieve the 1,000 Tufts radiograph bytes from the upstream Tufts/Kaggle dataset hosts. Public GitHub projects expose real TDD tooth masks and split metadata but deliberately exclude the patient radiographs.

The repository therefore does not fabricate an “exact paper run.” It now attempts all legitimate acquisition routes automatically:

1. cited full-TDD Kaggle mirror;
2. official Tufts `Radiographs.zip`;
3. active Tufts radiograph Kaggle fallback;
4. verified real TDD tooth masks;
5. strict original numeric-ID pairing;
6. >=900-pair provenance gate.

Paper mode is considered complete only after real TDD provenance, completed training/checkpoint, finite metrics, all 11 figures, generated paper comparison, and acceptance-check success.
