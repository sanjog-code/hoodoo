import os
from PIL import Image

for name in ['p1_black', 'p4_sand', 'p7_sand']:
    f = Image.open(f"public/assets/collection/{name}.png")
    b = Image.open(f"public/assets/collection/{name}_back.png")
    print(f"[{name}]")
    # Save a side-by-side comparison
    combo = Image.new('RGB', (800*2, 800))
    combo.paste(f, (0, 0))
    combo.paste(b, (800, 0))
    combo.save(f"public/assets/collection/debug_{name}_sidebyside.png")
    print(f"Saved debug_{name}_sidebyside.png")
