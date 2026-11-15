import sys
sys.path.append('.')
import os
import shutil
import math
import bpy
from scripts.bake_masterpiece_sneaker import create_masterpiece_skate_sneaker

out_dirs = [r"public/models", r"public/assets/models"]
for d in out_dirs:
    os.makedirs(d, exist_ok=True)

brain_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"

sneaker_configs = {
    'p9': {
        'name': "STREET LOW 'CHICANO BONE & GUM'",
        'profile': {
            'sole': (0.74, 0.48, 0.25, 1.0),       # Raw Gum Rubber
            'sole_roughness': 0.48,
            'vamp': (0.92, 0.90, 0.86, 1.0),       # Bone Tumbled Leather
            'vamp_roughness': 0.35,
            'quarter': (0.08, 0.045, 0.025, 1.0),  # Deep Chocolate Espresso Suede
            'quarter_roughness': 0.92,
            'silver': (0.92, 0.94, 0.98, 1.0),     # Polished Chrome Silver
            'silver_metal': 0.98,
            'silver_roughness': 0.10,
            'lace': (0.98, 0.98, 0.98, 1.0),       # Crisp White Fat Laces
            'lace_roughness': 0.65,
            'inner': (0.06, 0.06, 0.07, 1.0),      # Dark Velvet Padded Collar
            'inner_roughness': 0.95,
            'pedestal': (0.24, 0.25, 0.27, 1.0),   # Concrete Plinth
        }
    },
    'p10': {
        'name': "MIDNIGHT STEALTH RUNNER",
        'profile': {
            'sole': (0.12, 0.12, 0.13, 1.0),       # Charcoal Obsidian Rubber
            'sole_roughness': 0.55,
            'vamp': (0.09, 0.09, 0.10, 1.0),       # Stealth Noir Leather
            'vamp_roughness': 0.38,
            'quarter': (0.04, 0.04, 0.05, 1.0),    # Midnight Suede Overlays
            'quarter_roughness': 0.94,
            'silver': (0.60, 0.62, 0.66, 1.0),     # Gunmetal Chrome Wave
            'silver_metal': 0.92,
            'silver_roughness': 0.14,
            'lace': (0.11, 0.11, 0.12, 1.0),       # Charcoal Fat Laces
            'lace_roughness': 0.70,
            'inner': (0.03, 0.03, 0.04, 1.0),      # Stealth Lining
            'pedestal': (0.18, 0.18, 0.20, 1.0),   # Deep Charcoal Concrete
        }
    },
    'p11': {
        'name': "CHOPPER SUEDE SKATE LOW",
        'profile': {
            'sole': (0.72, 0.44, 0.20, 1.0),       # Golden Amber Gum
            'sole_roughness': 0.46,
            'vamp': (0.32, 0.20, 0.12, 1.0),       # Warm Saddle Tan Leather
            'vamp_roughness': 0.36,
            'quarter': (0.14, 0.08, 0.04, 1.0),    # Rich Tobacco Suede
            'quarter_roughness': 0.92,
            'silver': (0.92, 0.94, 0.98, 1.0),     # Polished Chrome Silver
            'silver_metal': 0.98,
            'silver_roughness': 0.10,
            'lace': (0.94, 0.91, 0.84, 1.0),       # Cream Fat Skate Laces
            'lace_roughness': 0.65,
            'inner': (0.08, 0.05, 0.03, 1.0),      # Espresso Velvet
            'pedestal': (0.28, 0.26, 0.24, 1.0),   # Warm Taupe Concrete
        }
    },
    'p12': {
        'name': "PAISLEY SWOOP RETRO LOW",
        'profile': {
            'sole': (0.88, 0.84, 0.76, 1.0),       # Vintage Sail Rubber
            'sole_roughness': 0.50,
            'vamp': (0.95, 0.94, 0.92, 1.0),       # Bright White Leather
            'vamp_roughness': 0.32,
            'quarter': (0.09, 0.11, 0.16, 1.0),    # Deep Navy Slate Suede
            'quarter_roughness': 0.90,
            'silver': (0.92, 0.94, 0.98, 1.0),     # Polished Chrome Silver
            'silver_metal': 0.98,
            'silver_roughness': 0.10,
            'lace': (0.92, 0.89, 0.82, 1.0),       # Sail Vintage Laces
            'lace_roughness': 0.65,
            'inner': (0.06, 0.07, 0.10, 1.0),      # Navy Velvet Collar
            'pedestal': (0.26, 0.27, 0.29, 1.0),   # Light Gray Concrete
        }
    },
    'p16': {
        'name': "EASTSIDE GUM SOLE RETRO",
        'profile': {
            'sole': (0.76, 0.46, 0.22, 1.0),       # Rich Amber Gum
            'sole_roughness': 0.48,
            'vamp': (0.08, 0.08, 0.09, 1.0),       # Pitch Black Leather
            'vamp_roughness': 0.35,
            'quarter': (0.04, 0.04, 0.05, 1.0),    # Noir Suede Overlays
            'quarter_roughness': 0.94,
            'silver': (0.92, 0.94, 0.98, 1.0),     # Polished Chrome Silver
            'silver_metal': 0.98,
            'silver_roughness': 0.10,
            'lace': (0.98, 0.98, 0.98, 1.0),       # High-Contrast White Fat Laces
            'lace_roughness': 0.65,
            'inner': (0.04, 0.04, 0.05, 1.0),      # Dark Velvet Collar
            'pedestal': (0.22, 0.23, 0.25, 1.0),   # Charcoal Concrete
        }
    },
}

