from __future__ import annotations
import cv2, numpy as np

def clean_mask(mask_u8,open_iter=1,close_iter=1):
    mask=(mask_u8>127).astype(np.uint8)*255; kernel=np.ones((3,3),np.uint8)
    if open_iter: mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel,iterations=open_iter)
    if close_iter: mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel,iterations=close_iter)
    return mask

def connected_components_visual(mask_u8,min_area=20):
    mask=clean_mask(mask_u8); n,labels,stats,centroids=cv2.connectedComponentsWithStats(mask,8); rng=np.random.default_rng(42); out=np.zeros((*mask.shape,3),np.uint8); comps=[]
    for label in range(1,n):
        area=int(stats[label,cv2.CC_STAT_AREA]);
        if area<min_area: continue
        color=rng.integers(60,230,size=3,dtype=np.uint8); out[labels==label]=color; x,y,w,h=[int(v) for v in stats[label,:4]]; comps.append((label,x,y,w,h,area))
    return out,comps

def contour_overlay(gray_u8,mask_u8):
    base=cv2.cvtColor(gray_u8,cv2.COLOR_GRAY2BGR); mask=clean_mask(mask_u8); contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(base,contours,-1,(255,255,255),1); return base,contours

def measurements_overlay(gray_u8,mask_u8,min_area=20):
    base=cv2.cvtColor(gray_u8,cv2.COLOR_GRAY2BGR); mask=clean_mask(mask_u8); contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE); idx=0
    for c in contours:
        if cv2.contourArea(c)<min_area: continue
        idx+=1; rect=cv2.minAreaRect(c); box=cv2.boxPoints(rect).astype(int); cv2.drawContours(base,[box],0,(255,255,255),1); (cx,cy),(w,h),ang=rect; cv2.putText(base,f"{idx}: {w:.0f}x{h:.0f}px",(max(0,int(cx)-35),max(10,int(cy))),cv2.FONT_HERSHEY_SIMPLEX,.32,(255,255,255),1,cv2.LINE_AA)
    return base
