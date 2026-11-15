import math
import os
import shutil
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import numpy as np

# =================================================================
# 1. GENERATE PRISTINE LOGO ATLASES & TEXTURES
# =================================================================
os.makedirs("public/assets/collection", exist_ok=True)
os.makedirs("public/assets/models/textures", exist_ok=True)
os.makedirs("public/models/textures", exist_ok=True)

# Generate clean transparent PNG logos from the user's uploaded master image
user_logo_path = r"C:/Users/sanjo/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/.user_uploaded/media_1794694568064_b9ab9699.jpg"

if os.path.exists(user_logo_path):
    im = Image.open(user_logo_path).convert('RGB')
    arr = np.array(im, dtype=float)
    gray = np.mean(arr, axis=2)
    alpha = np.clip((gray - 32.0) / 60.0 * 255.0, 0, 255).astype(np.uint8)
    
    # White logo for dark garments
    white_arr = np.zeros((im.height, im.width, 4), dtype=np.uint8)
    white_arr[:, :, 0] = 255
    white_arr[:, :, 1] = 255
    white_arr[:, :, 2] = 255
    white_arr[:, :, 3] = alpha
    white_logo = Image.fromarray(white_arr, mode='RGBA')
    bbox = white_logo.getbbox()
    white_logo_cropped = white_logo.crop(bbox)
    white_logo_cropped.save("public/assets/collection/hoodoo_logo_white.png")
    
    # Charcoal logo for light garments
    black_arr = np.zeros((im.height, im.width, 4), dtype=np.uint8)
    black_arr[:, :, 0] = 24
    black_arr[:, :, 1] = 24
    black_arr[:, :, 2] = 28
    black_arr[:, :, 3] = alpha
    black_logo = Image.fromarray(black_arr, mode='RGBA')
    black_logo_cropped = black_logo.crop(bbox)
    black_logo_cropped.save("public/assets/collection/hoodoo_logo_black.png")
    print("Generated master HooDoo logo stamps from user attachment!")

# Function to extract stamp from an image with soft alpha feathering
def extract_stamp(img_path, box, diff_cut=18, feather=14):
    if not os.path.exists(img_path):
        return None
    im = Image.open(img_path).convert('RGBA')
    crop = im.crop(box)
    w, h = crop.size
    arr = np.array(crop, dtype=float)
    sample = np.concatenate([
        arr[:10, :10, :3].reshape(-1, 3),
        arr[:10, -10:, :3].reshape(-1, 3),
        arr[-10:, :10, :3].reshape(-1, 3),
        arr[-10:, -10:, :3].reshape(-1, 3),
    ])
    bg_rgb = np.median(sample, axis=0)
    diff = np.linalg.norm(arr[:, :, :3] - bg_rgb, axis=2)
    alpha = np.clip((diff - diff_cut) / 22.0 * 255.0, 0, 255).astype(np.float32)
    
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((feather, feather, w - feather, h - feather), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather * 0.8))
    mask_arr = np.array(mask, dtype=np.float32) / 255.0
    arr[:, :, 3] = (alpha * mask_arr).astype(np.uint8)
    return Image.fromarray(arr.astype(np.uint8))

# Colorway configs for all hoodies
hoodie_swatches = {
    'hero': [('asphalt', (28, 28, 30), False), ('bone', (230, 226, 218), True), ('royal', (26, 38, 65), False)],
    'p1':   [('black', (14, 14, 16), False), ('red', (125, 24, 28), False), ('blue', (26, 50, 105), False)],
    'p2':   [('cocoa', (75, 52, 42), False), ('charcoal', (38, 38, 40), False), ('tan', (155, 130, 105), False)],
    'p3':   [('black', (18, 18, 20), False), ('ash', (95, 95, 100), False), ('khaki', (68, 75, 62), False)],
    'p4':   [('sand', (170, 158, 140), False), ('rose', (150, 115, 120), False), ('sage', (115, 130, 115), False)],
    'p13':  [('asphalt', (32, 32, 36), False), ('bone', (228, 224, 216), True), ('navy', (24, 34, 58), False)],
}

hoodie_meta = {
    'hero': {'back_src': 'public/assets/collection/hero_asphalt_back.png', 'back_box': (180, 170, 620, 570), 'has_paisley': True},
    'p1':   {'back_src': 'public/assets/collection/p1_black_back.png',     'back_box': (180, 160, 620, 580), 'has_paisley': True},
    'p2':   {'back_src': 'public/assets/collection/p2_cocoa_back.png',     'back_box': (200, 180, 600, 600), 'has_paisley': False},
    'p3':   {'back_src': 'public/assets/collection/p3_black_back.png',     'back_box': (200, 180, 600, 580), 'has_paisley': False},
    'p4':   {'back_src': 'public/assets/collection/p4_sand_back.png',      'back_box': (190, 170, 610, 590), 'has_paisley': False},
    'p13':  {'back_src': 'public/assets/collection/p13_asphalt_back.png',  'back_box': (180, 160, 620, 580), 'has_paisley': False},
}