def render_view(glb_path, out_png, cam_loc, focal=58.0):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb_path)
    
    world = bpy.data.worlds.new('Render_World')
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs['Color'].default_value = (0.08, 0.085, 0.095, 1.0)
        bg.inputs['Strength'].default_value = 0.85
        
    def add_light(name, ltype, loc, energy, color=(1,1,1), size=0.8):
        l_data = bpy.data.lights.new(name=name, type=ltype)
        l_data.energy = energy
        l_data.color = color
        if hasattr(l_data, 'size'):
            l_data.size = size
        l_obj = bpy.data.objects.new(name=name, object_data=l_data)
        l_obj.location = loc
        bpy.context.collection.objects.link(l_obj)
        return l_obj

    add_light("KeyLight", 'AREA', (-0.55, -0.60, 0.50), 16.0, (1.0, 0.96, 0.92), size=0.8)
    add_light("FillLight", 'AREA', (0.60, -0.50, 0.40), 8.0, (0.92, 0.96, 1.0), size=1.0)
    add_light("RimLight", 'SPOT', (0.0, 0.70, 0.60), 22.0, (1.0, 1.0, 1.0), size=0.4)
    add_light("TopSoft", 'AREA', (0.0, -0.05, 0.75), 8.0, (0.98, 0.98, 1.0), size=1.0)
    
    target = bpy.data.objects.new("Cam_Target", None)
    target.location = (0.0, 0.005, 0.035)
    bpy.context.collection.objects.link(target)

    cam_data = bpy.data.cameras.new(name="Render_Cam")
    cam_data.lens = focal
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
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.render.filepath = out_png
    
    scene.view_settings.view_transform = 'AgX' if 'AgX' in [c.identifier for c in scene.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'
    
    bpy.ops.render.render(write_still=True)
    print(f"[OK] Rendered: {out_png}")

print("=== BAKING ALL 5 MASTERPIECE ARTISAN SNEAKERS ===")
for pid, cfg in sneaker_configs.items():
    print(f"\n--- Baking {pid}: {cfg['name']} ---")
    model_name = f"kicks_{pid}.glb"
    dest_path = os.path.join(out_dirs[0], model_name)
    create_masterpiece_skate_sneaker(dest_path, color_profile=cfg['profile'])
    
    # Mirror to public/assets/models
    asset_dest = os.path.join(out_dirs[1], model_name)
    shutil.copyfile(dest_path, asset_dest)
    print(f"  Mirrored to: {asset_dest}")
    
    # Render Front-3/4 verification view
    render_front = os.path.join(brain_dir, f"test_render_sneaker_{pid}_front34.png")
    render_view(dest_path, render_front, cam_loc=(-0.36, -0.42, 0.20), focal=58.0)

    # Render Lateral profile verification view
    render_lateral = os.path.join(brain_dir, f"test_render_sneaker_{pid}_lateral.png")
    render_view(dest_path, render_lateral, cam_loc=(-0.52, 0.005, 0.08), focal=65.0)

print("\nALL 5 SNEAKERS BAKED, MIRRORED & RENDERED ACROSS MULTI-ANGLES!")
