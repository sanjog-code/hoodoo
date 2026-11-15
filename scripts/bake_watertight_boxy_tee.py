import bpy
import bmesh
import math
import os
import shutil

def build_watertight_boxy_tee(texture_path, out_glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Tee_Mesh")
    tee = bpy.data.objects.new("Tee_Model", mesh)
    bpy.context.collection.objects.link(tee)
    bpy.context.view_layer.objects.active = tee
    
    bm = bmesh.new()
    
    # -----------------------------------------------------------------
    # 1. TORSO (Authentic 300GSM Boxy Heavyweight Cut, Drop Shoulder)
    # Front faces -Y, Back faces +Y, Up is +Z
    # -----------------------------------------------------------------
    SEGS = 24
    torso_rings_data = [
        # (z, x_rad, y_front, y_back)
        (-0.42, 0.33, 0.14, 0.13), # 0: Open straight hem (double-needle stitch)
        (-0.28, 0.34, 0.15, 0.14), # 1: Lower torso / hip drape
        (-0.12, 0.35, 0.16, 0.15), # 2: Mid torso
        ( 0.06, 0.35, 0.16, 0.15), # 3: Upper torso / solar plexus
        ( 0.22, 0.36, 0.16, 0.15), # 4: Chest graphic center
        ( 0.34, 0.37, 0.15, 0.14), # 5: Armpit / armscye bottom
        ( 0.44, 0.41, 0.14, 0.13), # 6: Dropped shoulder line
        ( 0.49, 0.15, 0.11, 0.10), # 7: Tight 1.25" rib crewneck collar
    ]
    
    torso_rings = []
    for r_idx, (z, xr, yf, yb) in enumerate(torso_rings_data):
        r_verts = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            vx = ca * xr
            yr = yf if sa <= 0 else yb
            vy = sa * yr
            # Subtle natural cloth ripples
            if 1 <= r_idx <= 5:
                vy += 0.003 * math.sin(ang * 4.0)
            v = bm.verts.new((vx, vy, z))
            r_verts.append(v)
        torso_rings.append(r_verts)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge rings 0 to 5
    for r in range(5):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            i_next = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[i_next], r1[i_next], r1[i]))
            
    # Rings 5 -> 6 (Armscye): Leave openings on left and right for short sleeves
    # Left sleeve opening (x > 0): indices 23, 0, 1, 2
    # Right sleeve opening (x < 0): indices 11, 12, 13, 14
    r5 = torso_rings[5]
    r6 = torso_rings[6]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        if i in (23, 0, 1) or i_next in (23, 0, 1):
            continue
        if i in (11, 12, 13) or i_next in (11, 12, 13):
            continue
        bm.faces.new((r5[i], r5[i_next], r6[i_next], r6[i]))
        
    # Rings 6 -> 7 (Shoulders to crewneck collar)
    r7 = torso_rings[7]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        bm.faces.new((r6[i], r6[i_next], r7[i_next], r7[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 2. DROPPED RELAXED SHORT SLEEVES (90s Boxy Tee Cut)
    # Extends wide off the shoulder cap, draping toward the elbow
    # -----------------------------------------------------------------
    sleeve_profile = [
        # (x_center, y_center, z_center, radius)
        (0.41,  0.00,  0.42, 0.115), # 0: Dropped shoulder connection
        (0.46, -0.01,  0.32, 0.110), # 1: Mid short sleeve
        (0.50, -0.01,  0.20, 0.105), # 2: Lower short sleeve
        (0.51, -0.01,  0.10, 0.100), # 3: Sleeve hem opening (elbow level)
    ]
    
    SLEEVE_SEGS = 12
    for side_sign in (1.0, -1.0):
        s_rings = []
        for s_idx, (xc, yc, zc, rad) in enumerate(sleeve_profile):
            s_ring = []
            for j in range(SLEEVE_SEGS):
                ang = j * (2.0 * math.pi / SLEEVE_SEGS)
                sx = side_sign * (xc + math.cos(ang) * rad)
                sy = yc + math.sin(ang) * rad
                sz = zc
                v = bm.verts.new((sx, sy, sz))
                s_ring.append(v)
            s_rings.append(s_ring)
            
        for s in range(len(s_rings) - 1):
            s0 = s_rings[s]
            s1 = s_rings[s + 1]
            for j in range(SLEEVE_SEGS):
                j_next = (j + 1) % SLEEVE_SEGS
                if side_sign > 0:
                    bm.faces.new((s0[j], s0[j_next], s1[j_next], s1[j]))
                else:
                    bm.faces.new((s0[j_next], s0[j], s1[j], s1[j_next]))
                    
        # Bridge to torso armscye
        s0 = s_rings[0]
        if side_sign > 0:
            torso_arm = [r6[22], r6[23], r6[0], r6[1], r6[2], r6[3], r5[3], r5[2], r5[1], r5[0], r5[23], r5[22]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((torso_arm[k], torso_arm[k_next], s0[k_next], s0[k]))
        else:
            torso_arm = [r6[10], r6[11], r6[12], r6[13], r6[14], r6[15], r5[15], r5[14], r5[13], r5[12], r5[11], r5[10]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((torso_arm[k_next], torso_arm[k], s0[k], s0[k_next]))
                
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 3. THICK 1.25" RIBBED CREWNECK COLLAR
    # High-density mock neck that stays crisp
    # -----------------------------------------------------------------
    collar_top = []
    for i in range(SEGS):
        ang = i * (2.0 * math.pi / SEGS)
        cx = math.cos(ang) * 0.14
        cy = math.sin(ang) * (0.10 if math.sin(ang) <= 0 else 0.09)
        cz = 0.525
        v = bm.verts.new((cx, cy, cz))
        collar_top.append(v)
        
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        bm.faces.new((r7[i], r7[i_next], collar_top[i_next], collar_top[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 4. UNIFIED DUAL-PANEL UV UNWRAPPING
    # Front faces (c.y <= 0) -> Left Half [0.0, 0.50]
    # Back faces (c.y > 0)   -> Right Half [0.50, 1.0]
    # -----------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    min_x, max_x = -0.65, 0.65
    min_z, max_z = -0.48, 0.55
    span_x = max_x - min_x
    span_z = max_z - min_z
    
    for f in bm.faces:
        c = f.calc_center_median()
        is_front = c.y <= 0.0
        for l in f.loops:
            v = l.vert
            u_norm = (v.co.x - min_x) / span_x
            v_norm = (v.co.z - min_z) / span_z
            u_norm = max(0.0, min(1.0, u_norm))
            v_norm = max(0.0, min(1.0, v_norm))
            
            if is_front:
                # Left half: [0.0, 0.50]
                l[uv_layer].uv = (u_norm * 0.50, v_norm)
            else:
                # Right half: [0.50, 1.0]
                l[uv_layer].uv = (0.50 + (1.0 - u_norm) * 0.50, v_norm)
                
    bm.to_mesh(mesh)
    bm.free()
    
    # Modifiers: Subdivision & Solidify
    sub = tee.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    sol = tee.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.004
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    for p in tee.data.polygons:
        p.use_smooth = True
        
    # -----------------------------------------------------------------
    # 5. ATELIER MUSEUM MANNEQUIN STAND
    # -----------------------------------------------------------------
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.065, depth=0.30, location=(0, 0.01, 0.48))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Neck"
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.055, depth=0.02, location=(0, 0.01, 0.63))
    m_cap = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.02, depth=0.95, location=(0, 0, -0.45))
    m_pole = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.32, depth=0.03, location=(0, 0, -0.92))
    m_base = bpy.context.active_object
    
    bpy.ops.object.select_all(action='DESELECT')
    for m in [m_neck, m_cap, m_pole, m_base]:
        m.select_set(True)
    bpy.context.view_layer.objects.active = m_neck
    bpy.ops.object.join()
    mannequin = bpy.context.active_object
    mannequin.name = "Mannequin_Stand"
    
    for p in mannequin.data.polygons:
        p.use_smooth = True
        
    bpy.ops.object.select_all(action='SELECT')
    for obj in [tee, mannequin]:
        obj.location.z -= 0.05
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    
    # -----------------------------------------------------------------
    # 6. MATERIALS & EXPORT
    # -----------------------------------------------------------------
    mat_fabric = bpy.data.materials.new(name="Mat_Tee_Fabric")
    nodes_f = mat_fabric.node_tree.nodes
    bsdf_f = nodes_f.get("Principled BSDF")
    
    tex_abs = os.path.abspath(texture_path)
    if os.path.exists(tex_abs) and bsdf_f:
        tex_node = nodes_f.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(tex_abs)
        mat_fabric.node_tree.links.new(tex_node.outputs['Color'], bsdf_f.inputs['Base Color'])
        bsdf_f.inputs['Roughness'].default_value = 0.90
    tee.data.materials.append(mat_fabric)
    
    mat_mannequin = bpy.data.materials.new(name="Mat_Mannequin")
    bsdf_m = mat_mannequin.node_tree.nodes.get("Principled BSDF")
    if bsdf_m:
        bsdf_m.inputs['Base Color'].default_value = (0.04, 0.04, 0.05, 1.0)
        bsdf_m.inputs['Metallic'].default_value = 0.90
        bsdf_m.inputs['Roughness'].default_value = 0.22
    mannequin.data.materials.append(mat_mannequin)
    
    os.makedirs(os.path.dirname(out_glb_path), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True
    )
    print(f"Exported Tee GLB: {out_glb_path}")
    return tee, mannequin

tees_to_bake = [
    {'id': 'p5',  'tex': 'public/assets/models/textures/tex_p5.png',  'out': 'public/assets/models/tee_p5.glb'},
    {'id': 'p6',  'tex': 'public/assets/models/textures/tex_p6.png',  'out': 'public/assets/models/tee_p6.glb'},
    {'id': 'p7',  'tex': 'public/assets/models/textures/tex_p7.png',  'out': 'public/assets/models/tee_p7.glb'},
    {'id': 'p8',  'tex': 'public/assets/models/textures/tex_p8.png',  'out': 'public/assets/models/tee_p8.glb'},
    {'id': 'p14', 'tex': 'public/assets/models/textures/tex_p14.png', 'out': 'public/assets/models/tee_p14.glb'},
    {'id': 'p15', 'tex': 'public/assets/models/textures/tex_p15.png', 'out': 'public/assets/models/tee_p15.glb'},
]

if __name__ == '__main__':
    for item in tees_to_bake:
        print(f"Baking boxy tee: {item['id']}...")
        build_watertight_boxy_tee(item['tex'], os.path.abspath(item['out']))
    print("ALL BOXY T-SHIRTS BAKED SUCCESSFULLY!")
