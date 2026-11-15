import bpy
import math
import os

brain_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
glb_path = r"public/models/test_artisan_sneaker.glb"

def setup_scene(cam_loc, out_img, focal_length=60.0):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb_path)
    
    # World dark studio backdrop
    world = bpy.data.worlds.new('Render_World')
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs['Color'].default_value = (0.08, 0.085, 0.095, 1.0)
        bg.inputs['Strength'].default_value = 0.85
        
    def add_light(name, ltype, loc, energy, color=(1,1,1), size=0.5):
        l_data = bpy.data.lights.new(name=name, type=ltype)
        l_data.energy = energy
        l_data.color = color
        if hasattr(l_data, 'size'):
            l_data.size = size
        l_obj = bpy.data.objects.new(name=name, object_data=l_data)
        l_obj.location = loc
        bpy.context.collection.objects.link(l_obj)
        return l_obj

    # Studio 4-point softbox lighting rig with realistic studio wattages
    add_light("KeyLight", 'AREA', (-0.55, -0.60, 0.50), 16.0, (1.0, 0.96, 0.92), size=0.8)
    add_light("FillLight", 'AREA', (0.60, -0.50, 0.40), 8.0, (0.92, 0.96, 1.0), size=1.0)
    add_light("RimLight", 'SPOT', (0.0, 0.70, 0.60), 22.0, (1.0, 1.0, 1.0), size=0.4)
    add_light("TopSoft", 'AREA', (0.0, -0.05, 0.75), 8.0, (0.98, 0.98, 1.0), size=1.0)
    
    # Target Empty at center of sneaker footbed
    target = bpy.data.objects.new("Cam_Target", None)
    target.location = (0.0, 0.005, 0.035)
    bpy.context.collection.objects.link(target)

    # Camera with Track-To Constraint
    cam_data = bpy.data.cameras.new(name="Render_Cam")
    cam_data.lens = focal_length
    cam_obj = bpy.data.objects.new(name="Render_Cam", object_data=cam_data)
    cam_obj.location = cam_loc
    
    tt = cam_obj.constraints.new(type='TRACK_TO')
    tt.target = target
    tt.track_axis = 'TRACK_NEGATIVE_Z'
    tt.up_axis = 'UP_Y'
    
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.render.filepath = out_img
    
    # Rich photographic tone mapping
    scene.view_settings.view_transform = 'AgX' if 'AgX' in [c.identifier for c in scene.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'
    
    bpy.ops.render.render(write_still=True)
    print(f"[OK] Rendered: {out_img}")

# 1. Front-3/4 View: Camera at front-lateral angle looking down at toe dome, sole rim, laces, wave logo
setup_scene(
    cam_loc=(-0.36, -0.42, 0.20),
    out_img=os.path.join(brain_dir, "test_modular_sneaker_front34.png"),
    focal_length=58.0
)

# 2. Lateral Profile View: Looking directly at side profile, rubber cupsole sidewall, and 3D wave emblem
setup_scene(
    cam_loc=(-0.52, 0.005, 0.08),
    out_img=os.path.join(brain_dir, "test_modular_sneaker_lateral.png"),
    focal_length=65.0
)

# 3. Top-Down Toe & Laces View: Looking down at vamp perforations, fat laces, tongue brand patch
setup_scene(
    cam_loc=(-0.06, -0.26, 0.44),
    out_img=os.path.join(brain_dir, "test_modular_sneaker_topdown.png"),
    focal_length=55.0
)
