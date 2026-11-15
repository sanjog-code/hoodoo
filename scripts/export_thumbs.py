import os
from PIL import Image

out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\inspect_assets"
os.makedirs(out_dir, exist_ok=True)

items = [
    'hero_asphalt', 'p1_black', 'p2_cocoa', 'p3_black', 'p4_sand',
    'p5_white', 'p6_carbon', 'p7_sand', 'p8_indigo',
    'p9_bone', 'p10_noir', 'p11_choco', 'p12_sail',
    'p13_asphalt', 'p14_graphite', 'p15_espresso', 'p16_obsidian'
]

# Create a summary report of image contents
for name in items:
    f_path = f"public/assets/collection/{name}.png"
    b_path = f"public/assets/collection/{name}_back.png"
    if os.path.exists(f_path):
        f = Image.open(f_path).resize((200, 200))
        f.save(os.path.join(out_dir, f"{name}_front_sm.png"))
    if os.path.exists(b_path):
        b = Image.open(b_path).resize((200, 200))
        b.save(os.path.join(out_dir, f"{name}_back_sm.png"))

print("Exported small comparison thumbs.")
