with open('src/data/products.ts', 'r', encoding='utf-8') as f:
    text = f.read()

mapping = {
    'wc-hero-hoodie': '/assets/models/hoodie_hero.glb',
    'thumb-wc-01': '/assets/models/hoodie_p1.glb',
    'thumb-wc-02': '/assets/models/hoodie_p2.glb',
    'thumb-wc-03': '/assets/models/hoodie_p3.glb',
    'wc-cat-01': '/assets/models/hoodie_p1.glb',
    'wc-cat-02': '/assets/models/hoodie_p2.glb',
    'wc-cat-03': '/assets/models/hoodie_p3.glb',
    'wc-cat-04': '/assets/models/hoodie_p4.glb',
    'wc-cat-13': '/assets/models/hoodie_p13.glb',
}

for pid, model in mapping.items():
    pattern = f"id: '{pid}',"
    replacement = f"id: '{pid}',\n    model3d: '{model}',"
    if pattern in text and f"model3d: '{model}'" not in text:
        text = text.replace(pattern, replacement, 1)

with open('src/data/products.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated products.ts with 3D model paths!')
