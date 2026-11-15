import bpy
import os
import math
import sys
sys.path.append('.')

from scripts.bake_hyperrealistic_skate_sneaker_v2 import create_hyperrealistic_skate_sneaker

out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
sneaker_glb = os.path.join(out_dir, "test_sneaker_v10.glb")
create_hyperrealistic_skate_sneaker(sneaker_glb)

bpy.ops.wm.read_factory_settings(use_empty=True)
world = bpy.data.worlds.new('Render_World')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs['Color'].default_value = (0.05, 0.05, 0.06, 1.0)
    bg.inputs['Strength'].default_value = 1.0

bpy.ops.import_scene.gltf(filepath=sneaker_glb)

# Camera looking at front 3/4 of the shoe (toe and lateral wave logo)
cam_data = bpy.data.cameras.new("Camera")
cam_data.lens = 70
cam_obj = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (0.28, 0.32, 0.18)
cam_obj.rotation_euler = (math.radians(64), 0, math.radians(140))
bpy.context.scene.camera = cam_obj

# Studio Lights
key_light = bpy.data.lights.new("KeyLight", type='AREA')
key_light.energy = 400
key_light.size = 1.2
key_obj = bpy.data.objects.new("KeyLight", key_light)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (1.2, 0.8, 1.0)
key_obj.rotation_euler = (math.radians(55), 0, math.radians(110))

fill_light = bpy.data.lights.new("FillLight", type='AREA')
fill_light.energy = 160
fill_light.size = 1.8
fill_obj = bpy.data.objects.new("FillLight", fill_light)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (-1.2, 0.5, 0.6)
fill_obj.rotation_euler = (math.radians(60), 0, math.radians(-110))

rim_light = bpy.data.lights.new("RimLight", type='SPOT')
rim_light.energy = 450
rim_light.spot_size = math.radians(60)
rim_obj = bpy.data.objects.new("RimLight", rim_light)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (-0.5, -1.2, 1.2)
rim_obj.rotation_euler = (math.radians(-50), 0, 0)

out_png = os.path.join(out_dir, "test_render_sneaker_v10_front34.png")
scene = bpy.context.scene
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.filepath = out_png
scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print(f"Rendered: {out_png}")
