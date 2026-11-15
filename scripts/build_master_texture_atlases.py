import os
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import numpy as np

os.makedirs('public/assets/models/textures', exist_ok=True)

def create_pure_graphic_stamp(img_path, box, bg_color=None, diff_cutoff=18, feather=14):
    if not os.path.exists(img_path):
        return None
    im = Image.open(img_path).convert('RGBA')
    crop = im.crop(box)
    w, h = crop.size
    arr = np.array(crop, dtype=float)
    
    if bg_color is None:
        sample = np.concatenate([
            arr[:8, :8, :3].reshape(-1, 3),
            arr[:8, -8:, :3].reshape(-1, 3),
            arr[-8:, :8, :3].reshape(-1, 3),
            arr[-8:, -8:, :3].reshape(-1, 3),
        ])
        bg_rgb = np.median(sample, axis=0)
    else:
        bg_rgb = np.array(bg_color, dtype=float)
        
    diff = np.linalg.norm(arr[:, :, :3] - bg_rgb, axis=2)
    alpha = np.clip((diff - diff_cutoff) / 22.0 * 255.0, 0, 255).astype(np.float32)
    
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((feather, feather, w - feather, h - feather), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather * 0.8))
    mask_arr = np.array(mask, dtype=np.float32) / 255.0
    
    final_alpha = (alpha * mask_arr).astype(np.uint8)
    arr[:, :, 3] = final_alpha
    return Image.fromarray(arr.astype(np.uint8))

hoodies_config = [
    {
        'id': 'hero',
        'front_src': 'public/assets/collection/hero_asphalt.png',
        'front_box': (410, 250, 540, 340),
        'front_w': 380,
        'back_src': 'public/assets/collection/hero_asphalt_back.png',
        'back_box': (200, 200, 600, 520),
        'back_w': 720,
        'base_rgb': (30, 30, 32),
        'out': 'public/assets/models/textures/tex_hero.png'
    },
    {
        'id': 'p1',
        'front_src': 'public/assets/collection/p1_black.png',
        'front_box': (410, 240, 540, 350),
        'front_w': 360,
        'back_src': 'public/assets/collection/p1_black_back.png',
        'back_box': (220, 180, 580, 540),
        'back_w': 700,
        'base_rgb': (16, 16, 18),
        'out': 'public/assets/models/textures/tex_p1.png'
    },
    {
        'id': 'p2',
        'front_src': 'public/assets/collection/p2_cocoa.png',
        'front_box': (430, 250, 540, 335),
        'front_w': 380,
        'back_src': 'public/assets/collection/p2_cocoa_back.png',
        'back_box': (240, 220, 560, 580),
        'back_w': 740,
        'base_rgb': (78, 54, 44),
        'out': 'public/assets/models/textures/tex_p2.png'
    },
    {
        'id': 'p3',
        'front_src': 'public/assets/collection/p3_black.png',
        'front_box': (410, 240, 540, 340),
        'front_w': 340,
        'back_src': 'public/assets/collection/p3_black_back.png',
        'back_box': (240, 220, 560, 560),
        'back_w': 680,
        'base_rgb': (22, 22, 24),
        'out': 'public/assets/models/textures/tex_p3.png'
    },
    {
        'id': 'p4',
        'front_src': 'public/assets/collection/p4_sand.png',
        'front_box': (420, 240, 540, 340),
        'front_w': 360,
        'back_src': 'public/assets/collection/p4_sand_back.png',
        'back_box': (220, 200, 580, 560),
        'back_w': 720,
        'base_rgb': (176, 162, 142),
        'out': 'public/assets/models/textures/tex_p4.png'
    },
    {
        'id': 'p13',
        'front_src': 'public/assets/collection/p13_asphalt.png',
        'front_box': (410, 250, 540, 340),
        'front_w': 360,
        'back_src': 'public/assets/collection/p13_asphalt_back.png',
        'back_box': (220, 180, 580, 540),
        'back_w': 700,
        'base_rgb': (34, 34, 38),
        'out': 'public/assets/models/textures/tex_p13.png'
    },
]

def generate_master_atlas(cfg):
    base_rgb = cfg['base_rgb']
    atlas = Image.new('RGBA', (2048, 2048), base_rgb + (255,))
    
    # 1. 500GSM Loopback French Terry / Heavy Fleece procedural fabric weave
    noise = np.random.normal(0, 4.5, (2048, 2048, 1))
    arr = np.array(atlas, dtype=float)
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    atlas = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    draw = ImageDraw.Draw(atlas)
    
    # 2. Seam Stitching details (shoulder seams, pocket welt seams)
    stitch_lo = tuple(max(0, int(c * 0.72)) for c in base_rgb) + (255,)
    stitch_hi = tuple(min(255, int(c * 1.28)) for c in base_rgb) + (255,)
    
    # Waistband ribbing texture (PIL Y: 1850 to 2048)
    for y in range(1850, 2048, 6):
        draw.line([(0, y), (2048, y)], fill=stitch_lo, width=2)
        draw.line([(0, y+1), (2048, y+1)], fill=stitch_hi, width=1)
        
    # Kangaroo pocket welt outline on Front (X: 300 to 724, Y: 1420 to 1820)
    draw.polygon([(320, 1420), (704, 1420), (790, 1820), (234, 1820)], outline=stitch_lo, width=4)
    draw.polygon([(322, 1422), (702, 1422), (788, 1818), (236, 1818)], outline=stitch_hi, width=2)
    
    # 3. Paste Front Chest Artwork
    front_stamp = create_pure_graphic_stamp(
        cfg['front_src'],
        cfg['front_box'],
        diff_cutoff=16,
        feather=12
    )
    if front_stamp:
        gw = cfg['front_w']
        gh = int(front_stamp.height * (gw / front_stamp.width))
        f_res = front_stamp.resize((gw, gh), Image.Resampling.LANCZOS)
        # Position on chest (X center = 512, Y around 900)
        px = 512 - gw // 2
        py = 880 - gh // 2
        atlas.paste(f_res, (px, py), f_res)
        
    # 4. Paste Back Mural Artwork
    back_stamp = create_pure_graphic_stamp(
        cfg['back_src'],
        cfg['back_box'],
        diff_cutoff=16,
        feather=16
    )
    if back_stamp:
        gw = cfg['back_w']
        gh = int(back_stamp.height * (gw / back_stamp.width))
        b_res = back_stamp.resize((gw, gh), Image.Resampling.LANCZOS)
        # Position on back (X center = 1536, Y around 920)
        px = 1536 - gw // 2
        py = 920 - gh // 2
        atlas.paste(b_res, (px, py), b_res)
        
    atlas.save(cfg['out'], 'PNG')
    print(f"Generated atlas: {cfg['out']}")

for c in hoodies_config:
    generate_master_atlas(c)

print("ALL 6 MASTER TEXTURE ATLASES GENERATED CLEANLY!")
