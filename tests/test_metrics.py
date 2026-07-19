import torch
from src.metrics import dice_score_from_logits, iou_score_from_logits

def test_perfect_scores():
    target=torch.ones((1,1,4,4)); logits=torch.ones((1,1,4,4))*10
    assert float(dice_score_from_logits(logits,target)) > .999
    assert float(iou_score_from_logits(logits,target)) > .999
