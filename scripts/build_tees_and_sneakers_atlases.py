import os
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import numpy as np

os.makedirs('public/assets/models/textures', exist_ok=True)

# -----------------------------------------------------------------
# 1. TEXTURE BUILDER FOR BOXY T-SHIRTS
# -----------------------------------------------------------------
tee_palettes = {
    'p5': [
        ('white', (248, 248, 246), True),
        ('black', (20, 20, 22), False),
        ('gold',  (180, 83, 9), False),
    ],
    'p6': [
        ('carbon', (28, 25, 23), False),
        ('cement', (87, 83, 78), False),
        ('bone',   (231, 229, 228), True),
    ],
    'p7': [
        ('sand',    (184, 165, 138), False),
        ('obsidian',(16, 16, 18), False),
        ('olive',   (63, 67, 56), False),
    ],
    'p8': [
        ('indigo', (30, 41, 59), False),
        ('maroon', (69, 10, 10), False),
        ('ivory',  (245, 245, 244), True),
    ],
    'p14': [
        ('graphite', (63, 63, 70), False),
        ('white',    (248, 248, 248), True),
        ('onyx',     (24, 24, 27), False),
    ],
    'p15': [
        ('espresso', (66, 49, 41), False),
        ('pine',     (40, 54, 43), False),
        ('slate',    (51, 65, 85), False),
    ],
}

# -----------------------------------------------------------------
# 2. TEXTURE BUILDER FOR SKATE SNEAKERS
# -----------------------------------------------------------------
kicks_palettes = {
    'p9': [
        ('bone',  (232, 228, 220), (194, 144, 83), True,  'leather'),
        ('black', (18, 18, 18),    (24, 24, 24),   False, 'leather'),
        ('cocoa', (92, 64, 51),    (194, 144, 83), False, 'leather'),
    ],
    'p10': [
        ('noir', (16, 16, 18), (20, 20, 22), False, 'mesh'),
        ('grey', (64, 64, 68), (35, 35, 38), False, 'mesh'),
        ('onyx', (38, 38, 42), (24, 24, 26), False, 'mesh'),
    ],
    'p11': [
        ('choco', (74, 53, 40), (184, 134, 72), False, 'suede'),
        ('jet',   (23, 23, 25), (184, 134, 72), False, 'suede'),
        ('moss',  (49, 61, 51), (184, 134, 72), False, 'suede'),
    ],
    'p12': [
        ('sail',    (244, 244, 245), (220, 210, 185), True,  'leather'),
        ('crimson', (24, 24, 27),    (20, 20, 22),    False, 'leather'),
        ('khaki',   (156, 163, 175), (185, 140, 80),  False, 'leather'),
    ],
    'p16': [
        ('obsidian', (24, 24, 27),    (194, 144, 83), False, 'canvas'),
        ('duck',     (245, 245, 244), (194, 144, 83), True,  'canvas'),
        ('navy',     (30, 58, 138),   (194, 144, 83), False, 'canvas'),
    ],
}

def extract_graphic_crop(src_path, box, diff_cut=18, feather=14):
    if not os.path.exists(src_path):
        return None
    im = Image.open(src_path).convert('RGBA')
    crop = im.crop(box)
    w, h = crop.size
    arr = np.array(crop, dtype=float)
    
    # Sample corner pixels
    sample = np.concatenate([
        arr[:8, :8, :3].reshape(-1, 3),
        arr[:8, -8:, :3].reshape(-1, 3),
        arr[-8:, :8, :3].reshape(-1, 3),
        arr[-8:, -8:, :3].reshape(-1, 3),
    ])
    bg_rgb = np.median(sample, axis=0)
    diff = np.linalg.norm(arr[:, :, :3] - bg_rgb, axis=2)
    alpha = np.clip((diff - diff_cut) / 20.0 * 255.0, 0, 255).astype(np.float32)
    
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((feather, feather, w - feather, h - feather), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather * 0.8))
    mask_arr = np.array(mask, dtype=np.float32) / 255.0
    
    arr[:, :, 3] = (alpha * mask_arr).astype(np.uint8)
    return Image.fromarray(arr.astype(np.uint8))

