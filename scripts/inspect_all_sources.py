import os
from PIL import Image

sources = [
    ('hero', 'public/assets/westcoast_hero_hoodie.png'),
    ('p1', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_paisley_ghost_1794623856703.jpg'),
    ('p2', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_hydraulic_ghost_1794623904791.jpg'),
    ('p4', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_venice_ghost_1794623983058.jpg'),
    ('p13/p3', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_midnight_ghost_1794624031806.jpg'),
    ('p5', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_crenshaw_dark_bg_1794680274429.jpg'),
    ('p6', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_southcentral_ghost_1794678808478.jpg'),
    ('p7', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_localsonly_ghost_1794678828498.jpg'),
    ('p8', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_eastla_paisley_ghost_1794678851227.jpg'),
    ('p14', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chrome_ghost_1794678874804.jpg'),
    ('p15', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chicanosoul_ghost_1794678896392.jpg'),
    ('p9', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_1_chicano_bone_gum_1794678794364.jpg'),
    ('p10', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_2_midnight_stealth_runner_1794678820355.jpg'),
    ('p11', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_3_chopper_suede_skate_low_1794678841870.jpg'),
    ('p12', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_4_paisley_swoop_retro_low_1794678863208.jpg'),
    ('p16', r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_5_eastside_gum_sole_retro_1794678883648.jpg'),
]

out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\inspect_sources"
os.makedirs(out_dir, exist_ok=True)

for name, path in sources:
    if os.path.exists(path):
        im = Image.open(path)
        w, h = im.size
        # Resize to 800 wide preserving aspect
        rh = int(h * (800 / w))
        im_res = im.resize((800, rh))
        im_res.save(os.path.join(out_dir, f"{name.replace('/', '_')}_src.jpg"))
        print(f"Saved {name} source: {w}x{h}")
    else:
        print(f"MISSING: {name} at {path}")
