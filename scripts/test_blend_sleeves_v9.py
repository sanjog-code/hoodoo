import bpy
import bmesh
import math
import os

def test_sleeve_v9():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh = bpy.data.meshes.new("Tee_Mesh")
    obj = bpy.data.objects.new("Tee_Model", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bm = bmesh.new()
    
    SEGS = 24
    torso_levels = [
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
        
    # Bridge levels 6 to 9
    for r in range(6, len(torso_levels) - 1):
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((torso_rings[r][i], torso_rings[r][inxt], torso_rings[r+1][inxt], torso_rings[r+1][i]))
            
    bm.verts.ensure_lookup_table()
    
    # Armscye loops:
    # Left (+X):
    left_arm_loop = [
        r5[22], r5[23], r5[0], r5[1], r5[2],
        r6[2], r6[1], r6[0], r6[23], r6[22]
    ]
    # Right (-X):
    right_arm_loop = [
        r5[14], r5[13], r5[12], r5[11], r5[10],
        r6[10], r6[11], r6[12], r6[13], r6[14]
    ]
    
    arm_angle = math.radians(24.0)
    sin_a = math.sin(arm_angle)
    cos_a = math.cos(arm_angle)
    
    sleeve_steps = [
        # (s_dist, t_blend, r_w, r_d)
        (0.045, 0.40, 0.120, 0.114), # 1: Deltoid
        (0.105, 0.70, 0.116, 0.110), # 2: Upper bicep
        (0.170, 0.90, 0.112, 0.106), # 3: Mid bicep
        (0.235, 1.00, 0.108, 0.102), # 4: Boxy hem cut (100% planar)
        (0.245, 1.00, 0.105, 0.098), # 5: Clean inward hem fold
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
                
                # Zero-twist angle alignment:
                # k=7 is shoulder (+W), k=2 is armpit (-W), k=9 is back (+Y), k=4 is front (-Y)
                if sign > 0:
                    phi = (((k - 7) % N) / N) * 2.0 * math.pi
                    ca = math.cos(phi)
                    sa = math.sin(phi)
                    px = cx + sign * (ca * rw * cos_a)
                    py = cy + sa * rd
                    pz = cz + (ca * rw * sin_a)
                else:
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
    
    subsurf = obj.modifiers.new("Subsurf", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    cam_data = bpy.data.cameras.new("Cam")
    cam_obj = bpy.data.objects.new("Cam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = (0.0, -1.8, 0.05)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    
    light_data = bpy.data.lights.new("Sun", type='SUN')
    light_data.energy = 3.5
    light_obj = bpy.data.objects.new("Sun", light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (1.5, -2.0, 2.0)
    light_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(25))
    
    fill_data = bpy.data.lights.new("Fill", type='SUN')
    fill_data.energy = 1.8
    fill_obj = bpy.data.objects.new("Fill", fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-1.5, 2.0, 1.0)
    fill_obj.rotation_euler = (math.radians(-35), math.radians(-20), math.radians(-145))
    
    out_render = os.path.expanduser("~/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/test_render_tee_v9.png")
    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 1200
    bpy.context.scene.render.filepath = out_render
    bpy.ops.render.render(write_still=True)
    print("Rendered tee v9 successfully!")

test_sleeve_v9()
