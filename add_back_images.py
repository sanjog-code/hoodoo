with open('src/data/products.ts', 'r', encoding='utf-8') as f:
    lines = f.readlines()

clean = []
i = 0
while i < len(lines):
    line = lines[i]
    if "backImage: 'category:" in line:
        i += 1
        if i < len(lines) and "back.png" in lines[i]:
            i += 1
        continue
    clean.append(line)
    i += 1

with open('src/data/products.ts', 'w', encoding='utf-8') as f:
    f.writelines(clean)

print('Filtered corrupted lines!')
