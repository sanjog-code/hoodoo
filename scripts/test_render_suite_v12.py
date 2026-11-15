import bpy
import os
import math
import sys
sys.path.append('.')

from scripts.bake_masterpiece_apparel import create_masterpiece_hoodie, create_masterpiece_tee
from scripts.bake_masterpiece_sneaker import create_masterpiece_skate_sneaker

out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"

# 1. Bake Masterpiece Hoodie with Asphalt texture (which has our new master HooDoo logo)
hoodie_glb = os.path.join(out_dir, "test_hoodie_v12.glb")
hoodie_tex = r"public/assets/models/textures/tex_hero_asphalt.png"
create_masterpiece_hoodie(hoodie_glb, hoodie_tex if os.path.exists(hoodie_tex) else None)

# 2. Bake Masterpiece Tee with White texture (which has our new master HooDoo logo)
tee_glb = os.path.join(out_dir, "test_tee_v11.glb")
tee_tex = r"public/assets/models/textures/tex_p5_white.png"
create_masterpiece_tee(tee_glb, tee_tex if os.path.exists(tee_tex) else None)

# 3. Bake Masterpiece Skate Sneaker
sneaker_glb = os.path.join(out_dir, "test_sneaker_v11.glb")
create_masterpiece_skate_sneaker(sneaker_glb)

print("ALL MASTERPIECE GLBs BAKED!")

def render_glb_view(glb_path, out_png, cam_loc, cam_rot, energy_mult=1.0):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    world = bpy.data.worlds.new('Render_World')
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs['Color'].default_value = (0.05, 0.05, 0.06, 1.0)
        bg.inputs['Strength'].default_value = 1.0
        
    bpy.ops.import_scene.gltf(filepath=glb_path)
    
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 65
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location = cam_loc
    cam_obj.rotation_euler = cam_rot
    bpy.context.scene.camera = cam_obj
    
    # Key light
    key_light = bpy.data.lights.new("KeyLight", type='AREA')
    key_light.energy = 160 * energy_mult
    key_light.size = 1.2
    key_obj = bpy.data.objects.new("KeyLight", key_light)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (1.2, -1.6, 1.1)
    key_obj.rotation_euler = (math.radians(55), 0, math.radians(40))
    
    # Fill light
    fill_light = bpy.data.lights.new("FillLight", type='AREA')
    fill_light.energy = 70 * energy_mult
    fill_light.size = 1.8
    fill_obj = bpy.data.objects.new("FillLight", fill_light)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-1.5, -1.1, 0.7)
    fill_obj.rotation_euler = (math.radians(60), 0, math.radians(-50))
    
    # Rim light
    rim_light = bpy.data.lights.new("RimLight", type='SPOT')
    rim_light.energy = 200 * energy_mult
    rim_light.spot_size = math.radians(60)
    rim_obj = bpy.data.objects.new("RimLight", rim_light)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (0.0, 1.8, 1.4)
    rim_obj.rotation_euler = (math.radians(-50), 0, math.radians(180))
    
    scene = bpy.context.scene
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.filepath = out_png
    scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {out_png}")

# 1. Hoodie Front (Showing centered HooDoo logo, 3D kangaroo pocket, full sleeves)
render_glb_view(
    hoodie_glb,
    os.path.join(out_dir, "test_render_hoodie_v12_front.png"),
    cam_loc=(0.0, -1.55, 0.05),
    cam_rot=(math.radians(88), 0, 0),
    energy_mult=1.0
)

# 2. Hoodie Back (Showing attached hood draped on scapula, un-obscured mural, full sleeves)
render_glb_view(
    hoodie_glb,
    os.path.join(out_dir, "test_render_hoodie_v12_back.png"),
    cam_loc=(0.0, 1.55, 0.05),
    cam_rot=(math.radians(92), 0, math.radians(180)),
    energy_mult=1.0
)

# 3. Tee Front (Showing centered HooDoo logo, cylindrical sleeves, planar cuffs)
render_glb_view(
    tee_glb,
    os.path.join(out_dir, "test_render_tee_v11.png"),
    cam_loc=(0.0, -1.50, 0.05),
    cam_rot=(math.radians(88), 0, 0),
    energy_mult=1.0
)

# 4. Sneaker Front 3/4 Perspective (Showing toe box, 3D smooth silver wave, laces, tongue, cupsole)
bpy.ops.wm.read_factory_settings(use_empty=True)
world = bpy.data.worlds.new('Render_World_Sneaker')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.05, 0.05, 0.06, 1.0)
    bg.inputs['Strength'].default_value = 1.0

bpy.ops.import_scene.gltf(filepath=sneaker_glb)

cam_data = bpy.data.cameras.new("Camera_Sneaker")
cam_data.lens = 75
cam_obj = bpy.data.objects.new("Camera_Sneaker", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (0.24, 0.30, 0.16)
cam_obj.rotation_euler = (math.radians(65), 0, math.radians(142))
bpy.context.scene.camera = cam_obj

# Balanced sneaker lights
key_light = bpy.data.lights.new("Key_Snk", type='AREA')
key_light.energy = 85
key_light.size = 0.8
key_obj = bpy.data.objects.new("Key_Snk", key_light)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (0.8, 0.6, 0.7)
key_obj.rotation_euler = (math.radians(50), 0, math.radians(120))

fill_light = bpy.data.lights.new("Fill_Snk", type='AREA')
fill_light.energy = 35
fill_light.size = 1.2
fill_obj = bpy.data.objects.new("Fill_Snk", fill_light)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (-0.7, 0.4, 0.4)
fill_obj.rotation_euler = (math.radians(55), 0, math.radians(-110))

rim_light = bpy.data.lights.new("Rim_Snk", type='SPOT')
rim_light.energy = 95
rim_light.spot_size = math.radians(50)
rim_obj = bpy.data.objects.new("Rim_Snk", rim_light)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (-0.4, -0.8, 0.8)
rim_obj.rotation_euler = (math.radians(-45), 0, 0)

out_sneaker_png = os.path.join(out_dir, "test_render_sneaker_v11_front34.png")
scene = bpy.context.scene
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.filepath = out_sneaker_png
scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print(f"Rendered Sneaker: {out_sneaker_png}")

print("ALL RENDERS COMPLETED SUCCESSFULLY!")
