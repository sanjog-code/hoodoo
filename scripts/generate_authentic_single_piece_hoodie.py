import bpy
import bmesh
import math
import os

hoodie_configs = [
    {
        "name": "WESTSIDE LOWRIDER AIRBRUSH HOODIE",
        "tex_path": "public/assets/models/textures/tex_hero.png",
        "out_file": "public/assets/models/hoodie_hero.glb"
    },
    {
        "name": "WESTSIDE PAISLEY HEAVY HOODIE",
        "tex_path": "public/assets/models/textures/tex_p1.png",
        "out_file": "public/assets/models/hoodie_p1.glb"
    },
    {
        "name": "'64 LOWRIDER PINSTRIPE HOODIE",
        "tex_path": "public/assets/models/textures/tex_p2.png",
        "out_file": "public/assets/models/hoodie_p2.glb"
    },
    {
        "name": "COMPTON BLACKLETTER HOODIE",
        "tex_path": "public/assets/models/textures/tex_p3.png",
        "out_file": "public/assets/models/hoodie_p3.glb"
    },
    {
        "name": "VENICE BOARDWALK CLAY HOODIE",
        "tex_path": "public/assets/models/textures/tex_p4.png",
        "out_file": "public/assets/models/hoodie_p4.glb"
    },
    {
        "name": "MIDNIGHT RIDER GOTHIC HOODIE",
        "tex_path": "public/assets/models/textures/tex_p13.png",
        "out_file": "public/assets/models/hoodie_p13.glb"
    }
]

def create_single_piece_hoodie():
    # Reset
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # 1. Create Base Continuous Torso Mesh
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.35, depth=0.68, location=(0, 0, 0.44))
    hoodie = bpy.context.active_object
    hoodie.name = "Hoodie_Fabric_Body"
    hoodie.scale = (1.0, 0.52, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    bm = bmesh.new()
    bm.from_mesh(hoodie.data)

    # Deform cylinder into authentic streetwear boxy hoodie silhouette
    # Z ranges from 0.10 to 0.78
    for v in bm.verts:
        z = v.co.z
        norm_z = (z - 0.10) / 0.68 # 0 at bottom hem, 1 at shoulders
        
        # Bottom Ribbed Hem (z < 0.20)
        if norm_z < 0.15:
            v.co.x *= 0.90
            v.co.y *= 0.90
        # Kangaroo Pocket Bulge on front (0.22 < norm_z < 0.55 and y > 0.08)
        elif 0.20 <= norm_z <= 0.55 and v.co.y > 0.06:
            bulge = math.sin((norm_z - 0.20) / 0.35 * math.pi) * 0.048
            v.co.y += bulge
        # Dropped boxy shoulders (norm_z > 0.70)
        elif norm_z > 0.70:
            v.co.x *= 1.18

    # Extrude Sleeves seamlessly from side vertices
    # Find armscye region: x > 0.30 or x < -0.30, z between 0.50 and 0.72
    # We will bridge and extrude dropped sleeves
    bm.to_mesh(hoodie.data)
    bm.free()

    # Apply Subdivision for smooth organic cotton drape
    sub = hoodie.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 1
    bpy.ops.object.modifier_apply(modifier="Subsurf")

    # 2. Add Volumetric Hood (Sculpted onto collar)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.22, location=(0, -0.04, 0.94))
    hood = bpy.context.active_object
    hood.scale = (0.90, 1.15, 1.20)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Carve face opening
    bm_h = bmesh.new()
    bm_h.from_mesh(hood.data)
    faces_to_del = [
        f for f in bm_h.faces
        if f.calc_center_median().y > 0.03 and 0.76 < f.calc_center_median().z < 1.06
    ]
    bmesh.ops.delete(bm_h, geom=faces_to_del, context='FACES')
    for v in bm_h.verts:
        if v.co.z < 0.82:
            # Flare to collar
            v.co.x *= 1.25
            v.co.y *= 1.20
    bm_h.to_mesh(hood.data)
    bm_h.free()

    sol = hood.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.015
    bpy.ops.object.modifier_apply(modifier="Solidify")

    # 3. Add Dropped Sleeves
    sleeve_objs = []
    for side, x_mult in [("L", 1.0), ("R", -1.0)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=18, radius=0.12, depth=0.55, location=(x_mult * 0.48, 0.01, 0.46))
        sleeve = bpy.context.active_object
        sleeve.rotation_euler = (math.radians(-6), x_mult * math.radians(34), 0)
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        
        # Taper wrist cuff
        bm_s = bmesh.new()
        bm_s.from_mesh(sleeve.data)
        for v in bm_s.verts:
            if v.co.z < 0.28:
                v.co.x = (v.co.x - x_mult * 0.48) * 0.75 + x_mult * 0.48
                v.co.y *= 0.75
        bm_s.to_mesh(sleeve.data)
        bm_s.free()
        sleeve_objs.append(sleeve)

    # 4. Join Torso, Hood, and Sleeves into ONE SINGLE-PIECE CONTINUOUS HOODIE MESH
    bpy.ops.object.select_all(action='DESELECT')
    hoodie.select_set(True)
    hood.select_set(True)
    for s in sleeve_objs:
        s.select_set(True)
    bpy.context.view_layer.objects.active = hoodie
    bpy.ops.object.join()
    single_piece_hoodie = bpy.context.active_object
    single_piece_hoodie.name = "Hoodie_Fabric_Body"

    # Merge close boundary vertices between collar and hood to ensure watertight manifold
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    # Remesh / Weld to create continuous organic manifold cloth
    bpy.ops.mesh.remove_doubles(threshold=0.03)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Apply Subdivision for soft organic cloth curvature
    sub2 = single_piece_hoodie.modifiers.new("Subsurf", "SUBSURF")
    sub2.levels = 1
    bpy.ops.object.modifier_apply(modifier="Subsurf")

    # 5. ATELIER MANNEQUIN STAND (Inside the hoodie)
    # 5a. Neck bust visible at collar opening
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.068, depth=0.18, location=(0, -0.01, 0.88))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Bust"

    # 5b. Metallic Crown Finial
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.072, depth=0.02, location=(0, -0.01, 0.97))
    m_cap = bpy.context.active_object
    m_cap.name = "Mannequin_Cap"

    # 5c. Titanium Stand Pole
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.02, depth=0.75, location=(0, 0, -0.20))
    m_pole = bpy.context.active_object
    m_pole.name = "Mannequin_Pole"

    # 5d. Ground Museum Base Pedestal (Z = -0.58)
    bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.34, depth=0.03, location=(0, 0, -0.56))
    m_base = bpy.context.active_object
    m_base.name = "Mannequin_Base"

    # Join Mannequin parts into hardware object
    bpy.ops.object.select_all(action='DESELECT')
    for m in [m_neck, m_cap, m_pole, m_base]:
        m.select_set(True)
    bpy.context.view_layer.objects.active = m_neck
    bpy.ops.object.join()
    mannequin_obj = bpy.context.active_object
    mannequin_obj.name = "Model_Mannequin_Stand"

    # 6. Smooth Shading on all surfaces
    for obj in [single_piece_hoodie, mannequin_obj]:
        for poly in obj.data.polygons:
            poly.use_smooth = True

    # 7. Unpack & Generate Direct Conformal UV Mapping for Hoodie
    bpy.ops.object.select_all(action='DESELECT')
    single_piece_hoodie.select_set(True)
    bpy.context.view_layer.objects.active = single_piece_hoodie
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    # Smart project or cylinder projection so front faces map cleanly to center UV
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Center scene to origin
    bpy.ops.object.select_all(action='SELECT')
    for obj in [single_piece_hoodie, mannequin_obj]:
        obj.location.z -= 0.44
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

    return single_piece_hoodie, mannequin_obj

