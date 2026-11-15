import bpy
import os
import math
import sys
sys.path.append('.')

from scripts.bake_masterpiece_apparel import create_masterpiece_hoodie, create_masterpiece_tee
from scripts.bake_masterpiece_sneaker import create_masterpiece_skate_sneaker

out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
os.makedirs(out_dir, exist_ok=True)

# 1. Bake Test Hoodie
hoodie_glb = os.path.join(out_dir, "test_hoodie_v11.glb")
hoodie_tex = r"public/assets/models/textures/tex_hero_asphalt.png"
create_masterpiece_hoodie(hoodie_glb, hoodie_tex if os.path.exists(hoodie_tex) else None)

# 2. Bake Test Tee
tee_glb = os.path.join(out_dir, "test_tee_v10.glb")
tee_tex = r"public/assets/models/textures/tex_p5_white.png"
create_masterpiece_tee(tee_glb, tee_tex if os.path.exists(tee_tex) else None)

# 3. Bake Test Sneaker
sneaker_glb = os.path.join(out_dir, "test_sneaker_v9.glb")
create_masterpiece_skate_sneaker(sneaker_glb)

print("ALL TEST GLBs BAKED SUCCESSFULLY!")

# Function to render GLB file to PNG
def render_glb(glb_path, out_png, cam_loc, cam_rot, light_intensity=3.5):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    world = bpy.data.worlds.new('Render_World')
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs['Color'].default_value = (0.05, 0.05, 0.06, 1.0)
        bg.inputs['Strength'].default_value = 1.0
        
    bpy.ops.import_scene.gltf(filepath=glb_path)
    
    # Camera
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 65
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = cam_loc
    cam_obj.rotation_euler = cam_rot
    bpy.context.scene.camera = cam_obj
    
    # Lights
    # Key light
    key_light = bpy.data.lights.new("KeyLight", type='AREA')
    key_light.energy = 180 * light_intensity
    key_light.size = 1.2
    key_obj = bpy.data.objects.new("KeyLight", key_light)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (1.5, -1.8, 1.2)
    key_obj.rotation_euler = (math.radians(55), 0, math.radians(40))
    
    # Fill light
    fill_light = bpy.data.lights.new("FillLight", type='AREA')
    fill_light.energy = 80 * light_intensity
    fill_light.size = 1.8
    fill_obj = bpy.data.objects.new("FillLight", fill_light)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-1.8, -1.2, 0.8)
    fill_obj.rotation_euler = (math.radians(60), 0, math.radians(-50))
    
    # Rim light
    rim_light = bpy.data.lights.new("RimLight", type='SPOT')
    rim_light.energy = 220 * light_intensity
    rim_light.spot_size = math.radians(60)
    rim_obj = bpy.data.objects.new("RimLight", rim_light)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (0.0, 2.0, 1.5)
    rim_obj.rotation_euler = (math.radians(-50), 0, math.radians(180))
    
    # Render settings
    scene = bpy.context.scene
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.filepath = out_png
    scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {out_png}")

# Render Hoodie Front
render_glb(
    hoodie_glb,
    os.path.join(out_dir, "test_render_hoodie_v11_front.png"),
    cam_loc=(0.0, -1.55, 0.05),
    cam_rot=(math.radians(88), 0, 0)
)

# Render Hoodie Back
render_glb(
    hoodie_glb,
    os.path.join(out_dir, "test_render_hoodie_v11_back.png"),
    cam_loc=(0.0, 1.55, 0.05),
    cam_rot=(math.radians(92), 0, math.radians(180))
)

# Render Tee Front
render_glb(
    tee_glb,
    os.path.join(out_dir, "test_render_tee_v10.png"),
    cam_loc=(0.0, -1.50, 0.05),
    cam_rot=(math.radians(88), 0, 0)
)

# Render Sneaker 3/4 Perspective
render_glb(
    sneaker_glb,
    os.path.join(out_dir, "test_render_masterpiece_sneaker_v9.png"),
    cam_loc=(0.28, -0.38, 0.22),
    cam_rot=(math.radians(64), 0, math.radians(35)),
    light_intensity=2.2
)

print("ALL 4 BEAUTY RENDERS COMPLETED!")
