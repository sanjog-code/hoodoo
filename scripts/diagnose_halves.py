import os
from PIL import Image

src_files = [
    ('hero', 'public/assets/westcoast_hero_hoodie.png'),
    ('p1', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_paisley_ghost_1794623856703.jpg'),
    ('p2', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_hydraulic_ghost_1794623904791.jpg'),
    ('p4', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_venice_ghost_1794623983058.jpg'),
    ('p13_p3', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_midnight_ghost_1794624031806.jpg'),
    ('p5', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_crenshaw_dark_bg_1794680274429.jpg'),
    ('p6', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_southcentral_ghost_1794678808478.jpg'),
    ('p7', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_localsonly_ghost_1794678828498.jpg'),
    ('p8', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_eastla_paisley_ghost_1794678851227.jpg'),
    ('p14', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chrome_ghost_1794678874804.jpg'),
    ('p15', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chicanosoul_ghost_1794678896392.jpg'),
]

out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\diagnose_halves"
os.makedirs(out_dir, exist_ok=True)

for name, path in src_files:
    if not os.path.exists(path): continue
    im = Image.open(path)
    w, h = im.size
    left = im.crop((0, 0, w//2, h))
    right = im.crop((w//2, 0, w, h))
    
    # Save left as _L and right as _R
    left.save(os.path.join(out_dir, f"{name}_L.jpg"))
    right.save(os.path.join(out_dir, f"{name}_R.jpg"))

print("Exported all left and right halves for diagnosis.")