def setup_and_export_all():
    for conf in hoodie_configs:
        print(f"Building single-piece hoodie for: {conf['name']}...")
        hoodie_obj, mannequin_obj = create_single_piece_hoodie()

        # Create Fabric Material with Direct Baked Texture
        mat_fabric = bpy.data.materials.new(name="Mat_Hoodie_Fabric")
        nodes_f = mat_fabric.node_tree.nodes
        bsdf_f = nodes_f.get("Principled BSDF")
        
        tex_abs = os.path.abspath(conf["tex_path"])
        if os.path.exists(tex_abs) and bsdf_f:
            tex_node = nodes_f.new("ShaderNodeTexImage")
            tex_node.image = bpy.data.images.load(tex_abs)
            mat_fabric.node_tree.links.new(tex_node.outputs['Color'], bsdf_f.inputs['Base Color'])
            bsdf_f.inputs['Roughness'].default_value = 0.88
        hoodie_obj.data.materials.append(mat_fabric)

        # Create Mannequin Material
        mat_mannequin = bpy.data.materials.new(name="Mat_Mannequin")
        bsdf_m = mat_mannequin.node_tree.nodes.get("Principled BSDF")
        if bsdf_m:
            bsdf_m.inputs['Base Color'].default_value = (0.08, 0.08, 0.09, 1.0)
            bsdf_m.inputs['Metallic'].default_value = 0.85
            bsdf_m.inputs['Roughness'].default_value = 0.25
        mannequin_obj.data.materials.append(mat_mannequin)

        # Export GLB
        out_abs = os.path.abspath(conf["out_file"])
        bpy.ops.export_scene.gltf(
            filepath=out_abs,
            export_format='GLB',
            use_selection=False,
            export_apply=True,
            export_yup=True
        )
        print(f"Exported Single-Piece 3D Hoodie: {out_abs}")

if __name__ == "__main__":
    setup_and_export_all()
