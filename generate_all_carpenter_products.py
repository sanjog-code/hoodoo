import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('public/assets/products', exist_ok=True)

def create_wood_texture(width, height, base_rgb, secondary_rgb, grain_density=40, roughness=0.15):
    """Generates procedural anisotropic wood grain with organic growth rings and fibers."""
    x = np.linspace(0, 10, width)
    y = np.linspace(0, 10, height)
    xx, yy = np.meshgrid(x, y)
    
    # Growth ring distortion
    noise = np.sin(xx * 0.3 + np.sin(yy * 0.8) * 1.5) * 0.5 + np.sin(yy * grain_density * 0.05) * 0.5
    grain = np.sin(xx * 0.1 + yy * 0.05 + noise * 4.0)
    grain = (grain - grain.min()) / (grain.max() - grain.min() + 1e-5)
    
    # Micro fibers
    micro = np.random.normal(0, roughness, (height, width))
    combined = np.clip(grain * 0.85 + micro * 0.15, 0, 1)
    
    r = np.uint8(base_rgb[0] * (1 - combined) + secondary_rgb[0] * combined)
    g = np.uint8(base_rgb[1] * (1 - combined) + secondary_rgb[1] * combined)
    b = np.uint8(base_rgb[2] * (1 - combined) + secondary_rgb[2] * combined)
    
    arr = np.dstack((r, g, b, np.full((height, width), 255, dtype=np.uint8)))
    return Image.fromarray(arr)

def studio_background(width=1000, height=800, top_color=(245, 243, 238), bottom_color=(225, 222, 215)):
    """Creates a soft luxury studio infinity cove backdrop with subtle floor shadow plane."""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    arr = np.zeros((height, width, 4), dtype=np.uint8)
    
    for y in range(height):
        factor = y / height
        # Soft curve for studio cyclorama infinity cove
        t = math.pow(factor, 1.4)
        r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
        g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
        b = int(top_color[2] * (1 - t) + bottom_color[2] * t)
        arr[y, :, 0] = r
        arr[y, :, 1] = g
        arr[y, :, 2] = b
        arr[y, :, 3] = 255
        
    base = Image.fromarray(arr)
    # Add subtle soft vignette
    vignette = Image.new('L', (width, height), 0)
    vdraw = ImageDraw.Draw(vignette)
    vdraw.ellipse([-width*0.2, -height*0.2, width*1.2, height*1.2], fill=255)
    vignette = vignette.filter(ImageFilter.GaussianBlur(120))
    
    return base

def draw_soft_shadow(draw, cx, cy, rx, ry, opacity=90, blur_steps=4):
    """Draws multi-layered contact and ambient occlusion ground shadows."""
    for i in range(blur_steps):
        factor = (blur_steps - i) / blur_steps
        alpha = int(opacity * factor * 0.4)
        cur_rx = rx + i * 14
        cur_ry = ry + i * 6
        draw.ellipse([cx - cur_rx, cy - cur_ry, cx + cur_rx, cy + cur_ry], fill=(20, 18, 16, alpha))

# ==============================================================================
# PRODUCT GENERATORS
# ==============================================================================

