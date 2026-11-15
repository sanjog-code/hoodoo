import bpy
import bmesh
import math
import os

def create_perfect_streetwear_hoodie(tex_path=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Hoodie_Fabric_Body_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Fabric_Body", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # -----------------------------------------------------------------
    # STREETWEAR BOX-CUT 1:1.6 PROPORTIONS
    # -----------------------------------------------------------------
    SEGS = 16
    ring_specs = [
        # (z, x_rad, y_front, y_back)
        (-0.52, 0.38, 0.15, 0.15), # 0: Hem bottom
        (-0.42, 0.40, 0.16, 0.16), # 1: Hem top
        (-0.34, 0.44, 0.19, 0.18), # 2: Belly / pocket base
        (-0.18, 0.48, 0.22, 0.20), # 3: Belly pouch bulge
        (-0.02, 0.50, 0.21, 0.19), # 4: Pocket top seam
        ( 0.15, 0.51, 0.20, 0.18), # 5: Chest graphic center
        ( 0.26, 0.53, 0.19, 0.17), # 6: Armpit level
        ( 0.40, 0.56, 0.17, 0.16), # 7: Dropped shoulder line
        ( 0.47, 0.20, 0.13, 0.13), # 8: Collar opening
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
            
            # Subtle natural fabric ripples
            if 1 <= r_idx <= 6:
                vy += 0.007 * math.cos(ang * 4.0)
                
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
            
    # Rings 6 -> 7 (Armscye):
    r6 = torso_rings[6]
    r7 = torso_rings[7]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        # Skip armscye opening on right and left
        if i in (15, 0) or i_next in (15, 0):
            continue
        if i in (7, 8) or i_next in (7, 8):
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
    # SEAMLESS DRAPED SLEEVES (VERTICAL RELAXED DRAPE)
    # -----------------------------------------------------------------
    sleeve_def = [
        # (x_center, y_center, z_center, radius)
        (0.58,  0.00,  0.28, 0.14), # 0: Shoulder cap
        (0.60,  0.01,  0.10, 0.13), # 1: Upper arm
        (0.58,  0.02, -0.08, 0.12), # 2: Elbow drape fold
        (0.54,  0.01, -0.26, 0.11), # 3: Forearm
        (0.48, -0.01, -0.44, 0.095), # 4: Ribbed cuff
        (0.46, -0.01, -0.50, 0.090), # 5: Cuff hem
    ]
    
    SLEEVE_SEGS = 8
    for side_sign in (1.0, -1.0):
        s_rings = []
        for s_idx, (xc, yc, zc, rad) in enumerate(sleeve_def):
            s_ring = []
            for j in range(SLEEVE_SEGS):
                ang = j * (2.0 * math.pi / SLEEVE_SEGS)
                sx = side_sign * (xc + math.cos(ang) * rad)
                sy = yc + math.sin(ang) * rad
                sz = zc
                # Elbow crease
                if s_idx == 2 and math.cos(ang) * side_sign < 0:
                    sz += 0.02
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
            arm_torso_pts = [r7[14], r7[15], r7[0], r7[1], r6[1], r6[0], r6[15], r6[14]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((arm_torso_pts[k], arm_torso_pts[k_next], s0[k_next], s0[k]))
        else:
            # Reverse loop order on left side to match sleeve ring normal direction!
            arm_torso_pts = [r7[6], r7[7], r7[8], r7[9], r6[9], r6[8], r6[7], r6[6]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((arm_torso_pts[k_next], arm_torso_pts[k], s0[k], s0[k_next]))
            
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # SEAMLESS DRAPED HOOD (NATURAL ROUNDED STREETWEAR HOOD)
    # -----------------------------------------------------------------
    hood_specs = [
        # (z, y_cen, x_rad, y_rad)
        (0.50, -0.05, 0.21, 0.18), # Cowl base
        (0.58, -0.10, 0.23, 0.21), # Nape
        (0.66, -0.07, 0.22, 0.20), # Mid skull
        (0.72, -0.01, 0.19, 0.18), # Crown
        (0.69,  0.06, 0.16, 0.15), # Face opening
    ]
    
    HOOD_PTS = 8
    h_rings = []
    for h_idx, (hz, hyc, hrx, hry) in enumerate(hood_specs):
        h_ring = []
        for i in range(HOOD_PTS):
            t = i / (HOOD_PTS - 1)
            ang = math.pi * 0.15 + t * (math.pi * 1.70)
            hx = math.cos(ang) * hrx
            hy = hyc + math.sin(ang) * hry
            hsag = -0.015 * math.cos(t * math.pi)
            v = bm.verts.new((hx, hy, hz + hsag))
            h_ring.append(v)
        h_rings.append(h_ring)
        
    for h in range(len(h_rings) - 1):
        h0 = h_rings[h]
        h1 = h_rings[h + 1]
        for i in range(HOOD_PTS - 1):
            bm.faces.new((h0[i], h0[i+1], h1[i+1], h1[i]))
            
    # Bridge to collar ring r8
    h0 = h_rings[0]
    collar_idx = [2, 1, 0, 15, 14, 13, 12, 10]
    for i in range(len(collar_idx) - 1):
        bm.faces.new((r8[collar_idx[i]], r8[collar_idx[i+1]], h0[i+1], h0[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # KANGAROO POCKET (DEFINED 3D FRONT BELLE POUCH)
    # -----------------------------------------------------------------
    kp_verts = []
    for pz, py_off, px_span in [(-0.34, 0.035, 0.30), (-0.18, 0.055, 0.34), (-0.02, 0.035, 0.28)]:
        row = []
        for c in range(6):
            t = (c / 5.0) - 0.5
            px = t * 2.0 * px_span
            arch = math.cos(t * math.pi)
            base_y = 0.19 + arch * 0.02
            py = base_y + py_off * arch
            v = bm.verts.new((px, py, pz))
            row.append(v)
        kp_verts.append(row)
        
    for r in range(2):
        for c in range(5):
            bm.faces.new((kp_verts[r][c], kp_verts[r][c+1], kp_verts[r+1][c+1], kp_verts[r+1][c]))
            
    r1 = torso_rings[1]
    r4 = torso_rings[4]
    for c in range(5):
        bm.faces.new((r1[4], r1[5] if c >= 3 else r1[3], kp_verts[0][c+1], kp_verts[0][c]))
        bm.faces.new((kp_verts[2][c], kp_verts[2][c+1], r4[5] if c >= 3 else r4[3], r4[4]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # DRAWSTRINGS & AGLETS
    # -----------------------------------------------------------------
    for ds_sign in (1.0, -1.0):
        ds_pts = [
            (ds_sign * 0.045, 0.15, 0.44),
            (ds_sign * 0.055, 0.16, 0.32),
            (ds_sign * 0.050, 0.17, 0.20),
            (ds_sign * 0.045, 0.17, 0.10),
        ]
        prev_ring = []
        for p_co in ds_pts:
            ring = []
            for k in range(6):
                kang = k * (2.0 * math.pi / 6)
                cx = p_co[0] + math.cos(kang) * 0.008
                cy = p_co[1] + math.sin(kang) * 0.008
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
    
    # -----------------------------------------------------------------
    # DIRECT CONFORMAL UV MAPPING
    # -----------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    
    min_x, max_x = -0.72, 0.72
    min_z, max_z = -0.55, 0.76
    span_x = max_x - min_x
    span_z = max_z - min_z
    
    for f in bm.faces:
        c = f.calc_center_median()
        is_front = c.y >= -0.02
        for l in f.loops:
            v = l.vert
            norm_u = (v.co.x - min_x) / span_x
            norm_v = (v.co.z - min_z) / span_z
            
            if is_front:
                l[uv_layer].uv = (1.0 - norm_u, norm_v)
            else:
                l[uv_layer].uv = (norm_u, norm_v)
                
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
        
    # -----------------------------------------------------------------
    # ATELIER MANNEQUIN STAND
    # -----------------------------------------------------------------
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.075, depth=0.28, location=(0, -0.04, 0.46))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Bust"
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.060, depth=0.025, location=(0, -0.04, 0.60))
    m_cap = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.02, depth=0.95, location=(0, 0, -0.48))
    m_pole = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.36, depth=0.035, location=(0, 0, -0.95))
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
    
    # Assign Material & Direct Texture if supplied
    if tex_path and os.path.exists(tex_path):
        mat_fabric = bpy.data.materials.new(name="Mat_Hoodie_Fabric")
        nodes_f = mat_fabric.node_tree.nodes
        bsdf_f = nodes_f.get("Principled BSDF")
        tex_node = nodes_f.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(tex_path)
        mat_fabric.node_tree.links.new(tex_node.outputs['Color'], bsdf_f.inputs['Base Color'])
        bsdf_f.inputs['Roughness'].default_value = 0.88
        hoodie.data.materials.append(mat_fabric)
        
    mat_mannequin = bpy.data.materials.new(name="Mat_Mannequin")
    bsdf_m = mat_mannequin.node_tree.nodes.get("Principled BSDF")
    if bsdf_m:
        bsdf_m.inputs['Base Color'].default_value = (0.06, 0.06, 0.07, 1.0)
        bsdf_m.inputs['Metallic'].default_value = 0.85
        bsdf_m.inputs['Roughness'].default_value = 0.22
    mannequin.data.materials.append(mat_mannequin)
    
    return hoodie, mannequin

if __name__ == "__main__":
    tex = os.path.abspath("public/assets/collection/hero_asphalt.png")
    h, m = create_perfect_streetwear_hoodie(tex)
    bpy.ops.export_scene.gltf(filepath="public/assets/models/perfect_hoodie.glb", export_format='GLB')
    print("Exported refined perfect_hoodie.glb successfully!")
