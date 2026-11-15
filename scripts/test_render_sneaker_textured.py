import bpy
import os
import math
import sys
sys.path.append('.')

from scripts.bake_masterpiece_sneaker import create_masterpiece_skate_sneaker

out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
snk_glb = os.path.join(out_dir, "test_sneaker_v13.glb")
create_masterpiece_skate_sneaker(snk_glb)

bpy.ops.wm.read_factory_settings(use_empty=True)
world = bpy.data.worlds.new('Render_World_Snk')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value = (0.05, 0.05, 0.06, 1.0)
    bg.inputs['Strength'].default_value = 1.0

bpy.ops.import_scene.gltf(filepath=snk_glb)

cam_data = bpy.data.cameras.new('Camera_Snk')
cam_data.lens = 70
cam_obj = bpy.data.objects.new('Camera_Snk', cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = (0.28, 0.34, 0.18)
cam_obj.rotation_euler = (math.radians(65), 0, math.radians(140))
bpy.context.scene.camera = cam_obj

# Balanced Studio Lights
key_light = bpy.data.lights.new('Key_Snk', type='AREA')
key_light.energy = 95
key_light.size = 1.0
key_obj = bpy.data.objects.new('Key_Snk', key_light)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (0.9, 0.7, 0.8)
key_obj.rotation_euler = (math.radians(50), 0, math.radians(120))

fill_light = bpy.data.lights.new('Fill_Snk', type='AREA')
fill_light.energy = 45
fill_light.size = 1.4
fill_obj = bpy.data.objects.new('Fill_Snk', fill_light)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (-0.8, 0.5, 0.5)
fill_obj.rotation_euler = (math.radians(55), 0, math.radians(-110))

rim_light = bpy.data.lights.new('Rim_Snk', type='SPOT')
rim_light.energy = 110
rim_light.spot_size = math.radians(55)
rim_obj = bpy.data.objects.new('Rim_Snk', rim_light)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (-0.4, -0.9, 0.9)
rim_obj.rotation_euler = (math.radians(-45), 0, 0)

out_png = os.path.join(out_dir, "test_render_sneaker_v13_front34.png")
scene = bpy.context.scene
scene.render.resolution_x = 1024
scene.render.resolution_y = 1024
scene.render.filepath = out_png
scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print('Rendered:', out_png)
