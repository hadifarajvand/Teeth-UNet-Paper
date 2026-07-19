from __future__ import annotations
import torch

def dice_score_from_logits(logits, target, threshold=0.5, eps=1e-7):
    pred = (torch.sigmoid(logits) >= threshold).float(); inter = (pred*target).sum(dim=(1,2,3)); den = pred.sum(dim=(1,2,3)) + target.sum(dim=(1,2,3)); return ((2*inter+eps)/(den+eps)).mean()

def iou_score_from_logits(logits, target, threshold=0.5, eps=1e-7):
    pred = (torch.sigmoid(logits) >= threshold).float(); inter = (pred*target).sum(dim=(1,2,3)); union = pred.sum(dim=(1,2,3)) + target.sum(dim=(1,2,3)) - inter; return ((inter+eps)/(union+eps)).mean()
