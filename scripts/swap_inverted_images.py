import os
import shutil

collection_dir = "public/assets/collection"

def swap_pair(base_name):
    f_path = os.path.join(collection_dir, f"{base_name}.png")
    b_path = os.path.join(collection_dir, f"{base_name}_back.png")
    if os.path.exists(f_path) and os.path.exists(b_path):
        tmp_path = os.path.join(collection_dir, f"{base_name}_temp_swap.png")
        shutil.move(f_path, tmp_path)
        shutil.move(b_path, f_path)
        shutil.move(tmp_path, b_path)
        print(f"Swapped front/back for {base_name}")

# Swap p5 white, black, gold
swap_pair("p5_white")
swap_pair("p5_black")
swap_pair("p5_gold")

print("Completed 2D image swaps for p5!")