def render_butcher_block():
    img = studio_background(1000, 800)
    shadow = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 500, 560, 260, 60, opacity=140)
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(shadow)
    
    # 3D Isometric End-Grain Cutting Board
    board = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(board)
    
    # Top face checkerboard
    top_poly = [(220, 420), (500, 280), (780, 420), (500, 560)]
    bdraw.polygon(top_poly, fill=(58, 40, 28, 255))
    
    # Front-left side
    side_left = [(220, 420), (500, 560), (500, 620), (220, 480)]
    bdraw.polygon(side_left, fill=(42, 28, 18, 255))
    
    # Front-right side
    side_right = [(500, 560), (780, 420), (780, 480), (500, 620)]
    bdraw.polygon(side_right, fill=(30, 20, 12, 255))
    
    # Draw checkerboard grid on top face
    rows, cols = 8, 8
    for r in range(rows):
        for c in range(cols):
            # Bilinear interpolation for isometric diamond
            u0 = c / cols
            u1 = (c + 1) / cols
            v0 = r / rows
            v1 = (r + 1) / rows
            
            def map_pt(u, v):
                # top_poly: 0=left, 1=top, 2=right, 3=bottom
                x = (1-u)*(1-v)*220 + u*(1-v)*500 + u*v*780 + (1-u)*v*500
                y = (1-u)*(1-v)*420 + u*(1-v)*280 + u*v*420 + (1-u)*v*560
                return (x, y)
                
            pts = [map_pt(u0, v0), map_pt(u1, v0), map_pt(u1, v1), map_pt(u0, v1)]
            color = (78, 54, 38, 255) if (r + c) % 2 == 0 else (184, 150, 108, 255)
            bdraw.polygon(pts, fill=color)
            bdraw.polygon(pts, outline=(30, 20, 14, 80), width=1)
            
    # Brass Feet
    feet = [(240, 480), (500, 625), (760, 480)]
    for fx, fy in feet:
        bdraw.ellipse([fx-10, fy-4, fx+10, fy+12], fill=(212, 175, 55, 255))
        bdraw.ellipse([fx-8, fy-2, fx+8, fy+4], fill=(240, 210, 90, 255))
        
    img.alpha_composite(board)
    img.convert('RGB').save('public/assets/products/butcher-block.jpg', 'JPEG', quality=95)
    print("Generated butcher-block.jpg")

def render_hinoki_stool():
    img = studio_background(1000, 800)
    shadow = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 500, 680, 220, 50, opacity=120)
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(shadow)
    
    stool = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stool)
    
    # 3 Flared Timber Legs
    # Back leg
    draw.polygon([(480, 420), (520, 420), (510, 660), (490, 660)], fill=(185, 160, 125, 255))
    # Left leg
    draw.polygon([(380, 420), (410, 410), (330, 680), (300, 680)], fill=(215, 190, 155, 255))
    # Right leg
    draw.polygon([(590, 410), (620, 420), (700, 680), (670, 680)], fill=(195, 170, 135, 255))
    
    # Stretchers
    draw.polygon([(360, 560), (380, 555), (630, 555), (650, 560)], fill=(205, 180, 145, 255))
    
    # Circular Round Seat (Thickness + Top ellipse)
    seat_y = 380
    # Rim side
    draw.ellipse([320, seat_y, 680, seat_y + 110], fill=(190, 165, 130, 255))
    draw.rectangle([320, seat_y + 55, 680, seat_y + 90], fill=(190, 165, 130, 255))
    # Top surface
    draw.ellipse([320, seat_y - 20, 680, seat_y + 80], fill=(235, 215, 185, 255))
    # Chamfered specular rim
    draw.ellipse([325, seat_y - 17, 675, seat_y + 75], outline=(255, 245, 225, 180), width=2)
    
    # Exposed through-tenon wedged mortises on seat top
    tenons = [(420, seat_y + 20), (500, seat_y + 45), (580, seat_y + 20)]
    for tx, ty in tenons:
        draw.ellipse([tx-12, ty-7, tx+12, ty+7], fill=(160, 130, 95, 255))
        draw.line([(tx-8, ty), (tx+8, ty)], fill=(60, 40, 25, 255), width=2)
        
    img.alpha_composite(stool)
    img.convert('RGB').save('public/assets/products/hinoki-stool.jpg', 'JPEG', quality=95)
    print("Generated hinoki-stool.jpg")

def render_valet_tray():
    img = studio_background(1000, 800)
    shadow = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 500, 540, 280, 70, opacity=130)
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(shadow)
    
    tray = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tray)
    
    # Solid Walnut Base Polygon
    outer = [(240, 420), (500, 310), (760, 420), (500, 530)]
    draw.polygon(outer, fill=(45, 30, 20, 255))
    
    # Beveled rim
    rim_l = [(240, 420), (500, 530), (500, 560), (240, 450)]
    rim_r = [(500, 530), (760, 420), (760, 450), (500, 560)]
    draw.polygon(rim_l, fill=(35, 22, 14, 255))
    draw.polygon(rim_r, fill=(28, 18, 10, 255))
    
    # Carved inner basin
    inner = [(270, 420), (500, 330), (730, 420), (500, 510)]
    draw.polygon(inner, fill=(32, 20, 12, 255))
    
    # Fluted Pen channel
    pen_slot = [(310, 410), (470, 340), (490, 350), (330, 420)]
    draw.polygon(pen_slot, fill=(22, 14, 8, 255))
    
    # Solid Brass Insert Dish
    draw.ellipse([540, 410, 660, 480], fill=(205, 165, 45, 255))
    draw.ellipse([545, 415, 655, 475], fill=(230, 195, 75, 255))
    
    img.alpha_composite(tray)
    img.convert('RGB').save('public/assets/products/valet-tray.jpg', 'JPEG', quality=95)
    print("Generated valet-tray.jpg")

