import os
from PIL import Image, ImageFilter
import numpy as np
from collections import deque

os.makedirs('public/assets/collection', exist_ok=True)

hoodies_data = [
    {
        'id': 'hero',
        'src': 'public/assets/westcoast_hero_hoodie.png',
        'front_out': 'public/assets/collection/hero_asphalt.png',
        'back_out': 'public/assets/collection/hero_asphalt_back.png',
        'colorways': [
            {'name': 'hero_bone', 'tint': (232, 228, 220), 'mode': 'bone'},
            {'name': 'hero_royal', 'tint': (30, 58, 110), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p1',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_paisley_ghost_1794623856703.jpg',
        'front_out': 'public/assets/collection/p1_black.png',
        'back_out': 'public/assets/collection/p1_black_back.png',
        'colorways': [
            {'name': 'p1_red', 'tint': (140, 24, 32), 'mode': 'tint'},
            {'name': 'p1_blue', 'tint': (28, 52, 105), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p2',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_hydraulic_ghost_1794623904791.jpg',
        'front_out': 'public/assets/collection/p2_cocoa.png',
        'back_out': 'public/assets/collection/p2_cocoa_back.png',
        'colorways': [
            {'name': 'p2_charcoal', 'tint': (42, 42, 44), 'mode': 'charcoal'},
            {'name': 'p2_tan', 'tint': (160, 135, 110), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p4',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_venice_ghost_1794623983058.jpg',
        'front_out': 'public/assets/collection/p4_sand.png',
        'back_out': 'public/assets/collection/p4_sand_back.png',
        'colorways': [
            {'name': 'p4_rose', 'tint': (165, 125, 130), 'mode': 'tint'},
            {'name': 'p4_sage', 'tint': (120, 138, 122), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p13',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_midnight_ghost_1794624031806.jpg',
        'front_out': 'public/assets/collection/p13_asphalt.png',
        'back_out': 'public/assets/collection/p13_asphalt_back.png',
        'colorways': [
            {'name': 'p13_bone', 'tint': (228, 224, 216), 'mode': 'bone'},
            {'name': 'p13_navy', 'tint': (24, 38, 70), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p3',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\hoodie_midnight_ghost_1794624031806.jpg',
        'front_out': 'public/assets/collection/p3_black.png',
        'back_out': 'public/assets/collection/p3_black_back.png',
        'colorways': [
            {'name': 'p3_ash', 'tint': (110, 110, 115), 'mode': 'tint'},
            {'name': 'p3_khaki', 'tint': (75, 85, 68), 'mode': 'tint'},
        ]
    }
]

def extract_and_isolate_ghost(img_path, is_back=False, diff_thresh=42):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    
    # Split 16:9 into left (front) or right (back)
    crop_box = (w // 2, 0, w, h) if is_back else (0, 0, w // 2, h)
    half_im = im.crop(crop_box)
    cw, ch = half_im.size
    arr = np.array(half_im, dtype=float)
    
    # Background color estimation from edges
    borders = np.concatenate([arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]], axis=0)
    bg = np.median(borders, axis=0)
    diff = np.sqrt(np.sum((arr - bg)**2, axis=-1))
    
    is_bg = (diff < diff_thresh)
    visited = np.zeros((ch, cw), dtype=bool)
    q = deque()
    
    for x in range(cw):
        if is_bg[0, x]:
            q.append((0, x))
            visited[0, x] = True
        if is_bg[ch-1, x] and not visited[ch-1, x]:
            q.append((ch-1, x))
            visited[ch-1, x] = True
    for y in range(ch):
        if is_bg[y, 0] and not visited[y, 0]:
            q.append((y, 0))
            visited[y, 0] = True
        if is_bg[y, cw-1] and not visited[y, cw-1]:
            q.append((y, cw-1))
            visited[y, cw-1] = True
            
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((-1,0), (1,0), (0,-1), (0,1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < ch and 0 <= nx < cw and not visited[ny, nx]:
                if is_bg[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))
                    
    # Foreground mask
    alpha = (~visited).astype(np.uint8) * 255
    # Morphological erosion then dilation to kill background halos/fringes
    alpha_img = Image.fromarray(alpha, mode='L').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    
    rgba = half_im.convert('RGBA')
    rgba.putalpha(alpha_img)
    
    bbox = rgba.getbbox()
    if not bbox:
        return rgba
        
    pad = 10
    cropped = rgba.crop((
        max(0, bbox[0] - pad),
        max(0, bbox[1] - pad),
        min(cw, bbox[2] + pad),
        min(ch, bbox[3] + pad)
    ))
    
    target = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
    cropped.thumbnail((730, 730), Image.Resampling.LANCZOS)
    px = (800 - cropped.width) // 2
    py = (800 - cropped.height) // 2
    target.paste(cropped, (px, py), cropped)
    return target

def apply_colorway_shift(base_img, target_tint, mode='tint'):
    arr = np.array(base_img, dtype=float)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    
    tr, tg, tb = target_tint
    lum = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    
    if mode == 'bone':
        # Invert darkness to bone off-white while preserving graphic shadows
        inverted_lum = 255.0 - lum
        shift_rgb = np.zeros_like(rgb)
        factor = np.clip((lum / 60.0), 0.0, 1.0)
        # Highlight fabric to bone, keep deep graphics dark
        shift_rgb[:, :, 0] = np.clip(tr * 0.85 + (lum * 0.35), 0, 255)
        shift_rgb[:, :, 1] = np.clip(tg * 0.85 + (lum * 0.35), 0, 255)
        shift_rgb[:, :, 2] = np.clip(tb * 0.85 + (lum * 0.35), 0, 255)
        # Preserve text/graphic darkness
        mask = (lum < 55)
        shift_rgb[mask] = rgb[mask] * 0.8
    elif mode == 'charcoal':
        shift_rgb = rgb * 0.85
    else: # Natural dye tint
        shift_rgb = np.zeros_like(rgb)
        norm_tint = np.array([tr, tg, tb]) / 128.0
        shift_rgb[:, :, 0] = np.clip(rgb[:, :, 0] * 0.45 + lum * norm_tint[0] * 0.45, 0, 255)
        shift_rgb[:, :, 1] = np.clip(rgb[:, :, 1] * 0.45 + lum * norm_tint[1] * 0.45, 0, 255)
        shift_rgb[:, :, 2] = np.clip(rgb[:, :, 2] * 0.45 + lum * norm_tint[2] * 0.45, 0, 255)
        
    out_arr = np.dstack([shift_rgb.astype(np.uint8), alpha.astype(np.uint8)])
    return Image.fromarray(out_arr, mode='RGBA')

def process_all():
    for item in hoodies_data:
        src = item['src']
        if not os.path.exists(src):
            print(f"Skipping {item['id']}: {src} not found")
            continue
            
        print(f"Processing master ghost hoodie: {item['id']}...")
        front = extract_and_isolate_ghost(src, is_back=False)
        back = extract_and_isolate_ghost(src, is_back=True)
        
        front.save(item['front_out'], 'PNG')
        back.save(item['back_out'], 'PNG')
        print(f"  Saved front: {item['front_out']}")
        print(f"  Saved back: {item['back_out']}")
        
        # Colorway swatches
        for cw in item.get('colorways', []):
            cw_name = cw['name']
            cw_front = apply_colorway_shift(front, cw['tint'], cw['mode'])
            cw_back = apply_colorway_shift(back, cw['tint'], cw['mode'])
            
            f_path = f"public/assets/collection/{cw_name}.png"
            b_path = f"public/assets/collection/{cw_name}_back.png"
            cw_front.save(f_path, 'PNG')
            cw_back.save(b_path, 'PNG')
            print(f"    Colorway swatch: {cw_name} front & back saved")

if __name__ == '__main__':
    process_all()
    print("ALL GHOST MANNEQUIN HOODIES AND COLORWAYS SUCCESSFULLY GENERATED!")
