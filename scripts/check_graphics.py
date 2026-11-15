import os
from PIL import Image
import numpy as np

items = [
    'hero_asphalt', 'p1_black', 'p2_cocoa', 'p3_black', 'p4_sand',
    'p5_white', 'p6_carbon', 'p7_sand', 'p8_indigo',
    'p9_bone', 'p10_noir', 'p11_choco', 'p12_sail',
    'p13_asphalt', 'p14_graphite', 'p15_espresso', 'p16_obsidian'
]

for name in items:
    f_path = f"public/assets/collection/{name}.png"
    b_path = f"public/assets/collection/{name}_back.png"
    if not os.path.exists(f_path) or not os.path.exists(b_path):
        continue
    f = Image.open(f_path).convert('RGB')
    b = Image.open(b_path).convert('RGB')
    
    # Check if front has a huge graphic in the middle
    f_arr = np.array(f)
    b_arr = np.array(b)
    
    # Let's inspect center 400x400
    f_center = f_arr[200:600, 200:600]
    b_center = b_arr[200:600, 200:600]
    
    print(f"[{name}]")
    print(f"  Front center mean={np.mean(f_center, axis=(0,1)).astype(int)}, std={np.std(f_center):.1f}")
    print(f"  Back  center mean={np.mean(b_center, axis=(0,1)).astype(int)}, std={np.std(b_center):.1f}")