def render_fluted_bookends():
    img = studio_background(1000, 800)
    shadow = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 380, 600, 120, 40, opacity=110)
    draw_soft_shadow(sdraw, 620, 600, 120, 40, opacity=110)
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(shadow)
    
    be = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(be)
    
    for ox in [330, 570]:
        # Arch profile in White Oak
        draw.rounded_rectangle([ox, 260, ox+140, 580], radius=70, fill=(200, 175, 140, 255))
        # Side shade
        draw.polygon([(ox+140, 330), (ox+170, 310), (ox+170, 550), (ox+140, 580)], fill=(160, 135, 105, 255))
        # Top arch shade
        draw.ellipse([ox+70, 240, ox+170, 340], fill=(220, 195, 160, 160))
        
        # Fluted architectural vertical grooves
        for gx in range(ox+25, ox+120, 18):
            draw.line([(gx, 340), (gx, 560)], fill=(150, 125, 95, 255), width=4)
            draw.line([(gx+2, 340), (gx+2, 560)], fill=(230, 205, 170, 255), width=2)
            
    img.alpha_composite(be)
    img.convert('RGB').save('public/assets/products/fluted-bookends.jpg', 'JPEG', quality=95)
    print("Generated fluted-bookends.jpg")

def render_timber_sconce():
    img = studio_background(1000, 800, top_color=(20, 20, 22), bottom_color=(15, 15, 16))
    # Ambient warm LED glow
    glow = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([300, 100, 700, 500], fill=(255, 180, 80, 55))
    gdraw.ellipse([350, 400, 650, 700], fill=(255, 180, 80, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img.alpha_composite(glow)
    
    sconce = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sconce)
    
    # Vertical cantilevered Steamed Ash Blade
    draw.rounded_rectangle([450, 220, 550, 580], radius=8, fill=(210, 190, 160, 255))
    # Front facing shadow
    draw.line([(450, 220), (450, 580)], fill=(255, 240, 215, 200), width=2)
    draw.line([(550, 220), (550, 580)], fill=(120, 100, 75, 200), width=3)
    
    # Recessed brass bracket
    draw.rectangle([480, 380, 520, 420], fill=(210, 175, 60, 255))
    
    img.alpha_composite(sconce)
    img.convert('RGB').save('public/assets/products/timber-sconce.jpg', 'JPEG', quality=95)
    print("Generated timber-sconce.jpg")

def render_turned_vessel():
    img = studio_background(1000, 800)
    shadow = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 500, 660, 160, 45, opacity=130)
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(shadow)
    
    vessel = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vessel)
    
    # Lathe-turned bulbous form in Oregon Walnut
    # Side silhouettes
    points = [
        (380, 460), (360, 540), (400, 620), (460, 650),
        (540, 650), (600, 620), (640, 540), (620, 460),
        (580, 390), (540, 370), (460, 370), (420, 390)
    ]
    draw.polygon(points, fill=(55, 36, 22, 255))
    
    # Oval rim on top
    draw.ellipse([430, 355, 570, 395], fill=(35, 20, 12, 255))
    draw.ellipse([440, 362, 560, 388], fill=(15, 8, 4, 255))
    
    # Specular curved highlights
    draw.arc([385, 410, 615, 630], start=110, end=210, fill=(110, 80, 55, 140), width=6)
    
    img.alpha_composite(vessel)
    img.convert('RGB').save('public/assets/products/turned-vessel.jpg', 'JPEG', quality=95)
    print("Generated turned-vessel.jpg")

