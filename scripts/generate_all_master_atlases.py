import os
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import numpy as np

os.makedirs('public/assets/models/textures', exist_ok=True)

# Helper to extract clean graphic with feathered border
def extract_stamp(img_path, box, diff_cut=18, feather=14):
    if not os.path.exists(img_path):
        return None
    im = Image.open(img_path).convert('RGBA')
    crop = im.crop(box)
    w, h = crop.size
    arr = np.array(crop, dtype=float)
    
    # Sample corner borders for fabric color
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
swatch_palettes = {
    'hero': [
        ('asphalt', (28, 28, 30), False),
        ('bone',    (230, 226, 218), True),
        ('royal',   (26, 38, 65), False),
    ],
    'p1': [
        ('black',   (14, 14, 16), False),
        ('red',     (125, 24, 28), False),
        ('blue',    (26, 50, 105), False),
    ],
    'p2': [
        ('cocoa',   (75, 52, 42), False),
        ('charcoal',(38, 38, 40), False),
        ('tan',     (155, 130, 105), False),
    ],
    'p3': [
        ('black',   (18, 18, 20), False),
        ('ash',     (95, 95, 100), False),
        ('khaki',   (68, 75, 62), False),
    ],
    'p4': [
        ('sand',    (170, 158, 140), False),
        ('rose',    (150, 115, 120), False),
        ('sage',    (115, 130, 115), False),
    ],
    'p13': [
        ('asphalt', (32, 32, 36), False),
        ('bone',    (228, 224, 216), True),
        ('navy',    (24, 34, 58), False),
    ],
}

models_meta = {
    'hero': {
        'front_src': 'public/assets/collection/hero_asphalt.png',
        'front_box': (390, 240, 560, 360),
        'back_src': 'public/assets/collection/hero_asphalt_back.png',
        'back_box': (180, 170, 620, 570),
        'front_w': 520,
        'back_w': 940,
        'has_paisley': True,
    },
    'p1': {
        'front_src': 'public/assets/collection/p1_black.png',
        'front_box': (380, 220, 560, 360),
        'back_src': 'public/assets/collection/p1_black_back.png',
        'back_box': (180, 160, 620, 580),
        'front_w': 540,
        'back_w': 920,
        'has_paisley': True,
    },
    'p2': {
        'front_src': 'public/assets/collection/p2_cocoa.png',
        'front_box': (410, 230, 570, 350),
        'back_src': 'public/assets/collection/p2_cocoa_back.png',
        'back_box': (200, 180, 600, 600),
        'front_w': 520,
        'back_w': 940,
        'has_paisley': False,
    },
    'p3': {
        'front_src': 'public/assets/collection/p3_black.png',
        'front_box': (380, 220, 560, 350),
        'back_src': 'public/assets/collection/p3_black_back.png',
        'back_box': (200, 180, 600, 580),
        'front_w': 500,
        'back_w': 900,
        'has_paisley': False,
    },
    'p4': {
        'front_src': 'public/assets/collection/p4_sand.png',
        'front_box': (400, 220, 560, 350),
        'back_src': 'public/assets/collection/p4_sand_back.png',
        'back_box': (190, 170, 610, 590),
        'front_w': 500,
        'back_w': 920,
        'has_paisley': False,
    },
    'p13': {
        'front_src': 'public/assets/collection/p13_asphalt.png',
        'front_box': (380, 220, 560, 350),
        'back_src': 'public/assets/collection/p13_asphalt_back.png',
        'back_box': (180, 160, 620, 580),
        'front_w': 540,
        'back_w': 920,
        'has_paisley': False,
    },
}

