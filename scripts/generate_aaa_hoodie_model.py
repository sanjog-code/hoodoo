import bpy
import bmesh
import math
import os

def build_production_aaa_hoodie():
    # Reset scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 1. Torso
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.95))
    torso = bpy.context.active_object
    torso.name = "Hoodie_Torso"
    torso.scale = (0.36, 0.17, 0.42)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    mod_sub = torso.modifiers.new("Subsurf", "SUBSURF")
    mod_sub.levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    bm = bmesh.new()
    bm.from_mesh(torso.data)
    for v in bm.verts:
        z_rel = (v.co.z - 0.53) / 0.84
        if z_rel > 0.7:
            v.co.x *= 1.15
        elif z_rel < 0.2:
            v.co.x *= 0.92
            v.co.y *= 0.92
        if v.co.y > 0 and 0.4 < z_rel < 0.8:
            v.co.y += math.sin(z_rel * math.pi) * 0.04
    bm.to_mesh(torso.data)
    bm.free()

    # 2. Rib Hem
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.33, depth=0.08, location=(0, 0, 0.50))
    hem = bpy.context.active_object
    hem.name = "Hoodie_Rib_Hem"
    hem.scale = (1.0, 0.52, 1.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # 3. Kangaroo Pocket
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.17, 0.76))
    pocket = bpy.context.active_object
    pocket.name = "Hoodie_Kangaroo_Pocket"
    pocket.scale = (0.24, 0.035, 0.14)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bm = bmesh.new()
    bm.from_mesh(pocket.data)
    for v in bm.verts:
        if v.co.z > 0.82:
            v.co.x *= 0.78
        if v.co.y > 0.18:
            v.co.y += (1.0 - abs(v.co.x)/0.25) * 0.02
    bm.to_mesh(pocket.data)
    bm.free()
    
    pock_bevel = pocket.modifiers.new("Bevel", "BEVEL")
    pock_bevel.width = 0.012
    pock_bevel.segments = 3
    bpy.ops.object.modifier_apply(modifier="Bevel")

    # 4. Volumetric Hood
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=18, radius=0.22, location=(0, -0.04, 1.48))
    hood = bpy.context.active_object
    hood.name = "Hoodie_Hood"
    hood.scale = (0.88, 1.15, 1.25)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bm = bmesh.new()
    bm.from_mesh(hood.data)
    faces_to_delete = [
        f for f in bm.faces
        if f.calc_center_median().y > 0.04 and 1.30 < f.calc_center_median().z < 1.62
    ]
    bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')
    
    for v in bm.verts:
        if v.co.z < 1.36:
            v.co.x *= 1.18
            v.co.y *= 1.15
        elif v.co.z > 1.60:
            v.co.y -= 0.03
    bm.to_mesh(hood.data)
    bm.free()

    hood_sol = hood.modifiers.new("Solidify", "SOLIDIFY")
    hood_sol.thickness = 0.016
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    hood_sub = hood.modifiers.new("Subsurf", "SUBSURF")
    hood_sub.levels = 1
    bpy.ops.object.modifier_apply(modifier="Subsurf")

    # 5. Dropped Sleeves
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

    # 6. Hanging Drawstrings & Metal Aglets
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

    # 7. Front Chest Graphic Decal Plane (Subdivided & Curvature-conformed)
    bpy.ops.mesh.primitive_plane_add(size=0.38, location=(0, 0.175, 1.02))
    front_decal = bpy.context.active_object
    front_decal.name = "Hoodie_Front_Graphic"
    front_decal.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Subdivide & curve front decal slightly over chest
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bm = bmesh.new()
    bm.from_mesh(front_decal.data)
    for v in bm.verts:
        # Subtle convex curve
        v.co.y += (1.0 - (v.co.x / 0.19)**2) * 0.015
    bm.to_mesh(front_decal.data)
    bm.free()

    # 8. Back Graphic Decal Plane
    bpy.ops.mesh.primitive_plane_add(size=0.40, location=(0, -0.165, 1.04))
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
        v.co.y -= (1.0 - (v.co.x / 0.20)**2) * 0.012
    bm.to_mesh(back_decal.data)
    bm.free()

    # UV Unwrap Decals strictly 0 to 1
    for decal in [front_decal, back_decal]:
        bpy.ops.object.select_all(action='DESELECT')
        decal.select_set(True)
        bpy.context.view_layer.objects.active = decal
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.0)
        bpy.ops.object.mode_set(mode='OBJECT')

    # Join Hardware (Aglets)
    bpy.ops.object.select_all(action='DESELECT')
    for a in aglet_objects:
        a.select_set(True)
    bpy.context.view_layer.objects.active = aglet_objects[0]
    bpy.ops.object.join()
    hardware_obj = bpy.context.active_object
    hardware_obj.name = "Hoodie_Hardware_Aglets"

    # Join Body Parts
    bpy.ops.object.select_all(action='SELECT')
    hardware_obj.select_set(False)
    front_decal.select_set(False)
    back_decal.select_set(False)
    torso_obj = bpy.data.objects.get("Hoodie_Torso")
    bpy.context.view_layer.objects.active = torso_obj
    bpy.ops.object.join()
    body_obj = bpy.context.active_object
    body_obj.name = "Hoodie_Fabric_Body"

    # Assign Materials
    mat_fabric = bpy.data.materials.new(name="Mat_Hoodie_Fabric")
    bsdf_f = mat_fabric.node_tree.nodes.get("Principled BSDF")
    if bsdf_f:
        bsdf_f.inputs['Base Color'].default_value = (0.08, 0.08, 0.09, 1.0)
        bsdf_f.inputs['Roughness'].default_value = 0.88
    body_obj.data.materials.append(mat_fabric)

    mat_front = bpy.data.materials.new(name="Mat_Front_Graphic")
    mat_front.blend_method = 'BLEND'
    bsdf_fg = mat_front.node_tree.nodes.get("Principled BSDF")
    if bsdf_fg:
        bsdf_fg.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_fg.inputs['Roughness'].default_value = 0.65
    front_decal.data.materials.append(mat_front)

    mat_back = bpy.data.materials.new(name="Mat_Back_Graphic")
    mat_back.blend_method = 'BLEND'
    bsdf_bg = mat_back.node_tree.nodes.get("Principled BSDF")
    if bsdf_bg:
        bsdf_bg.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
        bsdf_bg.inputs['Roughness'].default_value = 0.65
    back_decal.data.materials.append(mat_back)

    mat_chrome = bpy.data.materials.new(name="Mat_Hardware_Chrome")
    bsdf_c = mat_chrome.node_tree.nodes.get("Principled BSDF")
    if bsdf_c:
        bsdf_c.inputs['Base Color'].default_value = (0.9, 0.9, 0.95, 1.0)
        bsdf_c.inputs['Metallic'].default_value = 0.95
        bsdf_c.inputs['Roughness'].default_value = 0.15
    hardware_obj.data.materials.append(mat_chrome)

    # Smooth shading
    for obj in [body_obj, front_decal, back_decal, hardware_obj]:
        for poly in obj.data.polygons:
            poly.use_smooth = True

    # Center origin to ground
    bpy.ops.object.select_all(action='SELECT')
    for obj in [body_obj, front_decal, back_decal, hardware_obj]:
        obj.location.z -= 0.95
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

    # Export to GLB
    output_path = os.path.abspath("public/assets/models/hoodie_master.glb")
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True
    )
    print(f"MASTER 3D HOODIE READY AT: {output_path}")

if __name__ == "__main__":
    build_production_aaa_hoodie()
