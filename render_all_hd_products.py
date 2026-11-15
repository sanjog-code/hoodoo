import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

out_dir = 'carpenter-shop-website/assets/products'
os.makedirs(out_dir, exist_ok=True)

def create_wood_surface(width, height, base_color, accent_color, rings=35, noise_amp=0.2):
    """Procedurally synthesize high-definition organic hardwood grain texture with growth rings."""
    x = np.linspace(0, 12, width)
    y = np.linspace(0, 12, height)
    xx, yy = np.meshgrid(x, y)
    
    # Growth ring distortion waves
    distortion = np.sin(xx * 0.4 + np.sin(yy * 0.9) * 2.2) * 0.5 + np.sin(yy * rings * 0.04) * 0.5
    grain = np.sin(xx * 0.12 + yy * 0.06 + distortion * 3.5)
    grain = (grain - grain.min()) / (grain.max() - grain.min() + 1e-6)
    
    # Fine wood fibers
    fibers = np.random.normal(0, noise_amp, (height, width))
    texture = np.clip(grain * 0.82 + fibers * 0.18, 0, 1)
    
    r = np.uint8(base_color[0] * (1 - texture) + accent_color[0] * texture)
    g = np.uint8(base_color[1] * (1 - texture) + accent_color[1] * texture)
    b = np.uint8(base_color[2] * (1 - texture) + accent_color[2] * texture)
    
    arr = np.dstack((r, g, b, np.full((height, width), 255, dtype=np.uint8)))
    return Image.fromarray(arr)

def luxury_studio_backdrop(width=1400, height=1050, wall_color=(32, 31, 29), floor_color=(20, 20, 19)):
    """Creates a high-end luxury studio architectural cove backdrop with warm directional lighting."""
    img = Image.new('RGB', (width, height), wall_color)
    arr = np.zeros((height, width, 3), dtype=np.float32)
    
    horizon = int(height * 0.58)
    for y in range(height):
        if y < horizon:
            # Wall gradient with soft top spotlight
            t = y / horizon
            factor = 0.85 + 0.15 * math.sin(t * math.pi * 0.5)
            arr[y, :, :] = np.array(wall_color, dtype=np.float32) * factor
        else:
            # Floor gradient with ambient ground occlusion
            t = (y - horizon) / (height - horizon)
            factor = 0.95 - 0.25 * t
            arr[y, :, :] = np.array(floor_color, dtype=np.float32) * factor
            
    # Soft warm spotlight in upper center-left
    xx, yy = np.meshgrid(np.arange(width), np.arange(height))
    spot_x, spot_y = int(width * 0.45), int(height * 0.3)
    dist = np.sqrt((xx - spot_x)**2 + (yy - spot_y)**2)
    glow = np.exp(- (dist**2) / (2 * (width * 0.4)**2)) * 38.0
    
    arr[:, :, 0] += glow * 1.1  # Warm gold
    arr[:, :, 1] += glow * 0.95
    arr[:, :, 2] += glow * 0.75
    
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def add_contact_shadow(base_img, box, blur_radius=28, opacity=0.65):
    """Draws a soft, realistic occlusion ground shadow beneath furniture."""
    shadow_layer = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_layer)
    x1, y1, x2, y2 = box
    
    # Multi-layer contact shadow
    alpha = int(255 * opacity)
    draw.ellipse([x1, y1, x2, y2], fill=(8, 7, 6, alpha))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # Sharp dark contact shadow right underneath
    draw2 = ImageDraw.Draw(shadow_layer)
    pad = (x2 - x1) * 0.15
    draw2.ellipse([x1 + pad, y1 + 5, x2 - pad, y2 - 5], fill=(5, 5, 4, 180))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))
    
    base_img.paste(Image.alpha_composite(base_img.convert('RGBA'), shadow_layer).convert('RGB'), (0, 0))