def build_tee_atlas(tee_id, swatch_slug, base_rgb, is_light=False):
    atlas = Image.new('RGBA', (2048, 2048), base_rgb + (255,))
    
    # 300GSM Cotton Jersey Grain
    noise = np.random.normal(0, 4.0, (2048, 2048, 1))
    arr = np.array(atlas, dtype=float)
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    atlas = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    draw = ImageDraw.Draw(atlas)
    
    # Stitching / seams
    s_col = tuple(max(0, int(c * (0.85 if is_light else 0.70))) for c in base_rgb) + (255,)
    
    # Mock neck rib lines at collar (Y: 100 to 260)
    for y in range(120, 260, 6):
        draw.line([(320, y), (704, y)], fill=s_col, width=2)
        draw.line([(1344, y), (1728, y)], fill=s_col, width=2)
        
    # Blind stitch hem at bottom (Y: 1980 to 2040)
    for y in [1990, 2005]:
        draw.line([(0, y), (2048, y)], fill=s_col, width=2)
        
    # Front and Back Graphics
    front_src = f"public/assets/collection/{tee_id}_{swatch_slug}.png"
    back_src = f"public/assets/collection/{tee_id}_{swatch_slug}_back.png"
    if not os.path.exists(front_src):
        front_src = f"public/assets/collection/{tee_id}_white.png" if os.path.exists(f"public/assets/collection/{tee_id}_white.png") else f"public/assets/collection/{tee_id}_carbon.png"
    if not os.path.exists(back_src):
        back_src = f"public/assets/collection/{tee_id}_white_back.png" if os.path.exists(f"public/assets/collection/{tee_id}_white_back.png") else f"public/assets/collection/{tee_id}_carbon_back.png"
        
    # Extract Front Chest Hit
    f_stamp = extract_graphic_crop(front_src, (380, 220, 580, 360), diff_cut=16, feather=10)
    if f_stamp:
        gw = 460
        gh = int(f_stamp.height * (gw / f_stamp.width))
        f_res = f_stamp.resize((gw, gh), Image.Resampling.LANCZOS)
        atlas.paste(f_res, (512 - gw // 2, 850 - gh // 2), f_res)
        
    # Extract Back Mural Hit
    b_stamp = extract_graphic_crop(back_src, (180, 160, 620, 600), diff_cut=16, feather=14)
    if b_stamp:
        gw = 940
        gh = int(b_stamp.height * (gw / b_stamp.width))
        b_res = b_stamp.resize((gw, gh), Image.Resampling.LANCZOS)
        atlas.paste(b_res, (1536 - gw // 2, 880 - gh // 2), b_res)
        
    out_path = f"public/assets/models/textures/tex_{tee_id}_{swatch_slug}.png"
    atlas.save(out_path, 'PNG')
    print(f"Saved Tee Atlas: {out_path}")
    
    # Save base model atlas
    if swatch_slug in ('white', 'carbon', 'sand', 'indigo', 'graphite', 'espresso'):
        base_path = f"public/assets/models/textures/tex_{tee_id}.png"
        atlas.save(base_path, 'PNG')
        print(f"  -> Copied to base: {base_path}")

def build_sneaker_atlas(kick_id, swatch_slug, upper_rgb, sole_rgb, is_light=False, mat_type='leather'):
    atlas = Image.new('RGBA', (2048, 2048), upper_rgb + (255,))
    
    # Material texture grain (leather / suede / canvas)
    noise_sigma = 3.5 if mat_type == 'leather' else (6.0 if mat_type == 'suede' else 4.8)
    noise = np.random.normal(0, noise_sigma, (2048, 2048, 1))
    arr = np.array(atlas, dtype=float)
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    atlas = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    draw = ImageDraw.Draw(atlas)
    
    # Vulcanized Rubber Cupsole & Foxing Tape (Bottom: Y = 1600 to 2048)
    sole_box = [(0, 1620), (2048, 1620), (2048, 2048), (0, 2048)]
    sole_col = sole_rgb + (255,)
    draw.rectangle([0, 1620, 2048, 2048], fill=sole_col)
    
    # Foxing texture stripes & knurled bumper
    groove_col = tuple(max(0, int(c * 0.82)) for c in sole_rgb) + (255,)
    hi_col = tuple(min(255, int(c * 1.18)) for c in sole_rgb) + (255,)
    draw.line([(0, 1622), (2048, 1622)], fill=groove_col, width=4)
    draw.line([(0, 1626), (2048, 1626)], fill=hi_col, width=2)
    
    # Rubber herringbone lines on sole edge
    for y in range(1650, 2048, 12):
        draw.line([(0, y), (2048, y)], fill=groove_col, width=2)
        
    # Upper Stitching & Eyestay Lines
    st_col = tuple(max(0, int(c * 0.70)) for c in upper_rgb) + (255,)
    st_hi = (240, 240, 240, 255) if mat_type == 'canvas' else tuple(min(255, int(c * 1.25)) for c in upper_rgb) + (255,)
    
    # Side panel overlay curve on Lateral (Left half: X = 0 to 1024)
    draw.arc([150, 700, 850, 1400], 190, 350, fill=st_col, width=4)
    draw.arc([152, 702, 848, 1398], 190, 350, fill=st_hi, width=2)
    
    # Side panel overlay curve on Medial (Right half: X = 1024 to 2048)
    draw.arc([1174, 700, 1874, 1400], 190, 350, fill=st_col, width=4)
    draw.arc([1176, 702, 1872, 1398], 190, 350, fill=st_hi, width=2)
    
    # Bandana Paisley Quarter Panel pattern (for p9 and p12)
    if kick_id in ('p9', 'p12'):
        p_col = (20, 20, 22, 230) if is_light else (240, 240, 245, 200)
        for cx in [450, 580, 1474, 1604]:
            for py in range(900, 1400, 110):
                draw.arc([cx - 35, py - 35, cx + 35, py + 35], 0, 360, fill=p_col, width=3)
                draw.ellipse([cx - 12, py - 12, cx + 12, py + 12], outline=p_col, width=2)
                draw.line([(cx - 25, py), (cx + 25, py)], fill=p_col, width=2)
                draw.line([(cx, py - 25), (cx, py + 25)], fill=p_col, width=2)
                
    # Perforated Toe Box dots at the front (Lateral: X = 750 to 950, Y = 1000 to 1350)
    dot_col = tuple(max(0, int(c * 0.65)) for c in upper_rgb) + (255,)
    for px in range(760, 930, 28):
        for py in range(1050, 1350, 32):
            draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=dot_col)
            draw.ellipse([px - 4 + 1024, py - 4, px + 4 + 1024, py + 4], fill=dot_col)
            
    out_path = f"public/assets/models/textures/tex_{kick_id}_{swatch_slug}.png"
    atlas.save(out_path, 'PNG')
    print(f"Saved Sneaker Atlas: {out_path}")
    
    # Save base model atlas
    if swatch_slug in ('bone', 'noir', 'choco', 'sail', 'obsidian'):
        base_path = f"public/assets/models/textures/tex_{kick_id}.png"
        atlas.save(base_path, 'PNG')
        print(f"  -> Copied to base: {base_path}")

def main():
    print("=== BUILDING ALL TEES TEXTURE ATLASES ===")
    for tee_id, swatches in tee_palettes.items():
        for slug, rgb, is_l in swatches:
            build_tee_atlas(tee_id, slug, rgb, is_light=is_l)
            
    print("=== BUILDING ALL SNEAKERS TEXTURE ATLASES ===")
    for kick_id, swatches in kicks_palettes.items():
        for slug, u_rgb, s_rgb, is_l, m_type in swatches:
            build_sneaker_atlas(kick_id, slug, u_rgb, s_rgb, is_light=is_l, mat_type=m_type)
            
    print("ALL 33 TEXTURE ATLASES BUILT SUCCESSFULLY!")

if __name__ == '__main__':
    main()
