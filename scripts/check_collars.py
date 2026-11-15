import os
from PIL import Image
import numpy as np

for name in ['p4_sand', 'p5_white', 'p7_sand', 'p1_black']:
    f = Image.open(f"public/assets/collection/{name}.png").convert('RGB')
    b = Image.open(f"public/assets/collection/{name}_back.png").convert('RGB')
    f_arr = np.array(f)
    b_arr = np.array(b)
    
    # Save the collar area for each
    f_collar = f.crop((320, 120, 480, 240))
    b_collar = b.crop((320, 120, 480, 240))
    f_collar.save(rf"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\crop_inspection\{name}_f_collar.png")
    b_collar.save(rf"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\crop_inspection\{name}_b_collar.png")
    
    # Check if there is drawstrings or pocket in front vs back
    print(f"[{name}] collar saved.")
