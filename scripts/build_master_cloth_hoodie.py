import bpy
import bmesh
import math
import os

def create_master_cloth_hoodie():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Hoodie_Fabric_Body_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Fabric_Body", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. TORSO RINGS (8 rings from bottom hem to shoulders/neck)
    # Number of radial segments = 16 for clean quad topology
    # -------------------------------------------------------------
    # We define the profile heights and radius (x_scale, y_scale)
    # Proportions: 1 : 1.6 streetwear boxy cut
    # Hem at z = -0.50, Shoulders at z = +0.42, Neck at z = +0.48
    
    ring_specs = [
        # (z, x_radius, y_radius_front, y_radius_back, is_pocket)
        (-0.50, 0.40, 0.18, 0.18, False), # 0: Bottom waistband cuff
        (-0.42, 0.41, 0.19, 0.19, False), # 1: Waistband seam
        (-0.36, 0.44, 0.22, 0.20, True),  # 2: Kangaroo pocket bottom
        (-0.20, 0.48, 0.26, 0.21, True),  # 3: Kangaroo pocket belly bulge
        (-0.04, 0.50, 0.24, 0.21, True),  # 4: Kangaroo pocket top seam
        ( 0.14, 0.52, 0.22, 0.21, False), # 5: Mid chest
        ( 0.30, 0.56, 0.21, 0.20, False), # 6: High chest / armscye base
        ( 0.42, 0.60, 0.19, 0.18, False), # 7: Dropped shoulder line
        ( 0.48, 0.22, 0.15, 0.15, False), # 8: Collar / neck ring
    ]
    
    NUM_SEGS = 16 # 16 vertices per ring
    # Angle 0 is right (+X), PI/2 is front (+Y), PI is left (-X), 3PI/2 is back (-Y)
    
    rings = []
    for r_idx, (z, xr, yrf, yrb, is_pocket) in enumerate(ring_specs):
        v_ring = []
        for i in range(NUM_SEGS):
            angle = i * (2.0 * math.pi / NUM_SEGS)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            
            x = cos_a * xr
            # Front / Back asymmetric depth
            yr = yrf if sin_a >= 0 else yrb
            y = sin_a * yr
            
            # If pocket ring, add pocket protrusion on front center (sin_a > 0.4)
            if is_pocket and sin_a > 0.35:
                # Add natural kangaroo pouch protrusion
                y += 0.055 * math.sin((sin_a - 0.35) / 0.65 * math.pi)
            
            # Natural cloth drape micro-waviness
            drape = 0.012 * math.cos(angle * 3.0) + 0.008 * math.sin(z * 8.0)
            if r_idx not in (0, 8):
                y += drape
            
            v = bm.verts.new((x, y, z))
            v_ring.append(v)
        rings.append(v_ring)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge torso rings with quad faces
    torso_faces = []
    for r_idx in range(len(rings) - 1):
        r0 = rings[r_idx]
        r1 = rings[r_idx + 1]
        for i in range(NUM_SEGS):
            i_next = (i + 1) % NUM_SEGS
            # Create quad (r0[i], r0[i_next], r1[i_next], r1[i])
            # Skip left/right faces on ring 6-7 to create armhole loops!
            # Side vertices for left: i around 8 (PI = -X), right: i around 0 (+X)
            # Armholes are between ring 5 to 7:
            is_armhole_r = (r_idx in (5, 6)) and (i in (0, 15))
            is_armhole_l = (r_idx in (5, 6)) and (i in (7, 8))
            
            if not (is_armhole_r or is_armhole_l):
                f = bm.faces.new((r0[i], r0[i_next], r1[i_next], r1[i]))
                torso_faces.append(f)
                
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. CONTINUOUS SLEEVES (Extruded directly from Armscyes)
    # Right armhole vertices and Left armhole vertices
    # -------------------------------------------------------------
    # We will build sleeves with 4 segments draping downward at -38 deg
    # Right armhole loop vertices:
    r_arm_v = [
        rings[5][15], rings[5][0], rings[5][1],
        rings[6][1], rings[7][0], rings[7][15], rings[6][15]
    ]
    # Sleeve loop generator
    sleeve_steps = [
        # (x_center, y_center, z_center, radius_x, radius_y)
        (0.66, 0.00, 0.32, 0.16, 0.16),  # Upper bicep
        (0.74, 0.02, 0.10, 0.15, 0.15),  # Elbow fold
        (0.70, 0.02, -0.15, 0.13, 0.13), # Forearm
        (0.60, 0.00, -0.38, 0.11, 0.11), # Wrist cuff top
        (0.56, -0.01, -0.46, 0.10, 0.10) # Wrist cuff hem
    ]
    
    # For both right (+X) and left (-X)
    for side_sign in (1.0, -1.0):
        prev_ring = []
        SLEEVE_SEGS = 8
        for s_idx, (xc, yc, zc, rx, ry) in enumerate(sleeve_steps):
            s_ring = []
            for i in range(SLEEVE_SEGS):
                ang = i * (2.0 * math.pi / SLEEVE_SEGS)
                vx = side_sign * (xc + math.cos(ang) * rx)
                vy = yc + math.sin(ang) * ry
                # Slight downward drape fold on bottom sleeve
                vz = zc - 0.015 * math.cos(ang)
                v = bm.verts.new((vx, vy, vz))
                s_ring.append(v)
            
            if prev_ring:
                for i in range(SLEEVE_SEGS):
                    i_next = (i + 1) % SLEEVE_SEGS
                    bm.faces.new((prev_ring[i], prev_ring[i_next], s_ring[i_next], s_ring[i]))
            prev_ring = s_ring
            
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 3. CONTINUOUS DRAPED HOOD (Extruded from Collar Ring)
    # The hood wraps from collar, arches up and back, with open front
    # -------------------------------------------------------------
    # Collar ring is rings[8] (z = 0.48)
    # Hood profiles ascending
    hood_levels = [
        # (z, y_center, x_rad, y_rad, open_front_ratio)
        (0.56, -0.06, 0.23, 0.22), # Neck cowl fold
        (0.68, -0.12, 0.24, 0.24), # Lower back skull
        (0.80, -0.10, 0.23, 0.23), # Mid skull
        (0.88, -0.04, 0.21, 0.21), # Crown top
        (0.84,  0.04, 0.18, 0.18), # Front brow brim
    ]
    
    HOOD_SEGS = 12
    prev_hood = []
    # Only span angles from -45 deg to 225 deg (leaving front opening for face)
    for h_idx, (hz, hyc, hrx, hry) in enumerate(hood_levels):
        h_ring = []
        for i in range(HOOD_SEGS):
            # angle from PI*0.1 to PI*1.9 (omitting front wedge)
            t = i / (HOOD_SEGS - 1)
            ang = math.pi * 0.15 + t * (math.pi * 1.7)
            hx = math.cos(ang) * hrx
            hy = hyc + math.sin(ang) * hry
            # Natural cloth sag
            sag = -0.02 * math.cos(t * math.pi)
            v = bm.verts.new((hx, hy, hz + sag))
            h_ring.append(v)
            
        if prev_hood:
            for i in range(HOOD_SEGS - 1):
                bm.faces.new((prev_hood[i], prev_hood[i+1], h_ring[i+1], h_ring[i]))
        prev_hood = h_ring

    # Bridge collar ring back vertices to lower hood ring
    # Collar vertices with y < 0.05
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 4. UNIFIED CONVENTIONAL GARMENT UV UNWRAPPING
    # -------------------------------------------------------------
    # UV Layer
    uv_layer = bm.loops.layers.uv.new("UVMap")
    
    # Map vertices deterministically based on garment coordinates:
    # Front Torso (Y > 0): maps to U [0.15, 0.85], V [0.15, 0.85]
    # Center chest is around U = 0.50, V = 0.65!
    # Back Torso (Y < 0): maps to clean secondary UV space
    for f in bm.faces:
        center = f.calc_center_median()
        is_front = center.y >= -0.02 and abs(center.x) < 0.58 and -0.52 <= center.z <= 0.48
        
        for l in f.loops:
            v = l.vert
            if is_front:
                # Direct conformal unwrap for chest & kangaroo pocket
                # X from -0.60 to +0.60 -> U from 0.10 to 0.90
                u = (v.co.x / 1.20) + 0.50
                # Z from -0.50 to +0.48 -> V from 0.10 to 0.90
                v_coord = ((v.co.z + 0.50) / 0.98) * 0.80 + 0.10
                l[uv_layer].uv = (u, v_coord)
            else:
                # Other parts mapped cleanly to perimeter UV space so they don't overlap front graphics
                u_off = (v.co.x / 1.60) + 0.50
                v_off = ((v.co.z + 0.50) / 1.50) * 0.40
                l[uv_layer].uv = (u_off * 0.50, v_off * 0.50)
                
    bm.to_mesh(mesh)
    bm.free()
    
    # Apply Subsurf Modifier for smooth organic cloth drape
    sub = hoodie.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 2
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    # Solidify modifier to give realistic 500GSM heavyweight fabric thickness
    sol = hoodie.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.009
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    # Smooth normals
    for p in hoodie.data.polygons:
        p.use_smooth = True
        
    # -------------------------------------------------------------
    # 5. ATELIER MANNEQUIN STAND (Inside the hoodie)
    # -------------------------------------------------------------
    # 5a. Torso bust core
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.10, depth=0.35, location=(0, -0.02, 0.45))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Bust"
    
    # 5b. Metallic finial
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.075, depth=0.03, location=(0, -0.02, 0.64))
    m_cap = bpy.context.active_object
    
    # 5c. Steel stand pole
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.022, depth=0.90, location=(0, 0, -0.45))
    m_pole = bpy.context.active_object
    
    # 5d. Museum circular base
    bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.38, depth=0.04, location=(0, 0, -0.90))
    m_base = bpy.context.active_object
    
    # Join stand
    bpy.ops.object.select_all(action='DESELECT')
    for m in [m_neck, m_cap, m_pole, m_base]:
        m.select_set(True)
    bpy.context.view_layer.objects.active = m_neck
    bpy.ops.object.join()
    mannequin_obj = bpy.context.active_object
    mannequin_obj.name = "Mannequin_Stand"
    
    # Offset entire scene so ground base sits at -1.10 and hoodie is centered at eye level
    bpy.ops.object.select_all(action='SELECT')
    for obj in [hoodie, mannequin_obj]:
        obj.location.z -= 0.10
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    
    print(f"Created Hoodie: {len(hoodie.data.vertices)} verts, {len(hoodie.data.polygons)} polys")
    return hoodie, mannequin_obj

if __name__ == "__main__":
    h, m = create_master_cloth_hoodie()
    # Export test glb
    bpy.ops.export_scene.gltf(filepath="public/assets/models/test_hoodie.glb", export_format='GLB')
    print("Test export done!")
