import bpy
import bmesh
import math
import os

# =================================================================
# 1. 300GSM BOXY FIT STREETWEAR TEE
# =================================================================
def create_masterpiece_tee(out_glb_path, texture_path=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Tee_Mesh")
    tee = bpy.data.objects.new("Tee_Model", mesh)
    bpy.context.collection.objects.link(tee)
    bpy.context.view_layer.objects.active = tee
    
    bm = bmesh.new()
    
    # Anatomical Torso (Chest: 0.54m wide, 0.23m deep)
    SEGS = 24
    torso_levels = [
        (-0.42, 0.250, 0.106, 0.096, 0.002), # 0: Hem
        (-0.28, 0.246, 0.104, 0.094, 0.003), # 1: Waist
        (-0.14, 0.252, 0.110, 0.098, 0.004), # 2: Mid torso
        ( 0.04, 0.260, 0.116, 0.104, 0.003), # 3: Lower chest
        ( 0.18, 0.268, 0.120, 0.106, 0.002), # 4: Chest graphic center
        ( 0.30, 0.278, 0.116, 0.102, 0.002), # 5: Armscye bottom (armpit)
        ( 0.40, 0.298, 0.108, 0.094, 0.001), # 6: Dropped shoulder seam
        ( 0.46, 0.192, 0.096, 0.084, 0.000), # 7: Shoulder slope
        ( 0.49, 0.098, 0.078, 0.068, 0.000), # 8: Ribbed collar base
        ( 0.52, 0.094, 0.074, 0.064, 0.000), # 9: Ribbed collar top
    ]
    
    torso_rings = []
    for z, xr, yf, yb, r_amp in torso_levels:
        ring = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            vx = ca * xr
            yr = yf if sa <= 0 else yb
            vy = sa * yr
            if r_amp > 0:
                vy += r_amp * math.sin(ang * 3.0 + z * 8.0)
            ring.append(bm.verts.new((vx, vy, z)))
        torso_rings.append(ring)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge torso levels 0 to 5
    for r in range(5):
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((torso_rings[r][i], torso_rings[r][inxt], torso_rings[r+1][inxt], torso_rings[r+1][i]))
            
    # Bridge level 5 to 6 excluding arm openings
    r5 = torso_rings[5]
    r6 = torso_rings[6]
    for i in range(SEGS):
        inxt = (i + 1) % SEGS
        if i in (22, 23, 0, 1) or inxt in (23, 0, 1, 2): continue
        if i in (10, 11, 12, 13) or inxt in (11, 12, 13, 14): continue
        bm.faces.new((r5[i], r5[inxt], r6[inxt], r6[i]))
        
    for r in range(6, len(torso_levels) - 1):
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((torso_rings[r][i], torso_rings[r][inxt], torso_rings[r+1][inxt], torso_rings[r+1][i]))
            
    bm.verts.ensure_lookup_table()
    
    # 10-vertex armscye boundary loops
    left_arm_loop = [
        r5[22], r5[23], r5[0], r5[1], r5[2],
        r6[2], r6[1], r6[0], r6[23], r6[22]
    ]
    right_arm_loop = [
        r5[14], r5[13], r5[12], r5[11], r5[10],
        r6[10], r6[11], r6[12], r6[13], r6[14]
    ]
    
    arm_angle = math.radians(24.0)
    sin_a = math.sin(arm_angle)
    cos_a = math.cos(arm_angle)
    
    sleeve_steps = [
        (0.045, 0.40, 0.122, 0.116), # 1: Deltoid
        (0.105, 0.70, 0.118, 0.112), # 2: Upper bicep
        (0.170, 0.90, 0.114, 0.108), # 3: Mid bicep
        (0.235, 1.00, 0.110, 0.104), # 4: Boxy hem cut (planar)
        (0.245, 1.00, 0.107, 0.100), # 5: Clean inward hem fold
    ]
    
    for arm_loop, sign in [(left_arm_loop, 1.0), (right_arm_loop, -1.0)]:
        c_root_x = sign * 0.285
        c_root_y = 0.005
        c_root_z = 0.350
        
        prev_loop = arm_loop
        for s_dist, t_blend, rw, rd in sleeve_steps:
            cx = c_root_x + sign * (sin_a * s_dist)
            cy = c_root_y
            cz = c_root_z - (cos_a * s_dist)
            
            new_loop = []
            N = len(arm_loop)
            for k in range(N):
                v_orig = arm_loop[k]
                phi = (((k - 7) % N) / N) * 2.0 * math.pi
                ca = math.cos(phi)
                sa = math.sin(phi)
                
                px = cx + sign * (ca * rw * cos_a)
                py = cy + sa * rd
                pz = cz + (ca * rw * sin_a)
                
                ox = v_orig.co.x + sign * (sin_a * s_dist)
                oy = v_orig.co.y
                oz = v_orig.co.z - (cos_a * s_dist)
                
                fx = (1.0 - t_blend) * ox + t_blend * px
                fy = (1.0 - t_blend) * oy + t_blend * py
                fz = (1.0 - t_blend) * oz + t_blend * pz
                new_loop.append(bm.verts.new((fx, fy, fz)))
                
            bm.verts.ensure_lookup_table()
            for k in range(N):
                knxt = (k + 1) % N
                if sign > 0:
                    bm.faces.new((prev_loop[k], prev_loop[knxt], new_loop[knxt], new_loop[k]))
                else:
                    bm.faces.new((prev_loop[k], new_loop[k], new_loop[knxt], prev_loop[knxt]))
            prev_loop = new_loop
            
        # Inward cuff lip to close the sleeve cleanly
        inward_cuff = []
        for v in prev_loop:
            dx = v.co.x - cx
            dy = v.co.y - cy
            dz = v.co.z - cz
            inward_cuff.append(bm.verts.new((cx + dx * 0.86, cy + dy * 0.86, cz + dz * 0.86 + 0.015)))
        bm.verts.ensure_lookup_table()
        for k in range(N):
            knxt = (k + 1) % N
            if sign > 0:
                bm.faces.new((prev_loop[k], prev_loop[knxt], inward_cuff[knxt], inward_cuff[k]))
            else:
                bm.faces.new((prev_loop[k], inward_cuff[k], inward_cuff[knxt], prev_loop[knxt]))
            
    # Atelier Bust Stand
    stand_levels = [
        (-0.62, 0.150),
        (-0.46, 0.120),
        ( 0.42, 0.090),
        ( 0.56, 0.045),
        ( 0.60, 0.038),
    ]
    stand_rings = []
    for sz, sr in stand_levels:
        s_ring = []
        for i in range(16):
            ang = i * (2.0 * math.pi / 16)
            s_ring.append(bm.verts.new((math.cos(ang) * sr, math.sin(ang) * sr, sz)))
        stand_rings.append(s_ring)
        
    bm.verts.ensure_lookup_table()
    for s in range(len(stand_levels) - 1):
        for i in range(16):
            inxt = (i + 1) % 16
            bm.faces.new((stand_rings[s][i], stand_rings[s][inxt], stand_rings[s+1][inxt], stand_rings[s+1][i]))
    bm.faces.new(reversed(stand_rings[0]))
    bm.faces.new(stand_rings[-1])
    
    # Dual-Panel UV Mapping
    uv_layer = bm.loops.layers.uv.new("UVMap")
    for face in bm.faces:
        for loop in face.loops:
            v = loop.vert
            vx, vy, vz = v.co.x, v.co.y, v.co.z
            u_norm = max(0.0, min(1.0, (vx + 0.55) / 1.10))
            v_norm = max(0.0, min(1.0, (vz + 0.45) / 1.05))
            if vy <= 0.01:
                loop[uv_layer].uv = (u_norm * 0.48 + 0.01, v_norm * 0.96 + 0.02)
            else:
                loop[uv_layer].uv = (0.51 + (1.0 - u_norm) * 0.48, v_norm * 0.96 + 0.02)
                
    bm.to_mesh(mesh)
    bm.free()
    
    subsurf = tee.modifiers.new("Subsurf", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    for poly in mesh.polygons: poly.use_smooth = True
    
    if texture_path and os.path.exists(texture_path):
        mat = bpy.data.materials.new("Tee_Fabric_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(os.path.abspath(texture_path))
        mat.node_tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.88
        bsdf.inputs['Specular IOR Level'].default_value = 0.12
        tee.data.materials.append(mat)
        
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False
    )
    print(f"Exported Masterpiece Tee: {out_glb_path}")


# =================================================================
# 2. 500GSM OVERSIZED STREETWEAR HOODIE
# (Full-Length Enclosed Sleeves, 3D Raised Kangaroo Pouch, Seamlessly Attached Hood)
# =================================================================
def create_masterpiece_hoodie(out_glb_path, texture_path=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Hoodie_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Model", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # Anatomical Torso & Ribbed Waistband
    SEGS = 24
    torso_levels = [
        (-0.46, 0.228, 0.102, 0.090, 0.000), # 0: 3" Ribbed waistband bottom
        (-0.40, 0.234, 0.104, 0.092, 0.000), # 1: Waistband top
        (-0.35, 0.264, 0.120, 0.104, 0.006), # 2: Torso pooling over band
        (-0.18, 0.270, 0.124, 0.108, 0.005), # 3: Mid abdomen
        ( 0.02, 0.276, 0.126, 0.110, 0.004), # 4: Mid chest
        ( 0.18, 0.278, 0.122, 0.106, 0.003), # 5: Chest graphic
        ( 0.32, 0.288, 0.116, 0.100, 0.002), # 6: Armscye bottom (armpit)
        ( 0.42, 0.308, 0.108, 0.094, 0.001), # 7: Dropped shoulder seam
        ( 0.48, 0.202, 0.098, 0.086, 0.000), # 8: Collar base
        ( 0.52, 0.112, 0.086, 0.076, 0.000), # 9: Hood neckline
    ]
    
    torso_rings = []
    for z, xr, yf, yb, r_amp in torso_levels:
        ring = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            vx = ca * xr
            yr = yf if sa <= 0 else yb
            vy = sa * yr
            if r_amp > 0:
                vy += r_amp * math.sin(ang * 3.0 + z * 7.0)
            ring.append(bm.verts.new((vx, vy, z)))
        torso_rings.append(ring)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge torso levels 0 to 6
    for r in range(6):
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((torso_rings[r][i], torso_rings[r][inxt], torso_rings[r+1][inxt], torso_rings[r+1][i]))
            
    # Bridge level 6 to 7 excluding arm openings
    r6 = torso_rings[6]
    r7 = torso_rings[7]
    for i in range(SEGS):
        inxt = (i + 1) % SEGS
        if i in (22, 23, 0, 1) or inxt in (23, 0, 1, 2): continue
        if i in (10, 11, 12, 13) or inxt in (11, 12, 13, 14): continue
        bm.faces.new((r6[i], r6[inxt], r7[inxt], r7[i]))
        
    for r in range(7, len(torso_levels) - 1):
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((torso_rings[r][i], torso_rings[r][inxt], torso_rings[r+1][inxt], torso_rings[r+1][i]))
            
    bm.verts.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # A. Full-Length Oversized Streetwear Sleeves (Wrists z = -0.63m)
    # -------------------------------------------------------------
    left_arm_loop = [
        r6[22], r6[23], r6[0], r6[1], r6[2],
        r7[2], r7[1], r7[0], r7[23], r7[22]
    ]
    right_arm_loop = [
        r6[14], r6[13], r6[12], r6[11], r6[10],
        r7[10], r7[11], r7[12], r7[13], r7[14]
    ]
    
    hoodie_sleeve_steps = [
        (0.060, 0.40, 0.128, 0.122, 0.015, 0.005, -0.065), # 1: Deltoid
        (0.140, 0.70, 0.130, 0.124, 0.030, 0.010, -0.155), # 2: Upper bicep
        (0.230, 0.90, 0.127, 0.122, 0.038, 0.015, -0.250), # 3: Elbow crease
        (0.320, 1.00, 0.124, 0.118, 0.040, 0.018, -0.345), # 4: Forearm
        (0.420, 1.00, 0.120, 0.114, 0.036, 0.020, -0.440), # 5: Lower forearm
        (0.510, 1.00, 0.112, 0.106, 0.028, 0.022, -0.530), # 6: Wrist stacking
        (0.580, 1.00, 0.096, 0.090, 0.018, 0.023, -0.590), # 7: Cuff gather
        (0.615, 1.00, 0.069, 0.063, 0.012, 0.024, -0.620), # 8: Ribbed elastic wrist cuff
        (0.630, 1.00, 0.066, 0.061, 0.010, 0.024, -0.635), # 9: Cuff rim
    ]
    
    arm_angle = math.radians(16.0)
    sin_a = math.sin(arm_angle)
    cos_a = math.cos(arm_angle)
    
    for arm_loop, sign in [(left_arm_loop, 1.0), (right_arm_loop, -1.0)]:
        c_root_x = sign * 0.295
        c_root_y = 0.005
        c_root_z = 0.370
        
        prev_loop = arm_loop
        for s_dist, t_blend, rw, rd, dx, dy, dz in hoodie_sleeve_steps:
            cx = c_root_x + sign * (sin_a * s_dist + dx)
            cy = c_root_y + dy
            cz = c_root_z - (cos_a * s_dist - dz * 0.2)
            
            new_loop = []
            N = len(arm_loop)
            for k in range(N):
                v_orig = arm_loop[k]
                phi = (((k - 7) % N) / N) * 2.0 * math.pi
                ca = math.cos(phi)
                sa = math.sin(phi)
                
                px = cx + sign * (ca * rw * cos_a)
                py = cy + sa * rd
                pz = cz + (ca * rw * sin_a)
                
                ox = v_orig.co.x + sign * (sin_a * s_dist + dx)
                oy = v_orig.co.y + dy
                oz = v_orig.co.z + dz
                
                fx = (1.0 - t_blend) * ox + t_blend * px
                fy = (1.0 - t_blend) * oy + t_blend * py
                fz = (1.0 - t_blend) * oz + t_blend * pz
                new_loop.append(bm.verts.new((fx, fy, fz)))
                
            bm.verts.ensure_lookup_table()
            for k in range(N):
                knxt = (k + 1) % N
                if sign > 0:
                    bm.faces.new((prev_loop[k], prev_loop[knxt], new_loop[knxt], new_loop[k]))
                else:
                    bm.faces.new((prev_loop[k], new_loop[k], new_loop[knxt], prev_loop[knxt]))
            prev_loop = new_loop
            
        # Inward wrist cuff lining to cleanly enclose the sleeve
        inward_cuff = []
        for v in prev_loop:
            dx = v.co.x - cx
            dy = v.co.y - cy
            dz = v.co.z - cz
            inward_cuff.append(bm.verts.new((cx + dx * 0.82, cy + dy * 0.82, cz + dz * 0.82 + 0.020)))
        bm.verts.ensure_lookup_table()
        for k in range(N):
            knxt = (k + 1) % N
            if sign > 0:
                bm.faces.new((prev_loop[k], prev_loop[knxt], inward_cuff[knxt], inward_cuff[k]))
            else:
                bm.faces.new((prev_loop[k], inward_cuff[k], inward_cuff[knxt], prev_loop[knxt]))

    # -------------------------------------------------------------
    # B. Genuine 3D Extruded Streetwear Kangaroo Front Pouch
    # Spans 70% width, base width 0.36m, top width 0.26m, raised 16mm forward
    # -------------------------------------------------------------
    pouch_stations = [
        # (z, base_w, protrusion_forward, y_torso_level)
        (-0.40, 0.34, 0.004, -0.104), # 0: Waistband seam
        (-0.35, 0.36, 0.016, -0.120), # 1: Lower belly pouch volume
        (-0.26, 0.34, 0.018, -0.123), # 2: Mid pouch maximum forward depth
        (-0.18, 0.28, 0.014, -0.124), # 3: Upper pouch taper
        (-0.15, 0.24, 0.003, -0.124), # 4: Top seam flush to chest
    ]
    
    pouch_outer_mesh = []
    pouch_base_mesh = []
    P_COLS = 6
    
    for pz, pw, prot, yt in pouch_stations:
        row_out = []
        row_base = []
        for c in range(P_COLS):
            # t_c from -1.0 (left) to +1.0 (right)
            t_c = -1.0 + c * (2.0 / (P_COLS - 1))
            vx = t_c * (pw * 0.5)
            # Smooth cylindrical curvature across front
            curve_y = math.cos(t_c * math.pi * 0.45)
            yo = yt - prot * curve_y
            yb = yt - 0.002 * curve_y
            row_out.append(bm.verts.new((vx, yo, pz)))
            row_base.append(bm.verts.new((vx, yb, pz)))
        pouch_outer_mesh.append(row_out)
        pouch_base_mesh.append(row_base)
        
    bm.verts.ensure_lookup_table()
    
    # 1. Front face quads
    for r in range(len(pouch_stations) - 1):
        r0 = pouch_outer_mesh[r]
        r1 = pouch_outer_mesh[r + 1]
        for c in range(P_COLS - 1):
            bm.faces.new((r0[c], r0[c + 1], r1[c + 1], r1[c]))
            
    # 2. Bottom seam: weld outer bottom to torso base
    rb_out = pouch_outer_mesh[0]
    rb_base = pouch_base_mesh[0]
    for c in range(P_COLS - 1):
        bm.faces.new((rb_out[c], rb_base[c], rb_base[c + 1], rb_out[c + 1]))
        
    # 3. Top seam: weld outer top to torso base
    rt_out = pouch_outer_mesh[-1]
    rt_base = pouch_base_mesh[-1]
    for c in range(P_COLS - 1):
        bm.faces.new((rt_out[c], rt_out[c + 1], rt_base[c + 1], rt_base[c]))
        
    # 4. Diagonal side hand openings (c = 0 left, c = P_COLS-1 right)
    for r in range(len(pouch_stations) - 1):
        ro0 = pouch_outer_mesh[r]
        ro1 = pouch_outer_mesh[r + 1]
        rb0 = pouch_base_mesh[r]
        rb1 = pouch_base_mesh[r + 1]
        # Left side opening
        bm.faces.new((ro0[0], ro1[0], rb1[0], rb0[0]))
        # Right side opening
        bm.faces.new((ro0[-1], rb0[-1], rb1[-1], ro1[-1]))

    # -------------------------------------------------------------
    # C. Hood ("Back Cap") Seamlessly Attached to Collar & Scapula
    # Welded to back collar (Z = 0.52m), folded cowl resting on scapula,
    # terminating at Z = 0.36m (leaving back mural completely un-obscured)
    # -------------------------------------------------------------
    r9 = torso_rings[9]
    # Collar vertices: i = 6 is back center (+Y), i = 0 is front center (-Y)
    collar_back = [r9[3], r9[4], r9[5], r9[6], r9[7], r9[8], r9[9]]
    
    hood_profile = [
        # (z, width_x, y_center, thickness_y)
        (0.52, 0.114, 0.076, 0.024), # 0: Welded to back neckline
        (0.49, 0.150, 0.110, 0.032), # 1: Roll over cervical spine
        (0.44, 0.165, 0.126, 0.034), # 2: Upper scapula crest
        (0.39, 0.155, 0.128, 0.030), # 3: Mid-scapula main cowl fold
        (0.35, 0.120, 0.115, 0.022), # 4: Soft rounded cowl hem
    ]
    
    H_SEGS = 12
    h_rings = []
    for s_idx, (hz, hwx, hy_center, h_th) in enumerate(hood_profile):
        h_ring = []
        for i in range(H_SEGS):
            theta = i * (2.0 * math.pi / H_SEGS)
            ca = math.cos(theta)
            sa = math.sin(theta)
            vx = ca * hwx
            vy = hy_center + sa * h_th
            vz = hz + abs(ca) * 0.012
            h_ring.append(bm.verts.new((vx, vy, vz)))
        h_rings.append(h_ring)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge hood tubular rings
    for h in range(len(hood_profile) - 1):
        r0 = h_rings[h]
        r1 = h_rings[h + 1]
        for i in range(H_SEGS):
            inxt = (i + 1) % H_SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # Close bottom cowl fold
    bm.faces.new(h_rings[-1])
    
    # Bridge the hood base ring directly to the back collar seam of the torso
    hood_front_arc = [h_rings[0][9], h_rings[0][8], h_rings[0][7], h_rings[0][6], h_rings[0][5], h_rings[0][4], h_rings[0][3]]
    for ci in range(len(collar_back) - 1):
        bm.faces.new((collar_back[ci], collar_back[ci + 1], hood_front_arc[ci + 1], hood_front_arc[ci]))
        
    # Atelier Bust Stand
    stand_levels = [
        (-0.66, 0.150),
        (-0.50, 0.120),
        ( 0.44, 0.090),
        ( 0.58, 0.045),
        ( 0.62, 0.038),
    ]
    stand_rings = []
    for sz, sr in stand_levels:
        s_ring = []
        for i in range(16):
            ang = i * (2.0 * math.pi / 16)
            s_ring.append(bm.verts.new((math.cos(ang) * sr, math.sin(ang) * sr, sz)))
        stand_rings.append(s_ring)
        
    bm.verts.ensure_lookup_table()
    for s in range(len(stand_levels) - 1):
        for i in range(16):
            inxt = (i + 1) % 16
            bm.faces.new((stand_rings[s][i], stand_rings[s][inxt], stand_rings[s+1][inxt], stand_rings[s+1][i]))
    bm.faces.new(reversed(stand_rings[0]))
    bm.faces.new(stand_rings[-1])
    
    # Dual-Panel UV Mapping
    uv_layer = bm.loops.layers.uv.new("UVMap")
    for face in bm.faces:
        for loop in face.loops:
            v = loop.vert
            vx, vy, vz = v.co.x, v.co.y, v.co.z
            u_norm = max(0.0, min(1.0, (vx + 0.55) / 1.10))
            v_norm = max(0.0, min(1.0, (vz + 0.45) / 1.05))
            if vy <= 0.01:
                loop[uv_layer].uv = (u_norm * 0.48 + 0.01, v_norm * 0.96 + 0.02)
            else:
                loop[uv_layer].uv = (0.51 + (1.0 - u_norm) * 0.48, v_norm * 0.96 + 0.02)
                
    bm.to_mesh(mesh)
    bm.free()
    
    subsurf = hoodie.modifiers.new("Subsurf", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    for poly in mesh.polygons: poly.use_smooth = True
    
    if texture_path and os.path.exists(texture_path):
        mat = bpy.data.materials.new("Hoodie_Fabric_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(os.path.abspath(texture_path))
        mat.node_tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
        bsdf.inputs['Roughness'].default_value = 0.90
        bsdf.inputs['Specular IOR Level'].default_value = 0.10
        hoodie.data.materials.append(mat)
        
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False
    )
    print(f"Exported Masterpiece Hoodie: {out_glb_path}")