def render_coffee_bench():
    img = studio_background(1000, 800)
    shadow = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 500, 620, 340, 70, opacity=140)
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    img.alpha_composite(shadow)
    
    bench = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bench)
    
    # Thick slab legs
    draw.polygon([(260, 480), (330, 480), (330, 620), (260, 620)], fill=(160, 135, 100, 255))
    draw.polygon([(670, 480), (740, 480), (740, 620), (670, 620)], fill=(145, 120, 85, 255))
    
    # Massive Bench Top Slab (Isometric Perspective)
    top_poly = [(160, 480), (500, 360), (840, 480), (500, 600)]
    draw.polygon(top_poly, fill=(215, 190, 155, 255))
    
    # Slab edge thickness
    side_l = [(160, 480), (500, 600), (500, 635), (160, 515)]
    side_r = [(500, 600), (840, 480), (840, 515), (500, 635)]
    draw.polygon(side_l, fill=(175, 150, 115, 255))
    draw.polygon(side_r, fill=(140, 115, 80, 255))
    
    # Inlaid dark walnut butterfly key
    draw.polygon([(460, 470), (540, 470), (510, 490), (540, 510), (460, 510), (490, 490)], fill=(45, 30, 18, 255))
    
    img.alpha_composite(bench)
    img.convert('RGB').save('public/assets/products/coffee-bench.jpg', 'JPEG', quality=95)
    print("Generated coffee-bench.jpg")

def render_knife_rack():
    img = studio_background(1000, 800)
    shadow = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 500, 480, 320, 40, opacity=120)
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    img.alpha_composite(shadow)
    
    rack = Image.new('RGBA', (1000, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(rack)
    
    # Smoked Bog Oak Blade
    draw.polygon([(180, 420), (820, 380), (820, 460), (180, 500)], fill=(30, 26, 22, 255))
    # Beveled edge
    draw.polygon([(180, 500), (820, 460), (820, 475), (180, 515)], fill=(18, 14, 10, 255))
    
    # Brass mounting caps
    draw.ellipse([210, 450, 226, 466], fill=(210, 175, 60, 255))
    draw.ellipse([774, 410, 790, 426], fill=(210, 175, 60, 255))
    
    img.alpha_composite(rack)
    img.convert('RGB').save('public/assets/products/knife-rack.jpg', 'JPEG', quality=95)
    print("Generated knife-rack.jpg")

# ==============================================================================
# COMMISSION PORTFOLIO ARTPIECE GENERATORS
# ==============================================================================

def render_tsuba_dining_table():
    img = studio_background(1200, 800, top_color=(235, 230, 222), bottom_color=(205, 200, 192))
    shadow = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 600, 640, 480, 90, opacity=160)
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    img.alpha_composite(shadow)
    
    table = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(table)
    
    # Architectural Trestle Legs with Wedged Tenons
    draw.polygon([(320, 440), (400, 440), (430, 640), (290, 640)], fill=(45, 30, 18, 255))
    draw.polygon([(800, 440), (880, 440), (910, 640), (770, 640)], fill=(35, 22, 12, 255))
    # Stretcher with exposed white oak wedge
    draw.polygon([(360, 560), (840, 560), (840, 595), (360, 595)], fill=(40, 25, 14, 255))
    draw.polygon([(330, 550), (350, 550), (345, 605), (335, 605)], fill=(210, 190, 155, 255))
    draw.polygon([(850, 550), (870, 550), (865, 605), (855, 605)], fill=(210, 190, 155, 255))
    
    # Monumental 10-ft Walnut Slab (Bookmatched Live Edge)
    top_poly = [(140, 440), (600, 280), (1060, 440), (600, 600)]
    draw.polygon(top_poly, fill=(58, 38, 24, 255))
    
    # Undercut Bevel Face
    face_l = [(140, 440), (600, 600), (600, 645), (140, 485)]
    face_r = [(600, 600), (1060, 440), (1060, 485), (600, 645)]
    draw.polygon(face_l, fill=(40, 26, 16, 255))
    draw.polygon(face_r, fill=(28, 18, 10, 255))
    
    # Center Fissure & Butterfly Splines
    draw.line([(600, 280), (600, 600)], fill=(20, 12, 6, 200), width=2)
    for by in [360, 460, 540]:
        draw.polygon([(575, by-10), (625, by-10), (610, by), (625, by+10), (575, by+10), (590, by)], fill=(215, 195, 165, 255))
        
    img.alpha_composite(table)
    img.convert('RGB').save('public/assets/products/tsuba-dining-table.jpg', 'JPEG', quality=95)
    print("Generated tsuba-dining-table.jpg")

def render_solstice_credenza():
    img = studio_background(1200, 800)
    shadow = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 600, 600, 420, 60, opacity=140)
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    img.alpha_composite(shadow)
    
    cred = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(cred)
    
    # Minimalist Cantilever Steel/Brass Base
    draw.rectangle([280, 560, 920, 575], fill=(140, 115, 45, 255))
    draw.rectangle([340, 575, 360, 615], fill=(120, 95, 35, 255))
    draw.rectangle([840, 575, 860, 615], fill=(120, 95, 35, 255))
    
    # White Oak Box Casework
    # Top face
    draw.polygon([(240, 360), (600, 260), (960, 360), (600, 460)], fill=(215, 190, 155, 255))
    # Front drawer face
    draw.polygon([(240, 360), (600, 460), (600, 565), (240, 465)], fill=(185, 160, 125, 255))
    # Right side face
    draw.polygon([(600, 460), (960, 360), (960, 465), (600, 565)], fill=(155, 130, 95, 255))
    
    # Drawer dividing reveals
    draw.line([(360, 395), (360, 500)], fill=(120, 100, 75, 255), width=2)
    draw.line([(480, 428), (480, 533)], fill=(120, 100, 75, 255), width=2)
    
    # Brass Bar Pulls
    for px, py in [(300, 445), (420, 478), (540, 512)]:
        draw.line([(px, py), (px+35, py+10)], fill=(230, 195, 75, 255), width=4)
        
    img.alpha_composite(cred)
    img.convert('RGB').save('public/assets/products/solstice-credenza.jpg', 'JPEG', quality=95)
    print("Generated solstice-credenza.jpg")