def build_hoodie_texture_atlas(model_id, swatch_slug, base_rgb, is_light=False):
    atlas = Image.new('RGBA', (2048, 2048), base_rgb + (255,))
    
    # 500GSM Loopback Cotton Fleece Grain
    noise = np.random.normal(0, 4.0, (2048, 2048, 1))
    arr = np.array(atlas, dtype=float)
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    atlas = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    draw = ImageDraw.Draw(atlas)
    
    stitch_lo = tuple(max(0, int(c * 0.70)) for c in base_rgb) + (255,)
    stitch_hi = tuple(min(255, int(c * 1.30)) for c in base_rgb) + (255,)
    if is_light:
        stitch_lo = tuple(max(0, int(c * 0.85)) for c in base_rgb) + (255,)
        stitch_hi = tuple(min(255, int(c * 1.05)) for c in base_rgb) + (255,)
        
    # Ribbed waistband
    for y in range(1850, 2048, 6):
        draw.line([(0, y), (2048, y)], fill=stitch_lo, width=2)
        draw.line([(0, y+1), (2048, y+1)], fill=stitch_hi, width=1)
        
    # Ribbed cuffs
    for sx1, sx2 in [(40, 270), (750, 980), (1060, 1290), (1770, 2000)]:
        for y in range(1860, 2048, 8):
            draw.line([(sx1, y), (sx2, y)], fill=stitch_lo, width=2)
            
    # Paisley sleeve art if applicable
    meta = hoodie_meta[model_id]
    if meta['has_paisley']:
        p_col = (40, 40, 44, 180) if is_light else (220, 220, 225, 120)
        for cx in [155, 865, 1175, 1885]:
            for py in range(950, 1700, 120):
                draw.arc([cx - 40, py - 40, cx + 40, py + 40], 0, 360, fill=p_col, width=3)
                draw.ellipse([cx - 15, py - 15, cx + 15, py + 15], outline=p_col, width=2)
                draw.line([(cx - 30, py), (cx + 30, py)], fill=p_col, width=2)
                draw.line([(cx, py - 30), (cx, py + 30)], fill=p_col, width=2)
                
    # 4. Front Chest HooDoo Logo (Centered on X=512, Y=830)
    logo_file = "public/assets/collection/hoodoo_logo_black.png" if is_light else "public/assets/collection/hoodoo_logo_white.png"
    if os.path.exists(logo_file):
        logo_img = Image.open(logo_file).convert('RGBA')
        target_w = 360
        target_h = int(logo_img.height * (target_w / logo_img.width))
        logo_res = logo_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        px = 512 - target_w // 2
        py = 830 - target_h // 2
        atlas.paste(logo_res, (px, py), logo_res)
        
    # 5. Back Mural Artwork (Centered on X=1536, Y=920)
    back_stamp = extract_stamp(meta['back_src'], meta['back_box'], diff_cut=16, feather=16)
    if back_stamp:
        gw = 820
        gh = int(back_stamp.height * (gw / back_stamp.width))
        b_res = back_stamp.resize((gw, gh), Image.Resampling.LANCZOS)
        if is_light:
            b_arr = np.array(b_res, dtype=float)
            is_white = (b_arr[:, :, 0] > 180) & (b_arr[:, :, 1] > 180) & (b_arr[:, :, 2] > 180)
            b_arr[is_white, :3] = [32, 32, 36]
            b_res = Image.fromarray(b_arr.astype(np.uint8))
        px = 1536 - gw // 2
        py = 920 - gh // 2
        atlas.paste(b_res, (px, py), b_res)
        
    out_path = f"public/assets/models/textures/tex_{model_id}_{swatch_slug}.png"
    atlas.save(out_path, 'PNG')
    if swatch_slug in ('asphalt', 'black', 'cocoa', 'sand'):
        base_out = f"public/assets/models/textures/tex_{model_id}.png"
        atlas.save(base_out, 'PNG')
    print(f"Generated Hoodie Atlas: {out_path}")

print("Generating all Hoodie Atlases with pristine HooDoo logo...")
for m_id, sw_list in hoodie_swatches.items():
    for slug, rgb, is_l in sw_list:
        build_hoodie_texture_atlas(m_id, slug, rgb, is_l)

