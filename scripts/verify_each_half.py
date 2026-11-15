import os
from PIL import Image
import numpy as np

src_files = [
    ('hero', 'public/assets/westcoast_hero_hoodie.png', 'hoodie'),
    ('p1', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_paisley_ghost_1794623856703.jpg', 'hoodie'),
    ('p2', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_hydraulic_ghost_1794623904791.jpg', 'hoodie'),
    ('p4', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_venice_ghost_1794623983058.jpg', 'hoodie'),
    ('p13_p3', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_midnight_ghost_1794624031806.jpg', 'hoodie'),
    ('p5', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_crenshaw_dark_bg_1794680274429.jpg', 'tee'),
    ('p6', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_southcentral_ghost_1794678808478.jpg', 'tee'),
    ('p7', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_localsonly_ghost_1794678828498.jpg', 'tee'),
    ('p8', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_eastla_paisley_ghost_1794678851227.jpg', 'tee'),
    ('p14', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chrome_ghost_1794678874804.jpg', 'tee'),
    ('p15', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chicanosoul_ghost_1794678896392.jpg', 'tee'),
]

diag_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\diagnose_halves"

for name, _, cat in src_files:
    l_path = os.path.join(diag_dir, f"{name}_L.jpg")
    r_path = os.path.join(diag_dir, f"{name}_R.jpg")
    if not os.path.exists(l_path): continue
    l_im = Image.open(l_path).convert('RGB')
    r_im = Image.open(r_path).convert('RGB')
    w, h = l_im.size
    
    # Check bottom pouch: kangaroo pocket produces horizontal / diagonal seam lines
    # in y: int(h*0.55) to int(h*0.85)
    l_pock = np.array(l_im)[int(h*0.55):int(h*0.85), int(w*0.25):int(w*0.75)]
    r_pock = np.array(r_im)[int(h*0.55):int(h*0.85), int(w*0.25):int(w*0.75)]
    
    # Vertical gradient (diff along Y) detects kangaroo pocket edges
    l_vgrad = np.mean(np.abs(np.diff(l_pock, axis=0)))
    r_vgrad = np.mean(np.abs(np.diff(r_pock, axis=0)))
    
    # Collar dip: in front view of tees, collar dips lower
    l_neck = np.array(l_im)[int(h*0.12):int(h*0.24), int(w*0.35):int(w*0.65)]
    r_neck = np.array(r_im)[int(h*0.12):int(h*0.24), int(w*0.35):int(w*0.65)]
    l_neck_var = np.var(l_neck)
    r_neck_var = np.var(r_neck)
    
    print(f"{name:8} ({cat:6}) | L_vgrad={l_vgrad:5.2f}, R_vgrad={r_vgrad:5.2f} | L_neck_var={l_neck_var:6.1f}, R_neck_var={r_neck_var:6.1f}")
