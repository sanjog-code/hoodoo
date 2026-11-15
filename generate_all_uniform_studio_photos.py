import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

os.makedirs('public/assets/collection', exist_ok=True)
font_path = 'C:/Windows/Fonts/OLDENGL.TTF'

def draw_paisley_motif(draw, x, y, scale=1.0, color=(240, 240, 240, 190)):
    s = scale
    pts = [
        (x, y), (x+12*s, y-18*s), (x+28*s, y-12*s), (x+32*s, y+12*s),
        (x+22*s, y+28*s), (x, y+22*s), (x-16*s, y+12*s), (x-12*s, y-6*s)
    ]
    draw.polygon(pts, fill=color)
    draw.ellipse([x+6*s, y-2*s, x+20*s, y+12*s], fill=(15, 15, 15, 160))
    draw.line([(x+28*s, y-12*s), (x+40*s, y-30*s)], fill=color, width=int(2.5*s))

def draw_lowrider_pinstripe(draw, cx, cy, span=140, color=(235, 235, 235, 210)):
    for i in range(-2, 3):
        off = i * 7
        draw.arc([cx - span//2 + off, cy - 35, cx + span//2 + off, cy + 35], start=180, end=360, fill=color, width=2)
        draw.arc([cx - span//3 + off, cy - 15, cx + span//3 + off, cy + 55], start=0, end=180, fill=color, width=2)
    # Center diamond
    draw.polygon([(cx, cy-12), (cx+10, cy), (cx, cy+12), (cx-10, cy)], fill=color)

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def render_uniform_hoodie(out_name, hex_color, title_text="Hoodoo", sleeve_paisley=True, chest_pinstripe=False, airbrush_mural=False):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    r, g, b = hex_to_rgb(hex_color)
    # Brightness check for text contrast
    lum = 0.299*r + 0.587*g + 0.114*b
    text_color = (25, 25, 25, 230) if lum > 160 else (245, 243, 238, 235)
    accent_color = (40, 40, 40, 180) if lum > 160 else (240, 240, 240, 180)

    # Architectural boxy hoodie silhouette
    torso = [
        (240, 290), (320, 255), (480, 255), (560, 290),
        (620, 470), (580, 700), (220, 700), (180, 470)
    ]
    left_sleeve = [(240, 290), (140, 380), (110, 580), (170, 595), (210, 440), (220, 370)]
    right_sleeve = [(560, 290), (660, 380), (690, 580), (630, 595), (590, 440), (580, 370)]
    hood_back = [(300, 270), (270, 190), (310, 120), (400, 95), (490, 120), (530, 190), (500, 270)]
    pocket = [(280, 520), (520, 520), (490, 650), (310, 650)]

    # Draw Back of Hood
    hood_shade = (max(0, int(r*0.65)), max(0, int(g*0.65)), max(0, int(b*0.65)), 255)
    draw.polygon(hood_back, fill=hood_shade)

    # Sleeves
    draw.polygon(left_sleeve, fill=(r, g, b, 255))
    draw.polygon(right_sleeve, fill=(r, g, b, 255))

    if sleeve_paisley:
        for py in range(350, 560, 38):
            draw_paisley_motif(draw, 140, py, scale=0.75, color=accent_color)
            draw_paisley_motif(draw, 660, py, scale=0.75, color=accent_color)

    # Torso
    draw.polygon(torso, fill=(r, g, b, 255))
    pocket_shade = (max(0, int(r*0.88)), max(0, int(g*0.88)), max(0, int(b*0.88)), 255)
    draw.polygon(pocket, fill=pocket_shade)

    # Chicano Blackletter Chest Hit
    font_oe = ImageFont.truetype(font_path, 40)
    bbox = draw.textbbox((0, 0), title_text, font=font_oe)
    tw = bbox[2] - bbox[0]
    draw.text((400 - tw//2, 360), title_text, font=font_oe, fill=text_color)

    # Airbrush Mural or Pinstriping
    if airbrush_mural:
        # Draw stylized lowrider silhouette
        car_pts = [(330, 470), (370, 450), (430, 450), (470, 470), (480, 490), (320, 490)]
        draw.polygon(car_pts, fill=accent_color)
        draw.ellipse([345, 485, 365, 505], fill=text_color)
        draw.ellipse([435, 485, 455, 505], fill=text_color)
        draw_lowrider_pinstripe(draw, 400, 460, span=160, color=accent_color)
    elif chest_pinstripe:
        draw_lowrider_pinstripe(draw, 400, 460, span=140, color=accent_color)
    else:
        draw_paisley_motif(draw, 340, 460, scale=1.1, color=accent_color)
        draw_paisley_motif(draw, 460, 460, scale=1.1, color=accent_color)

    # Ribbed hem & cuffs
    hem_shade = (max(0, int(r*0.78)), max(0, int(g*0.78)), max(0, int(b*0.78)), 255)
    draw.rounded_rectangle([220, 685, 580, 725], radius=8, fill=hem_shade)
    draw.polygon([(110, 575), (170, 590), (160, 615), (100, 600)], fill=hem_shade)
    draw.polygon([(690, 575), (630, 590), (640, 615), (700, 600)], fill=hem_shade)

    # Texture & lighting
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 8, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))

    # Studio contact shadow below (uniform style)
    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([230, 705, 570, 745], fill=(0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))

    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/collection', out_name))

def render_uniform_tee(out_name, hex_color, text_line="Crenshaw", graphic="chicano"):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r, g, b = hex_to_rgb(hex_color)
    lum = 0.299*r + 0.587*g + 0.114*b
    text_color = (25, 25, 25, 230) if lum > 160 else (245, 243, 238, 235)
    accent_color = (40, 40, 40, 180) if lum > 160 else (240, 240, 240, 180)

    # Oversized boxy dropped-shoulder tee
    torso = [(250, 240), (330, 210), (470, 210), (550, 240), (600, 390), (565, 700), (235, 700), (200, 390)]
    left_sleeve = [(250, 240), (140, 320), (175, 455), (250, 400)]
    right_sleeve = [(550, 240), (660, 320), (625, 455), (550, 400)]
    collar = [(330, 210), (400, 245), (470, 210), (450, 200), (400, 195), (350, 200)]

    draw.polygon(left_sleeve, fill=(r, g, b, 255))
    draw.polygon(right_sleeve, fill=(r, g, b, 255))
    draw.polygon(torso, fill=(r, g, b, 255))
    draw.polygon(collar, fill=(max(0, int(r*0.75)), max(0, int(g*0.75)), max(0, int(b*0.75)), 255))

    # Old English Graphic
    font_oe = ImageFont.truetype(font_path, 46)
    bbox = draw.textbbox((0, 0), text_line, font=font_oe)
    tw = bbox[2] - bbox[0]
    draw.text((400 - tw//2, 330), text_line, font=font_oe, fill=text_color)

    if graphic == "chicano":
        draw_paisley_motif(draw, 350, 460, scale=1.3, color=accent_color)
        draw_paisley_motif(draw, 450, 460, scale=1.3, color=accent_color)
        draw.line([(320, 540), (480, 540)], fill=accent_color, width=3)
    elif graphic == "lowrider":
        draw_lowrider_pinstripe(draw, 400, 460, span=160, color=accent_color)
    elif graphic == "cross":
        draw.line([(400, 420), (400, 540)], fill=text_color, width=6)
        draw.line([(360, 460), (440, 460)], fill=text_color, width=6)

    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 8, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))

    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([240, 685, 560, 725], fill=(0, 0, 0, 85))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))

    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/collection', out_name))

def render_uniform_sneaker(out_name, upper_hex, overlay_hex, sole_type="gum", paisley=True):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    ur, ug, ub = hex_to_rgb(upper_hex)
    or_, og, ob = hex_to_rgb(overlay_hex)

    if sole_type == "gum":
        sole_col = (195, 138, 72)
    elif sole_type == "aged":
        sole_col = (235, 230, 215)
    else: # black
        sole_col = (22, 22, 24)

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
    draw.polygon(upper, fill=(ur, ug, ub, 255))
    draw.polygon(overlay, fill=(or_, og, ob, 255))

    if paisley:
        p_col = (245, 245, 240, 190) if (0.299*or_ + 0.587*og + 0.114*ob) < 140 else (30, 30, 30, 190)
        draw_paisley_motif(draw, 330, 465, scale=0.7, color=p_col)
        draw_paisley_motif(draw, 410, 465, scale=0.7, color=p_col)
        draw_paisley_motif(draw, 480, 475, scale=0.6, color=p_col)

    # Fat West Coast skate laces
    lace_col = (245, 245, 240, 240) if (0.299*ur + 0.587*ug + 0.114*ub) < 160 else (30, 30, 30, 240)
    for lx in range(310, 460, 28):
        draw.line([(lx, 380), (lx+12, 415)], fill=lace_col, width=6)

    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 8, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))

    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([140, 560, 690, 600], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))

    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/collection', out_name))

