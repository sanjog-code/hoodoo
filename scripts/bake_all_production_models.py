import sys
sys.path.append('.')
import os
import shutil
from scripts.bake_masterpiece_apparel import create_masterpiece_hoodie, create_masterpiece_tee
from scripts.bake_masterpiece_sneaker import create_masterpiece_skate_sneaker

out_dirs = [r"public/models", r"public/assets/models"]
for d in out_dirs:
    os.makedirs(d, exist_ok=True)

# 1. Bake Masterpiece Hoodies (Attached Hood, 3D Raised Kangaroo Pouch, Full-Length Enclosed Sleeves)
print("=== BAKING 500GSM MASTERPIECE HOODIES (ATTACHED HOOD, 3D POUCH, FULL SLEEVES) ===")
hoodie_keys = ["hoodie_master", "hoodie_hero", "hoodie_p1", "hoodie_p2", "hoodie_p3", "hoodie_p4", "hoodie_p13"]
base_hoodie = os.path.join(out_dirs[0], "hoodie_master.glb")
create_masterpiece_hoodie(base_hoodie)

for k in hoodie_keys:
    for d in out_dirs:
        dest = os.path.join(d, f"{k}.glb")
        if os.path.abspath(base_hoodie) != os.path.abspath(dest):
            shutil.copyfile(base_hoodie, dest)
        print(f"  -> {dest}")

# 2. Bake Masterpiece Boxy Tees (Cylindrical Sleeves, Clean Inward Hem Cuffs)
print("\n=== BAKING 300GSM MASTERPIECE BOXY TEES (CYLINDRICAL SLEEVES, PLANAR CUFFS) ===")
tee_keys = ["tee_p5", "tee_p6", "tee_p7", "tee_p8", "tee_p14", "tee_p15"]
base_tee = os.path.join(out_dirs[0], "tee_p5.glb")
create_masterpiece_tee(base_tee)

for k in tee_keys:
    for d in out_dirs:
        dest = os.path.join(d, f"{k}.glb")
        if os.path.abspath(base_tee) != os.path.abspath(dest):
            shutil.copyfile(base_tee, dest)
        print(f"  -> {dest}")

# 3. Bake Masterpiece Skate Sneakers (Broad Skate Toe, Cupsole, 3D Wave, 5 Laces, Padded Collar)
print("\n=== BAKING MASTERPIECE SKATE SNEAKERS (ROUNDED TOE, CUPSOLE, 3D SILVER WAVE) ===")
kicks_keys = ["kicks_p9", "kicks_p10", "kicks_p11", "kicks_p12", "kicks_p16"]
base_kick = os.path.join(out_dirs[0], "kicks_p9.glb")
create_masterpiece_skate_sneaker(base_kick)

for k in kicks_keys:
    for d in out_dirs:
        dest = os.path.join(d, f"{k}.glb")
        if os.path.abspath(base_kick) != os.path.abspath(dest):
            shutil.copyfile(base_kick, dest)
        print(f"  -> {dest}")

print("\nALL PRODUCTION 3D GLB MODELS SUCCESSFULLY BAKED & SYNCHRONIZED!")
