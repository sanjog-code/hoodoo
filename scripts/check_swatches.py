import re

with open('src/data/products.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all swatches: { name: '...', color: '...', image: '...', backImage: '...' }
swatches = re.findall(r"\{\s*name:\s*['\"]([^'\"]+)['\"],\s*color:\s*['\"][^'\"]+['\"],\s*image:\s*['\"]([^'\"]+)['\"],\s*backImage:\s*['\"]([^'\"]+)['\"]\s*\}", text)

print(f"Total swatches parsed: {len(swatches)}")
for name, img, back in swatches:
    print(f"Swatch: {name:25} | img: {img:35} | back: {back}")
