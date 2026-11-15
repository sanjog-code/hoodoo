import os
from PIL import Image
import numpy as np

src_files = [
    ('p5', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_crenshaw_dark_bg_1794680274429.jpg'),
    ('p6', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_southcentral_ghost_1794678808478.jpg'),
    ('p7', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_localsonly_ghost_1794678828498.jpg'),
    ('p8', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_eastla_paisley_ghost_1794678851227.jpg'),
    ('p14', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chrome_ghost_1794678874804.jpg'),
    ('p15', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chicanosoul_ghost_1794678896392.jpg'),
]

for pid, path in src_files:
    if not os.path.exists(path):
        print(f"{pid}: not found")
        continue
    im = Image.open(path)
    w, h = im.size
    left = im.crop((0, 0, w//2, h))
    right = im.crop((w//2, 0, w, h))
    l_arr = np.array(left)
    r_arr = np.array(right)
    # Check neck collar: front collar dips lower
    # Check center graphic
    print(f"[{pid}] size: {w}x{h}")
    print(f"   Left  half std={np.std(l_arr[int(h*0.25):int(h*0.65), int(w*0.1):int(w*0.4)]):.1f}")
    print(f"   Right half std={np.std(r_arr[int(h*0.25):int(h*0.65), int(w*0.1):int(w*0.4)]):.1f}")
