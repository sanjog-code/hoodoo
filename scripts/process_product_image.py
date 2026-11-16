import os
import sys
from PIL import Image, ImageFilter
import numpy as np
from rembg import remove, new_session

# Initialize rembg session once for fast inference
_session = None

def get_session():
    global _session
    if _session is None:
        _session = new_session('u2net')
    return _session

def clean_and_isolate_product(input_path, output_path, target_size=(800, 800), padding=50):
    """
    Takes an input image with a studio or chroma background,
    runs neural background removal (rembg u2net),
    cleans fringes, centers the object, and pads into target_size RGBA image.
    """
    if not os.path.exists(input_path):
        print(f"Error: input file {input_path} does not exist")
        return False
        
    im = Image.open(input_path)
    
    # 1. Neural background removal
    session = get_session()
    rgba = remove(im, session=session)
    
    # 2. Get bounding box of non-zero alpha
    bbox = rgba.getbbox()
    if not bbox:
        print("Warning: empty alpha channel")
        return False
        
    cropped = rgba.crop(bbox)
    
    # 3. Fit into target square with padding
    tw, th = target_size
    avail_w = tw - 2 * padding
    avail_h = th - 2 * padding
    
    scale = min(avail_w / cropped.width, avail_h / cropped.height)
    new_w = int(cropped.width * scale)
    new_h = int(cropped.height * scale)
    
    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 4. Paste onto transparent canvas centered
    final_canvas = Image.new('RGBA', target_size, (0, 0, 0, 0))
    paste_x = (tw - new_w) // 2
    paste_y = (th - new_h) // 2
    final_canvas.paste(resized, (paste_x, paste_y), mask=resized)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    final_canvas.save(output_path, 'PNG')
    print(f"Saved clean transparent product image to: {output_path} ({target_size[0]}x{target_size[1]})")
    return True

if __name__ == '__main__':
    if len(sys.argv) > 2:
        clean_and_isolate_product(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python process_product_image.py <input> <output>")