# 1. Credenza
def render_solstice_credenza():
    w, h = 1400, 1050
    bg = luxury_studio_backdrop(w, h, (36, 35, 33), (22, 22, 20))
    wood = create_wood_surface(780, 260, (190, 155, 115), (135, 100, 65), rings=30)
    
    # Shadow
    add_contact_shadow(bg, (280, 720, 1120, 780), blur_radius=32, opacity=0.7)
    
    # Main floating body
    x0, y0 = 310, 480
    bg.paste(wood, (x0, y0))
    
    draw = ImageDraw.Draw(bg)
    # Bevel and brass reveals
    draw.rectangle([x0, y0, x0 + 780, y0 + 6], fill=(225, 195, 155)) # top highlight
    draw.line([x0 + 260, y0 + 6, x0 + 260, y0 + 260], fill=(20, 18, 16), width=2) # door split 1
    draw.line([x0 + 520, y0 + 6, x0 + 520, y0 + 260], fill=(20, 18, 16), width=2) # door split 2
    
    # Unlacquered brass machined pulls
    for px in [x0 + 130, x0 + 390, x0 + 650]:
        draw.rounded_rectangle([px - 4, y0 + 115, px + 4, y0 + 145], radius=2, fill=(212, 175, 55))
        draw.line([px - 3, y0 + 116, px - 3, y0 + 144], fill=(255, 235, 160), width=1)
        
    # Elegant minimalist ceramic on top
    draw.ellipse([x0 + 110, y0 - 90, x0 + 170, y0 - 10], fill=(235, 232, 226))
    draw.ellipse([x0 + 120, y0 - 94, x0 + 160, y0 - 84], fill=(215, 210, 200))
    
    bg.save(os.path.join(out_dir, 'solstice-credenza.jpg'), 'JPEG', quality=95)
    print("Rendered solstice-credenza.jpg")

# 2. Executive Desk
def render_kyoto_desk():
    w, h = 1400, 1050
    bg = luxury_studio_backdrop(w, h, (34, 33, 31), (20, 20, 19))
    top_wood = create_wood_surface(760, 90, (180, 145, 105), (120, 90, 58), rings=25)
    leg_wood = create_wood_surface(70, 360, (160, 125, 88), (110, 80, 50), rings=20)
    
    # Shadow
    add_contact_shadow(bg, (300, 780, 1100, 840), blur_radius=30, opacity=0.7)
    
    # Legs
    bg.paste(leg_wood, (360, 470))
    bg.paste(leg_wood, (970, 470))
    
    # Stretcher joinery
    draw = ImageDraw.Draw(bg)
    draw.rectangle([390, 680, 1010, 715], fill=(130, 95, 62))
    
    # Top Slab
    bg.paste(top_wood, (320, 410))
    draw.rectangle([320, 410, 1080, 416], fill=(220, 190, 150)) # top light
    
    # Leather blotter inset
    draw.rounded_rectangle([480, 412, 920, 460], radius=3, fill=(35, 32, 28))
    
    bg.save(os.path.join(out_dir, 'kyoto-desk.jpg'), 'JPEG', quality=95)
    print("Rendered kyoto-desk.jpg")