def render_bodleian_library():
    img = studio_background(1200, 800, top_color=(220, 215, 205), bottom_color=(195, 190, 180))
    lib = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(lib)
    
    # Floor shadow
    shadow = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 600, 680, 460, 60, opacity=150)
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    img.alpha_composite(shadow)
    
    # Monumental Pine Bookshelf Uprights
    draw.rectangle([200, 140, 1000, 660], fill=(65, 42, 22, 255))
    # Inner shelves
    for sy in range(220, 640, 80):
        draw.rectangle([220, sy, 980, sy + 18], fill=(165, 120, 70, 255))
        # Warm shelf light wash
        draw.rectangle([220, sy + 18, 980, sy + 22], fill=(255, 220, 130, 180))
        
    # Vertical Bay Dividers
    draw.rectangle([450, 140, 475, 660], fill=(85, 55, 30, 255))
    draw.rectangle([725, 140, 750, 660], fill=(85, 55, 30, 255))
    
    # Brass Library Rail & Ladder
    draw.rectangle([180, 360, 1020, 370], fill=(210, 175, 60, 255))
    draw.polygon([(780, 260), (810, 260), (850, 680), (820, 680)], fill=(45, 28, 14, 255))
    for ry in range(300, 660, 45):
        draw.line([(800 + (ry-260)*0.1, ry), (835 + (ry-260)*0.1, ry)], fill=(210, 175, 60, 255), width=3)
        
    img.alpha_composite(lib)
    img.convert('RGB').save('public/assets/products/bodleian-library.jpg', 'JPEG', quality=95)
    print("Generated bodleian-library.jpg")