# ----------------- EXECUTE UNIFORM PHOTOSHOOT FOR ALL 17 PRODUCTS ACROSS ALL 3 COLORWAYS (51 UNIQUE SHOTS) -----------------
print("Starting uniform photoshoot...")

# 0. Hero: WESTSIDE LOWRIDER AIRBRUSH HOODIE
render_uniform_hoodie('hero_asphalt.png', '#18181b', title_text="Westside", sleeve_paisley=True, airbrush_mural=True)
render_uniform_hoodie('hero_bone.png', '#e7e5e4', title_text="Westside", sleeve_paisley=True, airbrush_mural=True)
render_uniform_hoodie('hero_royal.png', '#1e293b', title_text="Westside", sleeve_paisley=True, airbrush_mural=True)

# 1. Westside Paisley Heavy Hoodie
render_uniform_hoodie('p1_black.png', '#09090b', title_text="Westside", sleeve_paisley=True)
render_uniform_hoodie('p1_red.png', '#7f1d1d', title_text="Westside", sleeve_paisley=True)
render_uniform_hoodie('p1_blue.png', '#1e3a8a', title_text="Westside", sleeve_paisley=True)

# 2. '64 Lowrider Pinstripe Hoodie
render_uniform_hoodie('p2_cocoa.png', '#3d2b24', title_text="Lowrider", chest_pinstripe=True)
render_uniform_hoodie('p2_charcoal.png', '#262626', title_text="Lowrider", chest_pinstripe=True)
render_uniform_hoodie('p2_tan.png', '#786452', title_text="Lowrider", chest_pinstripe=True)

