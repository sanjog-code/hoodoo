from PIL import Image
import numpy as np

f = Image.open('public/assets/collection/p5_white.png').convert('RGB')
b = Image.open('public/assets/collection/p5_white_back.png').convert('RGB')

# Let's inspect the collar area (y: 100-240, x: 300-500)
# A front view shows the front collar lower than the back collar (two collar curves, or inside of collar).
# A back view shows only the high rear collar curve.
f_crop = f.crop((320, 100, 480, 240))
b_crop = b.crop((320, 100, 480, 240))

f_crop.save(r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\crop_inspection\p5_f_neck.png')
b_crop.save(r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\crop_inspection\p5_b_neck.png')

print("Saved p5 neck crops.")
