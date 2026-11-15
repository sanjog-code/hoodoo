import os
from PIL import Image

tee_items = ['p5_white', 'p6_carbon', 'p7_sand', 'p8_indigo', 'p14_graphite', 'p15_espresso']
hoodie_items = ['hero_asphalt', 'p1_black', 'p2_cocoa', 'p3_black', 'p4_sand', 'p13_asphalt']

# Save high-res crops of chest and back for inspection
out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\crop_inspection"
os.makedirs(out_dir, exist_ok=True)

for name in tee_items + hoodie_items:
    f_path = f"public/assets/collection/{name}.png"
    b_path = f"public/assets/collection/{name}_back.png"
    if os.path.exists(f_path):
        f = Image.open(f_path)
        # Crop center graphic
        f_crop = f.crop((180, 160, 620, 600))
        f_crop.save(os.path.join(out_dir, f"{name}_front_graphic.png"))
    if os.path.exists(b_path):
        b = Image.open(b_path)
        b_crop = b.crop((180, 160, 620, 600))
        b_crop.save(os.path.join(out_dir, f"{name}_back_graphic.png"))

print("Saved all front and back graphic crops!")
