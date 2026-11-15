import os
from PIL import Image

for name in ['p5_white', 'p6_carbon', 'p7_sand', 'p8_indigo', 'p14_graphite', 'p15_espresso']:
    f = Image.open(f"public/assets/collection/{name}.png")
    b = Image.open(f"public/assets/collection/{name}_back.png")
    # Save a side by side image
    pair = Image.new('RGB', (1600, 800))
    pair.paste(f, (0, 0))
    pair.paste(b, (800, 0))
    pair.save(rf"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\crop_inspection\{name}_pair.png")
    print(f"Saved {name}_pair.png")
