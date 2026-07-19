from __future__ import annotations
from pathlib import Path
import argparse, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def generate_one(seed:int, size=(256,128)):
    rng=random.Random(seed); np_rng=np.random.default_rng(seed)
    w,h=size
    bg=np_rng.normal(60,10,(h,w)).clip(0,255).astype(np.uint8)
    img=Image.fromarray(bg,"L")
    mask=Image.new("L",(w,h),0)
    draw=ImageDraw.Draw(img); mdraw=ImageDraw.Draw(mask)
    for r,val in [(55,20),(42,16),(30,10)]:
        jaw=Image.new("L",(w,h),0); jd=ImageDraw.Draw(jaw)
        jd.arc((25,10,w-25,h+50),200,340,fill=val,width=r//3)
        img=Image.fromarray(np.maximum(np.asarray(img),np.asarray(jaw)).astype(np.uint8))
    draw=ImageDraw.Draw(img)
    n_top=rng.randint(10,13); n_bot=rng.randint(10,13)
    for row,n,cy,flip in [(0,n_top,45,False),(1,n_bot,88,True)]:
        for i in range(n):
            frac=(i+0.5)/n
            cx=int(20+frac*(w-40) + rng.uniform(-2,2))
            arch=12*((frac-.5)**2)
            y=int(cy + (arch if row==0 else -arch) + rng.uniform(-2,2))
            tw=rng.randint(10,16); th=rng.randint(20,31)
            box=(cx-tw//2,y-th//2,cx+tw//2,y+th//2)
            intensity=rng.randint(150,225)
            draw.ellipse(box,fill=intensity)
            if rng.random()<.8: draw.line((cx,y-th//3,cx,y+th//3),fill=max(90,intensity-55),width=1)
            mdraw.ellipse(box,fill=255)
    img=img.filter(ImageFilter.GaussianBlur(radius=1.0))
    arr=np.asarray(img).astype(np.float32)+np_rng.normal(0,5,(h,w))
    arr=np.clip(arr,0,255).astype(np.uint8)
    return Image.fromarray(arr,"L"), mask

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default="data/bootstrap_synthetic"); ap.add_argument("--count",type=int,default=48); args=ap.parse_args()
    root=Path(args.root); (root/"images").mkdir(parents=True,exist_ok=True); (root/"masks").mkdir(parents=True,exist_ok=True)
    for i in range(args.count):
        img,mask=generate_one(1000+i); img.save(root/"images"/f"sample_{i:03d}.png"); mask.save(root/"masks"/f"sample_{i:03d}.png")
    print(f"Generated {args.count} paired samples at {root}")

if __name__=="__main__": main()
