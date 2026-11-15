import re

with open('src/data/products.ts', 'r', encoding='utf-8') as f:
    text = f.read()

parts = text.split("id:")
for p in parts[1:]:
    pid_m = re.search(r"^\s*['\"]([^'\"]+)['\"]", p)
    name_m = re.search(r"name:\s*['\"]([^'\"]+)['\"]", p)
    model_m = re.search(r"model3d:\s*['\"]([^'\"]+)['\"]", p)
    cat_m = re.search(r"category:\s*['\"]([^'\"]+)['\"]", p)
    if pid_m:
        pid = pid_m.group(1)
        name = name_m.group(1) if name_m else ''
        cat = cat_m.group(1) if cat_m else ''
        model = model_m.group(1) if model_m else 'MISSING_MODEL3D'
        print(f"{pid:15} | {cat:6} | {model:35} | {name}")
