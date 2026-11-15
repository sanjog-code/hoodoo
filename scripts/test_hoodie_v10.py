import bpy
import bmesh
import math
import os

def build_hoodie_v10(out_glb_path, out_render_front, out_render_back):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh = bpy.data.meshes.new("Hoodie_Mesh")
    obj = bpy.data.objects.new("Hoodie_Model", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. TORSO & WAISTBAND (Heavy 500GSM Streetwear Silhouette)
    # -------------------------------------------------------------
    SEGS = 24
    torso_levels = [
        # (z, x_rad, y_front, y_back, ripple_amp)
        (-0.46, 0.225, 0.100, 0.088, 0.000), # 0: 3" Ribbed waistband bottom
        (-0.40, 0.230, 0.102, 0.090, 0.000), # 1: Waistband top
        (-0.35, 0.260, 0.118, 0.102, 0.006), # 2: Torso pooling over band
        (-0.18, 0.265, 0.122, 0.105, 0.005), # 3: Mid abdomen
        ( 0.02, 0.272, 0.124, 0.108, 0.004), # 4: Mid chest
        ( 0.18, 0.275, 0.120, 0.104, 0.003), # 5: Chest graphic
        ( 0.32, 0.285, 0.115, 0.098, 0.002), # 6: Armscye bottom (armpit)
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
    
    # Bridge torso levels 0 to 6
    for r in range(6):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # Bridge level 6 to 7 excluding arm openings
    r6 = torso_rings[6]
    r7 = torso_rings[7]
    for i in range(SEGS):
        inxt = (i + 1) % SEGS
        # Left opening (+X)
        if i in (22, 23, 0, 1) or inxt in (23, 0, 1, 2): continue
        # Right opening (-X)
        if i in (10, 11, 12, 13) or inxt in (11, 12, 13, 14): continue
        bm.faces.new((r6[i], r6[inxt], r7[inxt], r7[i]))
        
    # Bridge levels 7 to 9
    for r in range(7, len(torso_levels) - 1):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    bm.verts.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. FULL-LENGTH OVERSIZED STREETWEAR SLEEVES (To z = -0.62m)
    # -------------------------------------------------------------
    left_arm_loop = [
        r6[22], r6[23], r6[0], r6[1], r6[2],
        r7[2], r7[1], r7[0], r7[23], r7[22]
    ]
    right_arm_loop = [
        r6[14], r6[13], r6[12], r6[11], r6[10],
        r7[10], r7[11], r7[12], r7[13], r7[14]
    ]
    
    # Sleeve hangs inward naturally alongside torso
    # Reaching down past hem (-0.46) to wrists at z = -0.62m
    hoodie_sleeve_steps = [
        # (s_dist, t_blend, r_w, r_d, dx, dy, dz)
        (0.060, 0.40, 0.126, 0.120, 0.015, 0.005, -0.065), # 1: Deltoid
        (0.140, 0.70, 0.128, 0.122, 0.030, 0.010, -0.155), # 2: Upper bicep
        (0.230, 0.90, 0.125, 0.120, 0.038, 0.015, -0.250), # 3: Elbow crease
        (0.320, 1.00, 0.122, 0.116, 0.040, 0.018, -0.345), # 4: Forearm
        (0.420, 1.00, 0.118, 0.112, 0.036, 0.020, -0.440), # 5: Lower forearm (waistband level)
        (0.510, 1.00, 0.110, 0.104, 0.028, 0.022, -0.530), # 6: Wrist stacking
        (0.580, 1.00, 0.095, 0.088, 0.018, 0.023, -0.590), # 7: Cuff gather
        (0.615, 1.00, 0.068, 0.062, 0.012, 0.024, -0.620), # 8: Ribbed elastic wrist cuff
        (0.630, 1.00, 0.065, 0.060, 0.010, 0.024, -0.635), # 9: Cuff rim
    ]
    
    arm_angle = math.radians(16.0) # Sleek natural downward hang
    sin_a = math.sin(arm_angle)
    cos_a = math.cos(arm_angle)
    
    for arm_loop, sign in [(left_arm_loop, 1.0), (right_arm_loop, -1.0)]:
        c_root_x = sign * 0.295
        c_root_y = 0.005
        c_root_z = 0.370
        
        prev_loop = arm_loop
        for s_dist, t_blend, rw, rd, dx, dy, dz in hoodie_sleeve_steps:
            # Shift center downwards along sleeve curve
            cx = c_root_x + sign * (sin_a * s_dist + dx)
            cy = c_root_y + dy
            cz = c_root_z - (cos_a * s_dist - dz * 0.2)
            
            new_loop = []
            N = len(arm_loop)
            for k in range(N):
                v_orig = arm_loop[k]
                
                # Zero-twist angle alignment
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
            
    # -------------------------------------------------------------
    # 3. 3D KANGAROO FRONT POUCH
    # -------------------------------------------------------------
    kp_levels = [
        (-0.38, 0.21, 0.126),
        (-0.26, 0.24, 0.138),
        (-0.14, 0.18, 0.130),
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
    # 4. HOOD ("BACK CAP") SITTING NATURALLY ON THE BACK SIDE
    # Flush cowl drape against the upper back / scapula!
    # Does NOT stick out like a balloon; drapes gracefully down the spine.
    # -------------------------------------------------------------
    hood_stations = [
        # (z, width_x, y_drape, thickness)
        (0.51, 0.120, 0.082, 0.022), # 0: Nape of neck (collar seam)
        (0.48, 0.155, 0.110, 0.030), # 1: Roll over neck curve
        (0.42, 0.170, 0.128, 0.034), # 2: Upper scapula crest
        (0.35, 0.165, 0.132, 0.032), # 3: Mid-scapula main fold
        (0.28, 0.145, 0.125, 0.026), # 4: Lower back drape
        (0.22, 0.100, 0.112, 0.018), # 5: Bottom cowl crescent tip
    ]
    
    H_SEGS = 12
    h_rings = []
    for hz, hwx, hy_center, h_th in hood_stations:
        h_ring = []
        for i in range(H_SEGS):
            # Form an ellipse on the back side of the neck/back
            theta = i * (2.0 * math.pi / H_SEGS)
            ca = math.cos(theta)
            sa = math.sin(theta)
            vx = ca * hwx
            # sa > 0 is outer layer of fold, sa < 0 is inner layer touching the back
            vy = hy_center + sa * h_th
            vz = hz + abs(ca) * 0.015 # natural curve across the shoulders
            h_ring.append(bm.verts.new((vx, vy, vz)))
        h_rings.append(h_ring)
        
    bm.verts.ensure_lookup_table()
    for h in range(len(hood_stations) - 1):
        r0 = h_rings[h]
        r1 = h_rings[h + 1]
        for i in range(H_SEGS):
            inxt = (i + 1) % H_SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
    # Cap bottom crescent
    bm.faces.new(h_rings[-1])
    
    # -------------------------------------------------------------
    # 5. ATELIER BUST STAND
    # -------------------------------------------------------------
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
            v_norm = max(0.0, min(1.0, (vz + 0.50) / 1.15))
            if vy <= 0.01:
                loop[uv_layer].uv = (u_norm * 0.48 + 0.01, v_norm * 0.96 + 0.02)
            else:
                loop[uv_layer].uv = (0.51 + (1.0 - u_norm) * 0.48, v_norm * 0.96 + 0.02)
                
    bm.to_mesh(mesh)
    bm.free()
    
    subsurf = obj.modifiers.new("Subsurf", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False
    )
    print(f"Exported Hoodie GLB: {out_glb_path}")
    
    # Setup camera & lights
    cam_data = bpy.data.cameras.new("Cam")
    cam_obj = bpy.data.objects.new("Cam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    light_data = bpy.data.lights.new("Sun", type='SUN')
    light_data.energy = 3.5
    light_obj = bpy.data.objects.new("Sun", light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (1.5, -2.0, 2.0)
    light_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(25))
    
    fill_data = bpy.data.lights.new("Fill", type='SUN')
    fill_data.energy = 2.0
    fill_obj = bpy.data.objects.new("Fill", fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-1.5, 2.5, 1.5)
    fill_data.energy = 4.0
    fill_obj.rotation_euler = (math.radians(50), 0, math.radians(180))
    
    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 1200
    
    # 1. Front view
    cam_obj.location = (0.0, -2.1, 0.0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.render.filepath = out_render_front
    bpy.ops.render.render(write_still=True)
    print(f"Saved Front Render: {out_render_front}")
    
    # 2. Back 3/4 view (shows the hood sitting on the back side + sleeve drape)
    cam_obj.location = (0.0, 2.1, 0.10)
    cam_obj.rotation_euler = (math.radians(90), 0, math.radians(180))
    bpy.context.scene.render.filepath = out_render_back
    bpy.ops.render.render(write_still=True)
    print(f"Saved Back Render: {out_render_back}")

if __name__ == '__main__':
    out_glb = "public/models/hoodie_master.glb"
    front_png = os.path.expanduser("~/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/test_render_hoodie_v10_front.png")
    back_png = os.path.expanduser("~/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/test_render_hoodie_v10_back.png")
    build_hoodie_v10(out_glb, front_png, back_png)