# 3. Compton Blackletter Hoodie
render_uniform_hoodie('p3_black.png', '#0a0a0a', title_text="Compton", sleeve_paisley=False, chest_pinstripe=False)
render_uniform_hoodie('p3_ash.png', '#52525b', title_text="Compton", sleeve_paisley=False, chest_pinstripe=False)
render_uniform_hoodie('p3_khaki.png', '#2e3a2d', title_text="Compton", sleeve_paisley=False, chest_pinstripe=False)

# 4. Venice Boardwalk Clay Hoodie
render_uniform_hoodie('p4_sand.png', '#a89a87', title_text="Venice", chest_pinstripe=True)
render_uniform_hoodie('p4_sage.png', '#6b7280', title_text="Venice", chest_pinstripe=True)
render_uniform_hoodie('p4_rose.png', '#785b5b', title_text="Venice", chest_pinstripe=True)

# 5. Crenshaw Heavyweight Boxy Tee
render_uniform_tee('p5_white.png', '#fafaf9', text_line="Crenshaw", graphic="chicano")
render_uniform_tee('p5_black.png', '#171717', text_line="Crenshaw", graphic="chicano")
render_uniform_tee('p5_gold.png', '#b45309', text_line="Crenshaw", graphic="chicano")

# 6. South Central Lowrider Tee
render_uniform_tee('p6_carbon.png', '#1c1917', text_line="South Central", graphic="lowrider")
render_uniform_tee('p6_cement.png', '#57534e', text_line="South Central", graphic="lowrider")
render_uniform_tee('p6_bone.png', '#e7e5e4', text_line="South Central", graphic="lowrider")

