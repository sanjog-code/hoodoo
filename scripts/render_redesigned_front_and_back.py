import bpy
import math
import os

def render_test_views():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath="public/assets/models/hoodie_hero.glb")
    
    # 50mm Camera
    cam_data = bpy.data.cameras.new("TestCam")
    cam_data.lens = 50
    cam_obj = bpy.data.objects.new("TestCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    # Softbox lighting
    k_data = bpy.data.lights.new("KeyLight", 'AREA')
    k_data.energy = 380
    k_data.size = 2.0
    k_obj = bpy.data.objects.new("KeyLight", k_data)
    bpy.context.collection.objects.link(k_obj)
    k_obj.location = (1.5, -2.0, 1.4)
    k_obj.rotation_euler = (math.radians(55), math.radians(20), math.radians(-30))
    
    f_data = bpy.data.lights.new("FillLight", 'AREA')
    f_data.energy = 160
    f_obj = bpy.data.objects.new("FillLight", f_data)
    bpy.context.collection.objects.link(f_obj)
    f_obj.location = (-1.8, -1.8, 0.8)
    
    r_data = bpy.data.lights.new("RimLight", 'AREA')
    r_data.energy = 480
    r_obj = bpy.data.objects.new("RimLight", r_data)
    bpy.context.collection.objects.link(r_obj)
    r_obj.location = (0, 2.0, 1.2)
    r_obj.rotation_euler = (math.radians(-45), 0, math.radians(180))
    
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderEngineEEVEE_NEXT') else 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    # World Ambient Light so shadows are never 100% pitch black
    world = bpy.data.worlds.new("StudioWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs['Color'].default_value = (0.2, 0.2, 0.22, 1.0)
        bg.inputs['Strength'].default_value = 1.0
    
    # Front View
    cam_obj.location = (0, -2.4, -0.05)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    out_front = os.path.abspath("C:/Users/sanjo/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/render_redesign_front.png")
    bpy.context.scene.render.filepath = out_front
    bpy.ops.render.render(write_still=True)
    print(f"Rendered front: {out_front}")
    
    # Back View
    cam_obj.location = (0, 2.4, -0.05)
    cam_obj.rotation_euler = (math.radians(90), 0, math.radians(180))
    # Sun light pointing directly at back
    b_data = bpy.data.lights.new("BackSun", 'SUN')
    b_data.energy = 3.5
    b_obj = bpy.data.objects.new("BackSun", b_data)
    bpy.context.collection.objects.link(b_obj)
    b_obj.rotation_euler = (math.radians(45), 0, math.radians(180))
    out_back = os.path.abspath("C:/Users/sanjo/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/render_redesign_back.png")
    bpy.context.scene.render.filepath = out_back
    bpy.ops.render.render(write_still=True)
    print(f"Rendered back: {out_back}")

if __name__ == "__main__":
    render_test_views()
