import os
from PIL import Image
import numpy as np

diag_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\diagnose_halves"

items = ['hero', 'p1', 'p2', 'p4', 'p13_p3', 'p5', 'p6', 'p7', 'p8', 'p14', 'p15']

for name in items:
    l_path = os.path.join(diag_dir, f"{name}_L.jpg")
    r_path = os.path.join(diag_dir, f"{name}_R.jpg")
    if not os.path.exists(l_path): continue
    l_im = Image.open(l_path).convert('RGB')
    r_im = Image.open(r_path).convert('RGB')
    
    # Save a small composite showing L and R with text
    w, h = l_im.size
    comp = Image.new('RGB', (w*2, h))
    comp.paste(l_im, (0, 0))
    comp.paste(r_im, (w, 0))
    
    # Also analyze where the big graphic is
    # Usually: front has small chest print or centered title; back has huge art across the entire back
    l_arr = np.array(l_im)
    r_arr = np.array(r_im)
    
    # Bounding box of non-background content in torso
    # Torso: y from 0.2*h to 0.75*h, x from 0.15*w to 0.85*w
    l_torso = l_arr[int(h*0.2):int(h*0.75), int(w*0.15):int(w*0.85)]
    r_torso = r_arr[int(h*0.2):int(h*0.75), int(w*0.15):int(w*0.85)]
    
    l_std = np.std(l_torso)
    r_std = np.std(r_torso)
    
    print(f"{name:8}: L_std={l_std:5.1f}, R_std={r_std:5.1f} -> {'R is busier (likely BACK)' if r_std > l_std + 10 else 'L is busier (likely BACK)' if l_std > r_std + 10 else 'Similar'}")
