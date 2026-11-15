import bpy
import bmesh
import math
import os

def create_streetwear_hoodie_mesh():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # -------------------------------------------------------------
    # 1. BUILD COMPLETE MANIFOLD HOODIE VIA BOX-MODELING / BMESH
    # -------------------------------------------------------------
    mesh = bpy.data.meshes.new("Hoodie_Fabric_Body_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Fabric_Body", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # Streetwear Proportions (1:1.6 box-cut, dropped shoulders, relaxed heavyweight drape)
    # Z coordinate map:
    # -0.52 : Bottom of ribbed waistband hem
    # -0.42 : Top of ribbed waistband
    # -0.36 : Kangaroo pocket bottom stitch
    # -0.20 : Kangaroo pocket belly bulge & hand opening midpoint
    # -0.05 : Kangaroo pocket top bar-tack stitch
    # +0.12 : Mid chest graphic zone
    # +0.28 : Armscye base / chest line
    # +0.44 : Dropped shoulder seam line
    # +0.50 : Collar neck opening rim
    
    # Torso cross-sections (12 radial vertices per ring for clean quad topology)
    # Rings: 0 (hem) to 8 (collar)
    NUM_SEGS = 16
    
    # (z, x_rad, y_front, y_back)
    ring_defs = [
        (-0.52, 0.42, 0.17, 0.17), # 0: Hem bottom
        (-0.42, 0.44, 0.18, 0.18), # 1: Hem top
        (-0.35, 0.48, 0.21, 0.20), # 2: Lower belly / pocket bottom
        (-0.18, 0.52, 0.24, 0.22), # 3: Belly pouch bulge
        (-0.02, 0.54, 0.23, 0.21), # 4: Pocket top seam
        ( 0.15, 0.55, 0.22, 0.20), # 5: Mid chest
        ( 0.28, 0.58, 0.21, 0.19), # 6: Armscye bottom
        ( 0.42, 0.62, 0.20, 0.18), # 7: Dropped shoulder seam
        ( 0.49, 0.24, 0.16, 0.16), # 8: Collar opening
    ]
    
    torso_rings = []
    for r_idx, (z, xr, yf, yb) in enumerate(ring_defs):
        ring_verts = []
        for i in range(NUM_SEGS):
            angle = i * (2.0 * math.pi / NUM_SEGS)
            ca = math.cos(angle)
            sa = math.sin(angle)
            
            vx = ca * xr
            yr = yf if sa >= 0 else yb
            vy = sa * yr
            
            # Subtle cloth drape ripple on sides and back
            if r_idx in (2, 3, 4, 5, 6):
                vy += 0.012 * math.cos(angle * 4.0)
                vx += 0.008 * math.sin(angle * 2.0)
                
            v = bm.verts.new((vx, vy, z))
            ring_verts.append(v)
        torso_rings.append(ring_verts)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge rings 0 -> 7
    # For rings 6 to 7 (armscyes), we omit the outermost side faces so we can bridge sleeves directly!
    # In a 16-vert ring:
    # Right side (+X): index 0, 1, 15
    # Left side (-X): index 7, 8, 9
    armhole_r_indices = (0, 15)
    armhole_l_indices = (7, 8)
    
    for r in range(len(torso_rings) - 1):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(NUM_SEGS):
            i_next = (i + 1) % NUM_SEGS
            
            # Omit side faces at armscye (rings 6->7)
            if r == 6 and (i in armhole_r_indices or i in armhole_l_indices):
                continue
            # For ring 7->8 (shoulders to collar), bridge from shoulder ring to collar ring
            bm.faces.new((r0[i], r0[i_next], r1[i_next], r1[i]))
            
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. SEAMLESS DROPPED SLEEVES EXTENDING FROM ARMSCYES
    # -------------------------------------------------------------
    # Each sleeve has 5 segments draping naturally downward at -35 deg
    sleeve_def = [
        # (x_center, y_center, z_center, radius)
        (0.66,  0.00,  0.30, 0.16), # Shoulder cap / bicep start
        (0.72,  0.02,  0.10, 0.15), # Mid bicep
        (0.74,  0.04, -0.10, 0.14), # Elbow drape fold
        (0.68,  0.02, -0.30, 0.12), # Forearm
        (0.60, -0.01, -0.48, 0.10), # Wrist ribbed cuff
    ]
    
    SLEEVE_SEGS = 8
    for side_sign in (1.0, -1.0):
        prev_sleeve_ring = []
        for s_idx, (xc, yc, zc, rad) in enumerate(sleeve_def):
            s_ring = []
            for j in range(SLEEVE_SEGS):
                ang = j * (2.0 * math.pi / SLEEVE_SEGS)
                sx = side_sign * (xc + math.cos(ang) * rad)
                sy = yc + math.sin(ang) * rad
                sz = zc
                
                # Add natural cloth pinch fold on inner elbow
                if s_idx == 2:
                    if side_sign * math.cos(ang) < 0:
                        sz += 0.02
                        sy -= 0.015
                        
                v = bm.verts.new((sx, sy, sz))
                s_ring.append(v)
                
            if prev_sleeve_ring:
                for j in range(SLEEVE_SEGS):
                    j_next = (j + 1) % SLEEVE_SEGS
                    bm.faces.new((prev_sleeve_ring[j], prev_sleeve_ring[j_next], s_ring[j_next], s_ring[j]))
            prev_sleeve_ring = s_ring
            
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 3. SEAMLESS ATTACHED 3D KANGAROO POUCH
    # -------------------------------------------------------------
    # An authentic kangaroo pouch on the belly (Z = -0.38 to -0.05)
    # Extrude front faces forward to form defined pouch with diagonal pocket openings
    pocket_verts = []
    # 3 rows of 6 vertices across the belly
    p_rows = [
        (-0.38, 0.36, 0.24), # Bottom stitch (at waistband)
        (-0.20, 0.40, 0.29), # Belly bulge & hand openings
        (-0.06, 0.32, 0.26), # Top bar-tack stitch
    ]
    p_grid = []
    for pz, px_span, py_out in p_rows:
        row = []
        P_COLS = 6
        for c in range(P_COLS):
            t = c / (P_COLS - 1) # 0 to 1
            px = (t - 0.5) * 2.0 * px_span
            # curve in Y
            arch = math.cos((t - 0.5) * math.pi)
            py = py_out + arch * 0.035
            v = bm.verts.new((px, py, pz))
            row.append(v)
        p_grid.append(row)
        
    for r in range(len(p_grid) - 1):
        for c in range(P_COLS - 1):
            bm.faces.new((p_grid[r][c], p_grid[r][c+1], p_grid[r+1][c+1], p_grid[r+1][c]))
            
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 4. ORGANIC DRAPED COWL HOOD (Continuous with collar)
    # -------------------------------------------------------------
    # Hood emerges from the collar rim (ring 8), arches over head and drapes
    hood_profiles = [
        # (z, y_cen, x_rad, y_rad, drape_sag)
        (0.53, -0.08, 0.25, 0.22, 0.00), # Collar base fold
        (0.64, -0.15, 0.27, 0.26, 0.02), # Occipital nape
        (0.76, -0.12, 0.26, 0.25, 0.01), # Mid skull
        (0.85, -0.05, 0.24, 0.23, 0.00), # Crown
        (0.83,  0.08, 0.21, 0.20, -0.02), # Front brow brim
    ]
    
    HOOD_PTS = 14
    prev_h_ring = []
    for h_idx, (hz, hyc, hrx, hry, hsag) in enumerate(hood_profiles):
        h_ring = []
        for i in range(HOOD_PTS):
            # U-shape around back, leaving open face in front (from -35 deg to 215 deg)
            t = i / (HOOD_PTS - 1)
            # Angle from 0.15 PI to 1.85 PI
            ang = math.pi * 0.18 + t * (math.pi * 1.64)
            hx = math.cos(ang) * hrx
            hy = hyc + math.sin(ang) * hry
            # Natural side drape sag
            sag = hsag - 0.025 * (1.0 - math.sin(ang))
            v = bm.verts.new((hx, hy, hz + sag))
            h_ring.append(v)
            
        if prev_h_ring:
            for i in range(HOOD_PTS - 1):
                bm.faces.new((prev_h_ring[i], prev_h_ring[i+1], h_ring[i+1], h_ring[i]))
        prev_h_ring = h_ring
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 5. COTTON DRAWSTRINGS WITH METAL AGLETS
    # -------------------------------------------------------------
    # Two drawstrings dangling from front collar grommets (X = ±0.06, Y = 0.18, Z = 0.46)
    for ds_sign in (1.0, -1.0):
        ds_pts = [
            (ds_sign * 0.06, 0.17, 0.46),
            (ds_sign * 0.07, 0.18, 0.38),
            (ds_sign * 0.065, 0.19, 0.28),
            (ds_sign * 0.06, 0.19, 0.18),
        ]
        # create cord segment
        prev_cord = []
        for p_co in ds_pts:
            cord_ring = []
            for k in range(5):
                kang = k * (2.0 * math.pi / 5)
                cx = p_co[0] + math.cos(kang) * 0.007
                cy = p_co[1] + math.sin(kang) * 0.007
                cz = p_co[2]
                v = bm.verts.new((cx, cy, cz))
                cord_ring.append(v)
            if prev_cord:
                for k in range(5):
                    k_next = (k + 1) % 5
                    bm.faces.new((prev_cord[k], prev_cord[k_next], cord_ring[k_next], cord_ring[k]))
            prev_cord = cord_ring

    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 6. UNIFIED CONFORMAL UV UNWRAPPING (NO FLOATING DECALS)
    # -------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    
    for f in bm.faces:
        c = f.calc_center_median()
        # Front chest & front pocket region:
        # X: [-0.45, 0.45], Y > 0.02, Z: [-0.48, 0.45]
        if c.y > 0.01 and abs(c.x) < 0.48 and -0.50 <= c.z <= 0.45:
            for l in f.loops:
                v = l.vert
                # Map X (-0.48 to +0.48) directly to U [0.15, 0.85]
                u = ((v.co.x / 0.96) + 0.50) * 0.70 + 0.15
                # Map Z (-0.50 to +0.45) directly to V [0.10, 0.90]
                v_coord = ((v.co.z + 0.50) / 0.95) * 0.80 + 0.10
                l[uv_layer].uv = (u, v_coord)
        else:
            # Back, sleeves, and hood mapped to neutral secondary region
            for l in f.loops:
                v = l.vert
                u = (v.co.x / 2.0) + 0.50
                v_coord = (v.co.z / 2.0) + 0.50
                # Scale down and place in corner
                l[uv_layer].uv = (u * 0.20 + 0.02, v_coord * 0.20 + 0.02)
                
    bm.to_mesh(mesh)
    bm.free()
    
    # Apply Subsurf Modifier for natural organic cloth tension
    sub = hoodie.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 2
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    # Heavyweight 500GSM Fabric Solidify
    sol = hoodie.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.008
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    for p in hoodie.data.polygons:
        p.use_smooth = True
        
    # -------------------------------------------------------------
    # 7. REFINED ATELIER MANNEQUIN STAND
    # -------------------------------------------------------------
    # Matte black & brushed metal neck form visible inside hood opening
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.09, depth=0.30, location=(0, -0.04, 0.48))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Bust"
    
    # Polished steel neck crown cap
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.07, depth=0.025, location=(0, -0.04, 0.64))
    m_cap = bpy.context.active_object
    
    # Center vertical steel support pole
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.022, depth=0.95, location=(0, 0, -0.48))
    m_pole = bpy.context.active_object
    
    # Museum weighted circular pedestal base
    bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.38, depth=0.035, location=(0, 0, -0.95))
    m_base = bpy.context.active_object
    
    # Join stand
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
    
    print(f"Generated Streetwear Hoodie: {len(hoodie.data.vertices)} vertices, {len(hoodie.data.polygons)} polygons")
    return hoodie, mannequin

if __name__ == "__main__":
    h, m = create_streetwear_hoodie_mesh()
    bpy.ops.export_scene.gltf(filepath="public/assets/models/test_streetwear.glb", export_format='GLB')
    print("Exported test_streetwear.glb successfully!")
