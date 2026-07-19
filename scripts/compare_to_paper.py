#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

TARGET = {"dice": 0.88, "iou": 0.79}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--metrics', default='outputs/paper/metrics.json')
    ap.add_argument('--out', default='outputs/paper/PAPER_COMPARISON.md')
    args=ap.parse_args()
    p=Path(args.metrics)
    if not p.exists():
        raise SystemExit(f'Metrics not found: {p}')
    m=json.loads(p.read_text())
    rows=[]
    for k,t in TARGET.items():
        a=float(m[k]); diff=a-t; rel=diff/t*100
        rows.append((k.upper(), t, a, diff, rel))
    text=['# Paper vs Reproduction Comparison','',
          '| Metric | Paper target | Reproduction | Abs. difference | Relative difference |',
          '|---|---:|---:|---:|---:|']
    for name,t,a,d,r in rows:
        text.append(f'| {name} | {t:.4f} | {a:.4f} | {d:+.4f} | {r:+.2f}% |')
    text += ['', '## Interpretation', '',
             '- The paper reports approximately Dice ≈ 0.88 and IoU ≈ 0.79.',
             '- Exact point-for-point equality is not asserted unless the original authors’ split, seed, checkpoint, and preprocessing are available.',
             '- This report is generated automatically from the run metrics and must accompany final outputs.']
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text('\n'.join(text)+'\n')
    print(out)
if __name__=='__main__': main()
