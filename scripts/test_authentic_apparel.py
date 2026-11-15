import bpy
import bmesh
import math
import os

def create_debloated_boxy_tee():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Tee_Mesh")
    tee = bpy.data.objects.new("Tee_Model", mesh)
    bpy.context.collection.objects.link(tee)
    bpy.context.view_layer.objects.active = tee
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. ANATOMICALLY GROUNDED TORSO
    # Width across chest: 0.52m (rad 0.260m) - boxy streetwear cut
    # Depth: 0.210m (front 0.110m, back 0.100m) - debloated human frame!
    # Height: Z from -0.42 (hem) to +0.48 (collar base)
    # -------------------------------------------------------------
    SEGS = 24
    torso_levels = [
        # (z, x_rad, y_front, y_back, ripple_amp)
        (-0.42, 0.250, 0.105, 0.095, 0.002), # 0: Hem
        (-0.30, 0.245, 0.102, 0.092, 0.003), # 1: Lower torso / waist
        (-0.15, 0.250, 0.108, 0.096, 0.004), # 2: Mid torso
        ( 0.02, 0.258, 0.114, 0.102, 0.003), # 3: Lower chest
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
    
    # Bridge hem to armscye
    for r in range(5):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # Armscye gap at ring 5 -> 6
    # Left arm (+X): skip 22, 23, 0, 1, 2
    # Right arm (-X): skip 10, 11, 12, 13, 14
    r5 = torso_rings[5]
    r6 = torso_rings[6]
    for i in range(SEGS):
        inxt = (i + 1) % SEGS
        if i in (22, 23, 0, 1) or inxt in (23, 0, 1, 2): continue
        if i in (10, 11, 12, 13) or inxt in (11, 12, 13, 14): continue
        bm.faces.new((r5[i], r5[inxt], r6[inxt], r6[i]))
        
    # Shoulders and collar
    for r in range(6, len(torso_levels) - 1):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    bm.verts.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. NATURAL DRAPED SLEEVES (Angled downwards along gravity)
    # Extrude from armscye along arm vector (~48 deg downward)
    # -------------------------------------------------------------
    left_arm_loop_0 = [
        r5[22], r5[23], r5[0], r5[1], r5[2],
        r6[2], r6[1], r6[0], r6[23], r6[22]
    ]
    right_arm_loop_0 = [
        r5[14], r5[13], r5[12], r5[11], r5[10],
        r6[10], r6[11], r6[12], r6[13], r6[14]
    ]
    
    # Arm drape steps: 4 segments extending down toward elbow
    sleeve_steps = [
        (0.040, 0.002, -0.065, 0.96), # 1: Deltoid drape
        (0.080, 0.004, -0.135, 0.91), # 2: Mid bicep
        (0.115, 0.006, -0.205, 0.86), # 3: Lower bicep
        (0.145, 0.008, -0.270, 0.82), # 4: Above elbow hem
    ]
    
    for arm_loop, sign in [(left_arm_loop_0, 1.0), (right_arm_loop_0, -1.0)]:
        prev_loop = arm_loop
        for dx, dy, dz, sc in sleeve_steps:
            new_loop = []
            for v_orig in arm_loop:
                # Displace naturally along arm angle
                vx = v_orig.co.x + sign * dx
                vy = v_orig.co.y * sc + dy
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
            
    # Atelier Mannequin Stand
    man_levels = [
        (-0.65, 0.16, -0.02),
        (-0.45, 0.12,  0.00),
        ( 0.40, 0.10,  0.00),
        ( 0.58, 0.05,  0.00),
        ( 0.62, 0.04,  0.00),
    ]
    
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
    
    # Material
    mat = bpy.data.materials.new(name="Tee_Fabric")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.12, 0.12, 0.13, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.90
    tee.data.materials.append(mat)
    
    return tee

def create_debloated_draped_hoodie():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Hoodie_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Model", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. DEBLOATED HEAVYWEIGHT HOODIE TORSO
    # Width: 0.54m (rad 0.270m)
    # Depth: 0.220m (front 0.118m, back 0.102m)
    # -------------------------------------------------------------
    SEGS = 24
    torso_levels = [
        # (z, x_rad, y_front, y_back, ripple_amp)
        (-0.46, 0.235, 0.098, 0.088, 0.000), # 0: 3" Ribbed waistband bottom
        (-0.39, 0.240, 0.102, 0.092, 0.001), # 1: Ribbed waistband top
        (-0.33, 0.260, 0.118, 0.106, 0.004), # 2: Torso blousing above waistband
        (-0.16, 0.268, 0.122, 0.108, 0.005), # 3: Kangaroo pouch level
        ( 0.02, 0.272, 0.124, 0.108, 0.004), # 4: Mid chest
        ( 0.18, 0.275, 0.120, 0.104, 0.003), # 5: Chest graphic
        ( 0.32, 0.285, 0.115, 0.098, 0.002), # 6: Armscye bottom
        ( 0.42, 0.305, 0.106, 0.092, 0.001), # 7: Dropped shoulder seam
        ( 0.48, 0.200, 0.096, 0.084, 0.000), # 8: Collar base
        ( 0.52, 0.105, 0.082, 0.072, 0.000), # 9: Hood attachment neckline
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
            
    bm.verts.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. LONG DRAPED SLEEVES WITH WRIST CUFF
    # -------------------------------------------------------------
    left_arm_loop_0 = [
        r6[22], r6[23], r6[0], r6[1], r6[2],
        r7[2], r7[1], r7[0], r7[23], r7[22]
    ]
    right_arm_loop_0 = [
        r6[14], r6[13], r6[12], r6[11], r6[10],
        r7[10], r7[11], r7[12], r7[13], r7[14]
    ]
    
    long_sleeve_steps = [
        (0.045, 0.003, -0.075, 0.95), # Upper arm
        (0.090, 0.006, -0.155, 0.90), # Mid bicep
        (0.130, 0.012, -0.240, 0.85), # Elbow (slight forward bend)
        (0.165, 0.016, -0.325, 0.79), # Forearm
        (0.190, 0.018, -0.405, 0.74), # Wrist gather
        (0.205, 0.020, -0.465, 0.65), # 3" Ribbed cuff
    ]
    
    for arm_loop, sign in [(left_arm_loop_0, 1.0), (right_arm_loop_0, -1.0)]:
        prev_loop = arm_loop
        for dx, dy, dz, sc in long_sleeve_steps:
            new_loop = []
            for v_orig in arm_loop:
                vx = v_orig.co.x + sign * dx
                vy = v_orig.co.y * sc + dy
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
    # 3. 3D KANGAROO POUCH
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
    # 4. HOODIE "BACK CAP" (Draped Hood Hanging Down the Upper Back)
    # The hood originates from the neckline (Z=0.52, Y=0.07)
    # It curls BACKWARDS (+Y) and DOWNWARDS (-Z) across the upper back!
    # It hangs from Z=0.52 down to Z=0.32 in a relaxed crescent fold,
    # leaving the front collar completely open to showcase the chest graphic!
    # -------------------------------------------------------------
    hood_drape_stations = [
        # (z, x_width, y_front_collar, y_back_drape)
        (0.52, 0.105, 0.075, 0.075), # Station 0: Neckline seam
        (0.50, 0.130, 0.065, 0.125), # Station 1: Rolling over back of neck
        (0.45, 0.145, 0.055, 0.170), # Station 2: Draping down upper scapula
        (0.39, 0.150, 0.045, 0.195), # Station 3: Mid-back fold
        (0.34, 0.140, 0.040, 0.200), # Station 4: Lower pouch drape
        (0.31, 0.110, 0.035, 0.180), # Station 5: Bottom hood tip
    ]
    
    H_SEGS = 16
    h_rings = []
    for hz, hxw, hy_front, hy_back in hood_drape_stations:
        ring = []
        for i in range(H_SEGS):
            ang = i * (2.0 * math.pi / H_SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            
            vx = ca * hxw
            # sa > 0 is back drape (+Y), sa <= 0 is front collar rim
            if sa >= 0:
                vy = hy_back + (sa - 1.0) * 0.02
            else:
                vy = hy_front + sa * 0.015
                
            ring.append(bm.verts.new((vx, vy, hz)))
        h_rings.append(ring)
        
    bm.verts.ensure_lookup_table()
    for h in range(len(hood_drape_stations) - 1):
        r0 = h_rings[h]
        r1 = h_rings[h + 1]
        for i in range(H_SEGS):
            inxt = (i + 1) % H_SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # Cap bottom hood fold
    bm.faces.new(h_rings[-1])
    
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
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.10, 0.10, 0.11, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.92
    hoodie.data.materials.append(mat)
    
    return hoodie

def test_renders(out_dir):
    # 1. Render Tee
    create_debloated_boxy_tee()
    bpy.ops.object.light_add(type='SUN', location=(1.5, -2.0, 3.0))
    sun = bpy.context.active_object
    sun.data.energy = 3.5
    bpy.ops.object.light_add(type='POINT', location=(-1.2, 1.5, 1.5))
    fill = bpy.context.active_object
    fill.data.energy = 40.0
    
    bpy.ops.object.camera_add(location=(0, -2.2, 0.05))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = cam
    
    scene = bpy.context.scene
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.render.filepath = os.path.join(out_dir, "test_render_debloated_tee.png")
    bpy.ops.render.render(write_still=True)
    
    # 2. Render Hoodie Front & 3/4 Back
    create_debloated_draped_hoodie()
    bpy.ops.object.light_add(type='SUN', location=(1.5, -2.0, 3.0))
    sun = bpy.context.active_object
    sun.data.energy = 3.5
    bpy.ops.object.light_add(type='POINT', location=(-1.2, 1.5, 1.5))
    fill = bpy.context.active_object
    fill.data.energy = 40.0
    
    # Front
    bpy.ops.object.camera_add(location=(0, -2.2, 0.05))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = cam
    scene = bpy.context.scene
    scene.render.filepath = os.path.join(out_dir, "test_render_draped_hoodie_front.png")
    bpy.ops.render.render(write_still=True)
    
    # Back 3/4 Angle to inspect the "back cap" hood drape
    bpy.ops.object.camera_add(location=(1.4, 1.8, 0.35))
    cam_back = bpy.context.active_object
    cam_back.rotation_euler = (math.radians(80), 0, math.radians(145))
    bpy.context.scene.camera = cam_back
    scene.render.filepath = os.path.join(out_dir, "test_render_draped_hoodie_back.png")
    bpy.ops.render.render(write_still=True)
    
    print("All test apparel renders saved.")

if __name__ == "__main__":
    out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
    test_renders(out_dir)
