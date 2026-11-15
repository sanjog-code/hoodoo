import bpy
import bmesh
import math
import os

hoodie_definitions = [
    {
        "id": "wc-hero-hoodie",
        "name": "WESTSIDE LOWRIDER AIRBRUSH HOODIE",
        "front_img": "public/assets/collection/hero_asphalt.png",
        "back_img": "public/assets/collection/hero_asphalt_back.png",
        "base_color": (0.09, 0.09, 0.10, 1.0),
        "filename": "hoodie_hero.glb"
    },
    {
        "id": "wc-cat-01",
        "name": "WESTSIDE PAISLEY HEAVY HOODIE",
        "front_img": "public/assets/collection/p1_black.png",
        "back_img": "public/assets/collection/p1_black_back.png",
        "base_color": (0.04, 0.04, 0.04, 1.0),
        "filename": "hoodie_p1.glb"
    },
    {
        "id": "wc-cat-02",
        "name": "'64 LOWRIDER PINSTRIPE HOODIE",
        "front_img": "public/assets/collection/p2_cocoa.png",
        "back_img": "public/assets/collection/p2_cocoa_back.png",
        "base_color": (0.24, 0.17, 0.14, 1.0),
        "filename": "hoodie_p2.glb"
    },
    {
        "id": "wc-cat-03",
        "name": "COMPTON BLACKLETTER HOODIE",
        "front_img": "public/assets/collection/p3_black.png",
        "back_img": "public/assets/collection/p3_black_back.png",
        "base_color": (0.05, 0.05, 0.05, 1.0),
        "filename": "hoodie_p3.glb"
    },
    {
        "id": "wc-cat-04",
        "name": "VENICE BOARDWALK CLAY HOODIE",
        "front_img": "public/assets/collection/p4_sand.png",
        "back_img": "public/assets/collection/p4_sand_back.png",
        "base_color": (0.66, 0.60, 0.53, 1.0),
        "filename": "hoodie_p4.glb"
    },
    {
        "id": "wc-cat-13",
        "name": "MIDNIGHT RIDER GOTHIC HOODIE",
        "front_img": "public/assets/collection/p13_asphalt.png",
        "back_img": "public/assets/collection/p13_asphalt_back.png",
        "base_color": (0.15, 0.15, 0.16, 1.0),
        "filename": "hoodie_p13.glb"
    }
]

