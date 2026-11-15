import bpy
import bmesh
import math
import os

def create_photorealistic_skate_sneaker():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Sneaker_Mesh")
    obj = bpy.data.objects.new("Sneaker_Model", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # SNEAKER OUTLINE GENERATOR
    # Length: 285mm (-0.130 to +0.155)
    # Generates a closed 32-point perimeter polygon for any relative station
    # -------------------------------------------------------------
    PERIM_POINTS = 32
    
    def get_sole_perimeter(z_offset=0.0, scale_xy=1.0, toe_spring_mult=1.0):
        verts = []
        for i in range(PERIM_POINTS):
            ang = i * (2.0 * math.pi / PERIM_POINTS)
            # ang = 0 is +X (lateral), pi/2 is +Y (toe), pi is -X (medial), 3pi/2 is -Y (heel)
            sin_a = math.sin(ang)
            cos_a = math.cos(ang)
            
            # Y position along shoe length
            # sin_a: +1 at toe, -1 at heel
            if sin_a >= 0:
                y = sin_a * 0.155 # 0 to +0.155
            else:
                y = sin_a * 0.130 # 0 to -0.130
                
            t = (y + 0.130) / 0.285
            t = max(0.0, min(1.0, t))
            
            # Width X at this Y
            if t < 0.20: # Heel
                f = t / 0.20
                w = 0.038 * (0.6 + 0.4 * math.sin(f * math.pi * 0.5))
                x_med = -w * 0.98
                x_lat = w * 1.00
            elif t < 0.50: # Waist / Arch
                f = (t - 0.20) / 0.30
                x_med = -(0.038 - 0.015 * math.sin(f * math.pi))
                x_lat = 0.038 + 0.003 * math.sin(f * math.pi)
            elif t < 0.82: # Ball
                f = (t - 0.50) / 0.32
                x_med = -(0.023 + 0.028 * math.sin(f * math.pi * 0.75))
                x_lat = 0.041 + 0.013 * math.sin(f * math.pi * 0.75)
            else: # Toe curve
                f = (t - 0.82) / 0.18
                taper = max(0.05, 1.0 - (f ** 1.3))
                x_med = -0.051 * taper
                x_lat = 0.054 * taper
                
            x = (x_lat if cos_a >= 0 else (-x_med)) * cos_a
            # scale
            x *= scale_xy
            
            # Toe spring Z
            if t > 0.60:
                frac = (t - 0.60) / 0.40
                z = 0.018 * (frac ** 1.8) * toe_spring_mult
            elif t < 0.08:
                z = 0.004 * (1.0 - t / 0.08) # heel rocker
            else:
                z = 0.0
                
            z += z_offset
            verts.append((x, y, z))
        return verts

    # 1. OUTSOLE & MIDSOLE CUPSOLE (Multi-tiered vulcanized rubber)
    # Tier 0: Ground contact tread (Z = 0)
    # Tier 1: Outsole rim (Z = 0.007, gum rubber)
    # Tier 2: Foxing tape top (Z = 0.028 heel / 0.020 toe)
    # Tier 3: Upper welt shelf inset (Z = 0.024)
    perim_bot = get_sole_perimeter(z_offset=0.000, scale_xy=1.04)
    perim_gum = get_sole_perimeter(z_offset=0.007, scale_xy=1.04)
    perim_fox = get_sole_perimeter(z_offset=0.026, scale_xy=1.03)
    perim_shf = get_sole_perimeter(z_offset=0.022, scale_xy=0.98) # Upper sits here
    
    verts_bot = [bm.verts.new(p) for p in perim_bot]
    verts_gum = [bm.verts.new(p) for p in perim_gum]
    verts_fox = [bm.verts.new(p) for p in perim_fox]
    verts_shf = [bm.verts.new(p) for p in perim_shf]
    center_bot = bm.verts.new((0.0, 0.01, 0.0))
    center_shf = bm.verts.new((0.0, 0.01, 0.020)) # Footbed bottom
    
    bm.verts.ensure_lookup_table()
    
    for i in range(PERIM_POINTS):
        nxt = (i + 1) % PERIM_POINTS
        # Bottom sole fill
        bm.faces.new((center_bot, verts_bot[i], verts_bot[nxt]))
        # Gum outsole sidewall
        bm.faces.new((verts_bot[i], verts_bot[nxt], verts_gum[nxt], verts_gum[i]))
        # White foxing tape sidewall
        bm.faces.new((verts_gum[i], verts_gum[nxt], verts_fox[nxt], verts_fox[i]))
        # Top foxing bevel onto shelf
        bm.faces.new((verts_fox[i], verts_fox[nxt], verts_shf[nxt], verts_shf[i]))
        
    # 2. UPPER GEOMETRY
    # The upper extends from perim_shf vertices!
    # Let's categorize perimeter indices:
    # PERIM_POINTS = 32
    # i = 8 is +Y (toe tip, ~6..10)
    # i = 0 is +X (lateral ball)
    # i = 24 is -Y (heel back cap, ~22..26)
    # i = 16 is -X (medial ball)
    #
    # Heel & Collar: indices 19..29 (heel and ankle collar)
    # Eyestays: indices 11..15 (medial eyestay) and 1..5 (lateral eyestay)
    # Toe box (Vamp): indices 6..10 (toe front)
    
    # We build the upper in 3 vertical tiers above shelf:
    # Mid-wall tier: Z = shelf + 0.035 at heel, 0.020 at toe
    # Collar / Eyestay / Vamp crest tier
    # Collar padded rim and inner cavity!
    
    mid_upper_verts = []
    top_upper_verts = []
    inner_rim_verts = []
    inner_drop_verts = []
    
    for i in range(PERIM_POINTS):
        p_shf = perim_shf[i]
        x, y, z_base = p_shf
        t = (y + 0.130) / 0.285
        t = max(0.0, min(1.0, t))
        
        # Calculate heights
        if t < 0.22: # Heel counter
            f = t / 0.22
            z_top = z_base + 0.078 - 0.012 * f
            is_collar = True
            is_throat = False
        elif t < 0.46: # Ankle collar dip
            f = (t - 0.22) / 0.24
            z_top = z_base + 0.066 - 0.014 * math.sin(f * math.pi)
            is_collar = True
            is_throat = False
        elif t < 0.70: # Eyestay panels flanking throat
            f = (t - 0.46) / 0.24
            z_top = z_base + 0.052 - 0.014 * f
            is_collar = False
            is_throat = True
        else: # Domed toe box
            f = (t - 0.70) / 0.30
            z_top = z_base + 0.036 * (1.0 - (f ** 1.3)) + 0.005
            is_collar = False
            is_throat = False
            
        z_mid = z_base + (z_top - z_base) * 0.52
        
        # Mid wall vert (slightly tapered inward)
        vm = bm.verts.new((x * 0.94, y, z_mid))
        mid_upper_verts.append(vm)
        
        # Top vert
        if is_throat:
            # Eyestay pulls toward center leaving an 18mm throat gap
            gap = 0.009
            tx = (-gap) if x < 0 else gap
            vt = bm.verts.new((tx, y, z_top))
        elif is_collar:
            vt = bm.verts.new((x * 0.82, y, z_top))
            # Padded collar rim roll
            vr_inn = bm.verts.new((x * 0.65, y, z_top - 0.006))
            vr_drop = bm.verts.new((x * 0.40, y, z_base + 0.008))
            inner_rim_verts.append((i, vr_inn, vr_drop))
        else:
            # Vamp converges smoothly
            vt = bm.verts.new((x * 0.85, y, z_top))
            
        top_upper_verts.append(vt)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge shelf -> mid_upper -> top_upper around perimeter
    for i in range(PERIM_POINTS):
        nxt = (i + 1) % PERIM_POINTS
        # Shelf to Mid
        bm.faces.new((verts_shf[i], verts_shf[nxt], mid_upper_verts[nxt], mid_upper_verts[i]))
        # Mid to Top
        bm.faces.new((mid_upper_verts[i], mid_upper_verts[nxt], top_upper_verts[nxt], top_upper_verts[i]))
        
    # Bridge collar inner rim and drop into footbed
    # inner_rim_verts contains the collar indices
    for k in range(len(inner_rim_verts) - 1):
        idx0, vr0_inn, vr0_drop = inner_rim_verts[k]
        idx1, vr1_inn, vr1_drop = inner_rim_verts[k + 1]
        if idx1 == idx0 + 1:
            vt0 = top_upper_verts[idx0]
            vt1 = top_upper_verts[idx1]
            # Top to inner roll
            bm.faces.new((vt0, vr0_inn, vr1_inn, vt1))
            # Inner roll down into foot cavity
            bm.faces.new((vr0_inn, vr0_drop, vr1_drop, vr1_inn))
            # Drop down to footbed center
            bm.faces.new((vr0_drop, center_shf, vr1_drop))
            
    # Bridge the toe box dome (vamp indices ~6..10)
    # Vamp crest center
    vamp_crest = bm.verts.new((0.0, 0.075, top_upper_verts[8].co.z + 0.006))
    bm.verts.ensure_lookup_table()
    for i in range(6, 10):
        bm.faces.new((top_upper_verts[i], top_upper_verts[i + 1], vamp_crest))
        
    # 3. REALISTIC PUFFY TONGUE (Emerges from vamp throat, rises proudly above collar)
    tongue_rings = []
    T_STEPS = 8
    for s in range(T_STEPS):
        frac = s / (T_STEPS - 1)
        # Curve up and back
        ty = 0.055 - frac * 0.100 # from +0.055 to -0.045
        tz = 0.048 + frac * 0.068 + 0.006 * math.sin(frac * math.pi) # up to 0.122
        tw = 0.024 + 0.002 * math.sin(frac * math.pi)
        
        # Puffy cross-section
        vt_l = bm.verts.new((-tw, ty, tz + 0.003))
        vt_c = bm.verts.new((0.0, ty, tz + 0.006))
        vt_r = bm.verts.new(( tw, ty, tz + 0.003))
        vb_r = bm.verts.new(( tw * 0.85, ty - 0.003, tz - 0.004))
        vb_c = bm.verts.new((0.0, ty - 0.003, tz - 0.005))
        vb_l = bm.verts.new((-tw * 0.85, ty - 0.003, tz - 0.004))
        tongue_rings.append((vt_l, vt_c, vt_r, vb_r, vb_c, vb_l))
        
    bm.verts.ensure_lookup_table()
    for s in range(T_STEPS - 1):
        r0 = tongue_rings[s]
        r1 = tongue_rings[s + 1]
        bm.faces.new((r0[0], r1[0], r1[1], r0[1])) # top left
        bm.faces.new((r0[1], r1[1], r1[2], r0[2])) # top right
        bm.faces.new((r0[2], r1[2], r1[3], r0[3])) # right side
        bm.faces.new((r0[5], r1[5], r1[0], r0[0])) # left side
        bm.faces.new((r0[3], r1[3], r1[4], r0[4])) # bot right
        bm.faces.new((r0[4], r1[4], r1[5], r0[5])) # bot left
    # Cap tongue top edge
    bm.faces.new((tongue_rings[-1][0], tongue_rings[-1][1], tongue_rings[-1][2],
                  tongue_rings[-1][3], tongue_rings[-1][4], tongue_rings[-1][5]))
                  
    # 4. FAT SKATE LACES (5 Crisp Puffy Laces Across Eyestays)
    lace_stations = [0.042, 0.024, 0.006, -0.012, -0.028]
    for ly in lace_stations:
        t_ly = (ly + 0.130) / 0.285
        lz = 0.060 + (1.0 - t_ly) * 0.040
        lw = 0.0040 # half width
        th = 0.0022 # thickness
        
        lv0 = bm.verts.new((-0.016, ly - lw, lz))
        lv1 = bm.verts.new((-0.016, ly + lw, lz))
        lv2 = bm.verts.new(( 0.016, ly + lw, lz))
        lv3 = bm.verts.new(( 0.016, ly - lw, lz))
        
        lv0_t = bm.verts.new((-0.016, ly - lw, lz + th))
        lv1_t = bm.verts.new((-0.016, ly + lw, lz + th))
        lv2_t = bm.verts.new(( 0.016, ly + lw, lz + th))
        lv3_t = bm.verts.new(( 0.016, ly - lw, lz + th))
        
        bm.faces.new((lv0_t, lv1_t, lv2_t, lv3_t))
        bm.faces.new((lv0, lv3, lv2, lv1))
        bm.faces.new((lv0, lv1, lv1_t, lv0_t))
        bm.faces.new((lv2, lv3, lv3_t, lv2_t))
        bm.faces.new((lv1, lv2, lv2_t, lv1_t))
        bm.faces.new((lv3, lv0, lv0_t, lv3_t))
        
    # 5. ATELIER DISPLAY PEDESTAL
    PED_SEGS = 32
    ped_rad = 0.180
    center_top = bm.verts.new((0.0, 0.0, -0.004))
    center_bot = bm.verts.new((0.0, 0.0, -0.020))
    ped_top = [bm.verts.new((math.cos(i*2*math.pi/PED_SEGS)*ped_rad, math.sin(i*2*math.pi/PED_SEGS)*ped_rad, -0.004)) for i in range(PED_SEGS)]
    ped_bot = [bm.verts.new((math.cos(i*2*math.pi/PED_SEGS)*ped_rad*1.03, math.sin(i*2*math.pi/PED_SEGS)*ped_rad*1.03, -0.020)) for i in range(PED_SEGS)]
    
    bm.verts.ensure_lookup_table()
    for i in range(PED_SEGS):
        nxt = (i + 1) % PED_SEGS
        bm.faces.new((center_top, ped_top[i], ped_top[nxt]))
        bm.faces.new((ped_top[i], ped_bot[i], ped_bot[nxt], ped_top[nxt]))
        bm.faces.new((center_bot, ped_bot[nxt], ped_bot[i]))
        
    bm.to_mesh(mesh)
    bm.free()
    
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    
    # Material
    mat = bpy.data.materials.new(name="Sneaker_PBR")
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.86, 0.83, 0.80, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.50
    obj.data.materials.append(mat)
    
    return obj

def test_render_sneaker(out_png):
    create_photorealistic_skate_sneaker()
    
    # Studio 3-point lighting
    bpy.ops.object.light_add(type='SUN', location=(2.0, -2.5, 3.5))
    sun = bpy.context.active_object
    sun.data.energy = 4.0
    sun.data.color = (1.0, 0.98, 0.95)
    
    bpy.ops.object.light_add(type='POINT', location=(-1.5, 1.2, 1.8))
    fill = bpy.context.active_object
    fill.data.energy = 55.0
    fill.data.color = (0.75, 0.85, 1.0)
    
    bpy.ops.object.light_add(type='POINT', location=(0.0, 2.5, 1.2))
    rim = bpy.context.active_object
    rim.data.energy = 45.0
    rim.data.color = (1.0, 1.0, 1.0)
    
    # Camera at classic 3/4 beauty sneaker angle
    bpy.ops.object.camera_add(location=(0.38, -0.42, 0.28))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(65), 0, math.radians(42))
    bpy.context.scene.camera = cam
    
    scene = bpy.context.scene
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.render.filepath = out_png
    
    bpy.ops.render.render(write_still=True)
    print(f"Photorealistic sneaker render saved to {out_png}")

if __name__ == "__main__":
    out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
    out_png = os.path.join(out_dir, "test_render_photorealistic_sneaker.png")
    test_render_sneaker(out_png)
