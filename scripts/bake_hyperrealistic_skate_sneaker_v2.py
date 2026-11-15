import bpy
import bmesh
import math
import os

def create_hyperrealistic_skate_sneaker(out_glb_path, texture_path=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    world = bpy.data.worlds.new('Studio_World')
    bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.22, 0.23, 0.25, 1.0)
        bg_node.inputs['Strength'].default_value = 1.2
        
    # PBR Materials
    mat_gum = bpy.data.materials.new("Mat_Gum")
    mat_gum.use_nodes = True
    bsdf_g = mat_gum.node_tree.nodes.get("Principled BSDF")
    bsdf_g.inputs['Base Color'].default_value = (0.76, 0.49, 0.25, 1.0) # Raw Gum Rubber
    bsdf_g.inputs['Roughness'].default_value = 0.50
    
    mat_leather = bpy.data.materials.new("Mat_Leather")
    mat_leather.use_nodes = True
    bsdf_l = mat_leather.node_tree.nodes.get("Principled BSDF")
    bsdf_l.inputs['Base Color'].default_value = (0.94, 0.92, 0.89, 1.0) # Bone Tumbled Leather
    bsdf_l.inputs['Roughness'].default_value = 0.36
    
    mat_suede = bpy.data.materials.new("Mat_Suede")
    mat_suede.use_nodes = True
    bsdf_s = mat_suede.node_tree.nodes.get("Principled BSDF")
    bsdf_s.inputs['Base Color'].default_value = (0.26, 0.16, 0.10, 1.0) # Deep Chocolate Suede
    bsdf_s.inputs['Roughness'].default_value = 0.94
    
    mat_silver = bpy.data.materials.new("Mat_Silver")
    mat_silver.use_nodes = True
    bsdf_m = mat_silver.node_tree.nodes.get("Principled BSDF")
    bsdf_m.inputs['Base Color'].default_value = (0.95, 0.96, 0.98, 1.0)
    bsdf_m.inputs['Metallic'].default_value = 0.45
    bsdf_m.inputs['Roughness'].default_value = 0.22
    
    mat_lace = bpy.data.materials.new("Mat_Lace")
    mat_lace.use_nodes = True
    bsdf_c = mat_lace.node_tree.nodes.get("Principled BSDF")
    bsdf_c.inputs['Base Color'].default_value = (0.98, 0.98, 0.98, 1.0) # Crisp White Fat Laces
    bsdf_c.inputs['Roughness'].default_value = 0.65
    
    mat_inner = bpy.data.materials.new("Mat_Inner")
    mat_inner.use_nodes = True
    bsdf_i = mat_inner.node_tree.nodes.get("Principled BSDF")
    bsdf_i.inputs['Base Color'].default_value = (0.07, 0.07, 0.08, 1.0) # Dark Velvet Lining
    bsdf_i.inputs['Roughness'].default_value = 0.95
    
    mat_ped = bpy.data.materials.new("Mat_Pedestal")
    mat_ped.use_nodes = True
    bsdf_p = mat_ped.node_tree.nodes.get("Principled BSDF")
    bsdf_p.inputs['Base Color'].default_value = (0.42, 0.42, 0.43, 1.0) # Atelier Concrete Pedestal
    bsdf_p.inputs['Roughness'].default_value = 0.88

    # Skate Shoe Geometry Parameters
    # Y-axis: -0.130 (heel) to +0.150 (toe)
    STATIONS = 32
    y_stations = [-0.130 + i * (0.280 / (STATIONS - 1)) for i in range(STATIONS)]
    
    def profile_params(y):
        t = (y + 0.130) / 0.280
        t = max(0.0, min(1.0, t))
        
        # 1. Sole Floor & Toe Spring
        if t > 0.62:
            frac = (t - 0.62) / 0.38
            z_floor = 0.013 * (frac ** 1.9)
        elif t < 0.08:
            z_floor = 0.002 * (1.0 - t / 0.08)
        else:
            z_floor = 0.000
            
        sole_height = 0.026 - 0.005 * t
        z_rim = z_floor + sole_height
        
        # 2. Width Contours (Lateral xl > 0, Medial xm < 0)
        # Broad rounded skate toe box
        r_heel = math.sqrt(max(0.01, 1.0 - ((0.12 - t) / 0.12) ** 2)) if t < 0.12 else 1.0
        r_toe = math.sqrt(max(0.01, 1.0 - ((t - 0.82) / 0.18) ** 2)) if t > 0.82 else 1.0
        
        if t < 0.25:
            xm = -0.038 * r_heel
            xl =  0.039 * r_heel
        elif t < 0.55:
            f = (t - 0.25) / 0.30
            xm = -(0.038 - 0.003 * math.sin(f * math.pi))
            xl =  (0.039 + 0.002 * math.sin(f * math.pi))
        elif t < 0.85:
            f = (t - 0.55) / 0.30
            xm = -(0.035 + 0.011 * math.sin(f * math.pi * 0.85))
            xl =  (0.041 + 0.010 * math.sin(f * math.pi * 0.85))
        else:
            xm = -0.045 * r_toe
            xl =  0.048 * r_toe
            
        # 3. Upper Top Profile (smooth continuous spline)
        if t < 0.20:
            # Heel collar
            f = t / 0.20
            z_top = z_rim + 0.056 - 0.008 * f
            throat_half_w = 0.024 - 0.002 * f
            has_throat = False
        elif t < 0.44:
            # Ankle collar curve dipping to eyestay base
            f = (t - 0.20) / 0.24
            z_top = z_rim + 0.048 - 0.010 * math.sin(f * math.pi * 0.5)
            throat_half_w = 0.022 - 0.008 * f
            has_throat = False if t < 0.30 else True
        elif t < 0.72:
            # Eyestay lace throat
            f = (t - 0.44) / 0.28
            z_top = z_rim + 0.038 - 0.008 * f
            throat_half_w = 0.014 - 0.004 * f
            has_throat = True
        else:
            # Vamp and broad rounded toe box
            f = (t - 0.72) / 0.28
            z_top = z_rim + 0.028 * (1.0 - (f ** 1.4)) + 0.003
            throat_half_w = 0.0
            has_throat = False
            
        return z_floor, z_rim, z_top, xm, xl, throat_half_w, has_throat

    # 1. Main Sneaker Upper & Sole Mesh
    mesh = bpy.data.meshes.new("Sneaker_Mesh")
    obj = bpy.data.objects.new("Sneaker_Model", mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.data.materials.append(mat_gum)     # 0: Gum rubber sole
    obj.data.materials.append(mat_leather) # 1: Bone leather upper
    obj.data.materials.append(mat_suede)   # 2: Chocolate suede quarters
    obj.data.materials.append(mat_inner)   # 3: Padded interior
    
    bm = bmesh.new()
    station_loops = []
    
    for s, y in enumerate(y_stations):
        z_fl, z_rm, z_tp, xm, xl, th_w, has_th = profile_params(y)
        t = (y + 0.130) / 0.280
        
        # Sole bottom (3 points: lateral, center, medial)
        v_b_l = bm.verts.new((xl * 1.015, y, z_fl))
        v_b_c = bm.verts.new((0.0,         y, z_fl))
        v_b_m = bm.verts.new((xm * 1.015, y, z_fl))
        
        # Sole mid-rib (foxing line)
        z_mid = z_fl + (z_rm - z_fl) * 0.60
        v_m_l = bm.verts.new((xl * 1.015, y, z_mid))
        v_m_m = bm.verts.new((xm * 1.015, y, z_mid))
        
        # Cupsole top rim
        v_r_l = bm.verts.new((xl * 0.98, y, z_rm))
        v_r_m = bm.verts.new((xm * 0.98, y, z_rm))
        
        # Upper layers
        dz = z_tp - z_rm
        v_u1_l = bm.verts.new((xl * 0.95, y, z_rm + dz * 0.35))
        v_u1_m = bm.verts.new((xm * 0.95, y, z_rm + dz * 0.35))
        
        v_u2_l = bm.verts.new((xl * 0.88, y, z_rm + dz * 0.70))
        v_u2_m = bm.verts.new((xm * 0.88, y, z_rm + dz * 0.70))
        
        if has_th:
            v_u3_l = bm.verts.new(( th_w, y, z_tp))
            v_u3_m = bm.verts.new((-th_w, y, z_tp))
            v_in_l = bm.verts.new(( th_w * 0.7, y, z_tp - 0.010))
            v_in_m = bm.verts.new((-th_w * 0.7, y, z_tp - 0.010))
        elif t < 0.30:
            # Collar opening
            v_u3_l = bm.verts.new((xl * 0.65, y, z_tp))
            v_u3_m = bm.verts.new((xm * 0.65, y, z_tp))
            v_in_l = bm.verts.new((xl * 0.50, y, z_tp - 0.015))
            v_in_m = bm.verts.new((xm * 0.50, y, z_tp - 0.015))
        else:
            # Solid vamp
            v_u3_l = bm.verts.new((xl * 0.38, y, z_tp + 0.002))
            v_u3_m = bm.verts.new((xm * 0.38, y, z_tp + 0.002))
            v_in_l = None
            v_in_m = None
            
        station_loops.append({
            'b': (v_b_l, v_b_c, v_b_m),
            'm': (v_m_l, v_m_m),
            'r': (v_r_l, v_r_m),
            'u1': (v_u1_l, v_u1_m),
            'u2': (v_u2_l, v_u2_m),
            'u3': (v_u3_l, v_u3_m),
            'in': (v_in_l, v_in_m),
            'has_th': has_th,
            'is_vamp': (t >= 0.72)
        })
        
    bm.verts.ensure_lookup_table()
    
    # Bridge Stations
    for s in range(STATIONS - 1):
        s0 = station_loops[s]
        s1 = station_loops[s + 1]
        
        # Sole bottom quads
        f_b0 = bm.faces.new((s0['b'][0], s1['b'][0], s1['b'][1], s0['b'][1]))
        f_b1 = bm.faces.new((s0['b'][1], s1['b'][1], s1['b'][2], s0['b'][2]))
        f_b0.material_index = 0
        f_b1.material_index = 0
        
        # Cupsole sidewall quads
        f_sl0 = bm.faces.new((s0['b'][0], s0['m'][0], s1['m'][0], s1['b'][0]))
        f_sl1 = bm.faces.new((s0['m'][0], s0['r'][0], s1['r'][0], s1['m'][0]))
        f_sm0 = bm.faces.new((s0['b'][2], s1['b'][2], s1['m'][1], s0['m'][1]))
        f_sm1 = bm.faces.new((s0['m'][1], s1['m'][1], s1['r'][1], s0['r'][1]))
        f_sl0.material_index = 0
        f_sl1.material_index = 0
        f_sm0.material_index = 0
        f_sm1.material_index = 0
        
        # Upper sidewalls
        f_ul0 = bm.faces.new((s0['r'][0],  s0['u1'][0], s1['u1'][0], s1['r'][0]))
        f_ul1 = bm.faces.new((s0['u1'][0], s0['u2'][0], s1['u2'][0], s1['u1'][0]))
        f_ul2 = bm.faces.new((s0['u2'][0], s0['u3'][0], s1['u3'][0], s1['u2'][0]))
        
        f_um0 = bm.faces.new((s0['r'][1],  s1['r'][1],  s1['u1'][1], s0['u1'][1]))
        f_um1 = bm.faces.new((s0['u1'][1], s1['u1'][1], s1['u2'][1], s0['u2'][1]))
        f_um2 = bm.faces.new((s0['u2'][1], s1['u2'][1], s1['u3'][1], s0['u3'][1]))
        
        # Suede quarter panels in midfoot (stations 7 to 21)
        if 7 <= s <= 21:
            f_ul0.material_index = 1 # Leather foxing trim
            f_um0.material_index = 1
            f_ul1.material_index = 2 # Chocolate suede panel
            f_um1.material_index = 2
            f_ul2.material_index = 2
            f_um2.material_index = 2
        else:
            f_ul0.material_index = 1 # Bone leather vamp/heel
            f_um0.material_index = 1
            f_ul1.material_index = 1
            f_um1.material_index = 1
            f_ul2.material_index = 1
            f_um2.material_index = 1
            
        # Vamp bridge across forefoot
        if s0['is_vamp'] and s1['is_vamp']:
            f_v = bm.faces.new((s0['u3'][0], s0['u3'][1], s1['u3'][1], s1['u3'][0]))
            f_v.material_index = 1
        elif s0['has_th'] and s1['is_vamp']:
            f_v = bm.faces.new((s0['u3'][0], s0['u3'][1], s1['u3'][1], s1['u3'][0]))
            f_v.material_index = 1
            
        # Interior collar cavity
        if s0['in'][0] and s1['in'][0]:
            f_il = bm.faces.new((s0['u3'][0], s1['u3'][0], s1['in'][0], s0['in'][0]))
            f_im = bm.faces.new((s0['u3'][1], s0['in'][1], s1['in'][1], s1['u3'][1]))
            f_il.material_index = 3
            f_im.material_index = 3
            
    # Heel cap
    sh = station_loops[0]
    f_hc = bm.faces.new((sh['b'][0], sh['m'][0], sh['r'][0], sh['u1'][0], sh['u2'][0], sh['u3'][0],
                         sh['u3'][1], sh['u2'][1], sh['u1'][1], sh['r'][1], sh['m'][1], sh['b'][2], sh['b'][1]))
    f_hc.material_index = 1
    
    # Toe apex bumper fan
    st = station_loops[-1]
    z_fl, _, _, _, _, _, _ = profile_params(y_stations[-1])
    v_toe_apex = bm.verts.new((0.0, y_stations[-1] + 0.008, z_fl + 0.012))
    
    f_t0 = bm.faces.new((st['b'][0], st['m'][0], v_toe_apex))
    f_t1 = bm.faces.new((st['m'][0], st['r'][0], v_toe_apex))
    f_t2 = bm.faces.new((st['r'][0], st['u1'][0], v_toe_apex))
    f_t3 = bm.faces.new((st['u1'][0], st['u2'][0], v_toe_apex))
    f_t4 = bm.faces.new((st['u2'][0], st['u3'][0], v_toe_apex))
    f_t5 = bm.faces.new((st['u3'][0], st['u3'][1], v_toe_apex))
    f_t6 = bm.faces.new((st['u3'][1], st['u2'][1], v_toe_apex))
    f_t7 = bm.faces.new((st['u2'][1], st['u1'][1], v_toe_apex))
    f_t8 = bm.faces.new((st['u1'][1], st['r'][1], v_toe_apex))
    f_t9 = bm.faces.new((st['r'][1], st['m'][1], v_toe_apex))
    f_t10 = bm.faces.new((st['m'][1], st['b'][2], v_toe_apex))
    f_t11 = bm.faces.new((st['b'][2], st['b'][1], v_toe_apex))
    f_t12 = bm.faces.new((st['b'][1], st['b'][0], v_toe_apex))
    for f in [f_t0, f_t1, f_t9, f_t10, f_t11, f_t12]: f.material_index = 0 # Gum rubber bumper
    for f in [f_t2, f_t3, f_t4, f_t5, f_t6, f_t7, f_t8]: f.material_index = 1 # Leather toe cap
    
    # 3D Padded Skate Tongue (Curved Under Eyestay)
    T_STEPS = 14
    t_rings = []
    for i in range(T_STEPS):
        frac = i / (T_STEPS - 1)
        ty = 0.058 - frac * 0.092
        tz = 0.046 + frac * 0.052 + 0.006 * math.sin(frac * math.pi)
        tw = 0.023 + 0.002 * math.sin(frac * math.pi)
        
        # 6-vertex puffy cross section (12mm thick)
        p0 = bm.verts.new(( -tw,       ty, tz + 0.004))
        p1 = bm.verts.new((  0.0,       ty, tz + 0.007))
        p2 = bm.verts.new((  tw,       ty, tz + 0.004))
        p3 = bm.verts.new((  tw * 0.8, ty - 0.004, tz - 0.005))
        p4 = bm.verts.new((  0.0,       ty - 0.004, tz - 0.008))
        p5 = bm.verts.new(( -tw * 0.8, ty - 0.004, tz - 0.005))
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
    
    # Woven HooDoo Tongue Patch
    lbl_y = -0.022
    lbl_z = 0.096
    l0 = bm.verts.new((-0.012, lbl_y - 0.009, lbl_z + 0.005))
    l1 = bm.verts.new((-0.012, lbl_y + 0.009, lbl_z + 0.005))
    l2 = bm.verts.new(( 0.012, lbl_y + 0.009, lbl_z + 0.005))
    l3 = bm.verts.new(( 0.012, lbl_y - 0.009, lbl_z + 0.005))
    f_lbl = bm.faces.new((l0, l1, l2, l3))
    f_lbl.material_index = 3 # Black woven fabric
    
    bm.to_mesh(mesh)
    bm.free()
    
    sub = obj.modifiers.new("Subsurf", type='SUBSURF')
    sub.levels = 1
    for p in mesh.polygons: p.use_smooth = True

    # 2. Details Object (5 Fat White Skate Laces + Symmetrical 3D Wave Insignia)
    det_mesh = bpy.data.meshes.new("Details_Mesh")
    det_obj = bpy.data.objects.new("Sneaker_Details", det_mesh)
    bpy.context.collection.objects.link(det_obj)
    det_obj.data.materials.append(mat_lace)   # 0: White fat laces
    det_obj.data.materials.append(mat_silver) # 1: Brushed silver wave
    
    bm_d = bmesh.new()
    
    # 5 Fat White Skate Laces
    lace_stations = [
        ( 0.048, 0.052, 0.017), # Forefoot lace 1
        ( 0.030, 0.063, 0.018), # Lace 2
        ( 0.012, 0.074, 0.019), # Lace 3
        (-0.006, 0.084, 0.020), # Lace 4
        (-0.022, 0.093, 0.021), # Top collar lace 5
    ]
    for ly, lz, span in lace_stations:
        lw = 0.0048 # 9.6mm wide skate lace
        th = 0.0028 # 2.8mm thick
        lz_e = lz + 0.0050
        
        # 4 vertices across strap
        v_l   = bm_d.verts.new((-span,        ly - lw, lz_e))
        v_cl  = bm_d.verts.new((-span * 0.45, ly - lw, lz_e + 0.0030))
        v_cr  = bm_d.verts.new(( span * 0.45, ly - lw, lz_e + 0.0030))
        v_r   = bm_d.verts.new(( span,        ly - lw, lz_e))
        
        v_l_f  = bm_d.verts.new((-span,        ly + lw, lz_e))
        v_cl_f = bm_d.verts.new((-span * 0.45, ly + lw, lz_e + 0.0030))
        v_cr_f = bm_d.verts.new(( span * 0.45, ly + lw, lz_e + 0.0030))
        v_r_f  = bm_d.verts.new(( span,        ly + lw, lz_e))
        
        v_l_t  = bm_d.verts.new((-span,        ly - lw, lz_e + th))
        v_cl_t = bm_d.verts.new((-span * 0.45, ly - lw, lz_e + th + 0.0030))
        v_cr_t = bm_d.verts.new(( span * 0.45, ly - lw, lz_e + th + 0.0030))
        v_r_t  = bm_d.verts.new(( span,        ly - lw, lz_e + th))
        
        v_l_ft  = bm_d.verts.new((-span,        ly + lw, lz_e + th))
        v_cl_ft = bm_d.verts.new((-span * 0.45, ly + lw, lz_e + th + 0.0030))
        v_cr_ft = bm_d.verts.new(( span * 0.45, ly + lw, lz_e + th + 0.0030))
        v_r_ft  = bm_d.verts.new(( span,        ly + lw, lz_e + th))
        
        f_t0 = bm_d.faces.new((v_l_t,  v_cl_t,  v_cl_ft, v_l_ft))
        f_t1 = bm_d.faces.new((v_cl_t, v_cr_t,  v_cr_ft, v_cl_ft))
        f_t2 = bm_d.faces.new((v_cr_t, v_r_t,   v_r_ft,  v_cr_ft))
        
        f_f0 = bm_d.faces.new((v_l_ft, v_cl_ft, v_cl_f,  v_l_f))
        f_f1 = bm_d.faces.new((v_cl_ft,v_cr_ft, v_cr_f,  v_cl_f))
        f_f2 = bm_d.faces.new((v_cr_ft,v_r_ft,  v_r_f,   v_cr_f))
        
        f_b0 = bm_d.faces.new((v_l,    v_cl,    v_cl_t,  v_l_t))
        f_b1 = bm_d.faces.new((v_cl,   v_cr,    v_cr_t,  v_cl_t))
        f_b2 = bm_d.faces.new((v_cr,   v_r,     v_r_t,   v_cr_t))
        
        for fl in [f_t0, f_t1, f_t2, f_f0, f_f1, f_f2, f_b0, f_b1, f_b2]:
            fl.material_index = 0
            
    # 3D Extruded Silver Wave Insignia on BOTH Sides (Lateral & Medial)
    wave_curve = [
        # (wy, wz, wh)
        (-0.065, 0.052, 0.007),
        (-0.040, 0.058, 0.011),
        (-0.015, 0.049, 0.010),
        ( 0.010, 0.056, 0.012),
        ( 0.035, 0.048, 0.008),
    ]
    
    for side in [1.0, -1.0]:
        w_bl_inner = []
        w_tl_inner = []
        w_bl_outer = []
        w_tl_outer = []
        
        for wy, wz, wh in wave_curve:
            _, _, _, xm, xl, _, _ = profile_params(wy)
            base_x = (xl if side > 0 else xm) * 0.97
            
            xi = base_x + side * 0.0012
            xo = base_x + side * 0.0038
            
            w_bl_inner.append(bm_d.verts.new((xi, wy, wz)))
            w_tl_inner.append(bm_d.verts.new((xi, wy, wz + wh)))
            w_bl_outer.append(bm_d.verts.new((xo, wy, wz)))
            w_tl_outer.append(bm_d.verts.new((xo, wy, wz + wh)))
            
        bm_d.verts.ensure_lookup_table()
        for k in range(len(wave_curve) - 1):
            if side > 0:
                f_front = bm_d.faces.new((w_bl_outer[k], w_bl_outer[k+1], w_tl_outer[k+1], w_tl_outer[k]))
                f_top   = bm_d.faces.new((w_tl_inner[k], w_tl_inner[k+1], w_tl_outer[k+1], w_tl_outer[k]))
                f_bot   = bm_d.faces.new((w_bl_outer[k], w_bl_outer[k+1], w_bl_inner[k+1], w_bl_inner[k]))
            else:
                f_front = bm_d.faces.new((w_bl_outer[k], w_tl_outer[k], w_tl_outer[k+1], w_bl_outer[k+1]))
                f_top   = bm_d.faces.new((w_tl_inner[k], w_tl_outer[k], w_tl_outer[k+1], w_tl_inner[k+1]))
                f_bot   = bm_d.faces.new((w_bl_outer[k], w_bl_inner[k], w_bl_inner[k+1], w_bl_outer[k+1]))
                
            f_front.material_index = 1
            f_top.material_index = 1
            f_bot.material_index = 1
            
    bm_d.to_mesh(det_mesh)
    bm_d.free()
    for p in det_mesh.polygons: p.use_smooth = True

    # 3. Brutalist Atelier Concrete Pedestal
    ped_mesh = bpy.data.meshes.new("Pedestal_Mesh")
    ped_obj = bpy.data.objects.new("Sneaker_Pedestal", ped_mesh)
    bpy.context.collection.objects.link(ped_obj)
    ped_obj.data.materials.append(mat_ped)
    
    bm_p = bmesh.new()
    P_SEGS = 32
    ped_r = 0.180
    c_top = bm_p.verts.new((0.0, 0.012, 0.000))
    c_bot = bm_p.verts.new((0.0, 0.012, -0.024))
    r_top = []
    r_bot = []
    for i in range(P_SEGS):
        ang = i * (2.0 * math.pi / P_SEGS)
        px = math.cos(ang) * ped_r
        py = math.sin(ang) * ped_r + 0.012
        r_top.append(bm_p.verts.new((px, py, 0.000)))
        r_bot.append(bm_p.verts.new((px * 1.03, py, -0.024)))
        
    bm_p.verts.ensure_lookup_table()
    for i in range(P_SEGS):
        inxt = (i + 1) % P_SEGS
        bm_p.faces.new((c_top, r_top[i], r_top[inxt]))
        bm_p.faces.new((r_top[i], r_bot[i], r_bot[inxt], r_top[inxt]))
        bm_p.faces.new((c_bot, r_bot[inxt], r_bot[i]))
        
    bm_p.to_mesh(ped_mesh)
    bm_p.free()
    for p in ped_mesh.polygons: p.use_smooth = True

    # Optional dynamic texture hook
    if texture_path and os.path.exists(texture_path):
        mat = bpy.data.materials.new("Sneaker_Texture_Mat")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        tex_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(os.path.abspath(texture_path))
        mat.node_tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
        obj.data.materials[1] = mat

    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False
    )
    print(f"Exported Hyperrealistic Skate Sneaker: {out_glb_path}")
