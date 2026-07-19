from __future__ import annotations
import argparse, json, csv, random, sys
from pathlib import Path
import numpy as np
import yaml
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.data import paired_files, split_pairs, TeethDataset
from src.model import UNet
from src.metrics import dice_score_from_logits, iou_score_from_logits
from src.postprocess import connected_components_visual, contour_overlay, measurements_overlay
from src.figures import save_fig1, save_fig2, save_fig4

def set_seed(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.set_num_threads(max(1,min(4,torch.get_num_threads())))

@torch.no_grad()
def evaluate(model, loader, device, threshold):
    model.eval(); dices=[]; ious=[]; losses=[]; bce=torch.nn.BCEWithLogitsLoss()
    for x,y,_ in loader:
        x=x.to(device); y=y.to(device); z=model(x)
        losses.append(float(bce(z,y).item())); dices.append(float(dice_score_from_logits(z,y,threshold).item())); ious.append(float(iou_score_from_logits(z,y,threshold).item()))
    return {"loss":float(np.mean(losses)),"dice":float(np.mean(dices)),"iou":float(np.mean(ious))}

def train(cfg):
    seed=int(cfg["seed"]); set_seed(seed); data_root=ROOT/cfg["data_root"]; pairs=paired_files(data_root); train_pairs,val_pairs,test_pairs=split_pairs(pairs,seed=seed)
    out=ROOT/cfg.get("output_dir","outputs"); out.mkdir(parents=True,exist_ok=True)
    for name,ps in [("train",train_pairs),("validation",val_pairs),("test",test_pairs)]:
        with open(out/f"{name}_manifest.csv","w",newline="") as f:
            w=csv.writer(f); w.writerow(["image","mask"])
            for a,b in ps: w.writerow([str(a.relative_to(ROOT)),str(b.relative_to(ROOT))])
    size=(int(cfg["image_height"]),int(cfg["image_width"])); train_ds=TeethDataset(train_pairs,size); val_ds=TeethDataset(val_pairs,size); test_ds=TeethDataset(test_pairs,size)
    train_loader=DataLoader(train_ds,batch_size=int(cfg["batch_size"]),shuffle=True,num_workers=0); val_loader=DataLoader(val_ds,batch_size=int(cfg["batch_size"]),shuffle=False,num_workers=0); test_loader=DataLoader(test_ds,batch_size=int(cfg["batch_size"]),shuffle=False,num_workers=0)
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu"); model=UNet(base=int(cfg["base_channels"])).to(device); opt=torch.optim.Adam(model.parameters(),lr=float(cfg["learning_rate"])); criterion=torch.nn.BCEWithLogitsLoss(); hist=[]; best=-1
    ckpt=out/"checkpoints"/"best_model.pt"; ckpt.parent.mkdir(parents=True,exist_ok=True)
    for epoch in range(1,int(cfg["epochs"])+1):
        model.train(); tr_losses=[]
        for x,y,_ in train_loader:
            x=x.to(device); y=y.to(device); opt.zero_grad(set_to_none=True); z=model(x); loss=criterion(z,y); loss.backward(); opt.step(); tr_losses.append(float(loss.item()))
        tr=evaluate(model,train_loader,device,float(cfg["threshold"])); va=evaluate(model,val_loader,device,float(cfg["threshold"])); row={"epoch":epoch,"train_loss":float(np.mean(tr_losses)),"train_dice":tr["dice"],"train_iou":tr["iou"],"val_loss":va["loss"],"val_dice":va["dice"],"val_iou":va["iou"]}; hist.append(row); print(row)
        if va["dice"]>best: best=va["dice"]; torch.save({"model":model.state_dict(),"cfg":cfg},ckpt)
    state=torch.load(ckpt,map_location=device,weights_only=False); model.load_state_dict(state["model"]); metrics=evaluate(model,test_loader,device,float(cfg["threshold"])); metrics.update({"mode":cfg["mode"],"device":str(device),"n_train":len(train_ds),"n_val":len(val_ds),"n_test":len(test_ds),"note":"Smoke metrics are pipeline-validation metrics, not paper reproduction metrics." if cfg["mode"]=="smoke" else ""}); (out/"metrics.json").write_text(json.dumps(metrics,indent=2))
    with open(out/"history.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=hist[0].keys()); w.writeheader(); w.writerows(hist)
    return model,test_ds,hist,metrics,device

def generate_figures(model,test_ds,hist,cfg,device):
    figs=(ROOT/cfg.get("output_dir","outputs"))/"figures"; figs.mkdir(parents=True,exist_ok=True); save_fig1(figs/"figure_01_unet_architecture.png"); save_fig2(figs/"figure_02_workflow.png"); save_fig4(figs/"figure_04_iou_diagram.png")
    x,y,name=test_ds[0]; model.eval()
    with torch.no_grad(): logits=model(x[None].to(device)); prob=torch.sigmoid(logits)[0,0].cpu().numpy()
    pred=(prob>=float(cfg["threshold"])).astype(np.uint8)*255; gray=(x[0].numpy()*255).astype(np.uint8); gt=(y[0].numpy()*255).astype(np.uint8)
    fig,axs=plt.subplots(1,2,figsize=(10,3)); axs[0].imshow(gray,cmap="gray"); axs[0].set_title("Panoramic radiograph"); axs[0].axis("off"); axs[1].imshow(gt,cmap="gray"); axs[1].set_title("Corresponding tooth mask"); axs[1].axis("off"); fig.tight_layout(); fig.savefig(figs/"figure_03_radiograph_and_mask.png",dpi=180); plt.close(fig)
    ep=[r["epoch"] for r in hist]; fig,ax=plt.subplots(figsize=(6,4)); ax.plot(ep,[r["train_dice"] for r in hist],label="train Dice"); ax.plot(ep,[r["val_dice"] for r in hist],label="validation Dice"); ax.set_xlabel("Epoch"); ax.set_ylabel("Dice"); ax.set_ylim(0,1); ax.legend(); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(figs/"figure_05_dice_training_curve.png",dpi=180); plt.close(fig)
    fig,ax=plt.subplots(figsize=(6,4)); ax.plot(ep,[r["train_iou"] for r in hist],label="train IoU"); ax.plot(ep,[r["val_iou"] for r in hist],label="validation IoU"); ax.set_xlabel("Epoch"); ax.set_ylabel("IoU"); ax.set_ylim(0,1); ax.legend(); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(figs/"figure_06_iou_training_curve.png",dpi=180); plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4)); ax.imshow(gray,cmap="gray"); ax.set_title(f"Test panoramic radiograph — {name}"); ax.axis("off"); fig.tight_layout(); fig.savefig(figs/"figure_07_test_radiograph.png",dpi=180); plt.close(fig)
    comp,_=connected_components_visual(pred,min_area=15); contour,_=contour_overlay(gray,pred); fig,axs=plt.subplots(1,3,figsize=(13,4)); axs[0].imshow(pred,cmap="gray"); axs[0].set_title("Predicted binary mask"); axs[1].imshow(cv2.cvtColor(contour,cv2.COLOR_BGR2RGB)); axs[1].set_title("Contour extraction"); axs[2].imshow(cv2.cvtColor(comp,cv2.COLOR_BGR2RGB)); axs[2].set_title("Connected components"); [a.axis("off") for a in axs]; fig.tight_layout(); fig.savefig(figs/"figure_08_postprocessing_outputs.png",dpi=180); plt.close(fig)
    overlay=cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB); overlay[pred>0]=np.clip(0.55*overlay[pred>0]+0.45*np.array([255,255,255]),0,255).astype(np.uint8); fig,axs=plt.subplots(1,4,figsize=(15,4))
    for a,im,t,cmap in zip(axs,[gray,gt,pred,overlay],["Input","Ground truth","Prediction","Overlay"],["gray","gray","gray",None]): a.imshow(im,cmap=cmap); a.set_title(t); a.axis("off")
    fig.tight_layout(); fig.savefig(figs/"figure_09_final_outputs.png",dpi=180); plt.close(fig); measured=measurements_overlay(gray,pred,min_area=15); Image.fromarray(cv2.cvtColor(measured,cv2.COLOR_BGR2RGB)).save(figs/"figure_10_pixel_measurements.png"); cont,_=contour_overlay(gray,pred); Image.fromarray(cv2.cvtColor(cont,cv2.COLOR_BGR2RGB)).save(figs/"figure_11_contour_overlay.png")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--config",default="configs/smoke.yaml"); args=ap.parse_args(); cfg=yaml.safe_load((ROOT/args.config).read_text()); model,test_ds,hist,metrics,device=train(cfg); generate_figures(model,test_ds,hist,cfg,device); print(json.dumps(metrics,indent=2)); print("Generated 11 figures in",(ROOT/cfg.get("output_dir","outputs"))/"figures")

if __name__=="__main__": main()