def render_kyoto_desk():
    img = studio_background(1200, 800)
    shadow = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 600, 620, 400, 60, opacity=130)
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(shadow)
    
    desk = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(desk)
    
    # Left A-Frame Oak Leg
    draw.polygon([(260, 420), (300, 420), (280, 630), (240, 630)], fill=(165, 140, 105, 255))
    draw.polygon([(360, 420), (400, 420), (440, 630), (400, 630)], fill=(145, 120, 85, 255))
    
    # Right Drawer Pedestal
    draw.polygon([(720, 440), (880, 390), (880, 600), (720, 650)], fill=(185, 160, 125, 255))
    draw.polygon([(880, 390), (940, 410), (940, 620), (880, 600)], fill=(150, 125, 90, 255))
    
    # Desk Top Floating Slab
    top_poly = [(200, 420), (580, 300), (980, 420), (600, 540)]
    draw.polygon(top_poly, fill=(215, 190, 155, 255))
    # Bevel edge
    draw.polygon([(200, 420), (600, 540), (600, 565), (200, 445)], fill=(175, 150, 115, 255))
    draw.polygon([(600, 540), (980, 420), (980, 445), (600, 565)], fill=(140, 115, 80, 255))
    
    img.alpha_composite(desk)
    img.convert('RGB').save('public/assets/products/kyoto-desk.jpg', 'JPEG', quality=95)
    print("Generated kyoto-desk.jpg")

def render_hearth_chair():
    img = studio_background(1200, 800)
    shadow = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    draw_soft_shadow(sdraw, 600, 650, 260, 55, opacity=120)
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(shadow)
    
    chair = Image.new('RGBA', (1200, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(chair)
    
    # Hinoki Wood Frame
    # Backrest uprights
    draw.polygon([(460, 280), (490, 280), (470, 560), (440, 560)], fill=(205, 180, 145, 255))
    draw.polygon([(690, 280), (720, 280), (740, 560), (710, 560)], fill=(185, 160, 125, 255))
    # Top curved crest rail
    draw.rounded_rectangle([440, 260, 740, 310], radius=10, fill=(225, 200, 165, 255))
    
    # Sculpted Armrests
    draw.polygon([(400, 410), (490, 410), (470, 435), (380, 435)], fill=(225, 200, 165, 255))
    draw.polygon([(700, 410), (790, 410), (810, 435), (720, 435)], fill=(195, 170, 135, 255))
    
    # Belgian Raw Linen Deep Seat Cushion
    draw.polygon([(430, 470), (750, 470), (720, 570), (400, 570)], fill=(235, 230, 220, 255))
    draw.polygon([(400, 570), (720, 570), (720, 620), (400, 620)], fill=(210, 205, 195, 255))
    
    img.alpha_composite(chair)
    img.convert('RGB').save('public/assets/products/hearth-chair.jpg', 'JPEG', quality=95)
    print("Generated hearth-chair.jpg")

def render_timber_flitches():
    img = studio_background(1200, 800, top_color=(35, 30, 25), bottom_color=(20, 18, 15))
    draw = ImageDraw.Draw(img)
    
    # Studio Stack of Seasoned Hardwood Flitches (Live Bark Edge)
    slabs = [
        ((200, 640, 1000, 700), (55, 36, 22), 'WILLAMETTE BLACK WALNUT #742 [MC 6.8%]'),
        ((220, 560, 980, 620), (195, 170, 135), 'QUARTER-SAWN WHITE OAK #610 [MC 7.1%]'),
        ((240, 480, 960, 540), (225, 205, 175), 'JAPANESE HINOKI CYPRESS #804 [MC 6.2%]'),
        ((260, 400, 940, 460), (145, 95, 45), '1890s RECLAIMED HEART PINE #192 [MC 7.4%]')
    ]
    
    for (box, col, tag) in slabs:
        draw.rounded_rectangle(box, radius=8, fill=col)
        # Bark rough edge simulation
        draw.line([(box[0], box[3]-4), (box[2], box[3]-4)], fill=(20, 12, 6, 255), width=6)
        # Kiln lot stamp
        draw.text((box[0]+30, box[1]+18), tag, fill=(255, 255, 255, 200))
        
    img.convert('RGB').save('public/assets/products/timber-flitches.jpg', 'JPEG', quality=95)
    print("Generated timber-flitches.jpg")

if __name__ == '__main__':
    render_butcher_block()
    render_hinoki_stool()
    render_valet_tray()
    render_fluted_bookends()
    render_timber_sconce()
    render_turned_vessel()
    render_coffee_bench()
    render_knife_rack()
    render_tsuba_dining_table()
    render_solstice_credenza()
    render_bodleian_library()
    render_kyoto_desk()
    render_hearth_chair()
    render_timber_flitches()
    print("All 14 studio product images generated successfully!")
