import os
from PIL import Image
import numpy as np
from collections import deque

def make_transparent(img, tolerance=22):
    arr = np.array(img.convert('RGBA'))
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    white_mask = (r >= 255 - tolerance) & (g >= 255 - tolerance) & (b >= 255 - tolerance)
    
    h, w = white_mask.shape
    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    
    # Border pixels
    for x in range(w):
        if white_mask[0, x]: q.append((0, x)); visited[0, x] = True
        if white_mask[h-1, x]: q.append((h-1, x)); visited[h-1, x] = True
    for y in range(h):
        if white_mask[y, 0]: q.append((y, 0)); visited[y, 0] = True
        if white_mask[y, w-1]: q.append((y, w-1)); visited[y, w-1] = True
        
    while q:
        cy, cx = q.popleft()
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                if white_mask[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))
                    
    arr[visited, 3] = 0
    return Image.fromarray(arr)

def main():
    img_path = r'C:/Users/sanjo/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/.user_uploaded/media_1794593660745_5c5ebfd6.jpg'
    img = Image.open(img_path)
    os.makedirs('public/assets', exist_ok=True)

    # 1. Logo
    logo = img.crop((92, 18, 288, 88))
    logo_trans = make_transparent(logo, tolerance=30)
    logo_trans.save('public/assets/logo.png')

    # 2. Main Hero Hoodie (Dragon Ball Z)
    hero = img.crop((112, 235, 288, 415))
    hero_trans = make_transparent(hero, tolerance=25)
    hero_trans.save('public/assets/hero_hoodie.png')

    # 3. Hero Mini Swatches
    swatch_blue = img.crop((304, 452, 350, 498))
    swatch_blue_trans = make_transparent(swatch_blue, tolerance=25)
    swatch_blue_trans.save('public/assets/swatch_blue.png')

    swatch_brown = img.crop((355, 452, 402, 498))
    swatch_brown_trans = make_transparent(swatch_brown, tolerance=25)
    swatch_brown_trans.save('public/assets/swatch_brown.png')

    # 4. Hero Sub-thumbnails (3 items below hero)
    t1 = img.crop((95, 395, 225, 545))
    make_transparent(t1, tolerance=22).save('public/assets/hero_thumb_1.png')

    t2 = img.crop((235, 395, 355, 545))
    make_transparent(t2, tolerance=22).save('public/assets/hero_thumb_2.png')

    t3 = img.crop((370, 395, 495, 545))
    make_transparent(t3, tolerance=22).save('public/assets/hero_thumb_3.png')

    # 5. Right Catalog 4x4 Grid
    cols = [(510, 630), (635, 750), (755, 870), (875, 995)]
    rows = [(85, 205), (215, 335), (355, 450), (460, 570)]

    for r_idx, (y1, y2) in enumerate(rows):
        for c_idx, (x1, x2) in enumerate(cols):
            idx = r_idx * 4 + c_idx + 1
            crop = img.crop((x1, y1, x2, y2))
            crop_trans = make_transparent(crop, tolerance=22)
            crop_trans.save(f'public/assets/product_{idx:02d}.png')

    print('All assets processed and saved to public/assets/ successfully!')

if __name__ == '__main__':
    main()
