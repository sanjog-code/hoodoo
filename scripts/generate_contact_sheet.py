import os
from PIL import Image
import numpy as np

# We have:
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

# For each product, save side by side into a single contact sheet image so we can review them
sheet = Image.new('RGB', (800 * 2, 800 * len(products)), (255, 255, 255))

for idx, (p, cat) in enumerate(products):
    f_path = f"public/assets/collection/{p}.png"
    b_path = f"public/assets/collection/{p}_back.png"
    if os.path.exists(f_path):
        f = Image.open(f_path).convert('RGB')
        sheet.paste(f, (0, idx * 800))
    if os.path.exists(b_path):
        b = Image.open(b_path).convert('RGB')
        sheet.paste(b, (800, idx * 800))

sheet_path = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\all_products_front_back_sheet.png"
sheet.save(sheet_path)
print(f"Saved contact sheet to {sheet_path}")
