import bpy
import bmesh
import math
import os

def create_tailored_streetwear_hoodie():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Hoodie_Fabric_Body_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Fabric_Body", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # We construct a clean, symmetrical quad topology base mesh
    # Coordinates in meters:
    # -------------------------------------------------------------
    # 1. TORSO GRID
    # -------------------------------------------------------------
    # Z levels:
    # z0 = -0.52 (hem bottom)
    # z1 = -0.42 (hem top)
    # z2 = -0.32 (pocket bottom)
    # z3 = -0.16 (pocket belly)
    # z4 = -0.02 (pocket top)
    # z5 =  0.16 (chest line)
    # z6 =  0.28 (armscye bottom)
    # z7 =  0.42 (dropped shoulder line)
    # z8 =  0.48 (collar)
    
    # 12 vertices per ring for clean subdivision without pinch:
    # 0: Right side (+X, Y=0)
    # 1: Right front (+X, +Y)
    # 2: Front center-right (+X, +Y)
    # 3: Front center (X=0, +Y)
    # 4: Front center-left (-X, +Y)
    # 5: Left front (-X, +Y)
    # 6: Left side (-X, Y=0)
    # 7: Left back (-X, -Y)
    # 8: Back center-left (-X, -Y)
    # 9: Back center (X=0, -Y)
    # 10: Back center-right (+X, -Y)
    # 11: Right back (+X, -Y)
    
    SEGS = 12
    ring_data = [
        # (z, xr, y_front, y_back)
        (-0.52, 0.38, 0.16, 0.16), # z0
        (-0.42, 0.40, 0.17, 0.17), # z1
        (-0.32, 0.45, 0.20, 0.18), # z2
        (-0.16, 0.48, 0.24, 0.20), # z3
        (-0.02, 0.50, 0.23, 0.20), # z4
        ( 0.16, 0.50, 0.21, 0.19), # z5
        ( 0.28, 0.52, 0.20, 0.18), # z6 (armpit)
        ( 0.42, 0.55, 0.18, 0.17), # z7 (shoulder)
        ( 0.48, 0.20, 0.14, 0.14), # z8 (collar)
    ]
    
    rings = []
    for r_idx, (z, xr, yf, yb) in enumerate(ring_data):
        r_verts = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            vx = ca * xr
            yr = yf if sa >= 0 else yb
            vy = sa * yr
            
            # Subtle natural drape waves
            if 1 <= r_idx <= 6:
                vy += 0.008 * math.cos(ang * 3.0)
                
            v = bm.verts.new((vx, vy, z))
            r_verts.append(v)
        rings.append(r_verts)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge rings 0 -> 5
    for r in range(5):
        r0 = rings[r]
        r1 = rings[r + 1]
        for i in range(SEGS):
            i_next = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[i_next], r1[i_next], r1[i]))
            
    # Rings 5 -> 7 (Armscye):
    # Right armscye: index 0 (±1)
    # Left armscye: index 6 (±1)
    # Front/Back connect between r5, r6, r7
    r5 = rings[5]
    r6 = rings[6]
    r7 = rings[7]
    
    # We bridge front (indices 1 to 5) and back (indices 7 to 11)
    for i in [1, 2, 3, 4]:
        bm.faces.new((r5[i], r5[i+1], r6[i+1], r6[i]))
        bm.faces.new((r6[i], r6[i+1], r7[i+1], r7[i]))
    for i in [7, 8, 9, 10]:
        bm.faces.new((r5[i], r5[i+1], r6[i+1], r6[i]))
        bm.faces.new((r6[i], r6[i+1], r7[i+1], r7[i]))
        
    # Rings 7 -> 8 (Shoulders to collar):
    r8 = rings[8]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        bm.faces.new((r7[i], r7[i_next], r8[i_next], r8[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. SEAMLESS DRAPED SLEEVES (HANGING NATURALLY DOWNWARDS)
    # -------------------------------------------------------------
    # Right armhole loop on torso:
    # Top: r7[0], r7[1], r7[11]
    # Bottom: r5[0], r5[1], r5[11]
    # Left armhole loop on torso:
    # Top: r7[6], r7[5], r7[7]
    # Bottom: r5[6], r5[5], r5[7]
    
    # Sleeves hang naturally down at -65 deg angle, close to torso
    sleeve_configs = [
        # (x_center, y_center, z_center, rx, ry)
        (0.56,  0.00,  0.30, 0.14, 0.14), # 0: Upper arm / shoulder cap
        (0.58,  0.01,  0.12, 0.13, 0.13), # 1: Bicep
        (0.57,  0.03, -0.06, 0.12, 0.12), # 2: Elbow drape
        (0.54,  0.01, -0.24, 0.11, 0.11), # 3: Forearm
        (0.48, -0.01, -0.42, 0.10, 0.10), # 4: Ribbed cuff
        (0.46, -0.01, -0.48, 0.09, 0.09), # 5: Cuff hem
    ]
    
    ARM_SEGS = 6
    for side_sign, arm_torso_pts in [(1.0, [r7[11], r7[0], r7[1], r6[1], r5[0], r6[11]]),
                                     (-1.0, [r7[5], r7[6], r7[7], r6[7], r5[6], r6[5]])]:
        s_rings = []
        for s_idx, (xc, yc, zc, rx, ry) in enumerate(sleeve_configs):
            s_ring = []
            for j in range(ARM_SEGS):
                ang = j * (2.0 * math.pi / ARM_SEGS)
                sx = side_sign * (xc + math.cos(ang) * rx)
                sy = yc + math.sin(ang) * ry
                sz = zc
                # Natural elbow crease
                if s_idx == 2 and math.cos(ang) * side_sign < 0:
                    sz += 0.02
                    sy -= 0.015
                v = bm.verts.new((sx, sy, sz))
                s_ring.append(v)
            s_rings.append(s_ring)
            
        # Bridge sleeve segments
        for s in range(len(s_rings) - 1):
            s0 = s_rings[s]
            s1 = s_rings[s + 1]
            for j in range(ARM_SEGS):
                j_nxt = (j + 1) % ARM_SEGS
                bm.faces.new((s0[j], s0[j_nxt], s1[j_nxt], s1[j]))
                
        # Bridge s_rings[0] to arm_torso_pts (Seamless watertight armscye!)
        s0 = s_rings[0]
        for k in range(ARM_SEGS):
            k_nxt = (k + 1) % ARM_SEGS
            bm.faces.new((arm_torso_pts[k], arm_torso_pts[k_nxt], s0[k_nxt], s0[k]))
            
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 3. TAILORED DRAPED HOOD (EXTRUDING FROM COLLAR)
    # -------------------------------------------------------------
    # Collar ring r8 has 12 vertices.
    # Hood emerges from back & sides (indices 11, 0, 1, 2, 3, 4, 5, 6, 7)
    # with a center seam from nape to crown to forehead!
    
    hood_levels = [
        # (z, y_center, x_rad, y_rad)
        (0.53, -0.06, 0.22, 0.20), # Cowl base
        (0.64, -0.14, 0.24, 0.23), # Occipital nape
        (0.75, -0.10, 0.23, 0.22), # Mid skull
        (0.84, -0.02, 0.21, 0.20), # Crown
        (0.80,  0.08, 0.18, 0.17), # Forehead brim
    ]
    
    HOOD_PTS = 8
    h_rings = []
    for h_idx, (hz, hyc, hrx, hry) in enumerate(hood_levels):
        h_ring = []
        for i in range(HOOD_PTS):
            t = i / (HOOD_PTS - 1)
            # Arch from right cheek to left cheek
            ang = math.pi * 0.15 + t * (math.pi * 1.70)
            hx = math.cos(ang) * hrx
            hy = hyc + math.sin(ang) * hry
            # Natural back sag
            hsag = -0.02 * math.cos(t * math.pi)
            v = bm.verts.new((hx, hy, hz + hsag))
            h_ring.append(v)
        h_rings.append(h_ring)
        
    for h in range(len(h_rings) - 1):
        h0 = h_rings[h]
        h1 = h_rings[h + 1]
        for i in range(HOOD_PTS - 1):
            bm.faces.new((h0[i], h0[i+1], h1[i+1], h1[i]))
            
    # Bridge hood base h_rings[0] to collar back/side vertices r8:
    h0 = h_rings[0]
    # Collar indices from 1 to 11 across the back
    c_indices = [1, 0, 11, 10, 9, 8, 7, 5]
    for i in range(len(c_indices) - 1):
        bm.faces.new((r8[c_indices[i]], r8[c_indices[i+1]], h0[i+1], h0[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 4. KANGAROO POCKET (DEFINED 3D FRONT BELLE POUCH)
    # -------------------------------------------------------------
    # 3 rows of 6 vertices across belly (Z: -0.36 to -0.04)
    kp_verts = []
    for pz, py_off, px_span in [(-0.36, 0.030, 0.32), (-0.18, 0.055, 0.36), (-0.04, 0.035, 0.30)]:
        row = []
        for c in range(6):
            t = (c / 5.0) - 0.5 # -0.5 to 0.5
            px = t * 2.0 * px_span
            arch = math.cos(t * math.pi)
            # Find base torso y at this z
            base_y = 0.20 + arch * 0.02
            py = base_y + py_off * arch
            v = bm.verts.new((px, py, pz))
            row.append(v)
        kp_verts.append(row)
        
    for r in range(2):
        for c in range(5):
            bm.faces.new((kp_verts[r][c], kp_verts[r][c+1], kp_verts[r+1][c+1], kp_verts[r+1][c]))
            
    # Stitch bottom and top to torso
    r1 = rings[1] # -0.42
    r4 = rings[4] # -0.02
    for c in range(5):
        bm.faces.new((r1[3], r1[4] if c >= 3 else r1[2], kp_verts[0][c+1], kp_verts[0][c]))
        bm.faces.new((kp_verts[2][c], kp_verts[2][c+1], r4[4] if c >= 3 else r4[2], r4[3]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 5. COTTON DRAWSTRINGS & AGLETS
    # -------------------------------------------------------------
    for ds_sign in (1.0, -1.0):
        ds_pts = [
            (ds_sign * 0.05, 0.16, 0.44),
            (ds_sign * 0.06, 0.17, 0.32),
            (ds_sign * 0.055, 0.18, 0.20),
            (ds_sign * 0.050, 0.18, 0.10),
        ]
        prev_cord = []
        for p_co in ds_pts:
            ring = []
            for k in range(5):
                kang = k * (2.0 * math.pi / 5)
                cx = p_co[0] + math.cos(kang) * 0.006
                cy = p_co[1] + math.sin(kang) * 0.006
                cz = p_co[2]
                v = bm.verts.new((cx, cy, cz))
                ring.append(v)
            if prev_cord:
                for k in range(5):
                    k_nxt = (k + 1) % 5
                    bm.faces.new((prev_cord[k], prev_cord[k_nxt], ring[k_nxt], ring[k]))
            prev_cord = ring

    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 6. DIRECT CONFORMAL UV UNWRAPPING
    # -------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    
    for f in bm.faces:
        c = f.calc_center_median()
        # Front chest & kangaroo pocket: Y > 0.01, abs(X) < 0.45, Z: [-0.48, 0.45]
        if c.y > 0.01 and abs(c.x) < 0.45 and -0.48 <= c.z <= 0.45:
            for l in f.loops:
                v = l.vert
                # U: 0.15 to 0.85
                u = ((v.co.x / 0.90) + 0.50) * 0.70 + 0.15
                # V: 0.10 to 0.90
                v_coord = ((v.co.z + 0.48) / 0.93) * 0.80 + 0.10
                l[uv_layer].uv = (u, v_coord)
        else:
            for l in f.loops:
                v = l.vert
                u = (v.co.x / 1.80) + 0.50
                v_coord = (v.co.z / 1.80) + 0.50
                l[uv_layer].uv = (u * 0.18 + 0.02, v_coord * 0.18 + 0.02)
                
    bm.to_mesh(mesh)
    bm.free()
    
    # Apply Subdivision Surface Modifier (Smooth 500GSM heavyweight drape)
    sub = hoodie.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 2
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    # Solidify (Fleece thickness)
    sol = hoodie.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.007
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    for p in hoodie.data.polygons:
        p.use_smooth = True
        
    # -------------------------------------------------------------
    # 7. MANNEQUIN STAND
    # -------------------------------------------------------------
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.08, depth=0.28, location=(0, -0.04, 0.48))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Bust"
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.065, depth=0.025, location=(0, -0.04, 0.63))
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
        
    # Ground offset
    bpy.ops.object.select_all(action='SELECT')
    for obj in [hoodie, mannequin]:
        obj.location.z -= 0.08
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    
    print(f"Generated Clean Tailored Streetwear Hoodie: {len(hoodie.data.vertices)} vertices, {len(hoodie.data.polygons)} polygons")
    return hoodie, mannequin

if __name__ == "__main__":
    h, m = create_tailored_streetwear_hoodie()
    bpy.ops.export_scene.gltf(filepath="public/assets/models/test_tailored.glb", export_format='GLB')
    print("Exported test_tailored.glb successfully!")
