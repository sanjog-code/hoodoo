import os
from PIL import Image
import numpy as np

products = [
    ('hero_asphalt', 'hoodie'),
    ('p1_black', 'hoodie'),
    ('p2_cocoa', 'hoodie'),
    ('p3_black', 'hoodie'),
    ('p4_sand', 'hoodie'),
    ('p5_white', 'tee'),
    ('p6_carbon', 'tee'),
    ('p7_sand', 'tee'),
    ('p8_indigo', 'tee'),
    ('p9_bone', 'kicks'),
    ('p10_noir', 'kicks'),
    ('p11_choco', 'kicks'),
    ('p12_sail', 'kicks'),
    ('p13_asphalt', 'hoodie'),
    ('p14_graphite', 'tee'),
    ('p15_espresso', 'tee'),
    ('p16_obsidian', 'kicks'),
]

for p, cat in products:
    f_path = f"public/assets/collection/{p}.png"
    b_path = f"public/assets/collection/{p}_back.png"
    if not os.path.exists(f_path) or not os.path.exists(b_path):
        continue
    f = Image.open(f_path).convert('RGB')
    b = Image.open(b_path).convert('RGB')
    f_arr = np.array(f)
    b_arr = np.array(b)
    
    # 1. Check collar line (y: 120-220, x: 300-500)
    # A front collar dips down into dark opening or collar inner tag
    f_collar_mean = np.mean(f_arr[140:220, 360:440])
    b_collar_mean = np.mean(b_arr[140:220, 360:440])
    
    # 2. Check chest area (y: 220-420, x: 250-550)
    f_chest_std = np.std(f_arr[220:420, 250:550])
    b_chest_std = np.std(b_arr[220:420, 250:550])
    
    # 3. Check full torso (y: 220-650, x: 200-600)
    f_torso_std = np.std(f_arr[220:650, 200:600])
    b_torso_std = np.std(b_arr[220:650, 200:600])
    
    # 4. Check kangaroo pocket region (y: 520-720, x: 250-550)
    f_pock_std = np.std(f_arr[520:720, 250:550])
    b_pock_std = np.std(b_arr[520:720, 250:550])
    
    print(f"[{p:13} ({cat:6})]")
    print(f"   Front: collar={f_collar_mean:5.1f}, chest_std={f_chest_std:5.1f}, torso_std={f_torso_std:5.1f}, pock_std={f_pock_std:5.1f}")
    print(f"   Back : collar={b_collar_mean:5.1f}, chest_std={b_chest_std:5.1f}, torso_std={b_torso_std:5.1f}, pock_std={b_pock_std:5.1f}")
