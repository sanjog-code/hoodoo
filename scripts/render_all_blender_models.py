import bpy
import os
import sys
import math

def setup_studio_scene():
    # Delete default cube and lights
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    scene = bpy.context.scene
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    
    # Try EEVEE or CYCLES with High-Fidelity Depth
    scene.render.engine = 'BLENDER_EEVEE'
    if hasattr(scene, 'eevee'):
        try:
            scene.eevee.use_gtao = True
            scene.eevee.gtao_distance = 0.2
            scene.eevee.use_ssr = True
            scene.eevee.shadow_cube_size = '2048'
            scene.eevee.use_shadow_high_bit_depth = True
        except Exception:
            pass
            
    scene.view_settings.view_transform = 'Filmic'
    scene.view_settings.look = 'High Contrast'
    
    # Create Camera
    cam_data = bpy.data.cameras.new(name="StudioCamera")
    cam_data.lens = 70
    cam_data.clip_start = 0.01
    cam_data.clip_end = 100
    cam_obj = bpy.data.objects.new("StudioCamera", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Key Light
    key_data = bpy.data.lights.new(name="KeyLight", type='AREA')
    key_data.energy = 180
    key_data.color = (1.0, 0.98, 0.95)
    key_data.size = 1.2
    key_obj = bpy.data.objects.new("KeyLight", key_data)
    key_obj.location = (0.8, -1.0, 0.9)
    bpy.context.collection.objects.link(key_obj)
    
    # Fill Light
    fill_data = bpy.data.lights.new(name="FillLight", type='AREA')
    fill_data.energy = 60
    fill_data.color = (0.9, 0.95, 1.0)
    fill_data.size = 1.8
    fill_obj = bpy.data.objects.new("FillLight", fill_data)
    fill_obj.location = (-1.0, -0.8, 0.5)
    bpy.context.collection.objects.link(fill_obj)
    
    # Rim Light
    rim_data = bpy.data.lights.new(name="RimLight", type='SPOT')
    rim_data.energy = 280
    rim_data.color = (1.0, 1.0, 1.0)
    rim_data.spot_size = math.radians(65)
    rim_obj = bpy.data.objects.new("RimLight", rim_data)
    rim_obj.location = (0.0, 1.2, 1.1)
    bpy.context.collection.objects.link(rim_obj)
    
    return cam_obj, key_obj, fill_obj, rim_obj

def aim_at(obj, target=(0, 0, 0)):
    # Point object toward target
    import mathutils
    loc = obj.location
    direction = mathutils.Vector(target) - loc
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()

def render_model(glb_path, output_png, cam_pos, target_pos=(0, 0, 0)):
    cam_obj, key_obj, fill_obj, rim_obj = setup_studio_scene()
    
    # Import GLB
    bpy.ops.import_scene.gltf(filepath=glb_path)
    
    # Position camera
    cam_obj.location = cam_pos
    aim_at(cam_obj, target_pos)
    aim_at(key_obj, target_pos)
    aim_at(fill_obj, target_pos)
    aim_at(rim_obj, target_pos)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    bpy.context.scene.render.filepath = os.path.abspath(output_png)
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED: {output_png}")

if __name__ == '__main__':
    # Parse args
    argv = sys.argv
    if "--" in argv:
        args = argv[argv.index("--") + 1:]
    else:
        args = []
        
    if len(args) >= 2:
        glb = args[0]
        out = args[1]
        model_type = args[2] if len(args) > 2 else 'apparel'
        
        if model_type == 'sneaker':
            # Sneaker is around origin, length ~0.28m, height ~0.14m
            cam_pos = (0.24, -0.42, 0.22)
            target = (0, 0, 0.05)
        elif model_type == 'tee':
            # Tee is centered at z ~ 0.5-0.9m
            cam_pos = (0.45, -1.35, 0.65)
            target = (0, 0, 0.60)
        else: # hoodie
            cam_pos = (0.48, -1.45, 0.70)
            target = (0, 0, 0.62)
            
        render_model(glb, out, cam_pos, target)
    else:
        print("Usage: blender -b -P render_all_blender_models.py -- <glb_path> <out_png> [hoodie|tee|sneaker]")