# 3. Hearth Chair
def render_hearth_chair():
    w, h = 1400, 1050
    bg = luxury_studio_backdrop(w, h, (35, 34, 32), (21, 21, 20))
    wood = create_wood_surface(460, 480, (85, 55, 35), (45, 28, 16), rings=28)
    
    # Shadow
    add_contact_shadow(bg, (420, 780, 980, 840), blur_radius=26, opacity=0.68)
    
    # Frame
    bg.paste(wood, (470, 380))
    
    # Bouclé cushion
    draw = ImageDraw.Draw(bg)
    # Seat cushion
    draw.rounded_rectangle([490, 580, 910, 680], radius=18, fill=(238, 235, 226))
    # Texture noise for bouclé
    cushion = Image.new('RGBA', (420, 100), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(cushion)
    for _ in range(800):
        cx = np.random.randint(5, 415)
        cy = np.random.randint(5, 95)
        cdraw.point((cx, cy), fill=(210, 205, 195, 140))
    bg.paste(cushion, (490, 580), cushion)
    
    # Backrest pillow
    draw.rounded_rectangle([510, 420, 890, 570], radius=22, fill=(242, 240, 232))
    
    bg.save(os.path.join(out_dir, 'hearth-chair.jpg'), 'JPEG', quality=95)
    print("Rendered hearth-chair.jpg")

# 4. Library Wall
def render_bodleian_library():
    w, h = 1400, 1050
    bg = luxury_studio_backdrop(w, h, (30, 29, 28), (18, 18, 17))
    wood = create_wood_surface(700, 650, (140, 90, 50), (90, 55, 30), rings=35)
    
    add_contact_shadow(bg, (320, 820, 1080, 880), blur_radius=25, opacity=0.6)
    bg.paste(wood, (350, 210))
    
    draw = ImageDraw.Draw(bg)
    # Shelf compartments and dividers
    for sy in [340, 470, 600, 730]:
        draw.rectangle([350, sy, 1050, sy + 14], fill=(185, 130, 75))
    for sx in [520, 690, 860]:
        draw.line([sx, 210, sx, 860], fill=(50, 32, 18), width=8)
        
    # Brass rolling ladder rail
    draw.line([330, 580, 1070, 580], fill=(212, 175, 55), width=6)
    
    bg.save(os.path.join(out_dir, 'bodleian-library.jpg'), 'JPEG', quality=95)
    print("Rendered bodleian-library.jpg")

# 5. Butcher Block
def render_butcher_block():
    w, h = 1200, 900
    bg = luxury_studio_backdrop(w, h, (38, 37, 35), (24, 24, 22))
    add_contact_shadow(bg, (360, 580, 840, 650), blur_radius=24, opacity=0.7)
    
    # End-grain checkered walnut & maple block
    block = Image.new('RGB', (460, 280), (140, 95, 60))
    bdraw = ImageDraw.Draw(block)
    sq = 46
    for i in range(10):
        for j in range(6):
            if (i + j) % 2 == 0:
                c = (75, 48, 28) # dark walnut
            else:
                c = (195, 160, 115) # rock maple
            bdraw.rectangle([i*sq, j*sq, (i+1)*sq, (j+1)*sq], fill=c)
            bdraw.rectangle([i*sq, j*sq, (i+1)*sq, (j+1)*sq], outline=(50, 30, 18), width=1)
            
    # Perimeter juice groove
    bdraw.rounded_rectangle([15, 15, 445, 265], radius=10, outline=(35, 22, 12), width=5)
    bg.paste(block, (370, 360))
    
    draw = ImageDraw.Draw(bg)
    draw.rectangle([370, 360, 830, 366], fill=(220, 190, 150))
    
    bg.save(os.path.join(out_dir, 'butcher-block.jpg'), 'JPEG', quality=95)
    print("Rendered butcher-block.jpg")

# 6. Hinoki Stool
def render_hinoki_stool():
    w, h = 1200, 900
    bg = luxury_studio_backdrop(w, h, (36, 35, 33), (22, 22, 20))
    wood = create_wood_surface(340, 340, (235, 218, 190), (195, 175, 145), rings=18)
    
    add_contact_shadow(bg, (400, 680, 800, 740), blur_radius=24, opacity=0.65)
    
    # Round top
    mask = Image.new('L', (340, 340), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([20, 50, 320, 170], fill=255)
    
    bg.paste(wood, (430, 320), mask)
    
    draw = ImageDraw.Draw(bg)
    # Exposed through-tenon in center of stool top
    draw.rectangle([585, 395, 615, 425], fill=(90, 60, 35))
    
    # 3 architectural canted legs
    draw.polygon([(490, 420), (515, 420), (450, 690), (425, 690)], fill=(210, 190, 160))
    draw.polygon([(685, 420), (710, 420), (775, 690), (750, 690)], fill=(210, 190, 160))
    draw.polygon([(590, 420), (610, 420), (600, 700), (580, 700)], fill=(185, 165, 135))
    
    bg.save(os.path.join(out_dir, 'hinoki-stool.jpg'), 'JPEG', quality=95)
    print("Rendered hinoki-stool.jpg")

# 7. Valet Tray
def render_valet_tray():
    w, h = 1200, 900
    bg = luxury_studio_backdrop(w, h, (37, 36, 34), (23, 23, 21))
    add_contact_shadow(bg, (360, 540, 840, 600), blur_radius=22, opacity=0.65)
    
    tray = create_wood_surface(460, 240, (75, 48, 28), (42, 25, 14), rings=22)
    bg.paste(tray, (370, 360))
    
    draw = ImageDraw.Draw(bg)
    draw.rectangle([370, 360, 830, 365], fill=(120, 80, 48))
    
    # Inlaid solid brass dish
    draw.ellipse([420, 390, 560, 530], fill=(212, 175, 55))
    draw.ellipse([425, 395, 555, 525], fill=(180, 140, 35))
    draw.ellipse([435, 405, 545, 515], fill=(235, 205, 105)) # inner brass luster
    
    # Carved pen groove
    draw.rounded_rectangle([600, 410, 790, 450], radius=10, fill=(30, 18, 10))
    
    bg.save(os.path.join(out_dir, 'valet-tray.jpg'), 'JPEG', quality=95)
    print("Rendered valet-tray.jpg")

render_solstice_credenza()
render_kyoto_desk()
render_hearth_chair()
render_bodleian_library()
render_butcher_block()
render_hinoki_stool()
render_valet_tray()
print("All key HD model assets successfully compiled!")

# 8. Fluted Bookends
def render_fluted_bookends():
    w, h = 1200, 900
    bg = luxury_studio_backdrop(w, h, (35, 34, 32), (22, 22, 20))
    add_contact_shadow(bg, (360, 620, 840, 680), blur_radius=22, opacity=0.65)
    
    wood = create_wood_surface(180, 280, (70, 44, 25), (40, 24, 12), rings=25)
    bg.paste(wood, (410, 360))
    bg.paste(wood, (610, 360))
    
    draw = ImageDraw.Draw(bg)
    # Fluted vertical grooves
    for x in range(425, 580, 18):
        draw.line([x, 360, x, 640], fill=(25, 14, 8), width=4)
        draw.line([x+4, 360, x+4, 640], fill=(110, 75, 45), width=2)
    for x in range(625, 780, 18):
        draw.line([x, 360, x, 640], fill=(25, 14, 8), width=4)
        draw.line([x+4, 360, x+4, 640], fill=(110, 75, 45), width=2)
        
    bg.save(os.path.join(out_dir, 'fluted-bookends.jpg'), 'JPEG', quality=95)
    print("Rendered fluted-bookends.jpg")

# 9. Coffee Bench
def render_coffee_bench():
    w, h = 1200, 900
    bg = luxury_studio_backdrop(w, h, (36, 35, 33), (22, 22, 20))
    add_contact_shadow(bg, (300, 680, 900, 740), blur_radius=26, opacity=0.68)
    
    top = create_wood_surface(620, 80, (65, 40, 22), (38, 22, 12), rings=25)
    bg.paste(top, (290, 480))
    
    draw = ImageDraw.Draw(bg)
    draw.rectangle([290, 480, 910, 485], fill=(130, 85, 50)) # top bevel
    
    # Sled base legs
    draw.polygon([(340, 560), (370, 560), (330, 690), (300, 690)], fill=(45, 28, 16))
    draw.polygon([(830, 560), (860, 560), (900, 690), (870, 690)], fill=(45, 28, 16))
    
    bg.save(os.path.join(out_dir, 'coffee-bench.jpg'), 'JPEG', quality=95)
    print("Rendered coffee-bench.jpg")

# 10. Knife Rack
def render_knife_rack():
    w, h = 1200, 900
    bg = luxury_studio_backdrop(w, h, (38, 37, 35), (24, 24, 22))
    add_contact_shadow(bg, (320, 520, 880, 560), blur_radius=18, opacity=0.55)
    
    rack = create_wood_surface(580, 90, (48, 32, 20), (28, 18, 10), rings=30)
    bg.paste(rack, (310, 420))
    
    draw = ImageDraw.Draw(bg)
    draw.rectangle([310, 420, 890, 424], fill=(110, 80, 50))
    
    # Brass mounting pins
    for px in [340, 860]:
        draw.ellipse([px - 6, 465 - 6, px + 6, 465 + 6], fill=(212, 175, 55))
        draw.ellipse([px - 3, 465 - 3, px + 3, 465 + 3], fill=(255, 235, 150))
        
    bg.save(os.path.join(out_dir, 'knife-rack.jpg'), 'JPEG', quality=95)
    print("Rendered knife-rack.jpg")

# 11. Timber Sconce
def render_timber_sconce():
    w, h = 1200, 900
    bg = luxury_studio_backdrop(w, h, (32, 31, 30), (18, 18, 17))
    add_contact_shadow(bg, (480, 720, 720, 760), blur_radius=22, opacity=0.6)
    
    sconce = create_wood_surface(180, 460, (75, 48, 28), (42, 25, 14), rings=25)
    bg.paste(sconce, (510, 260))
    
    draw = ImageDraw.Draw(bg)
    # Warm golden light halo casting up and down
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse([420, 160, 780, 360], fill=(245, 185, 95, 80))
    gdraw.ellipse([420, 580, 780, 780], fill=(245, 185, 95, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(36))
    bg.paste(Image.alpha_composite(bg.convert('RGBA'), glow).convert('RGB'), (0, 0))
    
    bg.save(os.path.join(out_dir, 'timber-sconce.jpg'), 'JPEG', quality=95)
    print("Rendered timber-sconce.jpg")

# 12. Turned Vessel
def render_turned_vessel():
    w, h = 1200, 900
    bg = luxury_studio_backdrop(w, h, (36, 35, 33), (22, 22, 20))
    add_contact_shadow(bg, (420, 680, 780, 730), blur_radius=22, opacity=0.68)
    
    vessel = create_wood_surface(320, 340, (72, 45, 26), (40, 22, 12), rings=24)
    mask = Image.new('L', (320, 340), 0)
    mdraw = ImageDraw.Draw(mask)
    # Flared organic vessel silhouette
    mdraw.polygon([(100, 20), (220, 20), (270, 150), (220, 320), (100, 320), (50, 150)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1))
    
    bg.paste(vessel, (440, 360), mask)
    
    draw = ImageDraw.Draw(bg)
    draw.ellipse([540, 370, 660, 395], fill=(30, 18, 10))
    
    bg.save(os.path.join(out_dir, 'turned-vessel.jpg'), 'JPEG', quality=95)
    print("Rendered turned-vessel.jpg")

render_fluted_bookends()
render_coffee_bench()
render_knife_rack()
render_timber_sconce()
render_turned_vessel()
