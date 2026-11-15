import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

os.makedirs('public/assets/collection', exist_ok=True)
font_path = 'C:/Windows/Fonts/OLDENGL.TTF'

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def draw_paisley_motif(draw, x, y, scale=1.0, color=(240, 240, 240, 190)):
    s = scale
    pts = [
        (x, y), (x+12*s, y-18*s), (x+28*s, y-12*s), (x+32*s, y+12*s),
        (x+22*s, y+28*s), (x, y+22*s), (x-16*s, y+12*s), (x-12*s, y-6*s)
    ]
    draw.polygon(pts, fill=color)
    draw.ellipse([x+6*s, y-2*s, x+20*s, y+12*s], fill=(15, 15, 15, 160))
    draw.line([(x+28*s, y-12*s), (x+40*s, y-30*s)], fill=color, width=int(2.5*s))

def draw_lowrider_pinstripe(draw, cx, cy, span=160, color=(235, 235, 235, 210)):
    for i in range(-2, 3):
        off = i * 8
        draw.arc([cx - span//2 + off, cy - 40, cx + span//2 + off, cy + 40], start=180, end=360, fill=color, width=2)
        draw.arc([cx - span//3 + off, cy - 20, cx + span//3 + off, cy + 60], start=0, end=180, fill=color, width=2)
    draw.polygon([(cx, cy-15), (cx+12, cy), (cx, cy+15), (cx-12, cy)], fill=color)

def render_hoodie_back(out_name, hex_color, title_text="WESTSIDE", mural_type="lowrider"):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r, g, b = hex_to_rgb(hex_color)
    lum = 0.299*r + 0.587*g + 0.114*b
    text_color = (25, 25, 25, 235) if lum > 160 else (245, 243, 238, 240)
    accent_color = (40, 40, 40, 190) if lum > 160 else (240, 240, 240, 190)

    # Back silhouette: Clean back with hood draped down over upper shoulders
    torso = [
        (240, 290), (320, 255), (480, 255), (560, 290),
        (620, 470), (580, 700), (220, 700), (180, 470)
    ]
    left_sleeve = [(240, 290), (140, 380), (110, 580), (170, 595), (210, 440), (220, 370)]
    right_sleeve = [(560, 290), (660, 380), (690, 580), (630, 595), (590, 440), (580, 370)]
    
    # Draped hood on the back
    hood_drape = [
        (330, 255), (290, 340), (330, 410), (400, 430), (470, 410), (510, 340), (470, 255)
    ]

    draw.polygon(left_sleeve, fill=(r, g, b, 255))
    draw.polygon(right_sleeve, fill=(r, g, b, 255))
    draw.polygon(torso, fill=(r, g, b, 255))

    # Large prominent back mural graphic (West Coast street lore)
    font_oe_large = ImageFont.truetype(font_path, 56)
    bbox = draw.textbbox((0, 0), title_text, font=font_oe_large)
    tw = bbox[2] - bbox[0]
    draw.text((400 - tw//2, 450), title_text, font=font_oe_large, fill=text_color)

    if mural_type == "lowrider":
        # Lowrider hydraulic car silhouette on back
        car_pts = [(300, 570), (360, 530), (440, 530), (500, 570), (510, 600), (290, 600)]
        draw.polygon(car_pts, fill=accent_color)
        draw.ellipse([325, 595, 355, 625], fill=text_color)
        draw.ellipse([445, 595, 475, 625], fill=text_color)
        draw_lowrider_pinstripe(draw, 400, 540, span=180, color=accent_color)
    elif mural_type == "paisley":
        for px in range(290, 530, 65):
            draw_paisley_motif(draw, px, 550, scale=1.1, color=accent_color)
        draw.line([(280, 610), (520, 610)], fill=accent_color, width=3)
    else: # gothic cross
        draw.line([(400, 520), (400, 640)], fill=accent_color, width=8)
        draw.line([(350, 560), (450, 560)], fill=accent_color, width=8)

    # Draped Hood over shoulders (darker tone)
    hood_shade = (max(0, int(r*0.62)), max(0, int(g*0.62)), max(0, int(b*0.62)), 255)
    draw.polygon(hood_drape, fill=hood_shade)
    draw.line([(330, 255), (400, 430), (470, 255)], fill=(int(r*0.4), int(g*0.4), int(b*0.4), 255), width=3)

    # Ribbed hem & cuffs
    hem_shade = (max(0, int(r*0.78)), max(0, int(g*0.78)), max(0, int(b*0.78)), 255)
    draw.rounded_rectangle([220, 685, 580, 725], radius=8, fill=hem_shade)
    draw.polygon([(110, 575), (170, 590), (160, 615), (100, 600)], fill=hem_shade)
    draw.polygon([(690, 575), (630, 590), (640, 615), (700, 600)], fill=hem_shade)

    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 8, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))

    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([230, 705, 570, 745], fill=(0, 0, 0, 95))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))

    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/collection', out_name))

def render_tee_back(out_name, hex_color, text_line="Crenshaw Blvd", graphic="chicano"):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    r, g, b = hex_to_rgb(hex_color)
    lum = 0.299*r + 0.587*g + 0.114*b
    text_color = (25, 25, 25, 235) if lum > 160 else (245, 243, 238, 240)
    accent_color = (40, 40, 40, 190) if lum > 160 else (240, 240, 240, 190)

    # Boxy tee back
    torso = [(250, 240), (330, 210), (470, 210), (550, 240), (600, 390), (565, 700), (235, 700), (200, 390)]
    left_sleeve = [(250, 240), (140, 320), (175, 455), (250, 400)]
    right_sleeve = [(550, 240), (660, 320), (625, 455), (550, 400)]
    collar = [(330, 210), (400, 225), (470, 210)]

    draw.polygon(left_sleeve, fill=(r, g, b, 255))
    draw.polygon(right_sleeve, fill=(r, g, b, 255))
    draw.polygon(torso, fill=(r, g, b, 255))
    draw.line(collar, fill=(max(0, int(r*0.75)), max(0, int(g*0.75)), max(0, int(b*0.75)), 255), width=8)

    # Giant back statement print
    font_oe = ImageFont.truetype(font_path, 60)
    bbox = draw.textbbox((0, 0), text_line, font=font_oe)
    tw = bbox[2] - bbox[0]
    draw.text((400 - tw//2, 280), text_line, font=font_oe, fill=text_color)

    if graphic == "chicano":
        for py in range(370, 580, 55):
            draw_paisley_motif(draw, 340, py, scale=1.3, color=accent_color)
            draw_paisley_motif(draw, 460, py, scale=1.3, color=accent_color)
    elif graphic == "lowrider":
        draw_lowrider_pinstripe(draw, 400, 480, span=220, color=accent_color)
    else:
        draw.line([(400, 380), (400, 600)], fill=text_color, width=10)
        draw.line([(330, 450), (470, 450)], fill=text_color, width=10)

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

def render_sneaker_back(out_name, upper_hex, overlay_hex, sole_type="gum"):
    size = (800, 800)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    ur, ug, ub = hex_to_rgb(upper_hex)
    or_, og, ob = hex_to_rgb(overlay_hex)

    if sole_type == "gum":
        sole_col = (195, 138, 72)
    elif sole_type == "aged":
        sole_col = (235, 230, 215)
    else:
        sole_col = (22, 22, 24)

    # Heel perspective silhouette (viewed from behind)
    heel_sole = [(280, 560), (520, 560), (500, 610), (300, 610)]
    heel_cup = [(300, 400), (500, 400), (520, 560), (280, 560)]
    heel_tab = [(360, 360), (440, 360), (450, 420), (350, 420)]
    collar_interior = [(330, 380), (470, 380), (450, 440), (350, 440)]

    draw.polygon(heel_sole, fill=(*sole_col, 255))
    draw.polygon(heel_cup, fill=(ur, ug, ub, 255))
    draw.polygon(heel_tab, fill=(or_, og, ob, 255))
    draw.polygon(collar_interior, fill=(int(ur*0.6), int(ug*0.6), int(ub*0.6), 255))

    # Old English embossed "H" on heel tab
    font_h = ImageFont.truetype(font_path, 34)
    draw.text((388, 368), "H", font=font_h, fill=(245, 245, 240, 230))

    # Heel seam stitch
    draw.line([(400, 420), (400, 560)], fill=(230, 230, 230, 180), width=4)

    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, 8, (size[1], size[0], 3))
    arr[:, :, :3] = np.clip(arr[:, :, :3] + noise, 0, 255)
    res = Image.fromarray(arr.astype(np.uint8))

    shadow = Image.new('RGBA', size, (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.ellipse([260, 595, 540, 630], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))

    final_img = Image.alpha_composite(shadow, res)
    final_img.save(os.path.join('public/assets/collection', out_name))

# ----------------- GENERATE BACK VIEWS FOR ALL 17 PRODUCTS IN ALL 3 COLORWAYS -----------------
print("Rendering back views for all products...")

# 0. Hero
render_hoodie_back('hero_asphalt_back.png', '#18181b', title_text="WESTSIDE", mural_type="lowrider")
render_hoodie_back('hero_bone_back.png', '#e7e5e4', title_text="WESTSIDE", mural_type="lowrider")
render_hoodie_back('hero_royal_back.png', '#1e293b', title_text="WESTSIDE", mural_type="lowrider")

# 1. Westside Paisley Heavy Hoodie
render_hoodie_back('p1_black_back.png', '#09090b', title_text="WESTSIDE", mural_type="paisley")
render_hoodie_back('p1_red_back.png', '#7f1d1d', title_text="WESTSIDE", mural_type="paisley")
render_hoodie_back('p1_blue_back.png', '#1e3a8a', title_text="WESTSIDE", mural_type="paisley")

# 2. '64 Lowrider Pinstripe Hoodie
render_hoodie_back('p2_cocoa_back.png', '#3d2b24', title_text="LOWRIDER", mural_type="lowrider")
render_hoodie_back('p2_charcoal_back.png', '#262626', title_text="LOWRIDER", mural_type="lowrider")
render_hoodie_back('p2_tan_back.png', '#786452', title_text="LOWRIDER", mural_type="lowrider")

# 3. Compton Blackletter Hoodie
render_hoodie_back('p3_black_back.png', '#0a0a0a', title_text="COMPTON", mural_type="cross")
render_hoodie_back('p3_ash_back.png', '#52525b', title_text="COMPTON", mural_type="cross")
render_hoodie_back('p3_khaki_back.png', '#2e3a2d', title_text="COMPTON", mural_type="cross")

# 4. Venice Boardwalk Clay Hoodie
render_hoodie_back('p4_sand_back.png', '#a89a87', title_text="VENICE", mural_type="lowrider")
render_hoodie_back('p4_sage_back.png', '#6b7280', title_text="VENICE", mural_type="lowrider")
render_hoodie_back('p4_rose_back.png', '#785b5b', title_text="VENICE", mural_type="lowrider")

# 5. Crenshaw Heavyweight Boxy Tee
render_tee_back('p5_white_back.png', '#fafaf9', text_line="CRENSHAW", graphic="chicano")
render_tee_back('p5_black_back.png', '#171717', text_line="CRENSHAW", graphic="chicano")
render_tee_back('p5_gold_back.png', '#b45309', text_line="CRENSHAW", graphic="chicano")

# 6. South Central Lowrider Tee
render_tee_back('p6_carbon_back.png', '#1c1917', text_line="SOUTH CENTRAL", graphic="lowrider")
render_tee_back('p6_cement_back.png', '#57534e', text_line="SOUTH CENTRAL", graphic="lowrider")
render_tee_back('p6_bone_back.png', '#e7e5e4', text_line="SOUTH CENTRAL", graphic="lowrider")

# 7. Locals Only Chicano Tee
render_tee_back('p7_sand_back.png', '#b8a58a', text_line="LOCALS ONLY", graphic="cross")
render_tee_back('p7_obsidian_back.png', '#09090b', text_line="LOCALS ONLY", graphic="cross")
render_tee_back('p7_olive_back.png', '#3f4338', text_line="LOCALS ONLY", graphic="cross")

# 8. East LA Paisley Graphic Tee
render_tee_back('p8_indigo_back.png', '#1e293b', text_line="EAST LA", graphic="chicano")
render_tee_back('p8_maroon_back.png', '#450a0a', text_line="EAST LA", graphic="chicano")
render_tee_back('p8_ivory_back.png', '#f5f5f4', text_line="EAST LA", graphic="chicano")

# 9. Street Low 'Chicano Bone & Gum'
render_sneaker_back('p9_bone_back.png', '#e7e5e4', '#111111', sole_type="gum")
render_sneaker_back('p9_black_back.png', '#111111', '#404040', sole_type="gum")
render_sneaker_back('p9_cocoa_back.png', '#5c4033', '#111111', sole_type="gum")

# 10. Midnight Stealth Runner
render_sneaker_back('p10_noir_back.png', '#0f0f0f', '#262626', sole_type="black")
render_sneaker_back('p10_grey_back.png', '#404040', '#171717', sole_type="black")
render_sneaker_back('p10_onyx_back.png', '#262626', '#e7e5e4', sole_type="black")

# 11. Chopper Suede Skate Low
render_sneaker_back('p11_choco_back.png', '#4a3528', '#8c6d58', sole_type="gum")
render_sneaker_back('p11_jet_back.png', '#171717', '#404040', sole_type="gum")
render_sneaker_back('p11_moss_back.png', '#313d33', '#5c6b5e', sole_type="gum")

# 12. Paisley Swoop Retro Low
render_sneaker_back('p12_sail_back.png', '#f4f4f5', '#1e293b', sole_type="aged")
render_sneaker_back('p12_crimson_back.png', '#18181b', '#7f1d1d', sole_type="aged")
render_sneaker_back('p12_khaki_back.png', '#9ca3af', '#4b5563', sole_type="aged")

# 13. Midnight Rider Gothic Hoodie
render_hoodie_back('p13_asphalt_back.png', '#27272a', title_text="MIDNIGHT", mural_type="lowrider")
render_hoodie_back('p13_bone_back.png', '#d6d3d1', title_text="MIDNIGHT", mural_type="lowrider")
render_hoodie_back('p13_navy_back.png', '#172554', title_text="MIDNIGHT", mural_type="lowrider")

# 14. Blackletter Chrome Boxy Tee
render_tee_back('p14_graphite_back.png', '#3f3f46', text_line="CHROME", graphic="cross")
render_tee_back('p14_white_back.png', '#ffffff', text_line="CHROME", graphic="cross")
render_tee_back('p14_onyx_back.png', '#18181b', text_line="CHROME", graphic="cross")

# 15. Chicano Soul Vintage Tee
render_tee_back('p15_espresso_back.png', '#423129', text_line="CHICANO SOUL", graphic="chicano")
render_tee_back('p15_pine_back.png', '#28362b', text_line="CHICANO SOUL", graphic="chicano")
render_tee_back('p15_slate_back.png', '#334155', text_line="CHICANO SOUL", graphic="chicano")

# 16. Eastside Gum Sole Retro
render_sneaker_back('p16_obsidian_back.png', '#18181b', '#d6d3d1', sole_type="gum")
render_sneaker_back('p16_duck_back.png', '#f5f5f4', '#18181b', sole_type="gum")
render_sneaker_back('p16_navy_back.png', '#1e3a8a', '#18181b', sole_type="gum")

print("All 51 backside studio photographs created successfully!")
