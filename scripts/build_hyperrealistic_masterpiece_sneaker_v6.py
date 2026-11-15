import bpy
import bmesh
import math
import os

def create_masterpiece_sneaker(out_glb_path, out_render_beauty):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # -------------------------------------------------------------
    # 1. PBR MATERIALS
    # -------------------------------------------------------------
    mat_gum = bpy.data.materials.new("Mat_Gum")
    mat_gum.use_nodes = True
    bsdf_g = mat_gum.node_tree.nodes.get("Principled BSDF")
    bsdf_g.inputs['Base Color'].default_value = (0.78, 0.52, 0.28, 1.0) # Warm Raw Gum Rubber
    bsdf_g.inputs['Roughness'].default_value = 0.50
    
    mat_leather = bpy.data.materials.new("Mat_Leather")
    mat_leather.use_nodes = True
    bsdf_l = mat_leather.node_tree.nodes.get("Principled BSDF")
    bsdf_l.inputs['Base Color'].default_value = (0.93, 0.91, 0.88, 1.0) # Bone tumbled leather
    bsdf_l.inputs['Roughness'].default_value = 0.38
    
    mat_suede = bpy.data.materials.new("Mat_Suede")
    mat_suede.use_nodes = True
    bsdf_s = mat_suede.node_tree.nodes.get("Principled BSDF")
    bsdf_s.inputs['Base Color'].default_value = (0.28, 0.17, 0.11, 1.0) # Chocolate brown suede
    bsdf_s.inputs['Roughness'].default_value = 0.92
    
    mat_silver = bpy.data.materials.new("Mat_Silver")
    mat_silver.use_nodes = True
    bsdf_m = mat_silver.node_tree.nodes.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.95, 0.96, 0.98, 1.0) # Shiny brushed silver
    bsdf_m.inputs['Metallic'].default_value = 0.95
    bsdf_m.inputs['Roughness'].default_value = 0.12
    
    mat_lace = bpy.data.materials.new("Mat_Lace")
    mat_lace.use_nodes = True
    bsdf_c = mat_lace.node_tree.nodes.get("Principled BSDF")
    bsdf_c.inputs['Base Color'].default_value = (0.98, 0.98, 0.98, 1.0) # Crisp white fat laces
    bsdf_c.inputs['Roughness'].default_value = 0.65
    
    mat_inner = bpy.data.materials.new("Mat_Inner")
    mat_inner.use_nodes = True
    bsdf_i = mat_inner.node_tree.nodes.get("Principled BSDF")
    bsdf_i.inputs['Base Color'].default_value = (0.08, 0.08, 0.09, 1.0)
    bsdf_i.inputs['Roughness'].default_value = 0.95
    
    mat_ped = bpy.data.materials.new("Mat_Pedestal")
    mat_ped.use_nodes = True
    bsdf_p = mat_ped.node_tree.nodes.get("Principled BSDF")
    bsdf_p.inputs['Base Color'].default_value = (0.45, 0.45, 0.46, 1.0)
    bsdf_p.inputs['Roughness'].default_value = 0.85

    # -------------------------------------------------------------
    # 2. SKATE SNEAKER GEOMETRY (SOLID, BROAD TOE, FLAT STURDY CUPSOLE)
    # -------------------------------------------------------------
    STATIONS = 32
    y_vals = [-0.130 + s * (0.280 / (STATIONS - 1)) for s in range(STATIONS)]
    
    def foot_profile(y):
        t = (y + 0.130) / 0.280
        t = max(0.0, min(1.0, t))
        
        # 14mm gentle toe spring curve
        if t > 0.65:
            frac = (t - 0.65) / 0.35
            z_floor = 0.014 * (frac ** 1.8)
        elif t < 0.08:
            z_floor = 0.002 * (1.0 - t / 0.08)
        else:
            z_floor = 0.000
            
        sole_thick = 0.028 - 0.006 * t # 28mm heel to 22mm toe
        z_rim = z_floor + sole_thick
        
        # Skate cupsole footprint: stable, broad, rounded
        # Heel rounding
        r_heel = math.sqrt(max(0.01, 1.0 - ((0.12 - t) / 0.12) ** 2)) if t < 0.12 else 1.0
        # Broad rounded toe box (rounds over the front 10% smoothly)
        r_toe = math.sqrt(max(0.01, 1.0 - ((t - 0.85) / 0.15) ** 2)) if t > 0.85 else 1.0
        
        # Flat sturdy skate sole widths
        if t < 0.25: # Heel
            xm = -0.038 * r_heel
            xl =  0.039 * r_heel
        elif t < 0.55: # Waist / Arch (subtle taper only)
            f = (t - 0.25) / 0.30
            xm = -(0.038 - 0.005 * math.sin(f * math.pi))
            xl =  (0.039 + 0.002 * math.sin(f * math.pi))
        elif t < 0.85: # Ball of foot (roomy skate width)
            f = (t - 0.55) / 0.30
            xm = -(0.035 + 0.013 * math.sin(f * math.pi * 0.8))
            xl =  (0.041 + 0.012 * math.sin(f * math.pi * 0.8))
        else: # Broad round toe cap
            xm = -0.046 * r_toe
            xl =  0.050 * r_toe
            
        return z_floor, z_rim, xm, xl

    mesh = bpy.data.meshes.new("Sneaker_Mesh")
    obj = bpy.data.objects.new("Sneaker_Model", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(mat_gum)     # 0: Gum sole
    obj.data.materials.append(mat_leather) # 1: Bone leather
    obj.data.materials.append(mat_suede)   # 2: Chocolate suede
    obj.data.materials.append(mat_inner)   # 3: Dark inner lining
    obj.data.materials.append(mat_lace)    # 4: White fat laces
    obj.data.materials.append(mat_silver)  # 5: Brushed silver wave
    obj.data.materials.append(mat_ped)     # 6: Concrete pedestal
    
    bm = bmesh.new()
    
    stations_data = []
    for s, y in enumerate(y_vals):
        z_floor, z_rim, xm, xl = foot_profile(y)
        t = (y + 0.130) / 0.280
        
        # Sole bottom
        vb_l = bm.verts.new((xl * 1.015, y, z_floor))
        vb_c = bm.verts.new((0.0,        y, z_floor))
        vb_m = bm.verts.new((xm * 1.015, y, z_floor))
        
        # Sole mid groove
        z_mid = z_floor + (z_rim - z_floor) * 0.65
        vm_l = bm.verts.new((xl * 1.015, y, z_mid))
        vm_m = bm.verts.new((xm * 1.015, y, z_mid))
        
        # Exact shared rim
        vr_l = bm.verts.new((xl * 0.98, y, z_rim))
        vr_m = bm.verts.new((xm * 0.98, y, z_rim))
        
        # Upper heights
        if t < 0.22: # Heel counter
            z_top = z_rim + 0.058 - 0.010 * (t / 0.22)
            zone = 'collar'
        elif t < 0.48: # Ankle dip
            f = (t - 0.22) / 0.26
            z_top = z_rim + 0.048 - 0.012 * math.sin(f * math.pi)
            zone = 'collar'
        elif t < 0.72: # Throat
            f = (t - 0.48) / 0.24
            z_top = z_rim + 0.038 - 0.008 * f
            zone = 'throat'
        else: # Domed Vamp
            f = (t - 0.72) / 0.28
            z_top = z_rim + 0.026 * (1.0 - (f ** 1.3)) + 0.004
            zone = 'vamp'
            
        dz = z_top - z_rim
        
        vu1_l = bm.verts.new((xl * 0.95, y, z_rim + dz * 0.38))
        vu1_m = bm.verts.new((xm * 0.95, y, z_rim + dz * 0.38))
        
        vu2_l = bm.verts.new((xl * 0.88, y, z_rim + dz * 0.72))
        vu2_m = bm.verts.new((xm * 0.88, y, z_rim + dz * 0.72))
        
        if zone == 'collar':
            vu3_l = bm.verts.new((xl * 0.65, y, z_top))
            vu3_m = bm.verts.new((xm * 0.65, y, z_top))
            vin_l = bm.verts.new((xl * 0.50, y, z_top - 0.016))
            vin_m = bm.verts.new((xm * 0.50, y, z_top - 0.016))
        elif zone == 'throat':
            vu3_l = bm.verts.new(( 0.014, y, z_top))
            vu3_m = bm.verts.new((-0.014, y, z_top))
            vin_l = bm.verts.new(( 0.010, y, z_top - 0.010))
            vin_m = bm.verts.new((-0.010, y, z_top - 0.010))
        else: # vamp
            vu3_l = bm.verts.new((xl * 0.38, y, z_top + 0.003))
            vu3_m = bm.verts.new((xm * 0.38, y, z_top + 0.003))
            vin_l = None
            vin_m = None
            
        stations_data.append({
            'sole_b': (vb_l, vb_c, vb_m),
            'sole_m': (vm_l, vm_m),
            'rim':    (vr_l, vr_m),
            'up_1':   (vu1_l, vu1_m),
            'up_2':   (vu2_l, vu2_m),
            'up_3':   (vu3_l, vu3_m),
            'in':     (vin_l, vin_m),
            'zone':   zone
        })
        
    bm.verts.ensure_lookup_table()
    
    for s in range(STATIONS - 1):
        s0 = stations_data[s]
        s1 = stations_data[s + 1]
        
        # Sole bottom (Gum)
        f_b0 = bm.faces.new((s0['sole_b'][0], s1['sole_b'][0], s1['sole_b'][1], s0['sole_b'][1]))
        f_b1 = bm.faces.new((s0['sole_b'][1], s1['sole_b'][1], s1['sole_b'][2], s0['sole_b'][2]))
        f_b0.material_index = 0
        f_b1.material_index = 0
        
        # Sole sidewalls (Gum)
        f_sl0 = bm.faces.new((s0['sole_b'][0], s0['sole_m'][0], s1['sole_m'][0], s1['sole_b'][0]))
        f_sl1 = bm.faces.new((s0['sole_m'][0], s0['rim'][0],    s1['rim'][0],    s1['sole_m'][0]))
        f_sm0 = bm.faces.new((s0['sole_b'][2], s1['sole_b'][2], s1['sole_m'][1], s0['sole_m'][1]))
        f_sm1 = bm.faces.new((s0['sole_m'][1], s1['sole_m'][1], s1['rim'][1],    s0['rim'][1]))
        f_sl0.material_index = 0
        f_sl1.material_index = 0
        f_sm0.material_index = 0
        f_sm1.material_index = 0
        
        # Upper walls
        f_ul0 = bm.faces.new((s0['rim'][0],  s0['up_1'][0], s1['up_1'][0], s1['rim'][0]))
        f_ul1 = bm.faces.new((s0['up_1'][0], s0['up_2'][0], s1['up_2'][0], s1['up_1'][0]))
        f_ul2 = bm.faces.new((s0['up_2'][0], s0['up_3'][0], s1['up_3'][0], s1['up_2'][0]))
        
        f_um0 = bm.faces.new((s0['rim'][1],  s1['rim'][1],  s1['up_1'][1], s0['up_1'][1]))
        f_um1 = bm.faces.new((s0['up_1'][1], s1['up_1'][1], s1['up_2'][1], s0['up_2'][1]))
        f_um2 = bm.faces.new((s0['up_2'][1], s1['up_2'][1], s1['up_3'][1], s0['up_3'][1]))
        
        # Suede quarter panel (stations 7 to 22)
        if 7 <= s <= 21:
            f_ul0.material_index = 1
            f_um0.material_index = 1
            f_ul1.material_index = 2
            f_um1.material_index = 2
            f_ul2.material_index = 2
            f_um2.material_index = 2
        else:
            f_ul0.material_index = 1
            f_um0.material_index = 1
            f_ul1.material_index = 1
            f_um1.material_index = 1
            f_ul2.material_index = 1
            f_um2.material_index = 1
            
        # Top vamp deck
        if s0['zone'] == 'vamp' and s1['zone'] == 'vamp':
            f_v = bm.faces.new((s0['up_3'][0], s0['up_3'][1], s1['up_3'][1], s1['up_3'][0]))
            f_v.material_index = 1
        elif s0['zone'] == 'throat' and s1['zone'] == 'vamp':
            f_v = bm.faces.new((s0['up_3'][0], s0['up_3'][1], s1['up_3'][1], s1['up_3'][0]))
            f_v.material_index = 1
            
        # Inner collar lining
        if s0['in'][0] and s1['in'][0]:
            f_il = bm.faces.new((s0['up_3'][0], s1['up_3'][0], s1['in'][0], s0['in'][0]))
            f_im = bm.faces.new((s0['up_3'][1], s0['in'][1], s1['in'][1], s1['up_3'][1]))
            f_il.material_index = 3
            f_im.material_index = 3
            
    # Rounded heel cap
    sh = stations_data[0]
    f_hc = bm.faces.new((sh['sole_b'][0], sh['sole_m'][0], sh['rim'][0], sh['up_1'][0], sh['up_2'][0], sh['up_3'][0],
                         sh['up_3'][1], sh['up_2'][1], sh['up_1'][1], sh['rim'][1], sh['sole_m'][1], sh['sole_b'][2], sh['sole_b'][1]))
    f_hc.material_index = 1
    
    # Smooth rounded toe bumper cap
    st = stations_data[-1]
    f_tc = bm.faces.new((st['sole_b'][1], st['sole_b'][2], st['sole_m'][1], st['rim'][1], st['up_1'][1], st['up_2'][1], st['up_3'][1],
                         st['up_3'][0], st['up_2'][0], st['up_1'][0], st['rim'][0], st['sole_m'][0], st['sole_b'][0]))
    f_tc.material_index = 0
    
    # Heel pull loop
    tab_y = -0.132
    tab_w = 0.007
    tab_pts = [
        (-tab_w, tab_y, 0.068),
        (-tab_w, tab_y - 0.015, 0.086),
        ( tab_w, tab_y - 0.015, 0.086),
        ( tab_w, tab_y, 0.068),
    ]
    t_verts = [bm.verts.new(p) for p in tab_pts]
    f_tab = bm.faces.new(t_verts)
    f_tab.material_index = 2
    
    # -------------------------------------------------------------
    # 4. PUFFY PADDED TONGUE
    # -------------------------------------------------------------
    T_STEPS = 12
    t_rings = []
    for i in range(T_STEPS):
        frac = i / (T_STEPS - 1)
        ty = 0.055 - frac * 0.088
        tz = 0.046 + frac * 0.054 + 0.005 * math.sin(frac * math.pi)
        tw = 0.022 + 0.002 * math.sin(frac * math.pi)
        
        p0 = bm.verts.new(( -tw,       ty, tz + 0.003))
        p1 = bm.verts.new((  0.0,       ty, tz + 0.006))
        p2 = bm.verts.new((  tw,       ty, tz + 0.003))
        p3 = bm.verts.new((  tw * 0.8, ty - 0.003, tz - 0.004))
        p4 = bm.verts.new((  0.0,       ty - 0.003, tz - 0.006))
        p5 = bm.verts.new(( -tw * 0.8, ty - 0.003, tz - 0.004))
        t_rings.append((p0, p1, p2, p3, p4, p5))
        
    bm.verts.ensure_lookup_table()
    for s in range(T_STEPS - 1):
        r0 = t_rings[s]
        r1 = t_rings[s + 1]
        for k in range(6):
            knxt = (k + 1) % 6
            f = bm.faces.new((r0[k], r1[k], r1[knxt], r0[knxt]))
            f.material_index = 1 if k in (0, 1, 2) else 3
            
    f_ttop = bm.faces.new(reversed(t_rings[-1]))
    f_ttop.material_index = 1
    
    # Black woven patch with HooDoo branding
    lbl_y = -0.024
    lbl_z = 0.098
    l0 = bm.verts.new((-0.012, lbl_y - 0.008, lbl_z + 0.004))
    l1 = bm.verts.new((-0.012, lbl_y + 0.008, lbl_z + 0.004))
    l2 = bm.verts.new(( 0.012, lbl_y + 0.008, lbl_z + 0.004))
    l3 = bm.verts.new(( 0.012, lbl_y - 0.008, lbl_z + 0.004))
    f_lbl = bm.faces.new((l0, l1, l2, l3))
    f_lbl.material_index = 3
    
    # -------------------------------------------------------------
    # 5. 5 CHUNKY FAT WHITE SKATE LACES (CURVED OVER PUFFY TONGUE)
    # -------------------------------------------------------------
    lace_stations = [
        # (y, z, span_half_width)
        ( 0.046, 0.054, 0.018), # 1: Vamp throat base
        ( 0.028, 0.065, 0.019), # 2
        ( 0.010, 0.076, 0.020), # 3
        (-0.008, 0.086, 0.021), # 4
        (-0.024, 0.095, 0.022), # 5: Top lace near collar
    ]
    
    for ly, lz, span in lace_stations:
        lw = 0.0045
        th = 0.0026
        lz_e = lz + 0.0052
        
        v_l  = bm.verts.new((-span,        ly - lw, lz_e))
        v_cl = bm.verts.new((-span * 0.45, ly - lw, lz_e + 0.0025))
        v_cr = bm.verts.new(( span * 0.45, ly - lw, lz_e + 0.0025))
        v_r  = bm.verts.new(( span,        ly - lw, lz_e))
        
        v_l_f  = bm.verts.new((-span,        ly + lw, lz_e))
        v_cl_f = bm.verts.new((-span * 0.45, ly + lw, lz_e + 0.0025))
        v_cr_f = bm.verts.new(( span * 0.45, ly + lw, lz_e + 0.0025))
        v_r_f  = bm.verts.new(( span,        ly + lw, lz_e))
        
        v_l_t  = bm.verts.new((-span,        ly - lw, lz_e + th))
        v_cl_t = bm.verts.new((-span * 0.45, ly - lw, lz_e + th + 0.0025))
        v_cr_t = bm.verts.new(( span * 0.45, ly - lw, lz_e + th + 0.0025))
        v_r_t  = bm.verts.new(( span,        ly - lw, lz_e + th))
        
        v_l_ft  = bm.verts.new((-span,        ly + lw, lz_e + th))
        v_cl_ft = bm.verts.new((-span * 0.45, ly + lw, lz_e + th + 0.0025))
        v_cr_ft = bm.verts.new(( span * 0.45, ly + lw, lz_e + th + 0.0025))
        v_r_ft  = bm.verts.new(( span,        ly + lw, lz_e + th))
        
        f_t0 = bm.faces.new((v_l_t,  v_cl_t,  v_cl_ft, v_l_ft))
        f_t1 = bm.faces.new((v_cl_t, v_cr_t,  v_cr_ft, v_cl_ft))
        f_t2 = bm.faces.new((v_cr_t, v_r_t,   v_r_ft,  v_cr_ft))
        
        f_f0 = bm.faces.new((v_l_ft, v_cl_ft, v_cl_f,  v_l_f))
        f_f1 = bm.faces.new((v_cl_ft,v_cr_ft, v_cr_f,  v_cl_f))
        f_f2 = bm.faces.new((v_cr_ft,v_r_ft,  v_r_f,   v_cr_f))
        
        f_b0 = bm.faces.new((v_l,    v_cl,    v_cl_t,  v_l_t))
        f_b1 = bm.faces.new((v_cl,   v_cr,    v_cr_t,  v_cl_t))
        f_b2 = bm.faces.new((v_cr,   v_r,     v_r_t,   v_cr_t))
        
        for fl in [f_t0, f_t1, f_t2, f_f0, f_f1, f_f2, f_b0, f_b1, f_b2]:
            fl.material_index = 4
            
    # -------------------------------------------------------------
    # 6. SIGNATURE BRUSHED SILVER WAVE INSIGNIA (~)
    # Stitched 3D badge with 2mm proud thickness
    # -------------------------------------------------------------
    wave_curve = [
        # (x_sc, y, z, height)
        (0.97, -0.065, 0.052, 0.007),
        (0.98, -0.040, 0.058, 0.011),
        (0.98, -0.015, 0.049, 0.010),
        (0.97,  0.010, 0.056, 0.012),
        (0.96,  0.035, 0.048, 0.008),
    ]
    
    # Build 3D solid ribbon for lateral wave
    w_bl_in  = []
    w_tl_in  = []
    w_bl_out = []
    w_tl_out = []
    for xr, wy, wz, wh in wave_curve:
        _, _, xm, xl = foot_profile(wy)
        base_x = xl * xr + 0.0040
        w_bl_in.append(bm.verts.new((base_x, wy, wz)))
        w_tl_in.append(bm.verts.new((base_x, wy, wz + wh)))
        w_bl_out.append(bm.verts.new((base_x + 0.0022, wy, wz)))
        w_tl_out.append(bm.verts.new((base_x + 0.0022, wy, wz + wh)))
        
    bm.verts.ensure_lookup_table()
    for k in range(len(wave_curve) - 1):
        fw_out = bm.faces.new((w_bl_out[k], w_bl_out[k+1], w_tl_out[k+1], w_tl_out[k]))
        fw_top = bm.faces.new((w_tl_in[k], w_tl_in[k+1], w_tl_out[k+1], w_tl_out[k]))
        fw_bot = bm.faces.new((w_bl_in[k], w_bl_out[k], w_bl_out[k+1], w_bl_in[k+1]))
        fw_out.material_index = 5
        fw_top.material_index = 5
        fw_bot.material_index = 5

    # -------------------------------------------------------------
    # 7. ATELIER DISPLAY PEDESTAL (Concrete Disc)
    # -------------------------------------------------------------
    P_SEGS = 32
    ped_r = 0.180
    c_top = bm.verts.new((0.0, 0.012, 0.000))
    c_bot = bm.verts.new((0.0, 0.012, -0.024))
    
    r_top = []
    r_bot = []
    for i in range(P_SEGS):
        ang = i * (2.0 * math.pi / P_SEGS)
        px = math.cos(ang) * ped_r
        py = math.sin(ang) * ped_r + 0.012
        r_top.append(bm.verts.new((px, py, 0.000)))
        r_bot.append(bm.verts.new((px * 1.03, py, -0.024)))
        
    bm.verts.ensure_lookup_table()
    for i in range(P_SEGS):
        inxt = (i + 1) % P_SEGS
        f0 = bm.faces.new((c_top, r_top[i], r_top[inxt]))
        f1 = bm.faces.new((r_top[i], r_bot[i], r_bot[inxt], r_top[inxt]))
        f2 = bm.faces.new((c_bot, r_bot[inxt], r_bot[i]))
        f0.material_index = 6
        f1.material_index = 6
        f2.material_index = 6
        
    # Dual-Panel UV Mapping
    uv_layer = bm.loops.layers.uv.new("UVMap")
    for face in bm.faces:
        for loop in face.loops:
            v = loop.vert
            vx, vy, vz = v.co.x, v.co.y, v.co.z
            u_norm = max(0.0, min(1.0, (vx + 0.12) / 0.24))
            v_norm = max(0.0, min(1.0, (vy + 0.14) / 0.30))
            loop[uv_layer].uv = (u_norm, v_norm)
            
    bm.to_mesh(mesh)
    bm.free()
    
    sub = obj.modifiers.new("Subsurf", type='SUBSURF')
    sub.levels = 1
    for p in mesh.polygons: p.use_smooth = True
    
    # Export GLB
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False
    )
    print(f"Exported Masterpiece Sneaker GLB: {out_glb_path}")

    # -------------------------------------------------------------
    # BEAUTY CAMERA & STUDIO LIGHTING
    # -------------------------------------------------------------
    cam_data = bpy.data.cameras.new("Cam")
    cam_obj = bpy.data.objects.new("Cam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    # Front-lateral 3/4 beauty perspective:
    cam_obj.location = (0.34, 0.36, 0.18)
    cam_obj.rotation_euler = (math.radians(72), 0, math.radians(138))
    
    # Key light illuminating from camera position directly onto front and lateral face
    light_data = bpy.data.lights.new("Key_Sun", type='SUN')
    light_data.energy = 4.8
    light_obj = bpy.data.objects.new("Key_Sun", light_data)
    bpy.context.collection.objects.link(light_obj)
    light_obj.location = (1.5, 1.5, 2.5)
    # Shines towards origin from (+X, +Y, +Z)
    light_obj.rotation_euler = (math.radians(55), math.radians(-25), math.radians(-40))
    
    # Fill light from opposite side
    fill_data = bpy.data.lights.new("Fill_Sun", type='SUN')
    fill_data.energy = 2.0
    fill_obj = bpy.data.objects.new("Fill_Sun", fill_data)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-1.5, -1.0, 1.8)
    fill_obj.rotation_euler = (math.radians(45), math.radians(30), math.radians(140))
    
    bpy.context.scene.render.resolution_x = 1200
    bpy.context.scene.render.resolution_y = 1200
    bpy.context.scene.render.filepath = out_render_beauty
    bpy.ops.render.render(write_still=True)
    print(f"Saved Front 3/4 Beauty Render: {out_render_beauty}")

if __name__ == '__main__':
    out_glb = "public/models/kicks_p9.glb"
    out_png = os.path.expanduser("~/.gemini/antigravity/brain/234f9af8-00da-4e48-94a4-b01c33156985/test_render_masterpiece_sneaker_v6.png")
    create_masterpiece_sneaker(out_glb, out_png)