def create_colorway_atlas(model_id, swatch_slug, base_rgb, is_light=False):
    meta = models_meta[model_id]
    atlas = Image.new('RGBA', (2048, 2048), base_rgb + (255,))
    
    # 1. 500GSM Loopback Cotton Fleece Grain
    noise = np.random.normal(0, 4.5, (2048, 2048, 1))
    arr = np.array(atlas, dtype=float)
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    atlas = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    draw = ImageDraw.Draw(atlas)
    
    # 2. Construction Seam Details & Ribbing
    if is_light:
        stitch_lo = tuple(max(0, int(c * 0.85)) for c in base_rgb) + (255,)
        stitch_hi = tuple(min(255, int(c * 1.05)) for c in base_rgb) + (255,)
    else:
        stitch_lo = tuple(max(0, int(c * 0.70)) for c in base_rgb) + (255,)
        stitch_hi = tuple(min(255, int(c * 1.30)) for c in base_rgb) + (255,)
        
    # Ribbed waistband (Y: 1850 to 2048)
    for y in range(1850, 2048, 6):
        draw.line([(0, y), (2048, y)], fill=stitch_lo, width=2)
        draw.line([(0, y+1), (2048, y+1)], fill=stitch_hi, width=1)
        
    # Kangaroo pocket welt on front (X: 300 to 724, Y: 1420 to 1820)
    draw.polygon([(320, 1420), (704, 1420), (790, 1820), (234, 1820)], outline=stitch_lo, width=4)
    draw.polygon([(322, 1422), (702, 1422), (788, 1818), (236, 1818)], outline=stitch_hi, width=2)
    
    # Ribbed cuffs on sleeve hems (Y: 1850 to 2048 on sleeve strips)
    for sx1, sx2 in [(40, 270), (750, 980), (1060, 1290), (1770, 2000)]:
        for y in range(1860, 2048, 8):
            draw.line([(sx1, y), (sx2, y)], fill=stitch_lo, width=2)
            
    # 3. Bandana Paisley Sleeve Art (if model has it)
    if meta['has_paisley']:
        p_col = (40, 40, 44, 180) if is_light else (220, 220, 225, 120)
        # Paisley bands on left and right sleeves
        for cx in [155, 865, 1175, 1885]:
            for py in range(950, 1700, 120):
                # Stylized paisley teardrop / flower
                draw.arc([cx - 40, py - 40, cx + 40, py + 40], 0, 360, fill=p_col, width=3)
                draw.ellipse([cx - 15, py - 15, cx + 15, py + 15], outline=p_col, width=2)
                draw.line([(cx - 30, py), (cx + 30, py)], fill=p_col, width=2)
                draw.line([(cx, py - 30), (cx, py + 30)], fill=p_col, width=2)
                
    # 4. Front Chest Artwork
    front_stamp = extract_stamp(meta['front_src'], meta['front_box'], diff_cut=16, feather=12)
    if front_stamp:
        gw = meta['front_w']
        gh = int(front_stamp.height * (gw / front_stamp.width))
        f_res = front_stamp.resize((gw, gh), Image.Resampling.LANCZOS)
        
        # If light colorway, invert graphic or darken for contrast
        if is_light:
            f_arr = np.array(f_res, dtype=float)
            # Invert RGB values while keeping alpha
            f_arr[:, :, :3] = np.clip(255.0 - f_arr[:, :, :3], 10, 60)
            f_res = Image.fromarray(f_arr.astype(np.uint8))
            
        px = 512 - gw // 2
        py = 860 - gh // 2
        atlas.paste(f_res, (px, py), f_res)
        
    # 5. Back Mural Artwork
    back_stamp = extract_stamp(meta['back_src'], meta['back_box'], diff_cut=16, feather=16)
    if back_stamp:
        gw = meta['back_w']
        gh = int(back_stamp.height * (gw / back_stamp.width))
        b_res = back_stamp.resize((gw, gh), Image.Resampling.LANCZOS)
        
        if is_light:
            b_arr = np.array(b_res, dtype=float)
            # Convert bright whites in the text to dark graphite, preserve colored car
            is_white_txt = (b_arr[:, :, 0] > 180) & (b_arr[:, :, 1] > 180) & (b_arr[:, :, 2] > 180)
            b_arr[is_white_txt, :3] = [32, 32, 36]
            b_res = Image.fromarray(b_arr.astype(np.uint8))
            
        px = 1536 - gw // 2
        py = 880 - gh // 2
        atlas.paste(b_res, (px, py), b_res)
        
    out_path = f"public/assets/models/textures/tex_{model_id}_{swatch_slug}.png"
    atlas.save(out_path, 'PNG')
    print(f"Saved: {out_path}")
    
    # Also save as base model texture if primary swatch
    if swatch_slug in ('asphalt', 'black', 'cocoa', 'sand'):
        base_out = f"public/assets/models/textures/tex_{model_id}.png"
        atlas.save(base_out, 'PNG')
        print(f"  -> Also copied to base: {base_out}")

def main():
    for model_id, swatches in swatch_palettes.items():
        print(f"Generating texture atlases for: {model_id}...")
        for slug, rgb, is_light in swatches:
            create_colorway_atlas(model_id, slug, rgb, is_light)
            
    print("ALL 3D COLORWAY TEXTURE ATLASES GENERATED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
