import bpy
import bmesh
import math
import os

def create_anatomical_foot_last():
    """
    Creates a clean, watertight, beautifully contoured low-top skate shoe last.
    Returns the bmesh with face groups for sole, vamp, quarters, mudguard, eyestay, heel, collar.
    """
    # 20 rings along foot length (Y from -0.125m heel to +0.145m toe)
    # 16 vertices per radial ring around the cross-section
    RINGS = 22
    SEGS = 16
    
    y_coords = []
    for i in range(RINGS):
        u = i / (RINGS - 1)
        # Cosine distribution gives higher density at heel and toe
        y = -0.125 + 0.270 * (0.5 - 0.5 * math.cos(u * math.pi))
        y_coords.append(y)
        
    last_mesh = bpy.data.meshes.new("Foot_Last_Mesh")
    bm = bmesh.new()
    
    ring_verts = []
    
    for i, y in enumerate(y_coords):
        t = (y + 0.125) / 0.270
        t = max(0.0, min(1.0, t))
        
        # Sole bottom height with 12mm toe spring
        if t > 0.60:
            frac = (t - 0.60) / 0.40
            z_bot = 0.012 * (frac ** 1.9)
        elif t < 0.08:
            z_bot = 0.0018 * (1.0 - t / 0.08)
        else:
            z_bot = 0.000
            
        # Sole rim height (16mm heel, 13mm toe)
        sole_h = 0.0165 - 0.0035 * t
        z_rim = z_bot + sole_h
        
        # Foot Widths: Lateral (xl) and Medial (xm)
        # Heel
        r_heel = math.sqrt(max(0.01, 1.0 - ((0.12 - t) / 0.12) ** 2)) if t < 0.12 else 1.0
        # Toe
        r_toe = math.sqrt(max(0.01, 1.0 - ((t - 0.76) / 0.24) ** 2)) if t > 0.76 else 1.0
        
        if t < 0.25: # Heel
            xm = -0.035 * r_heel
            xl =  0.036 * r_heel
        elif t < 0.52: # Arch / Waist (medial tucks in)
            f = (t - 0.25) / 0.27
            xm = -(0.035 - 0.006 * math.sin(f * math.pi))
            xl =  (0.036 + 0.001 * math.sin(f * math.pi))
        elif t < 0.82: # Ball of foot flare
            f = (t - 0.52) / 0.30
            xm = -(0.031 + 0.011 * math.sin(f * math.pi * 0.9))
            xl =  (0.037 + 0.010 * math.sin(f * math.pi * 0.9))
        else: # Broad skate toe box
            xm = -0.042 * r_toe
            xl =  0.044 * r_toe
            
        # Heights: Foot Top
        if t < 0.20: # Heel collar & Achilles notch
            f = t / 0.20
            z_top = z_rim + 0.052 - 0.008 * f
        elif t < 0.44: # Collar dip / opening
            f = (t - 0.20) / 0.24
            z_top = z_rim + 0.044 - 0.010 * math.sin(f * math.pi * 0.5)
        elif t < 0.70: # Eyestay lace throat
            f = (t - 0.44) / 0.26
            z_top = z_rim + 0.034 - 0.007 * f
        else: # Toe vamp dome
            f = (t - 0.70) / 0.30
            z_top = z_rim + 0.027 * math.cos(f * math.pi * 0.48)
            
        # Radial vertices around this station ring (16 vertices)
        # k = 0: Bottom Center (z = z_bot)
        # k = 1..4: Lateral side wall (rising to z_rim and mid wall)
        # k = 4..8: Lateral top to Top Center (z = z_top)
        # k = 8: Top Center
        # k = 8..12: Medial top to mid wall
        # k = 12..15: Medial side wall down to bottom center
        cur_ring = []
        for k in range(SEGS):
            theta = k * (2.0 * math.pi / SEGS)
            sin_th = math.sin(theta)
            cos_th = math.cos(theta)
            
            # X coordinate
            if sin_th >= 0:
                vx = xl * sin_th
            else:
                vx = -xm * sin_th # xm is negative, so -xm is positive
                
            # Z coordinate
            # Map cos_th from [-1, 1] to [z_bot, z_top]
            # When cos_th = -1 (bottom, theta=pi): z = z_bot
            # When cos_th = 1 (top, theta=0): z = z_top
            # When cos_th = 0 (sides): z ~ z_rim + (z_top - z_rim)*0.45
            z_norm = 0.5 - 0.5 * cos_th # 0 at top (theta=0), 1 at bottom (theta=pi)
            
            if cos_th >= 0: # Top half (theta in [0, pi/2] or [3pi/2, 2pi])
                # Upper arch
                h_frac = cos_th ** 1.3
                vz = z_rim + (z_top - z_rim) * h_frac
            else: # Bottom half
                # Sole / footbed floor
                b_frac = (-cos_th) ** 1.4
                vz = z_rim - (z_rim - z_bot) * b_frac
                
            cur_ring.append(bm.verts.new((vx, y, vz)))
            
        ring_verts.append(cur_ring)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge rings along length
    faces_by_layer = {
        'sole': [],
        'vamp': [],
        'mudguard': [],
        'quarters': [],
        'heel': [],
        'collar': []
    }
    
    for i in range(RINGS - 1):
        r0 = ring_verts[i]
        r1 = ring_verts[i + 1]
        t = i / (RINGS - 1)
        
        for k in range(SEGS):
            knxt = (k + 1) % SEGS
            # Quad face
            f = bm.faces.new((r0[k], r0[knxt], r1[knxt], r1[k]))
            
            # Categorize face by physical shoe component:
            # k in [6, 7, 8, 9, 10] is bottom / sole area
            is_bottom = k in [6, 7, 8, 9, 10]
            
            if is_bottom:
                faces_by_layer['sole'].append(f)
            elif t >= 0.70: # Front toe box
                if is_bottom or k in [4, 5, 11, 12]:
                    faces_by_layer['mudguard'].append(f)
                else:
                    faces_by_layer['vamp'].append(f)
            elif t >= 0.25: # Midfoot quarters
                if is_bottom or k in [4, 5, 11, 12]:
                    faces_by_layer['quarters'].append(f)
                else:
                    faces_by_layer['quarters'].append(f)
            else: # Rear heel
                faces_by_layer['heel'].append(f)
                
    # Close heel cap (ring 0)
    c_heel = bm.verts.new((0.0, y_coords[0] - 0.005, st_data_z := 0.035))
    r_h = ring_verts[0]
    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm.faces.new((c_heel, r_h[knxt], r_h[k]))
        
    # Close toe cap (ring -1)
    c_toe = bm.verts.new((0.0, y_coords[-1] + 0.005, 0.024))
    r_t = ring_verts[-1]
    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm.faces.new((c_toe, r_t[k], r_t[knxt]))
        
    bm.to_mesh(last_mesh)
    bm.free()
    
    return last_mesh
