import os, re

for root, _, files in os.walk('src'):
    for f in files:
        if f.endswith(('.ts', '.tsx')):
            p = os.path.join(root, f)
            txt = open(p, 'r', encoding='utf-8').read()
            m = re.findall(r'models/textures/[a-zA-Z0-9_.]+', txt)
            if m:
                print(p, m)
