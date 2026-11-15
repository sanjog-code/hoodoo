from PIL import Image
import os

brain_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"

for img_name in ['live_3d_hoodie_modal.png', 'live_3d_tee_modal.png', 'live_3d_kicks_modal.png']:
    p = os.path.join(brain_dir, img_name)
    if os.path.exists(p):
        im = Image.open(p)
        crop = im.crop((350, 150, 1100, 750))
        crop.save(os.path.join(brain_dir, f"crop_{img_name}"))
        print(f"Saved crop for {img_name}")
