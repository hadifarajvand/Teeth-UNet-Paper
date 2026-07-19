#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',default='outputs/paper')
    ap.add_argument('--require-paper-data',action='store_true')
    args=ap.parse_args()
    out=Path(args.output_dir)
    required=[out/'metrics.json',out/'history.csv',out/'train_manifest.csv',out/'validation_manifest.csv',out/'test_manifest.csv',out/'checkpoints/best_model.pt']
    required += [out/'figures'/f'figure_{i:02d}_{name}.png' for i,name in [
      (1,'unet_architecture'),(2,'workflow'),(3,'radiograph_and_mask'),(4,'iou_diagram'),
      (5,'dice_training_curve'),(6,'iou_training_curve'),(7,'test_radiograph'),
      (8,'postprocessing_outputs'),(9,'final_outputs'),(10,'pixel_measurements'),(11,'contour_overlay')]]
    missing=[str(p) for p in required if not p.exists()]
    if missing:
        print('FAIL: missing artifacts:'); print('\n'.join(' - '+x for x in missing)); return 2
    m=json.loads((out/'metrics.json').read_text())
    for k in ('dice','iou','loss'):
        if k not in m or not isinstance(m[k],(int,float)):
            print(f'FAIL: invalid metric {k}'); return 3
    if args.require_paper_data and m.get('mode')!='paper':
        print('FAIL: output is not marked as paper mode'); return 4
    print('PASS: deliverable acceptance checks completed')
    print(json.dumps(m,indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
