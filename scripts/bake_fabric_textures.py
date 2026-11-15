import os
from PIL import Image, ImageDraw, ImageFilter

def create_baked_textures():
    os.makedirs("public/assets/models/textures", exist_ok=True)
    
    hoodies = [
        {
            "id": "hero",
            "base_color": (28, 28, 30),
            "front_img": "public/assets/collection/hero_asphalt.png",
            "back_img": "public/assets/collection/hero_asphalt_back.png",
            "out": "public/assets/models/textures/tex_hero.png"
        },
        {
            "id": "p1",
            "base_color": (16, 16, 18),
            "front_img": "public/assets/collection/p1_black.png",
            "back_img": "public/assets/collection/p1_black_back.png",
            "out": "public/assets/models/textures/tex_p1.png"
        },
        {
            "id": "p2",
            "base_color": (61, 43, 36),
            "front_img": "public/assets/collection/p2_cocoa.png",
            "back_img": "public/assets/collection/p2_cocoa_back.png",
            "out": "public/assets/models/textures/tex_p2.png"
        },
        {
            "id": "p3",
            "base_color": (18, 18, 20),
            "front_img": "public/assets/collection/p3_black.png",
            "back_img": "public/assets/collection/p3_black_back.png",
            "out": "public/assets/models/textures/tex_p3.png"
        },
        {
            "id": "p4",
            "base_color": (168, 154, 135),
            "front_img": "public/assets/collection/p4_sand.png",
            "back_img": "public/assets/collection/p4_sand_back.png",
            "out": "public/assets/models/textures/tex_p4.png"
        },
        {
            "id": "p13",
            "base_color": (39, 39, 42),
            "front_img": "public/assets/collection/p13_asphalt.png",
            "back_img": "public/assets/collection/p13_asphalt_back.png",
            "out": "public/assets/models/textures/tex_p13.png"
        }
    ]

    for h in hoodies:
        canvas = Image.new("RGBA", (2048, 2048), h["base_color"] + (255,))
        draw = ImageDraw.Draw(canvas)
        
        # Ribbing on bottom hem
        for y in range(1800, 2048, 12):
            draw.line([(0, y), (2048, y)], fill=(max(0, h["base_color"][0] - 12), max(0, h["base_color"][1] - 12), max(0, h["base_color"][2] - 12), 255), width=3)
            
        # Kangaroo pocket subtle stitch line
        draw.rectangle([540, 1320, 1508, 1780], outline=(h["base_color"][0] + 18, h["base_color"][1] + 18, h["base_color"][2] + 18, 255), width=5)

        # Front Chest Graphic
        if os.path.exists(h["front_img"]):
            fg = Image.open(h["front_img"]).convert("RGBA")
            bbox = fg.getbbox()
            if bbox:
                fg_crop = fg.crop(bbox)
                fg_crop.thumbnail((720, 720), Image.Resampling.LANCZOS)
                paste_x = (2048 - fg_crop.width) // 2
                paste_y = 520
                canvas.paste(fg_crop, (paste_x, paste_y), fg_crop)

        canvas.save(h["out"], "PNG")
        print(f"Baked Master Texture: {h['out']}")

if __name__ == "__main__":
    create_baked_textures()
