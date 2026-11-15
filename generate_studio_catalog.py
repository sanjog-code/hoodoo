import os
import math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

os.makedirs('public/assets/studio', exist_ok=True)

def create_studio_hoodie(filename, base_color, accent_color=None, texture_noise=0.03):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Coordinates for realistic oversized boxy hoodie silhouette
    # Draw body torso
    torso_box = [230, 310, 570, 710]
    # Torso polygon with dropped shoulders
    torso_poly = [
        (250, 310), (320, 270), (480, 270), (550, 310), # Shoulders & collar
        (610, 480), (570, 690), (230, 690), (190, 480)  # Sides & hem
    ]
    
    # Left sleeve
    left_sleeve = [
        (250, 310), (150, 390), (120, 580), (180, 595), (220, 440), (230, 380)
    ]
    # Right sleeve
    right_sleeve = [
        (550, 310), (650, 390), (680, 580), (620, 595), (580, 440), (570, 380)
    ]
    
    # Hood
    hood_poly = [
        (310, 290), (280, 210), (310, 140), (400, 115), (490, 140), (520, 210), (490, 290),
        (430, 260), (400, 275), (370, 260)
    ]
    # Kangaroo pocket
    pocket_poly = [
        (290, 520), (510, 520), (480, 640), (320, 640)
    ]
    
    # Draw elements with soft gradient shading
    r, g, b = base_color
    ar, ag, ab = accent_color if accent_color else (int(r*1.15), int(g*1.15), int(b*1.15))
    
    # Back of hood (darker)
    draw.polygon(hood_poly, fill=(int(r*0.75), int(g*0.75), int(b*0.75), 255))
    
    # Sleeves
    sleeve_color = accent_color if accent_color else base_color
    draw.polygon(left_sleeve, fill=(*sleeve_color, 255))
    draw.polygon(right_sleeve, fill=(*sleeve_color, 255))
    
    # Torso
    draw.polygon(torso_poly, fill=(*base_color, 255))
    
    # Kangaroo pocket
    draw.polygon(pocket_poly, fill=(int(r*0.9), int(g*0.9), int(b*0.9), 255))
    
    # Ribbed hem
    draw.rounded_rectangle([230, 675, 570, 715], radius=10, fill=(int(r*0.82), int(g*0.82), int(b*0.82), 255))
    # Ribbed cuffs
    draw.polygon([(120, 575), (180, 590), (170, 615), (110, 600)], fill=(int(r*0.82), int(g*0.82), int(b*0.82), 255))
    draw.polygon([(680, 575), (620, 590), (630, 615), (690, 600)], fill=(int(r*0.82), int(g*0.82), int(b*0.82), 255))
    
    # Hood interior fold
    draw.polygon([(340, 270), (400, 290), (460, 270), (450, 210), (400, 185), (350, 210)], fill=(int(r*0.5), int(g*0.5), int(b*0.5), 255))
    
    # Add subtle textile noise & folds
    arr = np.array(img).astype(np.float32)
    mask = arr[:, :, 3] > 0
    noise = np.random.normal(0, 12, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    
    res = Image.fromarray(arr.astype(np.uint8))
    # Soft contact shadow below
    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([260, 700, 540, 740], fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    
    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/studio', filename))

def create_studio_tee(filename, base_color):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    r, g, b = base_color
    
    # Oversized boxy tee silhouette
    torso = [
        (260, 250), (330, 220), (470, 220), (540, 250),
        (580, 390), (550, 680), (250, 680), (220, 390)
    ]
    left_sleeve = [(260, 250), (160, 320), (190, 440), (260, 390)]
    right_sleeve = [(540, 250), (640, 320), (610, 440), (540, 390)]
    collar = [(330, 220), (400, 250), (470, 220), (450, 210), (400, 205), (350, 210)]
    
    draw.polygon(left_sleeve, fill=(*base_color, 255))
    draw.polygon(right_sleeve, fill=(*base_color, 255))
    draw.polygon(torso, fill=(*base_color, 255))
    draw.polygon(collar, fill=(int(r*0.75), int(g*0.75), int(b*0.75), 255))
    
    # Textile folds
    draw.line([(310, 320), (330, 500)], fill=(int(r*0.88), int(g*0.88), int(b*0.88), 180), width=4)
    draw.line([(480, 330), (460, 520)], fill=(int(r*0.88), int(g*0.88), int(b*0.88), 180), width=4)
    
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 10, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))
    
    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([270, 670, 530, 710], fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    
    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/studio', filename))

def create_studio_sneaker(filename, primary_color, secondary_color, sole_color=(235, 230, 220)):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Retro Court Low profile silhouette
    # Outsole / Midsole
    midsole_poly = [
        (160, 520), (220, 530), (580, 530), (660, 500), (670, 535),
        (640, 565), (200, 565), (150, 545)
    ]
    
    # Upper silhouette
    upper_poly = [
        (180, 520), (190, 440), (270, 390), (370, 380), (460, 420),
        (560, 450), (650, 480), (660, 510), (220, 530)
    ]
    
    # Overlay panels / swoosh aesthetic
    overlay_poly = [
        (220, 520), (280, 450), (480, 450), (550, 480), (480, 520)
    ]
    
    # Collar & tongue
    collar_poly = [
        (260, 395), (320, 350), (360, 350), (370, 385)
    ]
    
    draw.polygon(midsole_poly, fill=(*sole_color, 255))
    draw.polygon(upper_poly, fill=(*primary_color, 255))
    draw.polygon(overlay_poly, fill=(*secondary_color, 255))
    draw.polygon(collar_poly, fill=(int(primary_color[0]*0.8), int(primary_color[1]*0.8), int(primary_color[2]*0.8), 255))
    
    # Eyestay & laces
    for lx in range(320, 460, 25):
        draw.line([(lx, 385), (lx+10, 420)], fill=(245, 245, 245, 220), width=3)
        
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 8, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))
    
    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([150, 555, 680, 595], fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    
    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/studio', filename))

# Generate clean, aesthetic studio items
# Hoodies
create_studio_hoodie('hoodie_obsidian.png', (32, 30, 34))
create_studio_hoodie('hoodie_cocoa.png', (65, 48, 42))
create_studio_hoodie('hoodie_plum.png', (48, 24, 72), accent_color=(88, 28, 135))
create_studio_hoodie('hoodie_clay.png', (148, 134, 122))
create_studio_hoodie('hoodie_charcoal.png', (44, 45, 48))

# Tees
create_studio_tee('tee_white.png', (242, 241, 238))
create_studio_tee('tee_carbon.png', (35, 34, 38))
create_studio_tee('tee_sand.png', (185, 172, 154))
create_studio_tee('tee_indigo.png', (30, 41, 62))
create_studio_tee('tee_espresso.png', (58, 44, 39))
create_studio_tee('tee_graphite.png', (60, 62, 65))
create_studio_tee('tee_bone.png', (225, 220, 212))

# Sneakers
create_studio_sneaker('sneaker_mocha.png', (235, 228, 218), (62, 45, 38), sole_color=(240, 235, 220))
create_studio_sneaker('sneaker_stealth.png', (26, 26, 28), (40, 40, 44), sole_color=(20, 20, 22))
create_studio_sneaker('sneaker_gum.png', (72, 54, 45), (120, 95, 80), sole_color=(198, 142, 78))
create_studio_sneaker('sneaker_sail.png', (240, 236, 228), (50, 48, 46), sole_color=(235, 230, 215))

print('All 16 studio catalog images generated!')
