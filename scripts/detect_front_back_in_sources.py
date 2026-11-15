import os
from PIL import Image
import numpy as np

src_files = [
    ('hero', 'public/assets/westcoast_hero_hoodie.png'),
    ('p1', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_paisley_ghost_1794623856703.jpg'),
    ('p2', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_hydraulic_ghost_1794623904791.jpg'),
    ('p4', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_venice_ghost_1794623983058.jpg'),
    ('p13_p3', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_midnight_ghost_1794624031806.jpg'),
    ('p5', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_crenshaw_dark_bg_1794680274429.jpg'),
    ('p6', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_southcentral_ghost_1794678808478.jpg'),
    ('p7', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_localsonly_ghost_1794678828498.jpg'),
    ('p8', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_eastla_paisley_ghost_1794678851227.jpg'),
    ('p14', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chrome_ghost_1794678874804.jpg'),
    ('p15', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chicanosoul_ghost_1794678896392.jpg'),
]

for name, path in src_files:
    if not os.path.exists(path):
        continue
    im = Image.open(path).convert('RGB')
    w, h = im.size
    
    # Left garment center is x ~ w*0.25, y ~ h*0.4
    # Right garment center is x ~ w*0.75, y ~ h*0.4
    left = im.crop((int(w * 0.05), int(h * 0.1), int(w * 0.45), int(h * 0.9)))
    right = im.crop((int(w * 0.55), int(h * 0.1), int(w * 0.95), int(h * 0.9)))
    
    l_arr = np.array(left)
    r_arr = np.array(right)
    
    # Collar dip: in front view, collar at top-center dips lower (around y: 0.15 to 0.3)
    # Check brightness or gradient in collar region (x: 0.35 to 0.65 of the half-width, y: 0.05 to 0.25 of half-height)
    lw, lh = left.size
    l_collar = l_arr[int(lh * 0.08):int(lh * 0.25), int(lw * 0.35):int(lw * 0.65)]
    r_collar = r_arr[int(lh * 0.08):int(lh * 0.25), int(lw * 0.35):int(lw * 0.65)]
    
    # Chest vs Back: full graphic std
    l_chest = l_arr[int(lh * 0.25):int(lh * 0.65), int(lw * 0.2):int(lw * 0.8)]
    r_chest = r_arr[int(lh * 0.25):int(lh * 0.65), int(lw * 0.2):int(lw * 0.8)]
    
    # Bottom pocket for hoodie (y: 0.55 to 0.85)
    l_pock = l_arr[int(lh * 0.55):int(lh * 0.85), int(lw * 0.25):int(lw * 0.75)]
    r_pock = r_arr[int(lh * 0.55):int(lh * 0.85), int(lw * 0.25):int(lw * 0.75)]
    
    print(f"[{name:8}]")
    print(f"   LEFT : collar_mean={np.mean(l_collar):.1f}, chest_std={np.std(l_chest):.1f}, pock_std={np.std(l_pock):.1f}")
    print(f"   RIGHT: collar_mean={np.mean(r_collar):.1f}, chest_std={np.std(r_chest):.1f}, pock_std={np.std(r_pock):.1f}")
