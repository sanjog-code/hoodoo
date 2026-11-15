import bpy
import bmesh
import math
import os

def create_perfect_tee(out_glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh = bpy.data.meshes.new("Tee_Mesh")
    tee = bpy.data.objects.new("Tee_Model", mesh)
    bpy.context.collection.objects.link(tee)
    bpy.context.view_layer.objects.active = tee
    bm = bmesh.new()
    
    # Anatomical Torso
    SEGS = 24
    torso_levels = [
        # (z, x_rad, y_front, y_back, ripple_amp)
        (-0.42, 0.248, 0.105, 0.095, 0.002), # 0: Hem
        (-0.28, 0.244, 0.102, 0.092, 0.003), # 1: Waist
        (-0.14, 0.250, 0.108, 0.096, 0.004), # 2: Mid torso
        ( 0.04, 0.258, 0.114, 0.102, 0.003), # 3: Lower chest
        ( 0.18, 0.265, 0.118, 0.104, 0.002), # 4: Chest graphic center
        ( 0.30, 0.275, 0.114, 0.100, 0.002), # 5: Armscye bottom
        ( 0.40, 0.295, 0.105, 0.092, 0.001), # 6: Dropped shoulder seam
        ( 0.46, 0.190, 0.095, 0.082, 0.000), # 7: Shoulder slope (20 deg)
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
    for r in range(5):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # Armscye gap 5 -> 6
    r5 = torso_rings[5]
    r6 = torso_rings[6]
    for i in range(SEGS):
        inxt = (i + 1) % SEGS
        if i in (22, 23, 0, 1) or inxt in (23, 0, 1, 2): continue
        if i in (10, 11, 12, 13) or inxt in (11, 12, 13, 14): continue
        bm.faces.new((r5[i], r5[inxt], r6[inxt], r6[i]))
        
    for r in range(6, len(torso_levels) - 1):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    bm.verts.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # SEAMLESS ROOMY CYLINDRICAL BOXY TEE SLEEVES
    # -------------------------------------------------------------
    left_arm_loop_0 = [
        r5[22], r5[23], r5[0], r5[1], r5[2],
        r6[2], r6[1], r6[0], r6[23], r6[22]
    ]
    right_arm_loop_0 = [
        r5[14], r5[13], r5[12], r5[11], r5[10],
        r6[10], r6[11], r6[12], r6[13], r6[14]
    ]
    
    # Natural ~22 deg downward hang, maintaining wide cylindrical volume
    tee_sleeve_steps = [
        # (dx, dy, dz, sc_x, sc_y)
        (0.020, 0.005, -0.065, 1.02, 1.30), # 1: Deltoid
        (0.040, 0.010, -0.135, 1.04, 1.45), # 2: Mid bicep
        (0.058, 0.015, -0.205, 1.06, 1.55), # 3: Above elbow
        (0.075, 0.018, -0.270, 1.08, 1.60), # 4: Boxy sleeve hem
        (0.078, 0.018, -0.285, 1.06, 1.58), # 5: Clean hem band (straight down)
    ]
    
    for arm_loop, sign in [(left_arm_loop_0, 1.0), (right_arm_loop_0, -1.0)]:
        prev_loop = arm_loop
        for dx, dy, dz, sc_x, sc_y in tee_sleeve_steps:
            new_loop = []
            for v_orig in arm_loop:
                vx = v_orig.co.x * sc_x + sign * dx
                vy = v_orig.co.y * sc_y + dy
                vz = v_orig.co.z + dz
                new_loop.append(bm.verts.new((vx, vy, vz)))
            bm.verts.ensure_lookup_table()
            
            N = len(prev_loop)
            for k in range(N):
                knxt = (k + 1) % N
                if sign > 0:
                    bm.faces.new((prev_loop[k], prev_loop[knxt], new_loop[knxt], new_loop[k]))
                else:
                    bm.faces.new((prev_loop[k], new_loop[k], new_loop[knxt], prev_loop[knxt]))
            prev_loop = new_loop
            
    # Atelier Bust Stand
    stand_levels = [
        (-0.62, 0.150, 0.00),
        (-0.46, 0.120, 0.00),
        ( 0.42, 0.090, 0.00),
        ( 0.56, 0.045, 0.00),
        ( 0.60, 0.038, 0.00),
    ]
    stand_rings = []
    for sz, sr, _ in stand_levels:
        s_ring = []
        for i in range(16):
            ang = i * (2.0 * math.pi / 16)
            s_ring.append(bm.verts.new((math.cos(ang) * sr, math.sin(ang) * sr, sz)))
        stand_rings.append(s_ring)
        
    bm.verts.ensure_lookup_table()
    for s in range(len(stand_levels) - 1):
        r0 = stand_rings[s]
        r1 = stand_rings[s + 1]
        for i in range(16):
            inxt = (i + 1) % 16
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
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
    
    bpy.ops.object.select_all(action='DESELECT')
    tee.select_set(True)
    bpy.context.view_layer.objects.active = tee
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    subsurf = tee.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    
    mat = bpy.data.materials.new(name="Tee_Fabric")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.88, 0.86, 0.84, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.88
    tee.data.materials.append(mat)
    
    os.makedirs(os.path.dirname(os.path.abspath(out_glb_path)), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=out_glb_path, export_format='GLB', use_selection=True, export_apply=True)
    print(f"Exported perfect tee to {out_glb_path}")
    return tee


def create_perfect_hoodie(out_glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh = bpy.data.meshes.new("Hoodie_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Model", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    bm = bmesh.new()
    
    # Anatomic Torso
    SEGS = 24
    torso_levels = [
        # (z, x_rad, y_front, y_back, ripple_amp)
        (-0.46, 0.235, 0.098, 0.088, 0.000), # 0: 3" Ribbed waistband bottom
        (-0.39, 0.240, 0.102, 0.092, 0.001), # 1: Ribbed waistband top
        (-0.33, 0.260, 0.118, 0.106, 0.004), # 2: Torso blousing
        (-0.16, 0.268, 0.122, 0.108, 0.005), # 3: Kangaroo pouch level
        ( 0.02, 0.272, 0.124, 0.108, 0.004), # 4: Mid chest
        ( 0.18, 0.275, 0.120, 0.104, 0.003), # 5: Chest graphic
        ( 0.32, 0.285, 0.115, 0.098, 0.002), # 6: Armscye bottom
        ( 0.42, 0.305, 0.106, 0.092, 0.001), # 7: Dropped shoulder seam
        ( 0.48, 0.200, 0.096, 0.084, 0.000), # 8: Collar base
        ( 0.52, 0.110, 0.084, 0.074, 0.000), # 9: Hood neckline
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
    for r in range(6):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # Armscye gap 6 -> 7
    r6 = torso_rings[6]
    r7 = torso_rings[7]
    for i in range(SEGS):
        inxt = (i + 1) % SEGS
        if i in (22, 23, 0, 1) or inxt in (23, 0, 1, 2): continue
        if i in (10, 11, 12, 13) or inxt in (11, 12, 13, 14): continue
        bm.faces.new((r6[i], r6[inxt], r7[inxt], r7[i]))
        
    for r in range(7, len(torso_levels) - 1):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # -------------------------------------------------------------
    # LONG FULL-LENGTH STACKED SLEEVES (Natural inward hang to Z = -0.62m)
    # Reaching past torso waistband with accordion fabric bunching
    # -------------------------------------------------------------
    left_arm_loop_0 = [
        r6[22], r6[23], r6[0], r6[1], r6[2],
        r7[2], r7[1], r7[0], r7[23], r7[22]
    ]
    right_arm_loop_0 = [
        r6[14], r6[13], r6[12], r6[11], r6[10],
        r7[10], r7[11], r7[12], r7[13], r7[14]
    ]
    
    # 7 articulated stations hanging naturally close to the hips
    hoodie_sleeve_steps = [
        # (dx, dy, dz, sc_x, sc_y, ripple)
        (0.015, 0.005, -0.075, 1.02, 1.25, 0.000), # 1: Bicep
        (0.025, 0.010, -0.165, 1.04, 1.40, 0.004), # 2: Mid bicep
        (0.030, 0.016, -0.260, 1.06, 1.50, 0.008), # 3: Elbow crease
        (0.030, 0.020, -0.360, 1.08, 1.55, 0.012), # 4: Forearm stack
        (0.025, 0.022, -0.460, 1.06, 1.45, 0.014), # 5: Lower forearm (at waistband)
        (0.018, 0.024, -0.550, 0.95, 1.25, 0.010), # 6: Wrist gather
        (0.012, 0.025, -0.620, 0.60, 0.80, 0.000), # 7: 3" Ribbed elastic wrist cuff
    ]
    
    for arm_loop, sign in [(left_arm_loop_0, 1.0), (right_arm_loop_0, -1.0)]:
        prev_loop = arm_loop
        for dx, dy, dz, sc_x, sc_y, ripple in hoodie_sleeve_steps:
            new_loop = []
            for k_idx, v_orig in enumerate(arm_loop):
                ang = k_idx * (2.0 * math.pi / len(arm_loop))
                r_add = ripple * math.sin(ang * 2.0 + dz * 20.0)
                
                vx = v_orig.co.x * sc_x + sign * dx
                vy = v_orig.co.y * sc_y + dy + r_add
                vz = v_orig.co.z + dz
                new_loop.append(bm.verts.new((vx, vy, vz)))
            bm.verts.ensure_lookup_table()
            
            N = len(prev_loop)
            for k in range(N):
                knxt = (k + 1) % N
                if sign > 0:
                    bm.faces.new((prev_loop[k], prev_loop[knxt], new_loop[knxt], new_loop[k]))
                else:
                    bm.faces.new((prev_loop[k], new_loop[k], new_loop[knxt], prev_loop[knxt]))
            prev_loop = new_loop
            
    # -------------------------------------------------------------
    # 3D KANGAROO POUCH
    # -------------------------------------------------------------
    kp_levels = [
        (-0.35, 0.22, 0.126),
        (-0.25, 0.25, 0.138),
        (-0.15, 0.18, 0.130),
    ]
    kp_rings = []
    for kz, kw, ky in kp_levels:
        v0 = bm.verts.new((-kw * 0.5, -ky, kz))
        v1 = bm.verts.new((-kw * 0.2, -ky - 0.007, kz))
        v2 = bm.verts.new(( kw * 0.2, -ky - 0.007, kz))
        v3 = bm.verts.new(( kw * 0.5, -ky, kz))
        kp_rings.append((v0, v1, v2, v3))
        
    bm.verts.ensure_lookup_table()
    for k in range(len(kp_levels) - 1):
        r0 = kp_rings[k]
        r1 = kp_rings[k + 1]
        for xi in range(3):
            bm.faces.new((r0[xi], r0[xi + 1], r1[xi + 1], r1[xi]))
            
    # -------------------------------------------------------------
    # VOLUMETRIC SCAPULA-DRAPED HOOD (Resting Flush Against the Upper Back)
    # The hood rolls over the nape (z=0.52 to 0.54) and drapes DOWN the scapula
    # to z = 0.22m, resting gently against the back fabric (y = 0.09 to 0.15m)!
    # -------------------------------------------------------------
    HOOD_RING_SEGS = 18
    hood_stations = [
        # (z, width_x, front_collar_y, back_drape_y)
        (0.52, 0.115, -0.075, 0.075), # 0: Collar rim
        (0.51, 0.145, -0.065, 0.115), # 1: Roll over nape
        (0.46, 0.165, -0.045, 0.145), # 2: Upper scapula
        (0.39, 0.170, -0.030, 0.155), # 3: Mid-back fold
        (0.32, 0.155, -0.020, 0.150), # 4: Lower fold
        (0.25, 0.125, -0.010, 0.138), # 5: Lower crescent tip
        (0.22, 0.080, -0.005, 0.120), # 6: Bottom seam
    ]
    
    h_rings = []
    for hz, hwx, hy_front, hy_back in hood_stations:
        ring = []
        for i in range(HOOD_RING_SEGS):
            ang = i * (2.0 * math.pi / HOOD_RING_SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            vx = ca * hwx
            if sa >= 0:
                vy = hy_back + sa * 0.015
            else:
                vy = hy_front + sa * 0.010
            vy += 0.004 * math.sin(ang * 3.0 + hz * 10.0)
            ring.append(bm.verts.new((vx, vy, hz)))
        h_rings.append(ring)
        
    bm.verts.ensure_lookup_table()
    for h in range(len(hood_stations) - 1):
        r0 = h_rings[h]
        r1 = h_rings[h + 1]
        for i in range(HOOD_RING_SEGS):
            inxt = (i + 1) % HOOD_RING_SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
    bm.faces.new(h_rings[-1])
    
    # Atelier Bust Stand
    stand_levels = [
        (-0.64, 0.150, 0.00),
        (-0.48, 0.120, 0.00),
        ( 0.44, 0.090, 0.00),
        ( 0.58, 0.045, 0.00),
        ( 0.62, 0.038, 0.00),
    ]
    stand_rings = []
    for sz, sr, _ in stand_levels:
        s_ring = []
        for i in range(16):
            ang = i * (2.0 * math.pi / 16)
            s_ring.append(bm.verts.new((math.cos(ang) * sr, math.sin(ang) * sr, sz)))
        stand_rings.append(s_ring)
        
    bm.verts.ensure_lookup_table()
    for s in range(len(stand_levels) - 1):
        r0 = stand_rings[s]
        r1 = stand_rings[s + 1]
        for i in range(16):
            inxt = (i + 1) % 16
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
    bm.faces.new(reversed(stand_rings[0]))
    bm.faces.new(stand_rings[-1])
    
    # Dual-Panel UV Mapping
    uv_layer = bm.loops.layers.uv.new("UVMap")
    for face in bm.faces:
        for loop in face.loops:
            v = loop.vert
            vx, vy, vz = v.co.x, v.co.y, v.co.z
            u_norm = max(0.0, min(1.0, (vx + 0.60) / 1.20))
            v_norm = max(0.0, min(1.0, (vz + 0.50) / 1.15))
            if vy <= 0.01:
                loop[uv_layer].uv = (u_norm * 0.48 + 0.01, v_norm * 0.96 + 0.02)
            else:
                loop[uv_layer].uv = (0.51 + (1.0 - u_norm) * 0.48, v_norm * 0.96 + 0.02)
                
    bm.to_mesh(mesh)
    bm.free()
    
    bpy.ops.object.select_all(action='DESELECT')
    hoodie.select_set(True)
    bpy.context.view_layer.objects.active = hoodie
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    subsurf = hoodie.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    
    mat = bpy.data.materials.new(name="Hoodie_Fabric")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.88, 0.86, 0.84, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.92
    hoodie.data.materials.append(mat)
    
    os.makedirs(os.path.dirname(os.path.abspath(out_glb_path)), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=out_glb_path, export_format='GLB', use_selection=True, export_apply=True)
    print(f"Exported perfect hoodie to {out_glb_path}")
    return hoodie
