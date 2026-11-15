import os
from PIL import Image
import numpy as np

items = [
    'hero_asphalt', 'p1_black', 'p2_cocoa', 'p3_black', 'p4_sand',
    'p5_white', 'p6_carbon', 'p7_sand', 'p8_indigo',
    'p13_asphalt', 'p14_graphite', 'p15_espresso'
]

for name in items:
    f_path = f"public/assets/collection/{name}.png"
    b_path = f"public/assets/collection/{name}_back.png"
    f = Image.open(f_path).convert('RGB')
    b = Image.open(b_path).convert('RGB')
    
    # Neckline area is typically y: 150 to 300, x: 350 to 450
    # In front view of a tee, collar drops lower. In back view, collar is straight across.
    # Also let's inspect the graphic size:
    # Usually a huge full-back mural is in the back image!
    # Does any FRONT image have a huge graphic while the BACK image has a small logo?
    f_arr = np.array(f)
    b_arr = np.array(b)
    
    # Check bounding box of graphic on front vs back
    # Compute diff from edge background
    bg = f_arr[10, 10]
    f_diff = np.linalg.norm(f_arr - bg, axis=2) > 30
    b_diff = np.linalg.norm(b_arr - bg, axis=2) > 30
    
    # Standard deviation in lower half (chest/stomach area y: 300 to 600)
    f_mid_std = np.std(f_arr[300:600, 250:550])
    b_mid_std = np.std(b_arr[300:600, 250:550])
    
    print(f"{name:15}: front_mid_std={f_mid_std:5.1f}, back_mid_std={b_mid_std:5.1f}")
