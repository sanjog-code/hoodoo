import bpy
import bmesh
import math
import os
import shutil

def build_single_watertight_hoodie(texture_path, out_glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Hoodie_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Model", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # -----------------------------------------------------------------
    # 1. TORSO (Authentic Heavyweight Boxy Cut, Drop Shoulder)
    # Front faces -Y, Back faces +Y, Up is +Z
    # -----------------------------------------------------------------
    SEGS = 24
    torso_rings_data = [
        # (z, x_rad, y_front, y_back)
        (-0.44, 0.28, 0.12, 0.12), # 0: Ribbed hem bottom
        (-0.36, 0.30, 0.13, 0.13), # 1: Ribbed hem top
        (-0.22, 0.33, 0.15, 0.14), # 2: Lower belly / pocket base
        (-0.06, 0.35, 0.16, 0.15), # 3: Mid belly
        ( 0.08, 0.35, 0.16, 0.15), # 4: Upper pocket seam
        ( 0.22, 0.36, 0.16, 0.15), # 5: Chest graphic
        ( 0.34, 0.37, 0.15, 0.14), # 6: Armpit / armscye bottom
        ( 0.44, 0.40, 0.14, 0.13), # 7: Dropped shoulder line
        ( 0.50, 0.16, 0.11, 0.11), # 8: Collar opening
    ]
    
    torso_rings = []
    for r_idx, (z, xr, yf, yb) in enumerate(torso_rings_data):
        r_verts = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            vx = ca * xr
            # Front is negative Y (sa < 0), Back is positive Y (sa > 0)
            yr = yf if sa <= 0 else yb
            vy = sa * yr
            # Subtle cloth micro-ripples on chest and back
            if 1 <= r_idx <= 6:
                vy += 0.004 * math.sin(ang * 4.0)
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
            
    # Rings 6 -> 7 (Armscye): Leave openings on left and right for sleeves
    # Left sleeve opening (x > 0): indices around 0 (23, 0, 1, 2)
    # Right sleeve opening (x < 0): indices around 12 (11, 12, 13, 14)
    r6 = torso_rings[6]
    r7 = torso_rings[7]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        # Skip armscye holes
        if i in (23, 0, 1) or i_next in (23, 0, 1):
            continue
        if i in (11, 12, 13) or i_next in (11, 12, 13):
            continue
        bm.faces.new((r6[i], r6[i_next], r7[i_next], r7[i]))
        
    # Rings 7 -> 8 (Shoulders to collar)
    r8 = torso_rings[8]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        bm.faces.new((r7[i], r7[i_next], r8[i_next], r8[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 2. RELAXED DOWNWARD-DRAPED SLEEVES
    # Naturally hanging beside the torso with clear armpit separation
    # -----------------------------------------------------------------
    sleeve_profile = [
        # (x_center, y_center, z_center, radius)
        (0.40,  0.00,  0.42, 0.115), # 0: Dropped shoulder connection
        (0.45, -0.01,  0.28, 0.105), # 1: Upper bicep
        (0.47, -0.02,  0.12, 0.098), # 2: Elbow drape fold
        (0.45, -0.02, -0.08, 0.090), # 3: Forearm
        (0.42, -0.02, -0.28, 0.080), # 4: Lower forearm
        (0.39, -0.02, -0.38, 0.070), # 5: Ribbed wrist cuff
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
                # Natural elbow crease
                if s_idx == 2 and math.cos(ang) * side_sign > 0:
                    sz -= 0.018
                    sy += 0.010
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
            torso_arm = [r7[22], r7[23], r7[0], r7[1], r7[2], r7[3], r6[3], r6[2], r6[1], r6[0], r6[23], r6[22]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((torso_arm[k], torso_arm[k_next], s0[k_next], s0[k]))
        else:
            torso_arm = [r7[10], r7[11], r7[12], r7[13], r7[14], r7[15], r6[15], r6[14], r6[13], r6[12], r6[11], r6[10]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((torso_arm[k_next], torso_arm[k], s0[k], s0[k_next]))
                
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 3. 3D KANGAROO POCKET (Front -Y)
    # -----------------------------------------------------------------
    kp_rows = [
        # (z, y_out, x_half_width)
        (-0.22, -0.18, 0.22), # Bottom hem of pocket
        (-0.06, -0.21, 0.24), # Bulge center pouch
        ( 0.08, -0.19, 0.18), # Top welt seam
    ]
    kp_verts = []
    for pz, py_front, px_span in kp_rows:
        row = []
        for c in range(7):
            t = (c / 6.0) - 0.5
            px = t * 2.0 * px_span
            arch = math.cos(t * math.pi)
            py = py_front - 0.02 * arch
            v = bm.verts.new((px, py, pz))
            row.append(v)
        kp_verts.append(row)
        
    for r in range(2):
        for c in range(6):
            bm.faces.new((kp_verts[r][c], kp_verts[r+1][c], kp_verts[r+1][c+1], kp_verts[r][c+1]))
            
    # Bridge pocket edges to torso
    r2 = torso_rings[2]
    r4 = torso_rings[4]
    # Pocket bottom to r2 (front indices 15 through 21)
    for c in range(6):
        bm.faces.new((kp_verts[0][c], kp_verts[0][c+1], r2[15 + c + 1], r2[15 + c]))
        bm.faces.new((kp_verts[2][c+1], kp_verts[2][c], r4[15 + c], r4[15 + c + 1]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 4. ORGANIC COWL HOOD
    # Attached to collar r8, draping over the back and neck
    # -----------------------------------------------------------------
    hood_rings_def = [
        # (z, y_center, x_rad, y_rad)
        (0.50,  0.03, 0.17, 0.15), # Collar base
        (0.58,  0.07, 0.19, 0.17), # Nape drape
        (0.66,  0.05, 0.18, 0.16), # Mid head
        (0.72,  0.01, 0.15, 0.14), # Crown apex
        (0.68, -0.04, 0.13, 0.12), # Forehead lip
    ]
    
    HOOD_PTS = 12
    h_rings = []
    for hz, hyc, hrx, hry in hood_rings_def:
        h_ring = []
        for i in range(HOOD_PTS):
            t = i / (HOOD_PTS - 1)
            # Arch around the back and sides from right jaw to left jaw
            ang = -math.pi * 0.40 + t * (math.pi * 1.80)
            hx = math.cos(ang) * hrx
            hy = hyc + math.sin(ang) * hry
            v = bm.verts.new((hx, hy, hz))
            h_ring.append(v)
        h_rings.append(h_ring)
        
    for h in range(len(h_rings) - 1):
        h0 = h_rings[h]
        h1 = h_rings[h + 1]
        for i in range(HOOD_PTS - 1):
            bm.faces.new((h0[i], h1[i], h1[i+1], h0[i+1]))
            
    # Bridge hood base to collar ring r8
    h0 = h_rings[0]
    collar_back_indices = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    for i in range(len(collar_back_indices) - 1):
        bm.faces.new((r8[collar_back_indices[i]], h0[i], h0[i+1], r8[collar_back_indices[i+1]]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 5. COTTON DRAWSTRINGS (Hanging down front -Y)
    # -----------------------------------------------------------------
    for ds_sign in (1.0, -1.0):
        ds_pts = [
            (ds_sign * 0.035, -0.13, 0.46),
            (ds_sign * 0.040, -0.14, 0.34),
            (ds_sign * 0.038, -0.15, 0.22),
            (ds_sign * 0.032, -0.15, 0.12),
        ]
        prev_ring = []
        for p_co in ds_pts:
            ring = []
            for k in range(6):
                kang = k * (2.0 * math.pi / 6)
                cx = p_co[0] + math.cos(kang) * 0.006
                cy = p_co[1] + math.sin(kang) * 0.006
                cz = p_co[2]
                v = bm.verts.new((cx, cy, cz))
                ring.append(v)
            if prev_ring:
                for k in range(6):
                    k_nxt = (k + 1) % 6
                    bm.faces.new((prev_ring[k], ring[k], ring[k_nxt], prev_ring[k_nxt]))
            prev_ring = ring
            
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 6. UNIFIED DUAL-PANEL UV UNWRAPPING
    # Front faces (c.y <= 0) -> Left Half [0.0, 0.50]
    # Back faces (c.y > 0)   -> Right Half [0.50, 1.0]
    # -----------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    min_x, max_x = -0.60, 0.60
    min_z, max_z = -0.50, 0.76
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
                # Viewer looking from -Y: left of screen is X < 0 -> u = 0.0
                l[uv_layer].uv = (u_norm * 0.50, v_norm)
            else:
                # Right half: [0.50, 1.0]
                # Viewer looking from +Y: left of screen is X > 0 -> u = 0.50
                l[uv_layer].uv = (0.50 + (1.0 - u_norm) * 0.50, v_norm)
                
    bm.to_mesh(mesh)
    bm.free()
    
    # Modifiers: Subdivision & Solidify
    sub = hoodie.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    sol = hoodie.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.005
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    for p in hoodie.data.polygons:
        p.use_smooth = True
        
    # -----------------------------------------------------------------
    # 7. SLEEK ATELIER MANNEQUIN STAND
    # -----------------------------------------------------------------
    # Bust neck inside collar
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.065, depth=0.25, location=(0, 0.01, 0.48))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Neck"
    
    # Neck cap
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.055, depth=0.02, location=(0, 0.01, 0.60))
    m_cap = bpy.context.active_object
    
    # Stand pole
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.02, depth=0.90, location=(0, 0, -0.45))
    m_pole = bpy.context.active_object
    
    # Heavy beveled base plate
    bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.32, depth=0.03, location=(0, 0, -0.90))
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
        
    # Center assembly
    bpy.ops.object.select_all(action='SELECT')
    for obj in [hoodie, mannequin]:
        obj.location.z -= 0.05
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    
    # -----------------------------------------------------------------
    # 8. MATERIALS & EXPORT
    # -----------------------------------------------------------------
    mat_fabric = bpy.data.materials.new(name="Mat_Hoodie_Fabric")
    mat_fabric.use_nodes = True
    nodes_f = mat_fabric.node_tree.nodes
    bsdf_f = nodes_f.get("Principled BSDF")
    
    tex_abs = os.path.abspath(texture_path)
    if os.path.exists(tex_abs) and bsdf_f:
        tex_node = nodes_f.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(tex_abs)
        mat_fabric.node_tree.links.new(tex_node.outputs['Color'], bsdf_f.inputs['Base Color'])
        bsdf_f.inputs['Roughness'].default_value = 0.92
    hoodie.data.materials.append(mat_fabric)
    
    mat_mannequin = bpy.data.materials.new(name="Mat_Mannequin")
    mat_mannequin.use_nodes = True
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
    print(f"Exported: {out_glb_path}")
    return hoodie, mannequin

all_models = [
    {'id': 'hero', 'tex': 'public/assets/models/textures/tex_hero.png', 'out': 'public/assets/models/hoodie_hero.glb'},
    {'id': 'p1',   'tex': 'public/assets/models/textures/tex_p1.png',   'out': 'public/assets/models/hoodie_p1.glb'},
    {'id': 'p2',   'tex': 'public/assets/models/textures/tex_p2.png',   'out': 'public/assets/models/hoodie_p2.glb'},
    {'id': 'p3',   'tex': 'public/assets/models/textures/tex_p3.png',   'out': 'public/assets/models/hoodie_p3.glb'},
    {'id': 'p4',   'tex': 'public/assets/models/textures/tex_p4.png',   'out': 'public/assets/models/hoodie_p4.glb'},
    {'id': 'p13',  'tex': 'public/assets/models/textures/tex_p13.png',  'out': 'public/assets/models/hoodie_p13.glb'},
]

if __name__ == '__main__':
    for item in all_models:
        print(f"Baking watertight atelier hoodie: {item['id']}...")
        build_single_watertight_hoodie(item['tex'], os.path.abspath(item['out']))
        
    # Also copy hero to hoodie_master.glb
    hero_glb = os.path.abspath('public/assets/models/hoodie_hero.glb')
    master_glb = os.path.abspath('public/assets/models/hoodie_master.glb')
    shutil.copyfile(hero_glb, master_glb)
    print("ALL 6 WATERTIGHT 3D ATELIER HOODIES BAKED & EXPORTED SUCCESSFULLY!")
