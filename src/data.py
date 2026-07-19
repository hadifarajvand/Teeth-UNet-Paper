from __future__ import annotations
from pathlib import Path
import random
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset

EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}

def paired_files(root: str | Path):
    root = Path(root)
    images_dir, masks_dir = root/"images", root/"masks"
    images = {p.stem: p for p in images_dir.iterdir() if p.suffix.lower() in EXTS}
    masks = {p.stem: p for p in masks_dir.iterdir() if p.suffix.lower() in EXTS}
    keys = sorted(set(images) & set(masks))
    if not keys:
        raise FileNotFoundError(f"No paired image/mask files found under {root}")
    return [(images[k], masks[k]) for k in keys]

def split_pairs(pairs, seed=42, ratios=(0.7,0.15,0.15)):
    pairs = list(pairs)
    rng = random.Random(seed)
    rng.shuffle(pairs)
    n = len(pairs)
    n_train = max(1, int(n*ratios[0]))
    n_val = max(1, int(n*ratios[1]))
    if n_train+n_val >= n:
        n_train = max(1,n-2); n_val=1
    return pairs[:n_train], pairs[n_train:n_train+n_val], pairs[n_train+n_val:]

class TeethDataset(Dataset):
    def __init__(self, pairs, size=(512,512)):
        self.pairs = list(pairs)
        self.size = (int(size[1]), int(size[0]))
    def __len__(self): return len(self.pairs)
    def __getitem__(self, idx):
        ip, mp = self.pairs[idx]
        img = Image.open(ip).convert("L").resize(self.size, Image.Resampling.BILINEAR)
        mask = Image.open(mp).convert("L").resize(self.size, Image.Resampling.NEAREST)
        x = np.asarray(img, np.float32)/255.0
        y = (np.asarray(mask, np.float32)>127).astype(np.float32)
        return torch.from_numpy(x[None]), torch.from_numpy(y[None]), ip.name