def build_mannequin_and_hoodie():
    # 1. ATELIER MANNEQUIN (Sculpted Headless Museum Mannequin)
    # 1a. Mannequin Neck
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.075, depth=0.22, location=(0, -0.01, 1.48))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Neck"
    
    # Taper neck slightly upward
    bm = bmesh.new()
    bm.from_mesh(m_neck.data)
    for v in bm.verts:
        if v.co.z > 1.48:
            v.co.x *= 0.90
            v.co.y *= 0.90
    bm.to_mesh(m_neck.data)
    bm.free()

    # 1b. Mannequin Crown Cap (Luxury brushed chrome top disc)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.078, depth=0.02, location=(0, -0.01, 1.59))
    m_cap = bpy.context.active_object
    m_cap.name = "Mannequin_Crown_Cap"

    # 1c. Mannequin Stand Pole (Brushed titanium column descending through bottom of hoodie)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.024, depth=0.75, location=(0, 0, 0.35))
    m_pole = bpy.context.active_object
    m_pole.name = "Mannequin_Stand_Pole"

    # 1d. Mannequin Studio Pedestal Base (Heavy round museum-grade bevel base)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.36, depth=0.035, location=(0, 0, 0.018))
    m_base = bpy.context.active_object
    m_base.name = "Mannequin_Base_Pedestal"
    
    mod_b = m_base.modifiers.new("Bevel", "BEVEL")
    mod_b.width = 0.008
    mod_b.segments = 3
    bpy.ops.object.modifier_apply(modifier="Bevel")

    # 2. OVERSIZED 500GSM STREETWEAR HOODIE DRAPED ON MANNEQUIN
    # 2a. Torso Body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.98))
    torso = bpy.context.active_object
    torso.name = "Hoodie_Torso"
    torso.scale = (0.37, 0.18, 0.44)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    mod_sub = torso.modifiers.new("Subsurf", "SUBSURF")
    mod_sub.levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    # Shape torso with realistic heavyweight cotton slouch & drape
    bm = bmesh.new()
    bm.from_mesh(torso.data)
    for v in bm.verts:
        z_rel = (v.co.z - 0.54) / 0.88 # 0 at bottom, 1 at collar
        if z_rel > 0.72:
            # Dropped shoulder width
            v.co.x *= 1.16
        elif z_rel < 0.22:
            # Bottom hem gather
            v.co.x *= 0.92
            v.co.y *= 0.92
        # Front chest fullness over mannequin
        if v.co.y > 0 and 0.35 < z_rel < 0.85:
            v.co.y += math.sin(z_rel * math.pi) * 0.045
    bm.to_mesh(torso.data)
    bm.free()

    # 2b. Bottom Ribbed Hem (Gathering around waist above stand)
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.33, depth=0.08, location=(0, 0, 0.52))
    hem = bpy.context.active_object
    hem.name = "Hoodie_Rib_Hem"
    hem.scale = (1.0, 0.52, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # 2c. Kangaroo Front Pocket
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.18, 0.78))
    pocket = bpy.context.active_object
    pocket.name = "Hoodie_Kangaroo_Pocket"
    pocket.scale = (0.24, 0.035, 0.14)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bm = bmesh.new()
    bm.from_mesh(pocket.data)
    for v in bm.verts:
        if v.co.z > 0.84:
            v.co.x *= 0.78
        if v.co.y > 0.19:
            v.co.y += (1.0 - abs(v.co.x)/0.25) * 0.02
    bm.to_mesh(pocket.data)
    bm.free()
    
    pock_bevel = pocket.modifiers.new("Bevel", "BEVEL")
    pock_bevel.width = 0.012
    pock_bevel.segments = 3
    bpy.ops.object.modifier_apply(modifier="Bevel")

    # 2d. Volumetric Sculpted Hood (Resting naturally on mannequin neck/shoulders)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=26, ring_count=20, radius=0.22, location=(0, -0.05, 1.48))
    hood = bpy.context.active_object
    hood.name = "Hoodie_Hood"
    hood.scale = (0.92, 1.18, 1.25)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bm = bmesh.new()
    bm.from_mesh(hood.data)
    faces_to_delete = [
        f for f in bm.faces
        if f.calc_center_median().y > 0.02 and 1.28 < f.calc_center_median().z < 1.62
    ]
    bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
    
    for v in bm.verts:
        if v.co.z < 1.36:
            # Flare to rest on mannequin shoulder line
            v.co.x *= 1.20
            v.co.y *= 1.16
        elif v.co.z > 1.60:
            v.co.y -= 0.04
    bm.to_mesh(hood.data)
    bm.free()

    hood_sol = hood.modifiers.new("Solidify", "SOLIDIFY")
    hood_sol.thickness = 0.016
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    hood_sub = hood.modifiers.new("Subsurf", "SUBSURF")
    hood_sub.levels = 1
    bpy.ops.object.modifier_apply(modifier="Subsurf")

    # 2e. Dropped Oversized Sleeves
    for side, x_mult in [("L", 1.0), ("R", -1.0)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.13, depth=0.34, location=(x_mult * 0.44, 0, 1.12))
        arm = bpy.context.active_object
        arm.name = f"Hoodie_Arm_Upper_{side}"
        arm.rotation_euler = (0, x_mult * math.radians(38), math.radians(8))
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.11, depth=0.32, location=(x_mult * 0.58, 0.02, 0.88))
        forearm = bpy.context.active_object
        forearm.name = f"Hoodie_Arm_Lower_{side}"
        forearm.rotation_euler = (math.radians(-6), x_mult * math.radians(24), 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.088, depth=0.07, location=(x_mult * 0.67, 0.03, 0.73))
        cuff = bpy.context.active_object
        cuff.name = f"Hoodie_Cuff_{side}"
        cuff.rotation_euler = (math.radians(-6), x_mult * math.radians(24), 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

    # 2f. Hanging Drawstrings & Metal Aglets
    aglet_objects = []
    string_objects = []
    for side, x_mult in [("L", 1.0), ("R", -1.0)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.0055, depth=0.22, location=(x_mult * 0.065, 0.17, 1.20))
        string = bpy.context.active_object
        string.name = f"Hoodie_Drawstring_{side}"
        string.rotation_euler = (math.radians(12), x_mult * math.radians(5), 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        string_objects.append(string)
        
        bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.007, depth=0.03, location=(x_mult * 0.075, 0.19, 1.08))
        aglet = bpy.context.active_object
        aglet.name = f"Hoodie_Aglet_{side}"
        aglet.rotation_euler = (math.radians(12), x_mult * math.radians(5), 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        aglet_objects.append(aglet)

    # 3. HIGH-RESOLUTION FRONT & BACK GRAPHIC DECAL PLANES
    # 3a. Front Chest Decal Plane
    bpy.ops.mesh.primitive_plane_add(size=0.38, location=(0, 0.185, 1.04))
    front_decal = bpy.context.active_object
    front_decal.name = "Hoodie_Front_Graphic"
    front_decal.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bm = bmesh.new()
    bm.from_mesh(front_decal.data)
    for v in bm.verts:
        v.co.y += (1.0 - (v.co.x / 0.19)**2) * 0.016
    bm.to_mesh(front_decal.data)
    bm.free()

    # 3b. Back Decal Plane
    bpy.ops.mesh.primitive_plane_add(size=0.40, location=(0, -0.175, 1.05))
    back_decal = bpy.context.active_object
    back_decal.name = "Hoodie_Back_Graphic"
    back_decal.rotation_euler = (math.radians(-90), 0, math.radians(180))
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bm = bmesh.new()
    bm.from_mesh(back_decal.data)
    for v in bm.verts:
        v.co.y -= (1.0 - (v.co.x / 0.20)**2) * 0.014
    bm.to_mesh(back_decal.data)
    bm.free()

    # UV Unwrap Decals
    for decal in [front_decal, back_decal]:
        bpy.ops.object.select_all(action='DESELECT')
        decal.select_set(True)
        bpy.context.view_layer.objects.active = decal
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.0)
        bpy.ops.object.mode_set(mode='OBJECT')

    # 4. JOIN SUB-ASSEMBLIES BY MATERIAL
    # 4a. Mannequin Stand & Hardware
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [m_cap, m_pole, m_base] + aglet_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = m_cap
    bpy.ops.object.join()
    hardware_obj = bpy.context.active_object
    hardware_obj.name = "Model_Hardware_Titanium"

    # 4b. Mannequin Body (Neck)
    bpy.ops.object.select_all(action='DESELECT')
    m_neck.select_set(True)
    bpy.context.view_layer.objects.active = m_neck
    mannequin_body = m_neck
    mannequin_body.name = "Model_Mannequin_Obsidian"

    # 4c. Hoodie Fabric Body
    bpy.ops.object.select_all(action='SELECT')
    hardware_obj.select_set(False)
    mannequin_body.select_set(False)
    front_decal.select_set(False)
    back_decal.select_set(False)
    torso_obj = bpy.data.objects.get("Hoodie_Torso")
    bpy.context.view_layer.objects.active = torso_obj
    bpy.ops.object.join()
    body_obj = bpy.context.active_object
    body_obj.name = "Hoodie_Fabric_Body"

    # Smooth shading across all meshes
    for obj in [body_obj, front_decal, back_decal, hardware_obj, mannequin_body]:
        for poly in obj.data.polygons:
            poly.use_smooth = True

    # Center origin to ground base (Z = 0 is the pedestal floor)
    # The base pedestal sits at Z = 0.018, so we can shift Z down by ~0.95 or keep Z=0 as floor
    # Keeping Z=0 at base pedestal gives a grounded museum stand!
    bpy.ops.object.select_all(action='SELECT')
    for obj in [body_obj, front_decal, back_decal, hardware_obj, mannequin_body]:
        obj.location.z -= 0.95
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

    return body_obj, front_decal, back_decal, hardware_obj, mannequin_body

def setup_materials_and_export(hoodie_def):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    body_obj, front_decal, back_decal, hardware_obj, mannequin_body = build_mannequin_and_hoodie()

    # 1. Hoodie Fabric Material
    mat_fabric = bpy.data.materials.new(name="Mat_Hoodie_Fabric")
    bsdf_f = mat_fabric.node_tree.nodes.get("Principled BSDF")
    if bsdf_f:
        bsdf_f.inputs['Base Color'].default_value = hoodie_def["base_color"]
        bsdf_f.inputs['Roughness'].default_value = 0.88
    body_obj.data.materials.append(mat_fabric)

    # 2. Front Graphic Material with Image Texture
    mat_front = bpy.data.materials.new(name="Mat_Front_Graphic")
    mat_front.blend_method = 'BLEND'
    nodes_fg = mat_front.node_tree.nodes
    bsdf_fg = nodes_fg.get("Principled BSDF")
    front_img_path = os.path.abspath(hoodie_def["front_img"])
    if os.path.exists(front_img_path) and bsdf_fg:
        img_node = nodes_fg.new("ShaderNodeTexImage")
        img_node.image = bpy.data.images.load(front_img_path)
        mat_front.node_tree.links.new(img_node.outputs['Color'], bsdf_fg.inputs['Base Color'])
        mat_front.node_tree.links.new(img_node.outputs['Alpha'], bsdf_fg.inputs['Alpha'])
        bsdf_fg.inputs['Roughness'].default_value = 0.65
    front_decal.data.materials.append(mat_front)

    # 3. Back Graphic Material with Image Texture
    mat_back = bpy.data.materials.new(name="Mat_Back_Graphic")
    mat_back.blend_method = 'BLEND'
    nodes_bg = mat_back.node_tree.nodes
    bsdf_bg = nodes_bg.get("Principled BSDF")
    back_img_path = os.path.abspath(hoodie_def["back_img"])
    if os.path.exists(back_img_path) and bsdf_bg:
        img_node_b = nodes_bg.new("ShaderNodeTexImage")
        img_node_b.image = bpy.data.images.load(back_img_path)
        mat_back.node_tree.links.new(img_node_b.outputs['Color'], bsdf_bg.inputs['Base Color'])
        mat_back.node_tree.links.new(img_node_b.outputs['Alpha'], bsdf_bg.inputs['Alpha'])
        bsdf_bg.inputs['Roughness'].default_value = 0.65
    back_decal.data.materials.append(mat_back)

    # 4. Hardware Titanium / Chrome (Aglets, Crown Cap, Stand Pole, Base)
    mat_chrome = bpy.data.materials.new(name="Mat_Hardware_Titanium")
    bsdf_c = mat_chrome.node_tree.nodes.get("Principled BSDF")
    if bsdf_c:
        bsdf_c.inputs['Base Color'].default_value = (0.85, 0.85, 0.90, 1.0)
        bsdf_c.inputs['Metallic'].default_value = 0.95
        bsdf_c.inputs['Roughness'].default_value = 0.16
    hardware_obj.data.materials.append(mat_chrome)

    # 5. Luxury Obsidian Atelier Mannequin Body
    mat_mannequin = bpy.data.materials.new(name="Mat_Mannequin_Obsidian")
    bsdf_m = mat_mannequin.node_tree.nodes.get("Principled BSDF")
    if bsdf_m:
        bsdf_m.inputs['Base Color'].default_value = (0.06, 0.06, 0.07, 1.0)
        bsdf_m.inputs['Roughness'].default_value = 0.32
    mannequin_body.data.materials.append(mat_mannequin)

    # Export to GLB
    out_dir = "public/assets/models"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.abspath(os.path.join(out_dir, hoodie_def["filename"]))
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True
    )
    print(f"Generated Mannequin 3D Model: {hoodie_def['name']} -> {out_path}")

def run_all():
    for h in hoodie_definitions:
        print(f"Baking Mannequin 3D Model for: {h['name']}...")
        setup_materials_and_export(h)

if __name__ == "__main__":
    run_all()
