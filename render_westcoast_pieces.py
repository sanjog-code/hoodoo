import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

os.makedirs('public/assets/westcoast', exist_ok=True)
font_path = 'C:/Windows/Fonts/OLDENGL.TTF'

def draw_paisley_pattern(draw, x, y, scale=1.0, color=(240, 240, 240, 180)):
    # Draws stylized street bandana paisley motifs
    s = scale
    pts = [
        (x, y), (x+10*s, y-15*s), (x+25*s, y-10*s), (x+30*s, y+10*s),
        (x+20*s, y+25*s), (x, y+20*s), (x-15*s, y+10*s), (x-10*s, y-5*s)
    ]
    draw.polygon(pts, fill=color)
    draw.ellipse([x+5*s, y-2*s, x+18*s, y+10*s], fill=(20, 20, 20, 150))
    # teardrop tail
    draw.line([(x+25*s, y-10*s), (x+35*s, y-25*s)], fill=color, width=int(2*s))

def draw_pinstripes(draw, cx, cy, span=120, color=(230, 230, 230, 200)):
    # Classic lowrider hood pinstriping
    for i in range(-2, 3):
        offset = i * 6
        draw.arc([cx - span//2 + offset, cy - 30, cx + span//2 + offset, cy + 30], start=180, end=360, fill=color, width=2)
        draw.arc([cx - span//3 + offset, cy - 10, cx + span//3 + offset, cy + 50], start=0, end=180, fill=color, width=2)

def generate_westcoast_hoodie(filename, base_color, title_text, paisley=True, pinstripe=False, sleeve_bandana=False):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    r, g, b = base_color
    
    # Oversized boxy silhouette (dropped shoulders, aggressive street cut)
    torso_poly = [
        (240, 300), (320, 260), (480, 260), (560, 300),
        (620, 480), (580, 710), (220, 710), (180, 480)
    ]
    left_sleeve = [(240, 300), (140, 390), (110, 590), (170, 605), (210, 450), (220, 380)]
    right_sleeve = [(560, 300), (660, 390), (690, 590), (630, 605), (590, 450), (580, 380)]
    hood_back = [(300, 280), (270, 200), (310, 130), (400, 105), (490, 130), (530, 200), (500, 280)]
    pocket = [(280, 530), (520, 530), (490, 660), (310, 660)]
    
    # Draw Hood
    draw.polygon(hood_back, fill=(int(r*0.7), int(g*0.7), int(b*0.7), 255))
    
    # Sleeves (Bandana print option for West Coast gang aesthetics)
    draw.polygon(left_sleeve, fill=(*base_color, 255))
    draw.polygon(right_sleeve, fill=(*base_color, 255))
    
    if sleeve_bandana:
        for py in range(360, 560, 35):
            draw_paisley_pattern(draw, 140, py, scale=0.8, color=(240, 240, 240, 140))
            draw_paisley_pattern(draw, 660, py, scale=0.8, color=(240, 240, 240, 140))
            
    # Torso
    draw.polygon(torso_poly, fill=(*base_color, 255))
    draw.polygon(pocket, fill=(int(r*0.88), int(g*0.88), int(b*0.88), 255))
    
    # Old English Script Print Across Chest
    font_oe = ImageFont.truetype(font_path, 42)
    bbox = draw.textbbox((0, 0), title_text, font=font_oe)
    tw = bbox[2] - bbox[0]
    draw.text((400 - tw//2, 370), title_text, font=font_oe, fill=(240, 238, 230, 230))
    
    if paisley:
        draw_paisley_pattern(draw, 330, 470, scale=1.1, color=(245, 245, 245, 120))
        draw_paisley_pattern(draw, 470, 470, scale=1.1, color=(245, 245, 245, 120))
        
    if pinstripe:
        draw_pinstripes(draw, 400, 460, span=140, color=(220, 220, 220, 160))
        
    # Ribbed hem & cuffs
    draw.rounded_rectangle([220, 695, 580, 735], radius=8, fill=(int(r*0.8), int(g*0.8), int(b*0.8), 255))
    draw.polygon([(110, 585), (170, 600), (160, 625), (100, 610)], fill=(int(r*0.8), int(g*0.8), int(b*0.8), 255))
    draw.polygon([(690, 585), (630, 600), (640, 625), (700, 610)], fill=(int(r*0.8), int(g*0.8), int(b*0.8), 255))
    
    # Texture & shadow
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 10, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))
    
    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([240, 715, 560, 755], fill=(0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    
    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/westcoast', filename))

def generate_westcoast_tee(filename, base_color, text_line, graphic_type="chicano"):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    r, g, b = base_color
    
    # Heavyweight raw boxy drop-shoulder tee
    torso = [(250, 240), (330, 210), (470, 210), (550, 240), (600, 390), (565, 700), (235, 700), (200, 390)]
    left_sleeve = [(250, 240), (140, 320), (175, 455), (250, 400)]
    right_sleeve = [(550, 240), (660, 320), (625, 455), (550, 400)]
    collar = [(330, 210), (400, 245), (470, 210), (450, 200), (400, 195), (350, 200)]
    
    draw.polygon(left_sleeve, fill=(*base_color, 255))
    draw.polygon(right_sleeve, fill=(*base_color, 255))
    draw.polygon(torso, fill=(*base_color, 255))
    draw.polygon(collar, fill=(int(r*0.75), int(g*0.75), int(b*0.75), 255))
    
    # Street Graphics in Old English & Chicano Art
    font_oe = ImageFont.truetype(font_path, 48)
    bbox = draw.textbbox((0, 0), text_line, font=font_oe)
    tw = bbox[2] - bbox[0]
    draw.text((400 - tw//2, 330), text_line, font=font_oe, fill=(240, 240, 235, 230))
    
    if graphic_type == "chicano":
        draw_paisley_pattern(draw, 350, 460, scale=1.3, color=(240, 240, 240, 150))
        draw_paisley_pattern(draw, 450, 460, scale=1.3, color=(240, 240, 240, 150))
        draw.line([(320, 540), (480, 540)], fill=(230, 230, 230, 180), width=3)
    elif graphic_type == "lowrider":
        draw_pinstripes(draw, 400, 460, span=160, color=(235, 235, 235, 180))
    elif graphic_type == "cross":
        # Chicano cross motif
        draw.line([(400, 420), (400, 540)], fill=(240, 240, 240, 200), width=6)
        draw.line([(360, 460), (440, 460)], fill=(240, 240, 240, 200), width=6)
        
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 9, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))
    
    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([250, 690, 550, 725], fill=(0, 0, 0, 85))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    
    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/westcoast', filename))

def generate_westcoast_sneaker(filename, primary_color, overlay_color, sole_type="gum", bandana_overlay=True):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Sole colors
    if sole_type == "gum":
        sole_col = (195, 138, 72)
    elif sole_type == "aged":
        sole_col = (235, 230, 215)
    else: # black
        sole_col = (24, 24, 26)
        
    midsole = [
        (150, 520), (220, 530), (580, 530), (670, 495), (680, 535),
        (650, 570), (190, 570), (140, 550)
    ]
    upper = [
        (170, 520), (180, 430), (260, 380), (370, 370), (470, 410),
        (570, 440), (660, 475), (670, 505), (220, 530)
    ]
    overlay = [
        (210, 520), (280, 440), (480, 440), (560, 470), (490, 520)
    ]
    
    draw.polygon(midsole, fill=(*sole_col, 255))
    draw.polygon(upper, fill=(*primary_color, 255))
    draw.polygon(overlay, fill=(*overlay_color, 255))
    
    # Bandana Paisley pattern on overlay
    if bandana_overlay:
        draw_paisley_pattern(draw, 330, 465, scale=0.7, color=(245, 245, 245, 190))
        draw_paisley_pattern(draw, 410, 465, scale=0.7, color=(245, 245, 245, 190))
        draw_paisley_pattern(draw, 480, 475, scale=0.6, color=(245, 245, 245, 190))
        
    # Fat West Coast laces
    for lx in range(310, 460, 28):
        draw.line([(lx, 380), (lx+12, 415)], fill=(245, 245, 240, 240), width=6)
        
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 8, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))
    
    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([140, 560, 690, 600], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    
    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/westcoast', filename))

# 1. Hoodies
generate_westcoast_hoodie('wc_hoodie_01.png', (22, 22, 25), "Westside", paisley=True, sleeve_bandana=True)
generate_westcoast_hoodie('wc_hoodie_02.png', (52, 40, 36), "Lowrider", pinstripe=True)
generate_westcoast_hoodie('wc_hoodie_03.png', (28, 28, 38), "Compton", paisley=True)
generate_westcoast_hoodie('wc_hoodie_04.png', (120, 110, 102), "Venice", pinstripe=True)

# 2. Tees
generate_westcoast_tee('wc_tee_01.png', (238, 236, 230), "Crenshaw", graphic_type="chicano")
generate_westcoast_tee('wc_tee_02.png', (25, 25, 28), "South Central", graphic_type="lowrider")
generate_westcoast_tee('wc_tee_03.png', (160, 148, 132), "Locals Only", graphic_type="cross")
generate_westcoast_tee('wc_tee_04.png', (26, 32, 46), "East LA", graphic_type="chicano")

# 3. Footwear / Kicks
generate_westcoast_sneaker('wc_kick_01.png', (230, 225, 215), (28, 28, 30), sole_type="gum", bandana_overlay=True)
generate_westcoast_sneaker('wc_kick_02.png', (24, 24, 26), (42, 42, 48), sole_type="black", bandana_overlay=False)
generate_westcoast_sneaker('wc_kick_03.png', (64, 46, 38), (110, 85, 70), sole_type="gum", bandana_overlay=True)
generate_westcoast_sneaker('wc_kick_04.png', (235, 230, 220), (45, 45, 48), sole_type="aged", bandana_overlay=True)

# 4. Mixed Tops & Kicks
generate_westcoast_hoodie('wc_hoodie_05.png', (38, 38, 42), "Midnight Rider", pinstripe=True, sleeve_bandana=True)
generate_westcoast_tee('wc_tee_05.png', (55, 58, 62), "Blackletter", graphic_type="cross")
generate_westcoast_tee('wc_tee_06.png', (48, 38, 34), "Chicano Soul", graphic_type="chicano")
generate_westcoast_sneaker('wc_kick_05.png', (28, 28, 30), (220, 215, 205), sole_type="gum", bandana_overlay=True)

print("All 16 West Coast Streetwear designer pieces created successfully!")
