import os
from PIL import Image

sheet = Image.open(r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\all_products_front_back_sheet.png")

# Cut out each 1600x800 row and save it
row_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\product_rows"
os.makedirs(row_dir, exist_ok=True)

names = [
    'hero_asphalt', 'p1_black', 'p2_cocoa', 'p3_black', 'p4_sand',
    'p5_white', 'p6_carbon', 'p7_sand', 'p8_indigo',
    'p9_bone', 'p10_noir', 'p11_choco', 'p12_sail',
    'p13_asphalt', 'p14_graphite', 'p15_espresso', 'p16_obsidian'
]

for idx, name in enumerate(names):
    row = sheet.crop((0, idx * 800, 1600, (idx + 1) * 800))
    row.save(os.path.join(row_dir, f"{idx:02d}_{name}_row.png"))

print("Saved all 17 product rows!")
