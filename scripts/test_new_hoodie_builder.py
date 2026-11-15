import os
from PIL import Image, ImageFilter, ImageOps, ImageDraw
import numpy as np

os.makedirs('public/assets/models/textures', exist_ok=True)

# 1. Helper to extract clean graphic without background or garment border
def extract_pure_graphic(img_path, crop_box, bg_sample_box=None, diff_thresh=25, feather=15):
    if not os.path.exists(img_path):
        return None
    im = Image.open(img_path).convert('RGBA')
    crop = im.crop(crop_box)
    w, h = crop.size
    arr = np.array(crop, dtype=float)
    
    # Sample background color from edges of crop
    if bg_sample_box:
        bg_sample = np.array(crop.crop(bg_sample_box), dtype=float)
        bg_rgb = np.median(bg_sample.reshape(-1, 4)[:, :3], axis=0)
    else:
        edges = np.concatenate([
            arr[:10, :10, :3].reshape(-1, 3),
            arr[:10, -10:, :3].reshape(-1, 3),
            arr[-10:, :10, :3].reshape(-1, 3),
            arr[-10:, -10:, :3].reshape(-1, 3)
        ])
        bg_rgb = np.median(edges, axis=0)
        
    diff = np.linalg.norm(arr[:, :, :3] - bg_rgb, axis=2)
    # Alpha based on color difference
    alpha = np.clip((diff - diff_thresh) / 20.0 * 255.0, 0, 255).astype(np.float32)
    
    # Elliptical border fade so no hard square edges ever exist
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((feather, feather, w - feather, h - feather), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(feather * 0.7))
    mask_arr = np.array(mask, dtype=np.float32) / 255.0
    
    final_alpha = (alpha * mask_arr).astype(np.uint8)
    arr[:, :, 3] = final_alpha
    return Image.fromarray(arr.astype(np.uint8))

def build_texture_atlas(front_img, back_img, out_path, base_rgb=(32, 32, 34)):
    # 2048 x 2048 texture atlas
    # U [0, 1024]: Front (Torso, Front of Sleeves, Front of Hood)
    # U [1024, 2048]: Back (Torso, Back of Sleeves, Back of Hood)
    atlas = Image.new('RGBA', (2048, 2048), base_rgb + (255,))
    
    # A. 500GSM Loopback French Terry / Heavy Fleece procedural fabric weave
    r, g, b = base_rgb
    # High-frequency micro-grain
    noise = np.random.normal(0, 5.0, (2048, 2048, 1))
    arr = np.array(atlas, dtype=float)
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    atlas = Image.fromarray(arr.astype(np.uint8), mode='RGBA')
    draw = ImageDraw.Draw(atlas)
    
    # B. Seam Stitching details (shoulder seams, pocket welt seams)
    stitch_color = tuple(max(0, int(c * 0.75)) for c in base_rgb) + (255,)
    stitch_hi = tuple(min(255, int(c * 1.25)) for c in base_rgb) + (255,)
    
    # Waistband ribbing texture (V: 0 to 200 in UV space -> PIL Y: 1848 to 2048)
    for y in range(1850, 2048, 6):
        draw.line([(0, y), (2048, y)], fill=stitch_color, width=2)
        draw.line([(0, y+1), (2048, y+1)], fill=stitch_hi, width=1)
        
    # Kangaroo pocket outline on Front (X: 260 to 764, Y: 1400 to 1800)
    draw.polygon([(320, 1420), (704, 1420), (790, 1820), (234, 1820)], outline=stitch_color, width=4)
    draw.polygon([(322, 1422), (702, 1422), (788, 1818), (236, 1818)], outline=stitch_hi, width=2)
    
    # C. Paste Graphic Artworks
    # 1. Front Graphic Hit (Chest area: X ~ 512, Y: 850 to 1250)
    front_g = extract_pure_graphic(
        front_img,
        crop_box=(220, 240, 580, 500),
        diff_thresh=18,
        feather=12
    )
    if front_g:
        # Resize to fit chest perfectly
        gw = 520
        gh = int(front_g.height * (gw / front_g.width))
        front_res = front_g.resize((gw, gh), Image.Resampling.LANCZOS)
        # Center in front half (X center = 512, Y around 950)
        px = 512 - gw // 2
        py = 920 - gh // 2
        atlas.paste(front_res, (px, py), front_res)
        print(f"Pasted front chest graphic at ({px}, {py})")
        
    # 2. Back Graphic Mural (Back area: X ~ 1536, Y: 700 to 1350)
    back_g = extract_pure_graphic(
        back_img,
        crop_box=(160, 160, 640, 560),
        diff_thresh=18,
        feather=16
    )
    if back_g:
        gw = 780
        gh = int(back_g.height * (gw / back_g.width))
        back_res = back_g.resize((gw, gh), Image.Resampling.LANCZOS)
        # Center in back half (X center = 1536, Y around 980)
        px = 1536 - gw // 2
        py = 960 - gh // 2
        atlas.paste(back_res, (px, py), back_res)
        print(f"Pasted back mural graphic at ({px}, {py})")
        
    atlas.save(out_path, 'PNG')
    print(f"Saved texture atlas: {out_path}")

if __name__ == '__main__':
    build_texture_atlas(
        'public/assets/collection/hero_asphalt.png',
        'public/assets/collection/hero_asphalt_back.png',
        'public/assets/models/textures/tex_hero_master.png',
        base_rgb=(32, 32, 34)
    )
