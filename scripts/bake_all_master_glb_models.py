import bpy
import bmesh
import math
import os
import shutil

models_config = [
    {
        'id': 'hero',
        'tex': 'public/assets/models/textures/tex_hero.png',
        'out': 'public/assets/models/hoodie_hero.glb'
    },
    {
        'id': 'p1',
        'tex': 'public/assets/models/textures/tex_p1.png',
        'out': 'public/assets/models/hoodie_p1.glb'
    },
    {
        'id': 'p2',
        'tex': 'public/assets/models/textures/tex_p2.png',
        'out': 'public/assets/models/hoodie_p2.glb'
    },
    {
        'id': 'p3',
        'tex': 'public/assets/models/textures/tex_p3.png',
        'out': 'public/assets/models/hoodie_p3.glb'
    },
    {
        'id': 'p4',
        'tex': 'public/assets/models/textures/tex_p4.png',
        'out': 'public/assets/models/hoodie_p4.glb'
    },
    {
        'id': 'p13',
        'tex': 'public/assets/models/textures/tex_p13.png',
        'out': 'public/assets/models/hoodie_p13.glb'
    },
]

def build_hoodie_mesh(texture_path, out_glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Hoodie_Fabric_Body_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Fabric_Body", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. TORSO RINGS (HEAVYWEIGHT STREETWEAR BOX-CUT)
    # Proportions: Width ~ 0.98m, Height ~ 0.88m (1:1.1 authentic drop)
    # -------------------------------------------------------------
    SEGS = 20
    ring_specs = [
        # (z, x_rad, y_front, y_back)
        (-0.46, 0.40, 0.17, 0.16), # 0: Ribbed hem bottom
        (-0.36, 0.43, 0.18, 0.17), # 1: Ribbed hem top
        (-0.24, 0.47, 0.22, 0.20), # 2: Lower belly / pocket base
        (-0.08, 0.50, 0.24, 0.21), # 3: Mid belly pouch bulge
        ( 0.08, 0.51, 0.23, 0.20), # 4: Upper pocket seam
        ( 0.22, 0.52, 0.21, 0.19), # 5: Chest graphic center
        ( 0.34, 0.53, 0.20, 0.18), # 6: Armscye / armpit level
        ( 0.44, 0.54, 0.18, 0.16), # 7: Dropped shoulder line
        ( 0.50, 0.22, 0.14, 0.13), # 8: Collar opening
    ]
    
    torso_rings = []
    for r_idx, (z, xr, yf, yb) in enumerate(ring_specs):
        r_verts = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            vx = ca * xr
            yr = yf if sa >= 0 else yb
            vy = sa * yr
            if 1 <= r_idx <= 6:
                vy += 0.007 * math.sin(ang * 3.0) + 0.004 * math.cos(ang * 5.0)
            v = bm.verts.new((vx, vy, z))
            r_verts.append(v)
        torso_rings.append(r_verts)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge rings 0 to 6
    for r in range(6):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            i_next = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[i_next], r1[i_next], r1[i]))
            
    # Rings 6 -> 7 (Armscye): Leave openings for sleeves (indices 19,0,1,2 and 8,9,10,11)
    r6 = torso_rings[6]
    r7 = torso_rings[7]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        if i in (19, 0, 1) or i_next in (19, 0, 1):
            continue
        if i in (9, 10, 11) or i_next in (9, 10, 11):
            continue
        bm.faces.new((r6[i], r6[i_next], r7[i_next], r7[i]))
        
    # Rings 7 -> 8 (Shoulders to collar)
    r8 = torso_rings[8]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        bm.faces.new((r7[i], r7[i_next], r8[i_next], r8[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. RELAXED DOWNWARD-DRAPED SLEEVES
    # Naturally hanging beside the torso
    # -------------------------------------------------------------
    sleeve_def = [
        # (x_cen, y_cen, z_cen, radius)
        (0.53,  0.00,  0.36, 0.150), # 0: Shoulder cap drop
        (0.51,  0.01,  0.18, 0.138), # 1: Upper arm
        (0.48,  0.02, -0.02, 0.126), # 2: Elbow drape fold
        (0.44,  0.01, -0.22, 0.114), # 3: Forearm
        (0.40, -0.01, -0.38, 0.096), # 4: Ribbed cuff
        (0.38, -0.01, -0.45, 0.090), # 5: Cuff hem
    ]
    
    SLEEVE_SEGS = 10
    for side_sign in (1.0, -1.0):
        s_rings = []
        for s_idx, (xc, yc, zc, rad) in enumerate(sleeve_def):
            s_ring = []
            for j in range(SLEEVE_SEGS):
                ang = j * (2.0 * math.pi / SLEEVE_SEGS)
                sx = side_sign * (xc + math.cos(ang) * rad)
                sy = yc + math.sin(ang) * rad
                sz = zc
                if s_idx == 2 and math.cos(ang) * side_sign < 0:
                    sz += 0.025
                    sy -= 0.015
                v = bm.verts.new((sx, sy, sz))
                s_ring.append(v)
            s_rings.append(s_ring)
            
        for s in range(len(s_rings) - 1):
            s0 = s_rings[s]
            s1 = s_rings[s + 1]
            for j in range(SLEEVE_SEGS):
                j_next = (j + 1) % SLEEVE_SEGS
                bm.faces.new((s0[j], s0[j_next], s1[j_next], s1[j]))
                
        # Bridge to torso armhole with consistent normal winding!
        s0 = s_rings[0]
        if side_sign > 0:
            arm_torso = [r7[18], r7[19], r7[0], r7[1], r7[2], r6[2], r6[1], r6[0], r6[19], r6[18]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((arm_torso[k], arm_torso[k_next], s0[k_next], s0[k]))
        else:
            arm_torso = [r7[8], r7[9], r7[10], r7[11], r7[12], r6[12], r6[11], r6[10], r6[9], r6[8]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((arm_torso[k_next], arm_torso[k], s0[k], s0[k_next]))
                
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 3. ORGANIC COWL-DRAPED HOOD
    # -------------------------------------------------------------
    hood_specs = [
        # (z, y_cen, x_rad, y_rad)
        (0.51, -0.04, 0.23, 0.20), # Cowl base
        (0.59, -0.10, 0.25, 0.23), # Nape drape
        (0.67, -0.07, 0.23, 0.22), # Mid skull curve
        (0.72, -0.02, 0.20, 0.19), # Crown apex
        (0.69,  0.05, 0.17, 0.16), # Face opening lip
    ]
    
    HOOD_PTS = 10
    h_rings = []
    for h_idx, (hz, hyc, hrx, hry) in enumerate(hood_specs):
        h_ring = []
        for i in range(HOOD_PTS):
            t = i / (HOOD_PTS - 1)
            ang = math.pi * 0.12 + t * (math.pi * 1.76)
            hx = math.cos(ang) * hrx
            hy = hyc + math.sin(ang) * hry
            hsag = -0.018 * math.cos(t * math.pi)
            v = bm.verts.new((hx, hy, hz + hsag))
            h_ring.append(v)
        h_rings.append(h_ring)
        
    for h in range(len(h_rings) - 1):
        h0 = h_rings[h]
        h1 = h_rings[h + 1]
        for i in range(HOOD_PTS - 1):
            bm.faces.new((h0[i], h0[i+1], h1[i+1], h1[i]))
            
    # Bridge hood to collar ring r8
    h0 = h_rings[0]
    collar_map = [3, 2, 1, 0, 19, 18, 17, 16, 15, 13]
    for i in range(len(collar_map) - 1):
        bm.faces.new((r8[collar_map[i]], r8[collar_map[i+1]], h0[i+1], h0[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 4. 3D KANGAROO POCKET
    # -------------------------------------------------------------
    kp_verts = []
    for pz, py_off, px_span in [(-0.24, 0.040, 0.32), (-0.08, 0.060, 0.36), (0.08, 0.040, 0.30)]:
        row = []
        for c in range(7):
            t = (c / 6.0) - 0.5
            px = t * 2.0 * px_span
            arch = math.cos(t * math.pi)
            base_y = 0.21 + arch * 0.02
            py = base_y + py_off * arch
            v = bm.verts.new((px, py, pz))
            row.append(v)
        kp_verts.append(row)
        
    for r in range(2):
        for c in range(6):
            bm.faces.new((kp_verts[r][c], kp_verts[r][c+1], kp_verts[r+1][c+1], kp_verts[r+1][c]))
            
    r2 = torso_rings[2]
    r4 = torso_rings[4]
    for c in range(6):
        bm.faces.new((r2[5], r2[6] if c >= 3 else r2[4], kp_verts[0][c+1], kp_verts[0][c]))
        bm.faces.new((kp_verts[2][c], kp_verts[2][c+1], r4[6] if c >= 3 else r4[4], r4[5]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 5. COTTON DRAWSTRINGS
    # -------------------------------------------------------------
    for ds_sign in (1.0, -1.0):
        ds_pts = [
            (ds_sign * 0.040, 0.16, 0.46),
            (ds_sign * 0.048, 0.17, 0.34),
            (ds_sign * 0.044, 0.18, 0.22),
            (ds_sign * 0.038, 0.18, 0.12),
        ]
        prev_ring = []
        for p_co in ds_pts:
            ring = []
            for k in range(6):
                kang = k * (2.0 * math.pi / 6)
                cx = p_co[0] + math.cos(kang) * 0.007
                cy = p_co[1] + math.sin(kang) * 0.007
                cz = p_co[2]
                v = bm.verts.new((cx, cy, cz))
                ring.append(v)
            if prev_ring:
                for k in range(6):
                    k_nxt = (k + 1) % 6
                    bm.faces.new((prev_ring[k], prev_ring[k_nxt], ring[k_nxt], ring[k]))
            prev_ring = ring
            
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 6. UV ATLAS UNWRAPPING (DUAL-PANEL FRONT & BACK)
    # Front faces -> U in [0.0, 0.50]
    # Back faces  -> U in [0.50, 1.0]
    # -------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    min_x, max_x = -0.68, 0.68
    min_z, max_z = -0.52, 0.78
    span_x = max_x - min_x
    span_z = max_z - min_z
    
    for f in bm.faces:
        c = f.calc_center_median()
        is_front = c.y >= -0.02
        for l in f.loops:
            v = l.vert
            u_norm = (v.co.x - min_x) / span_x
            v_norm = (v.co.z - min_z) / span_z
            
            if is_front:
                # Left half of atlas (0.0 to 0.5)
                # Un-mirrored: (1.0 - u_norm) * 0.5
                l[uv_layer].uv = ((1.0 - u_norm) * 0.5, v_norm)
            else:
                # Right half of atlas (0.5 to 1.0)
                l[uv_layer].uv = (0.5 + u_norm * 0.5, v_norm)
                
    bm.to_mesh(mesh)
    bm.free()
    
    sub = hoodie.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 2
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    sol = hoodie.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.006
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    for p in hoodie.data.polygons:
        p.use_smooth = True
        
    # -------------------------------------------------------------
    # 7. SLEEK ATELIER MANNEQUIN STAND
    # -------------------------------------------------------------
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.075, depth=0.28, location=(0, -0.03, 0.48))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Bust"
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.060, depth=0.025, location=(0, -0.03, 0.62))
    m_cap = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.022, depth=0.95, location=(0, 0, -0.46))
    m_pole = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.35, depth=0.035, location=(0, 0, -0.93))
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
    for obj in [hoodie, mannequin]:
        obj.location.z -= 0.08
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    
    # Fabric Material with Direct Atlas Texture
    mat_fabric = bpy.data.materials.new(name="Mat_Hoodie_Fabric")
    nodes_f = mat_fabric.node_tree.nodes
    bsdf_f = nodes_f.get("Principled BSDF")
    
    tex_abs = os.path.abspath(texture_path)
    if os.path.exists(tex_abs) and bsdf_f:
        tex_node = nodes_f.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(tex_abs)
        mat_fabric.node_tree.links.new(tex_node.outputs['Color'], bsdf_f.inputs['Base Color'])
        bsdf_f.inputs['Roughness'].default_value = 0.90
    hoodie.data.materials.append(mat_fabric)
    
    # Mannequin Material
    mat_mannequin = bpy.data.materials.new(name="Mat_Mannequin")
    bsdf_m = mat_mannequin.node_tree.nodes.get("Principled BSDF")
    if bsdf_m:
        bsdf_m.inputs['Base Color'].default_value = (0.05, 0.05, 0.06, 1.0)
        bsdf_m.inputs['Metallic'].default_value = 0.85
        bsdf_m.inputs['Roughness'].default_value = 0.25
    mannequin.data.materials.append(mat_mannequin)
    
    # Export GLB
    os.makedirs(os.path.dirname(out_glb_path), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True
    )
    print(f"Exported: {out_glb_path}")
    return hoodie, mannequin

def main():
    for item in models_config:
        print(f"Baking master 3D model for: {item['id']}...")
        build_hoodie_mesh(item['tex'], os.path.abspath(item['out']))
        
    hero_glb = os.path.abspath("public/assets/models/hoodie_hero.glb")
    master_glb = os.path.abspath("public/assets/models/hoodie_master.glb")
    shutil.copyfile(hero_glb, master_glb)
    print("All master 3D models baked successfully!")

if __name__ == "__main__":
    main()
