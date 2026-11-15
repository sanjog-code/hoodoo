import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

font_path = 'C:/Windows/Fonts/OLDENGL.TTF'
font = ImageFont.truetype(font_path, 130)

# Create high-res canvas for West Coast street logo
w, h = 900, 240
img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# West Coast Gang & Street Life Typography:
# Sharp chicano drop shadow, raw bone fill, and clean razor-sharp outlines
text = "Hoodoo"

# Drop shadow (deep obsidian)
draw.text((54, 44), text, font=font, fill=(10, 10, 10, 220))
draw.text((53, 43), text, font=font, fill=(15, 15, 15, 230))
draw.text((52, 42), text, font=font, fill=(20, 20, 20, 240))

# Stroke outline (pure black)
for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (2,2), (-2,2), (2,-2)]:
    draw.text((50+dx, 40+dy), text, font=font, fill=(10, 10, 10, 255))

# Main fill: Raw bone ivory with subtle street chrome gradient feel
draw.text((50, 40), text, font=font, fill=(245, 244, 240, 255))

# Crop tightly around text
bbox = img.getbbox()
cropped = img.crop((bbox[0]-10, bbox[1]-10, bbox[2]+10, bbox[3]+10))
cropped.save('public/assets/hoodoo_westcoast_logo.png')
print('Saved public/assets/hoodoo_westcoast_logo.png with size:', cropped.size)
