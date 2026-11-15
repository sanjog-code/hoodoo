import re

with open('src/data/products.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Pattern for product blocks
blocks = re.findall(r'\{\s*id:\s*[\'"]([^\'"]+)[\'"][\s\S]*?inStock:', text)
for b in text.split('id:'):
    if 'image:' in b:
        pid_m = re.search(r'^\s*[\'"]([^\'"]+)[\'"]', b)
        name_m = re.search(r'name:\s*[\'"]([^\'"]+)[\'"]', b)
        img_m = re.search(r'image:\s*[\'"]([^\'"]+)[\'"]', b)
        back_m = re.search(r'backImage:\s*[\'"]([^\'"]+)[\'"]', b)
        if pid_m and img_m:
            pid = pid_m.group(1)
            name = name_m.group(1) if name_m else ''
            img = img_m.group(1)
            back = back_m.group(1) if back_m else 'NONE'
            print(f"{pid:15} | {name:32} | {img:35} | {back}")
