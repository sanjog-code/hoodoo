import bpy
import bmesh
import math
import random
import os

# Set output path
output_dir = r"C:\Users\sanjo\Downloads\portfolio\public\assets\models"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "krunch_burger_4k.glb")

# Clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Helper: Create material
def create_pbr_material(name, base_color, roughness=0.4, specular=0.5, subsurface=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Roughness'].default_value = roughness
        if 'Specular IOR Level' in bsdf.inputs:
            bsdf.inputs['Specular IOR Level'].default_value = specular
        elif 'Specular' in bsdf.inputs:
            bsdf.inputs['Specular'].default_value = specular
        if 'Subsurface Weight' in bsdf.inputs:
            bsdf.inputs['Subsurface Weight'].default_value = subsurface
    return mat

# Materials
mat_bun_top = create_pbr_material("Mat_BunTop", (0.82, 0.46, 0.15, 1.0), roughness=0.35, specular=0.7)
mat_sesame = create_pbr_material("Mat_Sesame", (0.95, 0.90, 0.80, 1.0), roughness=0.3, specular=0.6)
mat_cucumber = create_pbr_material("Mat_Cucumber", (0.15, 0.65, 0.25, 1.0), roughness=0.25, specular=0.8, subsurface=0.2)
mat_tomato = create_pbr_material("Mat_Tomato", (0.85, 0.12, 0.10, 1.0), roughness=0.2, specular=0.9, subsurface=0.3)
mat_cheese = create_pbr_material("Mat_Cheese", (0.98, 0.68, 0.08, 1.0), roughness=0.35, specular=0.7, subsurface=0.2)
mat_patty = create_pbr_material("Mat_Patty", (0.22, 0.12, 0.08, 1.0), roughness=0.85, specular=0.3)
mat_bun_bottom = create_pbr_material("Mat_BunBottom", (0.78, 0.42, 0.14, 1.0), roughness=0.4, specular=0.6)

# 1. Top Bun
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=1.0, location=(0, 0, 0.75))
top_bun = bpy.context.active_object
top_bun.name = "TopBun"
top_bun.scale = (1.25, 1.25, 0.65)
bpy.ops.object.transform_apply(scale=True)
top_bun.data.materials.append(mat_bun_top)
bpy.ops.object.shade_smooth()

# Cut bottom of top bun flat
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(top_bun.data)
for v in bm.verts:
    if v.co.z < 0.65:
        v.co.z = 0.65
bmesh.update_edit_mesh(top_bun.data)
bpy.ops.object.mode_set(mode='OBJECT')

# 2. Sesame Seeds
random.seed(42)
for i in range(120):
    theta = random.uniform(0, 2 * math.pi)
    phi = random.uniform(0.2, 0.9)
    r = 1.25 * math.sin(phi)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    z = 0.65 + 0.65 * math.cos(phi) + 0.02
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=0.035, location=(x, y, z))
    seed = bpy.context.active_object
    seed.name = f"Sesame_{i}"
    seed.scale = (0.7, 1.6, 0.4)
    seed.rotation_euler = (random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3), theta + random.uniform(-0.5, 0.5))
    seed.data.materials.append(mat_sesame)
    bpy.ops.object.shade_smooth()

# 3. Cucumber / Pickle Slices
cucumber_positions = [
    (-0.45, 0.25, 0.52, 0.15),
    (0.42, 0.30, 0.53, -0.1),
    (-0.15, -0.45, 0.51, 0.2),
    (0.40, -0.35, 0.54, -0.18)
]
for idx, (cx, cy, cz, rot_z) in enumerate(cucumber_positions):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.45, depth=0.06, location=(cx, cy, cz))
    cuc = bpy.context.active_object
    cuc.name = f"Cucumber_{idx+1}"
    cuc.rotation_euler = (random.uniform(-0.08, 0.08), random.uniform(-0.08, 0.08), rot_z)
    cuc.data.materials.append(mat_cucumber)
    bpy.ops.object.shade_smooth()

# 4. Tomato Slices
tomato_positions = [
    (-0.35, -0.1, 0.38, 0.05),
    (0.35, 0.1, 0.37, -0.05)
]
for idx, (tx, ty, tz, rot_x) in enumerate(tomato_positions):
    bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=0.62, depth=0.11, location=(tx, ty, tz))
    tom = bpy.context.active_object
    tom.name = f"Tomato_{idx+1}"
    tom.rotation_euler = (rot_x, random.uniform(-0.05, 0.05), random.uniform(-0.2, 0.2))
    tom.data.materials.append(mat_tomato)
    bpy.ops.object.shade_smooth()

# 5. Melted Cheddar Cheese
bpy.ops.mesh.primitive_plane_add(size=1.9, location=(0, 0, 0.24))
cheese = bpy.context.active_object
cheese.name = "MeltedCheese"
cheese.rotation_euler = (0, 0, math.radians(45))
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=6)
bm = bmesh.from_edit_mesh(cheese.data)
# Droop corners
for v in bm.verts:
    dist = math.sqrt(v.co.x**2 + v.co.y**2)
    if dist > 0.8:
        v.co.z -= (dist - 0.8) * 0.45
bmesh.update_edit_mesh(cheese.data)
bpy.ops.object.mode_set(mode='OBJECT')

# Solidify cheese
mod_sol = cheese.modifiers.new(name="Solidify", type='SOLIDIFY')
mod_sol.thickness = 0.045
cheese.data.materials.append(mat_cheese)
bpy.ops.object.shade_smooth()

# 6. Smash Beef Patty
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1.28, depth=0.28, location=(0, 0, 0.05))
patty = bpy.context.active_object
patty.name = "SmashPatty"
# Add displacement / cragginess
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(patty.data)
for v in bm.verts:
    noise_val = (math.sin(v.co.x * 12) * math.cos(v.co.y * 12) + math.sin(v.co.z * 18)) * 0.035
    v.co.x += noise_val * 0.5
    v.co.y += noise_val * 0.5
    v.co.z += noise_val
bmesh.update_edit_mesh(patty.data)
bpy.ops.object.mode_set(mode='OBJECT')
patty.data.materials.append(mat_patty)
bpy.ops.object.shade_smooth()

# 7. Bottom Bun
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=1.22, depth=0.38, location=(0, 0, -0.26))
bottom_bun = bpy.context.active_object
bottom_bun.name = "BottomBun"
bottom_bun.scale = (1.0, 1.0, 0.9)
bpy.ops.object.transform_apply(scale=True)
bottom_bun.data.materials.append(mat_bun_bottom)
bpy.ops.object.shade_smooth()

# Select all objects for export
bpy.ops.object.select_all(action='SELECT')

# Export GLTF
print(f"Exporting 3D Burger to {output_path}...")
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    use_selection=True,
    export_apply=True
)
print("GLB export complete!")
