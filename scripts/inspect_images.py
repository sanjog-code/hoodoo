import os
from PIL import Image

def analyze_image(path):
    if not os.path.exists(path):
        return "NOT_FOUND"
    im = Image.open(path).convert('RGB')
    w, h = im.size
    # Check top/chest area (y from 0.2*h to 0.5*h)
    # Check if there is a hood visible in front, or hood cowl hanging on back
    # Or text/graphics
    return f"{w}x{h}"

images = [
    'hero_asphalt', 'p1_black', 'p2_cocoa', 'p3_black', 'p4_sand',
    'p5_white', 'p6_carbon', 'p7_sand', 'p8_indigo',
    'p9_bone', 'p10_noir', 'p11_choco', 'p12_sail',
    'p13_asphalt', 'p14_graphite', 'p15_espresso', 'p16_obsidian'
]

for img in images:
    f_path = f"public/assets/collection/{img}.png"
    b_path = f"public/assets/collection/{img}_back.png"
    print(f"{img:15} -> front: {analyze_image(f_path)}, back: {analyze_image(b_path)}")