# -------------------------------------------------------------
# Boxy Tee Atlases with HooDoo Logo on Front & Back Art on Back
# -------------------------------------------------------------
tee_palettes = {
    'p5':  [('white', (248, 248, 246), True), ('black', (20, 20, 22), False), ('gold', (180, 83, 9), False)],
    'p6':  [('carbon', (28, 25, 23), False),  ('cement', (87, 83, 78), False), ('bone', (231, 229, 228), True)],
    'p7':  [('sand', (184, 165, 138), False), ('obsidian', (16, 16, 18), False), ('olive', (63, 67, 56), False)],
    'p8':  [('indigo', (30, 41, 59), False),  ('maroon', (69, 10, 10), False), ('ivory', (245, 245, 244), True)],
    'p14': [('graphite', (63, 63, 70), False),('white', (248, 248, 248), True), ('onyx', (24, 24, 27), False)],
    'p15': [('espresso', (66, 49, 41), False),('pine', (40, 54, 43), False), ('slate', (51, 65, 85), False)],
}

tee_meta = {
    'p5':  {'back_src': 'public/assets/collection/p5_white_back.png',    'back_box': (190, 180, 610, 580)},
    'p6':  {'back_src': 'public/assets/collection/p6_carbon_back.png',   'back_box': (180, 180, 620, 580)},
    'p7':  {'back_src': 'public/assets/collection/p7_sand_back.png',     'back_box': (190, 180, 610, 580)},
    'p8':  {'back_src': 'public/assets/collection/p8_indigo_back.png',   'back_box': (180, 170, 620, 580)},
    'p14': {'back_src': 'public/assets/collection/p14_graphite_back.png', 'back_box': (190, 180, 610, 580)},
    'p15': {'back_src': 'public/assets/collection/p15_espresso_back.png', 'back_box': (180, 170, 620, 580)},
}

def build_tee_texture_atlas(tee_id, swatch_slug, base_rgb, is_light=False):
    atlas = Image.new('RGBA', (2048, 2048), base_rgb + (255,))
    noise = np.random.normal(0, 3.5, (2048, 2048, 1))
    arr = np.array(atlas, dtype=float)
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    atlas = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    draw = ImageDraw.Draw(atlas)
    
    stitch_col = tuple(max(0, int(c * 0.75)) for c in base_rgb) + (255,) if not is_light else tuple(max(0, int(c * 0.88)) for c in base_rgb) + (255,)
    # Collar seam line
    draw.arc([400, 320, 624, 480], 0, 180, fill=stitch_col, width=3)
    draw.arc([1424, 320, 1648, 480], 180, 360, fill=stitch_col, width=3)
    
    # 1. Front Chest HooDoo Logo (Centered on X=512, Y=830)
    logo_file = "public/assets/collection/hoodoo_logo_black.png" if is_light else "public/assets/collection/hoodoo_logo_white.png"
    if os.path.exists(logo_file):
        logo_img = Image.open(logo_file).convert('RGBA')
        target_w = 340
        target_h = int(logo_img.height * (target_w / logo_img.width))
        logo_res = logo_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        px = 512 - target_w // 2
        py = 830 - target_h // 2
        atlas.paste(logo_res, (px, py), logo_res)
        
    # 2. Back Graphic (Centered on X=1536, Y=920)
    t_meta = tee_meta.get(tee_id)
    if t_meta:
        back_stamp = extract_stamp(t_meta['back_src'], t_meta['back_box'], diff_cut=18, feather=14)
        if back_stamp:
            gw = 780
            gh = int(back_stamp.height * (gw / back_stamp.width))
            b_res = back_stamp.resize((gw, gh), Image.Resampling.LANCZOS)
            if is_light:
                b_arr = np.array(b_res, dtype=float)
                is_white = (b_arr[:, :, 0] > 180) & (b_arr[:, :, 1] > 180) & (b_arr[:, :, 2] > 180)
                b_arr[is_white, :3] = [28, 28, 32]
                b_res = Image.fromarray(b_arr.astype(np.uint8))
            px = 1536 - gw // 2
            py = 920 - gh // 2
            atlas.paste(b_res, (px, py), b_res)
        
    out_path = f"public/assets/models/textures/tex_{tee_id}_{swatch_slug}.png"
    atlas.save(out_path, 'PNG')
    if swatch_slug in ('white', 'carbon', 'sand', 'indigo', 'graphite', 'espresso'):
        base_out = f"public/assets/models/textures/tex_{tee_id}.png"
        atlas.save(base_out, 'PNG')
    print(f"Generated Tee Atlas: {out_path}")

print("Generating all Tee Atlases with HooDoo logo on front & artwork on back...")
for t_id, sw_list in tee_palettes.items():
    for slug, rgb, is_l in sw_list:
        build_tee_texture_atlas(t_id, slug, rgb, is_l)

# Mirror to public/models/textures
shutil.copytree("public/assets/models/textures", "public/models/textures", dirs_exist_ok=True)
print("Mirrored all texture atlases to public/models/textures!")