# 7. Locals Only Chicano Tee
render_uniform_tee('p7_sand.png', '#b8a58a', text_line="Locals Only", graphic="cross")
render_uniform_tee('p7_obsidian.png', '#09090b', text_line="Locals Only", graphic="cross")
render_uniform_tee('p7_olive.png', '#3f4338', text_line="Locals Only", graphic="cross")

# 8. East LA Paisley Graphic Tee
render_uniform_tee('p8_indigo.png', '#1e293b', text_line="East LA", graphic="chicano")
render_uniform_tee('p8_maroon.png', '#450a0a', text_line="East LA", graphic="chicano")
render_uniform_tee('p8_ivory.png', '#f5f5f4', text_line="East LA", graphic="chicano")

# 9. Street Low 'Chicano Bone & Gum'
render_uniform_sneaker('p9_bone.png', '#e7e5e4', '#111111', sole_type="gum", paisley=True)
render_uniform_sneaker('p9_black.png', '#111111', '#404040', sole_type="gum", paisley=True)
render_uniform_sneaker('p9_cocoa.png', '#5c4033', '#111111', sole_type="gum", paisley=True)

# 10. Midnight Stealth Runner
render_uniform_sneaker('p10_noir.png', '#0f0f0f', '#262626', sole_type="black", paisley=False)
render_uniform_sneaker('p10_grey.png', '#404040', '#171717', sole_type="black", paisley=False)
render_uniform_sneaker('p10_onyx.png', '#262626', '#e7e5e4', sole_type="black", paisley=False)

# 11. Chopper Suede Skate Low
render_uniform_sneaker('p11_choco.png', '#4a3528', '#8c6d58', sole_type="gum", paisley=True)
render_uniform_sneaker('p11_jet.png', '#171717', '#404040', sole_type="gum", paisley=True)
render_uniform_sneaker('p11_moss.png', '#313d33', '#5c6b5e', sole_type="gum", paisley=True)

# 12. Paisley Swoop Retro Low
render_uniform_sneaker('p12_sail.png', '#f4f4f5', '#1e293b', sole_type="aged", paisley=True)
render_uniform_sneaker('p12_crimson.png', '#18181b', '#7f1d1d', sole_type="aged", paisley=True)
render_uniform_sneaker('p12_khaki.png', '#9ca3af', '#4b5563', sole_type="aged", paisley=True)

# 13. Midnight Rider Gothic Hoodie
render_uniform_hoodie('p13_asphalt.png', '#27272a', title_text="Midnight Rider", chest_pinstripe=True, sleeve_paisley=True)
render_uniform_hoodie('p13_bone.png', '#d6d3d1', title_text="Midnight Rider", chest_pinstripe=True, sleeve_paisley=True)
render_uniform_hoodie('p13_navy.png', '#172554', title_text="Midnight Rider", chest_pinstripe=True, sleeve_paisley=True)

# 14. Blackletter Chrome Boxy Tee
render_uniform_tee('p14_graphite.png', '#3f3f46', text_line="Chrome", graphic="cross")
render_uniform_tee('p14_white.png', '#ffffff', text_line="Chrome", graphic="cross")
render_uniform_tee('p14_onyx.png', '#18181b', text_line="Chrome", graphic="cross")

# 15. Chicano Soul Vintage Tee
render_uniform_tee('p15_espresso.png', '#423129', text_line="Chicano Soul", graphic="chicano")
render_uniform_tee('p15_pine.png', '#28362b', text_line="Chicano Soul", graphic="chicano")
render_uniform_tee('p15_slate.png', '#334155', text_line="Chicano Soul", graphic="chicano")

# 16. Eastside Gum Sole Retro
render_uniform_sneaker('p16_obsidian.png', '#18181b', '#d6d3d1', sole_type="gum", paisley=True)
render_uniform_sneaker('p16_duck.png', '#f5f5f4', '#18181b', sole_type="gum", paisley=True)
render_uniform_sneaker('p16_navy.png', '#1e3a8a', '#18181b', sole_type="gum", paisley=True)

print("Uniform photoshoot finished: 51 unique transparent studio images created in public/assets/collection/")
