import bpy
import bmesh
import math
import os

def build_perfect_tee(out_glb_path, out_render_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh = bpy.data.meshes.new("Tee_Mesh")
    obj = bpy.data.objects.new("Tee_Model", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. TORSO GEOMETRY (Boxy Streetwear Fit)
    # -------------------------------------------------------------
    SEGS = 24
    torso_levels = [
        # (z, x_rad, y_front, y_back, ripple)
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
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # Bridge level 5 to 6 excluding arm openings:
    # Left opening (+X): indices 22, 23, 0, 1, 2
    # Right opening (-X): indices 10, 11, 12, 13, 14
    r5 = torso_rings[5]
    r6 = torso_rings[6]
    for i in range(SEGS):
        inxt = (i + 1) % SEGS
        if i in (22, 23, 0, 1) or inxt in (23, 0, 1, 2):
            continue
        if i in (10, 11, 12, 13) or inxt in (11, 12, 13, 14):
            continue
        bm.faces.new((r5[i], r5[inxt], r6[inxt], r6[i]))
        
    # Bridge levels 6 to 9
    for r in range(6, len(torso_levels) - 1):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[inxt], r1[inxt], r1[i]))
            
    # -------------------------------------------------------------
    # 2. SEAMLESS, ROOMY CYLINDRICAL BOXY TEE SLEEVES
    # -------------------------------------------------------------
    # Each sleeve has planar, perfectly perpendicular circular/elliptical rings.
    # To connect seamlessly to the armscye opening (which has 8 boundary verts on each side),
    # we use 8 segments per sleeve ring, matching the armscye topology 1:1!
    
    arm_angle = math.radians(22.0) # 22 degrees downward drape
    sin_a = math.sin(arm_angle)
    cos_a = math.cos(arm_angle)
    
    # 8-segment armscye loops:
    # Left arm (+X):
    # Front-to-back: r5[23], r5[0], r5[1], r6[1], r6[0], r6[23], r6[22], r5[22]
    left_armscye_loop = [
        r5[23], r5[0], r5[1],
        r6[1], r6[0], r6[23], r6[22],
        r5[22]
    ]
    # Right arm (-X):
    # Front-to-back: r5[11], r5[12], r5[13], r6[13], r6[12], r6[11], r6[10], r5[10]
    right_armscye_loop = [
        r5[11], r5[12], r5[13],
        r6[13], r6[12], r6[11], r6[10],
        r5[10]
    ]
    
    # Sleeve stations along the 22-deg arm axis:
    # distance along axis, radius_width (cross-section), radius_depth (Y)
    sleeve_stations = [
        # (dist, r_w, r_d)
        (0.045, 0.108, 0.102), # 1: Deltoid contour
        (0.110, 0.105, 0.098), # 2: Upper bicep
        (0.180, 0.102, 0.094), # 3: Mid bicep
        (0.245, 0.098, 0.090), # 4: Forearm hem opening (boxy planar cutoff)
        (0.255, 0.095, 0.088), # 5: Clean inward hem fold
    ]
    
    for armscye_loop, sign in [(left_armscye_loop, 1.0), (right_armscye_loop, -1.0)]:
        # Root origin for the arm axis
        c_root_x = sign * 0.285
        c_root_y = 0.005
        c_root_z = 0.355
        
        prev_loop = armscye_loop
        for s_dist, rw, rd in sleeve_stations:
            # Center of the planar cross-section
            cx = c_root_x + sign * (sin_a * s_dist)
            cy = c_root_y
            cz = c_root_z - (cos_a * s_dist)
            
            # Basis vectors:
            # Arm vector A = (sign * sin_a, 0, -cos_a)
            # Normal vector in XZ plane W = (sign * cos_a, 0, sin_a)
            # Depth vector U = (0, 1, 0)
            s_ring = []
            N = len(armscye_loop)
            for k in range(N):
                theta = k * (2.0 * math.pi / N)
                ca = math.cos(theta)
                sa = math.sin(theta)
                
                # Displacement strictly perpendicular to arm vector
                vx = cx + sign * (ca * rw * cos_a)
                vy = cy + sa * rd
                vz = cz + (ca * rw * sin_a)
                s_ring.append(bm.verts.new((vx, vy, vz)))
                
            bm.verts.ensure_lookup_table()
            
            # Bridge previous loop to this new planar ring
            for k in range(N):
                knxt = (k + 1) % N
                if sign > 0:
                    bm.faces.new((prev_loop[k], prev_loop[knxt], s_ring[knxt], s_ring[k]))
                else:
                    bm.faces.new((prev_loop[k], s_ring[k], s_ring[knxt], prev_loop[knxt]))
            prev_loop = s_ring
            
    # -------------------------------------------------------------
    # 3. ATELIER BUST STAND
    # -------------------------------------------------------------
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
    
    # -------------------------------------------------------------
    # 4. DUAL-PANEL UV MAPPING
    # -------------------------------------------------------------
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
    
    # Subdivision Surface & Smooth Shading
    subsurf = obj.modifiers.new("Subsurf", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # Export GLB
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False
    )
    print(f"Exported Tee GLB: {out_glb_path}")
    
    # Setup camera & lighting for render verification
    cam_data = bpy.data.cameras.new("Cam")
    cam_obj = bpy.data.objects.new("Cam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = (0.0, -1.8, 0.05)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    
    # Lighting
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
    
    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 1200
    bpy.context.scene.render.filepath = out_render_path
    bpy.ops.render.render(write_still=True)
    print(f"Saved Tee Render: {out_render_path}")

if __name__ == '__main__':
    out_glb = "public/models/tee_p5.glb"
    out_png = os.path.expanduser("~/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/test_render_tee_v6.png")
    build_perfect_tee(out_glb, out_png)
