import os
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np
from collections import deque

os.makedirs('public/assets/collection', exist_ok=True)

# -------------------------------------------------------------
# Clean Background Extraction Functions
# -------------------------------------------------------------
def isolate_tee(img_path, is_right_half=False, diff_thresh=38):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    
    crop_box = (w // 2, 0, w, h) if is_right_half else (0, 0, w // 2, h)
    half = im.crop(crop_box)
    cw, ch = half.size
    arr = np.array(half, dtype=float)
    
    # Sample background from borders
    borders = np.concatenate([arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]], axis=0)
    bg = np.median(borders, axis=0)
    diff = np.sqrt(np.sum((arr - bg)**2, axis=-1))
    
    is_bg = diff < diff_thresh
    visited = np.zeros((ch, cw), dtype=bool)
    q = deque()
    
    for x in range(cw):
        if is_bg[0, x]: q.append((0, x)); visited[0, x] = True
        if is_bg[ch-1, x] and not visited[ch-1, x]: q.append((ch-1, x)); visited[ch-1, x] = True
    for y in range(ch):
        if is_bg[y, 0] and not visited[y, 0]: q.append((y, 0)); visited[y, 0] = True
        if is_bg[y, cw-1] and not visited[y, cw-1]: q.append((y, cw-1)); visited[y, cw-1] = True
        
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((-1,0), (1,0), (0,-1), (0,1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < ch and 0 <= nx < cw and not visited[ny, nx]:
                if is_bg[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))
                    
    alpha = (~visited).astype(np.uint8) * 255
    alpha_img = Image.fromarray(alpha, mode='L').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    
    rgba = half.convert('RGBA')
    rgba.putalpha(alpha_img)
    
    bbox = rgba.getbbox()
    if not bbox:
        return rgba
    cropped = rgba.crop(bbox)
    
    # Fit into 800x800 square
    tw, th = 800, 800
    pad = 70
    scale = min((tw - 2*pad) / cropped.width, (th - 2*pad) / cropped.height)
    nw, nh = int(cropped.width * scale), int(cropped.height * scale)
    res = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
    
    final = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    final.paste(res, ((tw - nw) // 2, (th - nh) // 2), res)
    return final

def isolate_kicks(img_path, is_right_half=False, max_y=495, max_step=7.5):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    
    crop_box = (w // 2, 0, w, h) if is_right_half else (0, 0, w // 2, h)
    half = im.crop(crop_box)
    cw, ch = half.size
    arr = np.array(half, dtype=float)
    
    visited = np.zeros((ch, cw), dtype=bool)
    starts = [(0, x) for x in range(cw)] + [(y, 0) for y in range(ch)] + [(y, cw-1) for y in range(ch)]
    q = deque(starts)
    for p in starts:
        visited[p[0], p[1]] = True
        
    while q:
        cy, cx = q.popleft()
        c_val = arr[cy, cx]
        for dy, dx in ((-1,0), (1,0), (0,-1), (0,1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < ch and 0 <= nx < cw and not visited[ny, nx]:
                if max_y and ny >= max_y:
                    visited[ny, nx] = True
                    q.append((ny, nx))
                    continue
                n_val = arr[ny, nx]
                step_diff = np.sqrt(np.sum((c_val - n_val)**2))
                if step_diff < max_step:
                    visited[ny, nx] = True
                    q.append((ny, nx))
                    
    alpha = (~visited).astype(np.uint8) * 255
    alpha_img = Image.fromarray(alpha, mode='L').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = half.convert('RGBA')
    rgba.putalpha(alpha_img)
    
    bbox = rgba.getbbox()
    if not bbox:
        return rgba
    cropped = rgba.crop(bbox)
    
    tw, th = 800, 800
    pad = 90
    scale = min((tw - 2*pad) / cropped.width, (th - 2*pad) / cropped.height)
    nw, nh = int(cropped.width * scale), int(cropped.height * scale)
    res = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
    
    final = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    final.paste(res, ((tw - nw) // 2, (th - nh) // 2), res)
    return final

# Helper to generate tinted colorway swatches
def create_swatch(base_rgba, tint_rgb, mode='tint'):
    arr = np.array(base_rgba, dtype=float)
    alpha = arr[:, :, 3]
    mask = alpha > 40
    
    if mode == 'bone' or mode == 'white':
        # Lighten / desaturate towards cream/bone
        gray = 0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2]
        norm = gray / 255.0
        r_t, g_t, b_t = tint_rgb
        for c, t_val in enumerate((r_t, g_t, b_t)):
            arr[mask, c] = np.clip(t_val * (0.65 + 0.35 * norm[mask]), 0, 255)
    elif mode == 'black' or mode == 'dark':
        gray = 0.299 * arr[:,:,0] + 0.587 * arr[:,:,1] + 0.114 * arr[:,:,2]
        norm = gray / 255.0
        for c in range(3):
            arr[mask, c] = np.clip(tint_rgb[c] * (0.8 + 0.4 * norm[mask]), 0, 255)
    else: # Normal tint
        r_t, g_t, b_t = tint_rgb
        gray = (arr[:,:,0] + arr[:,:,1] + arr[:,:,2]) / 3.0
        norm = gray / 255.0
        for c, t_val in enumerate((r_t, g_t, b_t)):
            arr[mask, c] = np.clip(t_val * (0.5 + 0.5 * norm[mask]), 0, 255)
            
    arr[:, :, 3] = alpha
    return Image.fromarray(arr.astype(np.uint8))

# -------------------------------------------------------------
# Configuration for T-Shirts
# -------------------------------------------------------------
tees_specs = [
    {
        'id': 'p5',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_crenshaw_dark_bg_1794680274429.jpg',
        'front_out': 'public/assets/collection/p5_white.png',
        'back_out': 'public/assets/collection/p5_white_back.png',
        'swatches': [
            {'name': 'p5_black', 'tint': (23, 23, 23), 'mode': 'black'},
            {'name': 'p5_gold',  'tint': (180, 83, 9),  'mode': 'tint'},
        ]
    },
    {
        'id': 'p6',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_southcentral_ghost_1794678808478.jpg',
        'front_out': 'public/assets/collection/p6_carbon.png',
        'back_out': 'public/assets/collection/p6_carbon_back.png',
        'swatches': [
            {'name': 'p6_cement', 'tint': (87, 83, 78), 'mode': 'tint'},
            {'name': 'p6_bone',   'tint': (231, 229, 228), 'mode': 'bone'},
        ]
    },
    {
        'id': 'p7',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_localsonly_ghost_1794678828498.jpg',
        'front_out': 'public/assets/collection/p7_sand.png',
        'back_out': 'public/assets/collection/p7_sand_back.png',
        'swatches': [
            {'name': 'p7_obsidian', 'tint': (16, 16, 18), 'mode': 'black'},
            {'name': 'p7_olive',    'tint': (63, 67, 56), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p8',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_eastla_paisley_ghost_1794678851227.jpg',
        'front_out': 'public/assets/collection/p8_indigo.png',
        'back_out': 'public/assets/collection/p8_indigo_back.png',
        'swatches': [
            {'name': 'p8_maroon', 'tint': (69, 10, 10), 'mode': 'tint'},
            {'name': 'p8_ivory',  'tint': (245, 245, 244), 'mode': 'bone'},
        ]
    },
    {
        'id': 'p14',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chrome_ghost_1794678874804.jpg',
        'front_out': 'public/assets/collection/p14_graphite.png',
        'back_out': 'public/assets/collection/p14_graphite_back.png',
        'swatches': [
            {'name': 'p14_white', 'tint': (250, 250, 250), 'mode': 'white'},
            {'name': 'p14_onyx',  'tint': (24, 24, 27), 'mode': 'black'},
        ]
    },
    {
        'id': 'p15',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\tee_chicanosoul_ghost_1794678896392.jpg',
        'front_out': 'public/assets/collection/p15_espresso.png',
        'back_out': 'public/assets/collection/p15_espresso_back.png',
        'swatches': [
            {'name': 'p15_pine',  'tint': (40, 54, 43), 'mode': 'tint'},
            {'name': 'p15_slate', 'tint': (51, 65, 85), 'mode': 'tint'},
        ]
    },
]

# -------------------------------------------------------------
# Configuration for Skate Sneakers
# -------------------------------------------------------------
kicks_specs = [
    {
        'id': 'p9',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_1_chicano_bone_gum_1794678794364.jpg',
        'front_out': 'public/assets/collection/p9_bone.png',
        'back_out': 'public/assets/collection/p9_bone_back.png',
        'swatches': [
            {'name': 'p9_black', 'tint': (18, 18, 18), 'mode': 'black'},
            {'name': 'p9_cocoa', 'tint': (92, 64, 51), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p10',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_2_midnight_stealth_runner_1794678820355.jpg',
        'front_out': 'public/assets/collection/p10_noir.png',
        'back_out': 'public/assets/collection/p10_noir_back.png',
        'swatches': [
            {'name': 'p10_grey', 'tint': (64, 64, 64), 'mode': 'tint'},
            {'name': 'p10_onyx', 'tint': (38, 38, 38), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p11',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_3_chopper_suede_skate_low_1794678841870.jpg',
        'front_out': 'public/assets/collection/p11_choco.png',
        'back_out': 'public/assets/collection/p11_choco_back.png',
        'swatches': [
            {'name': 'p11_jet',  'tint': (23, 23, 23), 'mode': 'black'},
            {'name': 'p11_moss', 'tint': (49, 61, 51), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p12',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_4_paisley_swoop_retro_low_1794678863208.jpg',
        'front_out': 'public/assets/collection/p12_sail.png',
        'back_out': 'public/assets/collection/p12_sail_back.png',
        'swatches': [
            {'name': 'p12_crimson', 'tint': (24, 24, 27), 'mode': 'black'},
            {'name': 'p12_khaki',   'tint': (156, 163, 175), 'mode': 'tint'},
        ]
    },
    {
        'id': 'p16',
        'src': r'C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985\sneaker_5_eastside_gum_sole_retro_1794678883648.jpg',
        'front_out': 'public/assets/collection/p16_obsidian.png',
        'back_out': 'public/assets/collection/p16_obsidian_back.png',
        'swatches': [
            {'name': 'p16_duck', 'tint': (245, 245, 244), 'mode': 'bone'},
            {'name': 'p16_navy', 'tint': (30, 58, 138), 'mode': 'tint'},
        ]
    },
]

def main():
    print("=== PROCESSING ALL BOXY T-SHIRTS ===")
    for spec in tees_specs:
        print(f"Processing tee {spec['id']}...")
        f_img = isolate_tee(spec['src'], is_right_half=False)
        b_img = isolate_tee(spec['src'], is_right_half=True)
        f_img.save(spec['front_out'], 'PNG')
        b_img.save(spec['back_out'], 'PNG')
        print(f"  Saved {spec['front_out']} and {spec['back_out']}")
        
        for sw in spec['swatches']:
            sw_f = create_swatch(f_img, sw['tint'], mode=sw['mode'])
            sw_b = create_swatch(b_img, sw['tint'], mode=sw['mode'])
            sw_f_out = f"public/assets/collection/{sw['name']}.png"
            sw_b_out = f"public/assets/collection/{sw['name']}_back.png"
            sw_f.save(sw_f_out, 'PNG')
            sw_b.save(sw_b_out, 'PNG')
            print(f"  Saved swatch {sw_f_out} and {sw_b_out}")
            
    print("=== PROCESSING ALL SKATE SNEAKERS ===")
    for spec in kicks_specs:
        print(f"Processing kicks {spec['id']}...")
        f_img = isolate_kicks(spec['src'], is_right_half=False)
        b_img = isolate_kicks(spec['src'], is_right_half=True)
        f_img.save(spec['front_out'], 'PNG')
        b_img.save(spec['back_out'], 'PNG')
        print(f"  Saved {spec['front_out']} and {spec['back_out']}")
        
        for sw in spec['swatches']:
            sw_f = create_swatch(f_img, sw['tint'], mode=sw['mode'])
            sw_b = create_swatch(b_img, sw['tint'], mode=sw['mode'])
            sw_f_out = f"public/assets/collection/{sw['name']}.png"
            sw_b_out = f"public/assets/collection/{sw['name']}_back.png"
            sw_f.save(sw_f_out, 'PNG')
            sw_b.save(sw_b_out, 'PNG')
            print(f"  Saved swatch {sw_f_out} and {sw_b_out}")
            
    print("ALL 11 PRODUCT COLLECTIONS (TEES & SNEAKERS) EXTRACTED & SAVED CLEANLY!")

if __name__ == '__main__':
    main()
