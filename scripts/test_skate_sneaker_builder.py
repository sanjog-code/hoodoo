import bpy
import bmesh
import math
import os

def build_sneaker_mesh():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Sneaker_Mesh")
    obj = bpy.data.objects.new("Sneaker_Model", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. PARAMETRIC FOOT LAST OUTLINE
    # Y runs from -0.130 (heel) to +0.155 (toe tip) -> length 0.285m
    # -------------------------------------------------------------
    def get_last_contour(y):
        # t from 0.0 (heel back) to 1.0 (toe tip)
        t = (y + 0.130) / 0.285
        t = max(0.0, min(1.0, t))
        
        # Ground Z of sole bottom
        if t < 0.60:
            z_ground = 0.000
        else:
            frac = (t - 0.60) / 0.40
            z_ground = 0.018 * (frac ** 1.8) # 18mm toe spring
        if t < 0.06:
            z_ground += 0.004 * (1.0 - t / 0.06) # heel rocker
            
        # Cupsole top Z
        sole_h = 0.028 - 0.008 * t # 28mm at heel to 20mm at toe
        z_sole_top = z_ground + sole_h
        
        # Asymmetrical Foot half-widths (medial -X, lateral +X)
        if t < 0.20: # Heel
            f = t / 0.20
            w = 0.038 * math.sin(f * math.pi * 0.5)
            x_med = -w * 0.98
            x_lat = w * 1.00
        elif t < 0.48: # Arch / Waist
            f = (t - 0.20) / 0.28
            x_med = -(0.038 - 0.014 * math.sin(f * math.pi)) # deep medial arch cut
            x_lat = 0.038 + 0.004 * math.sin(f * math.pi)
        elif t < 0.80: # Ball of foot (widest)
            f = (t - 0.48) / 0.32
            x_med = -(0.024 + 0.026 * math.sin(f * math.pi * 0.8))
            x_lat = 0.042 + 0.012 * math.sin(f * math.pi * 0.8)
        else: # Toe box rounding
            f = (t - 0.80) / 0.20
            taper = max(0.02, 1.0 - (f ** 1.3))
            x_med = -0.050 * taper
            x_lat = 0.052 * taper
            
        return z_ground, z_sole_top, x_med, x_lat
        
    # Stations along length
    STATIONS = 28
    y_vals = [-0.130 + i * (0.285 / (STATIONS - 1)) for i in range(STATIONS)]
    
    # -------------------------------------------------------------
    # 2. CUPSOLE GEOMETRY (Solid rubber tray with wall and lip)
    # -------------------------------------------------------------
    # For each station, we build:
    # 0: bottom center (x=0, z=z_ground)
    # 1: bottom medial edge (x=x_med - 0.003, z=z_ground)
    # 2: cupsole top medial rim (x=x_med - 0.003, z=z_sole_top)
    # 3: cupsole shelf medial (x=x_med, z=z_sole_top - 0.004) -> where upper starts
    # 4: cupsole shelf lateral (x=x_lat, z=z_sole_top - 0.004)
    # 5: cupsole top lateral rim (x=x_lat + 0.003, z=z_sole_top)
    # 6: bottom lateral edge (x=x_lat + 0.003, z=z_ground)
    sole_rings = []
    for y in y_vals:
        zg, zst, xm, xl = get_last_contour(y)
        # expand slightly for rubber sidewall
        v_bot_c = bm.verts.new((0.0, y, zg))
        v_bot_m = bm.verts.new((xm - 0.0035, y, zg))
        v_top_m = bm.verts.new((xm - 0.0035, y, zst))
        v_shf_m = bm.verts.new((xm, y, zst - 0.004))
        v_shf_l = bm.verts.new((xl, y, zst - 0.004))
        v_top_l = bm.verts.new((xl + 0.0035, y, zst))
        v_bot_l = bm.verts.new((xl + 0.0035, y, zg))
        sole_rings.append((v_bot_c, v_bot_m, v_top_m, v_shf_m, v_shf_l, v_top_l, v_bot_l))
        
    bm.verts.ensure_lookup_table()
    
    # Bridge sole rings
    for s in range(STATIONS - 1):
        r0 = sole_rings[s]
        r1 = sole_rings[s + 1]
        # Outsole bottom (medial & lateral halves)
        bm.faces.new((r0[0], r1[0], r1[1], r0[1])) # bot medial
        bm.faces.new((r0[0], r0[6], r1[6], r1[0])) # bot lateral
        # Rubber sidewalls
        bm.faces.new((r0[1], r1[1], r1[2], r0[2])) # medial wall
        bm.faces.new((r0[2], r1[2], r1[3], r0[3])) # medial rim lip
        bm.faces.new((r0[6], r0[5], r1[5], r1[6])) # lateral wall
        bm.faces.new((r0[5], r0[4], r1[4], r1[5])) # lateral rim lip
        
    # Cap heel and toe sole ends
    bm.faces.new((sole_rings[0][1], sole_rings[0][0], sole_rings[0][6], sole_rings[0][5], sole_rings[0][2]))
    bm.faces.new((sole_rings[-1][0], sole_rings[-1][1], sole_rings[-1][2], sole_rings[-1][5], sole_rings[-1][6]))
    
    # -------------------------------------------------------------
    # 3. SNEAKER UPPER: VAMP, QUARTERS, ANKLE COLLAR CAVITY
    # Stations 0..STATIONS-1
    # -------------------------------------------------------------
    # We create upper loops rising from the shelf vertices (v_shf_m, v_shf_l).
    # From heel (station 0) to collar front (station 12, Y ~ -0.01):
    #   There is an OPEN ANKLE HOLE!
    #   The upper has a side wall on medial and lateral, a padded collar rim at top,
    #   and an interior lining that drops down into the footbed!
    # From throat (station 13, Y ~ 0.00) to toe (station 27, Y ~ 0.155):
    #   Station 13..18: Eyestay panels flanking open throat gap (where tongue sits).
    #   Station 19..27: Domed toe box (vamp).
    
    upper_rings = []
    footbed_verts = []
    
    for s, y in enumerate(y_vals):
        zg, zst, xm, xl = get_last_contour(y)
        t = (y + 0.130) / 0.285
        shelf_m = sole_rings[s][3]
        shelf_l = sole_rings[s][4]
        
        # Height of upper at this station
        if t < 0.15: # Heel counter tab
            f = t / 0.15
            collar_z = zst + 0.080 - 0.015 * f
            is_collar = True
            is_throat = False
        elif t < 0.44: # Ankle collar dip around malleolus
            f = (t - 0.15) / 0.29
            collar_z = zst + 0.065 - 0.012 * math.sin(f * math.pi)
            is_collar = True
            is_throat = False
        elif t < 0.68: # Eyestay / throat gap
            f = (t - 0.44) / 0.24
            eyestay_z = zst + 0.052 - 0.012 * f
            is_collar = False
            is_throat = True
        else: # Domed toe box
            f = (t - 0.68) / 0.32
            vamp_z = zst + 0.038 * (1.0 - (f ** 1.4)) + 0.004
            is_collar = False
            is_throat = False
            
        # Interior footbed vert
        v_footbed = bm.verts.new((0.0, y, zst - 0.002))
        footbed_verts.append(v_footbed)
        
        if is_collar:
            # Medial side wall + padded collar rim + inner lining
            # Wall mid vert
            v_wm = bm.verts.new((xm * 0.96, y, zst + (collar_z - zst) * 0.55))
            # Collar top rim (outer edge and inner padded roll)
            v_cm_out = bm.verts.new((xm * 0.78, y, collar_z))
            v_cm_inn = bm.verts.new((xm * 0.60, y, collar_z - 0.006))
            # Inner wall dropping into footbed
            v_cm_drop = bm.verts.new((xm * 0.35, y, zst + 0.010))
            
            # Lateral side wall + padded collar rim + inner lining
            v_wl = bm.verts.new((xl * 0.96, y, zst + (collar_z - zst) * 0.55))
            v_cl_out = bm.verts.new((xl * 0.78, y, collar_z))
            v_cl_inn = bm.verts.new((xl * 0.60, y, collar_z - 0.006))
            v_cl_drop = bm.verts.new((xl * 0.35, y, zst + 0.010))
            
            upper_rings.append(('collar', shelf_m, v_wm, v_cm_out, v_cm_inn, v_cm_drop,
                                shelf_l, v_wl, v_cl_out, v_cl_inn, v_cl_drop, v_footbed))
                                
        elif is_throat:
            # Eyestay panels flanking open throat gap
            throat_gap = 0.011 # half gap = 11mm
            v_wm = bm.verts.new((xm * 0.92, y, zst + (eyestay_z - zst) * 0.50))
            v_eye_m = bm.verts.new((-throat_gap, y, eyestay_z))
            
            v_wl = bm.verts.new((xl * 0.92, y, zst + (eyestay_z - zst) * 0.50))
            v_eye_l = bm.verts.new(( throat_gap, y, eyestay_z))
            
            upper_rings.append(('throat', shelf_m, v_wm, v_eye_m,
                                shelf_l, v_wl, v_eye_l, v_footbed))
                                
        else:
            # Continuous closed domed toe box (5 verts across)
            v_wm = bm.verts.new((xm * 0.92, y, zst + (vamp_z - zst) * 0.55))
            v_crest = bm.verts.new((0.0, y, vamp_z))
            v_wl = bm.verts.new((xl * 0.92, y, zst + (vamp_z - zst) * 0.55))
            
            upper_rings.append(('vamp', shelf_m, v_wm, v_crest, v_wl, shelf_l, v_footbed))
            
    bm.verts.ensure_lookup_table()
    
    # Bridge upper stations along length
    for s in range(STATIONS - 1):
        type0 = upper_rings[s][0]
        type1 = upper_rings[s + 1][0]
        r0 = upper_rings[s]
        r1 = upper_rings[s + 1]
        
        # 1. Outer sidewalls always bridge cleanly from sole shelf
        # Medial wall: shelf -> wm
        bm.faces.new((r0[1], r1[1], r1[2], r0[2]))
        # Lateral wall: shelf -> wl
        # indices vary by type
        wl0 = r0[7] if type0 == 'collar' else (r0[5] if type0 == 'throat' else r0[4])
        wl1 = r1[7] if type1 == 'collar' else (r1[5] if type1 == 'throat' else r1[4])
        shl0 = r0[6] if type0 == 'collar' else (r0[4] if type0 == 'throat' else r0[5])
        shl1 = r1[6] if type1 == 'collar' else (r1[4] if type1 == 'throat' else r1[5])
        bm.faces.new((shl0, wl0, wl1, shl1))
        
        # 2. Footbed bridge
        fb0 = r0[-1]
        fb1 = r1[-1]
        
        if type0 == 'collar' and type1 == 'collar':
            # Medial collar rim and drop
            bm.faces.new((r0[2], r1[2], r1[3], r0[3])) # wm -> cm_out
            bm.faces.new((r0[3], r1[3], r1[4], r0[4])) # cm_out -> cm_inn (padded rim)
            bm.faces.new((r0[4], r1[4], r1[5], r0[5])) # cm_inn -> cm_drop
            bm.faces.new((r0[5], r1[5], fb1, fb0))     # cm_drop -> footbed
            
            # Lateral collar rim and drop
            bm.faces.new((r0[7], r0[8], r1[8], r1[7])) # wl -> cl_out
            bm.faces.new((r0[8], r0[9], r1[9], r1[8])) # cl_out -> cl_inn (padded rim)
            bm.faces.new((r0[9], r0[10], r1[10], r1[9])) # cl_inn -> cl_drop
            bm.faces.new((r0[10], fb0, fb1, r1[10]))     # cl_drop -> footbed
            
        elif type0 == 'collar' and type1 == 'throat':
            # Transition from collar opening into eyestay throat
            bm.faces.new((r0[2], r1[2], r1[3], r0[3]))
            bm.faces.new((r0[7], r0[8], r1[6], r1[5]))
            # Cap the collar forward drop into throat
            bm.faces.new((r0[3], r1[3], r0[4]))
            bm.faces.new((r0[8], r0[9], r1[6]))
            
        elif type0 == 'throat' and type1 == 'throat':
            # Eyestay panels flanking open throat gap
            bm.faces.new((r0[2], r1[2], r1[3], r0[3])) # medial eyestay
            bm.faces.new((r0[5], r0[6], r1[6], r1[5])) # lateral eyestay
            
        elif type0 == 'throat' and type1 == 'vamp':
            # Eyestay panels join at the vamp crest
            bm.faces.new((r0[2], r1[2], r1[3], r0[3]))
            bm.faces.new((r0[5], r0[6], r1[3], r1[4]))
            # Center throat bridge
            bm.faces.new((r0[3], r1[3], r0[6]))
            
        elif type0 == 'vamp' and type1 == 'vamp':
            # Smooth domed toe box quads
            bm.faces.new((r0[2], r1[2], r1[3], r0[3])) # medial vamp
            bm.faces.new((r0[3], r1[3], r1[4], r0[4])) # lateral vamp
            
    # Cap heel collar tab at station 0
    r_h = upper_rings[0]
    bm.faces.new((r_h[2], r_h[3], r_h[8], r_h[7]))
    bm.faces.new((r_h[3], r_h[4], r_h[9], r_h[8]))
    
    # Cap toe tip at final station
    r_tip = upper_rings[-1]
    bm.faces.new((r_tip[1], r_tip[2], r_tip[3], r_tip[4], r_tip[5]))
    
    # -------------------------------------------------------------
    # 4. PUFFY PADDED TONGUE (3D volume rising through throat gap)
    # -------------------------------------------------------------
    # Tongue starts at vamp junction (Y=0.05, Z=0.050)
    # Curves up and back to Y=-0.045, Z=0.115 (above collar!)
    tongue_steps = 7
    tongue_rings = []
    tw_base = 0.024
    for i in range(tongue_steps):
        t_frac = i / (tongue_steps - 1)
        ty = 0.052 - t_frac * 0.096 # from +0.052 back to -0.044
        tz = 0.050 + t_frac * 0.064 + 0.005 * math.sin(t_frac * math.pi) # up to 0.119
        tw = tw_base + 0.003 * math.sin(t_frac * math.pi)
        
        # Padded tongue has top surface and bottom surface
        v_top_l = bm.verts.new((-tw, ty, tz + 0.004))
        v_top_c = bm.verts.new((0.0, ty, tz + 0.007))
        v_top_r = bm.verts.new(( tw, ty, tz + 0.004))
        v_bot_r = bm.verts.new(( tw * 0.9, ty - 0.003, tz - 0.004))
        v_bot_c = bm.verts.new((0.0, ty - 0.003, tz - 0.005))
        v_bot_l = bm.verts.new((-tw * 0.9, ty - 0.003, tz - 0.004))
        tongue_rings.append((v_top_l, v_top_c, v_top_r, v_bot_r, v_bot_c, v_bot_l))
        
    bm.verts.ensure_lookup_table()
    for t in range(tongue_steps - 1):
        tr0 = tongue_rings[t]
        tr1 = tongue_rings[t + 1]
        # Top surface
        bm.faces.new((tr0[0], tr1[0], tr1[1], tr0[1]))
        bm.faces.new((tr0[1], tr1[1], tr1[2], tr0[2]))
        # Sides
        bm.faces.new((tr0[2], tr1[2], tr1[3], tr0[3]))
        bm.faces.new((tr0[5], tr1[5], tr1[0], tr0[0]))
        # Bottom
        bm.faces.new((tr0[3], tr1[3], tr1[4], tr0[4]))
        bm.faces.new((tr0[4], tr1[4], tr1[5], tr0[5]))
        
    # Cap tongue top edge
    tr_top = tongue_rings[-1]
    bm.faces.new((tr_top[0], tr_top[1], tr_top[2], tr_top[3], tr_top[4], tr_top[5]))
    
    # -------------------------------------------------------------
    # 5. FAT SKATE LACES (4 horizontal cross-laces spanning eyestays)
    # -------------------------------------------------------------
    lace_y_levels = [0.038, 0.018, -0.002, -0.022]
    for ly in lace_y_levels:
        # get eyestay height at ly
        t_ly = (ly + 0.130) / 0.285
        lz = 0.062 + (1.0 - t_ly) * 0.035
        # lace is a puffy strap from x=-0.013 to +0.013
        lw = 0.0042 # half lace width
        th = 0.0018 # thickness
        
        lv0 = bm.verts.new((-0.015, ly - lw, lz))
        lv1 = bm.verts.new((-0.015, ly + lw, lz))
        lv2 = bm.verts.new(( 0.015, ly + lw, lz))
        lv3 = bm.verts.new(( 0.015, ly - lw, lz))
        
        lv0_top = bm.verts.new((-0.015, ly - lw, lz + th))
        lv1_top = bm.verts.new((-0.015, ly + lw, lz + th))
        lv2_top = bm.verts.new(( 0.015, ly + lw, lz + th))
        lv3_top = bm.verts.new(( 0.015, ly - lw, lz + th))
        
        bm.faces.new((lv0_top, lv1_top, lv2_top, lv3_top))
        bm.faces.new((lv0, lv3, lv2, lv1))
        bm.faces.new((lv0, lv1, lv1_top, lv0_top))
        bm.faces.new((lv2, lv3, lv3_top, lv2_top))
        bm.faces.new((lv1, lv2, lv2_top, lv1_top))
        bm.faces.new((lv3, lv0, lv0_top, lv3_top))
        
    # -------------------------------------------------------------
    # 6. ATELIER DISPLAY PEDESTAL (Museum presentation disc)
    # -------------------------------------------------------------
    PED_SEGS = 32
    ped_rad = 0.180
    ped_top_z = -0.004
    ped_bot_z = -0.022
    
    top_verts = []
    bot_verts = []
    center_top = bm.verts.new((0.0, 0.0, ped_top_z))
    center_bot = bm.verts.new((0.0, 0.0, ped_bot_z))
    
    for i in range(PED_SEGS):
        ang = i * (2.0 * math.pi / PED_SEGS)
        px = math.cos(ang) * ped_rad
        py = math.sin(ang) * ped_rad
        vt = bm.verts.new((px, py, ped_top_z))
        vb = bm.verts.new((px * 1.03, py * 1.03, ped_bot_z))
        top_verts.append(vt)
        bot_verts.append(vb)
        
    bm.verts.ensure_lookup_table()
    for i in range(PED_SEGS):
        i_next = (i + 1) % PED_SEGS
        # Disc top
        bm.faces.new((center_top, top_verts[i], top_verts[i_next]))
        # Sidewall
        bm.faces.new((top_verts[i], bot_verts[i], bot_verts[i_next], top_verts[i_next]))
        # Disc bottom
        bm.faces.new((center_bot, bot_verts[i_next], bot_verts[i]))
        
    bm.to_mesh(mesh)
    bm.free()
    
    # Recalculate normals & smooth shading
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    # Level 1 Subdivision surface for production organic curves
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    
    # Add material
    mat = bpy.data.materials.new(name="Sneaker_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.88, 0.85, 0.82, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.55
    obj.data.materials.append(mat)
    
    return obj

def test_render(out_png):
    obj = build_sneaker_mesh()
    
    # Lighting
    bpy.ops.object.light_add(type='SUN', location=(1.5, -2.0, 3.0))
    sun = bpy.context.active_object
    sun.data.energy = 3.5
    sun.data.color = (1.0, 0.98, 0.95)
    
    bpy.ops.object.light_add(type='POINT', location=(-1.2, 1.0, 1.5))
    fill = bpy.context.active_object
    fill.data.energy = 50.0
    fill.data.color = (0.7, 0.8, 1.0)
    
    # Camera at 3/4 angle
    bpy.ops.object.camera_add(location=(0.35, -0.42, 0.28))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(65), 0, math.radians(40))
    bpy.context.scene.camera = cam
    
    # Render settings
    scene = bpy.context.scene
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.render.filepath = out_png
    
    bpy.ops.render.render(write_still=True)
    print(f"Rendered test sneaker to {out_png}")

if __name__ == "__main__":
    out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
    out_png = os.path.join(out_dir, "test_render_authentic_sneaker.png")
    test_render(out_png)
