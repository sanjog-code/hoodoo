import bpy
import bmesh
import math
import os

def build_perfect_sneaker(out_glb_path, color_profile=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)

    cp = {
        'sole': (0.74, 0.48, 0.25, 1.0),       # Raw Gum Rubber Cupsole
        'sole_roughness': 0.48,
        'vamp': (0.92, 0.90, 0.86, 1.0),       # Bone Tumbled Leather
        'vamp_roughness': 0.35,
        'quarter': (0.08, 0.045, 0.025, 1.0),  # Deep Chocolate Espresso Suede
        'quarter_roughness': 0.92,
        'silver': (0.92, 0.94, 0.98, 1.0),     # Polished Chrome Silver
        'silver_metal': 0.98,
        'silver_roughness': 0.10,
        'lace': (0.98, 0.98, 0.98, 1.0),       # Crisp White Fat Laces
        'lace_roughness': 0.65,
        'inner': (0.06, 0.06, 0.07, 1.0),      # Dark Velvet Padded Collar
        'inner_roughness': 0.95,
        'eyelet': (0.88, 0.90, 0.94, 1.0),     # Nickel Eyelets
        'eyelet_metal': 0.95,
        'pedestal': (0.24, 0.25, 0.27, 1.0),   # Concrete Plinth
        'pedestal_roughness': 0.85,
    }
    if color_profile:
        cp.update(color_profile)

    def create_mat(name, col, rough=0.5, metal=0.0):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        out = nodes.new('ShaderNodeOutputMaterial')
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.inputs['Base Color'].default_value = col
        bsdf.inputs['Roughness'].default_value = rough
        bsdf.inputs['Metallic'].default_value = metal
        links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
        return mat, nodes, links, bsdf

    mat_sole, s_nodes, s_links, s_bsdf = create_mat("Mat_Sole", cp['sole'], cp['sole_roughness'])
    tex_s = s_nodes.new('ShaderNodeTexNoise')
    tex_s.inputs['Scale'].default_value = 350.0
    bmp_s = s_nodes.new('ShaderNodeBump')
    bmp_s.inputs['Strength'].default_value = 0.06
    bmp_s.inputs['Distance'].default_value = 0.001
    s_links.new(tex_s.outputs['Fac'], bmp_s.inputs['Height'])
    s_links.new(bmp_s.outputs['Normal'], s_bsdf.inputs['Normal'])

    mat_upper, u_nodes, u_links, u_bsdf = create_mat("Mat_Upper_Leather", cp['vamp'], cp['vamp_roughness'])
    tex_u = u_nodes.new('ShaderNodeTexVoronoi')
    tex_u.inputs['Scale'].default_value = 450.0
    bmp_u = u_nodes.new('ShaderNodeBump')
    bmp_u.inputs['Strength'].default_value = 0.035
    bmp_u.inputs['Distance'].default_value = 0.001
    u_links.new(tex_u.outputs['Distance'], bmp_u.inputs['Height'])
    u_links.new(bmp_u.outputs['Normal'], u_bsdf.inputs['Normal'])

    mat_suede, d_nodes, d_links, d_bsdf = create_mat("Mat_Suede_Overlay", cp['quarter'], cp['quarter_roughness'])
    tex_d = d_nodes.new('ShaderNodeTexNoise')
    tex_d.inputs['Scale'].default_value = 480.0
    bmp_d = d_nodes.new('ShaderNodeBump')
    bmp_d.inputs['Strength'].default_value = 0.10
    bmp_d.inputs['Distance'].default_value = 0.0015
    d_links.new(tex_d.outputs['Fac'], bmp_d.inputs['Height'])
    d_links.new(bmp_d.outputs['Normal'], d_bsdf.inputs['Normal'])

    mat_silver, _, _, _ = create_mat("Mat_Chrome_Wave", cp['silver'], cp['silver_roughness'], cp['silver_metal'])

    mat_lace, l_nodes, l_links, l_bsdf = create_mat("Mat_Laces", cp['lace'], cp['lace_roughness'])
    tex_l = l_nodes.new('ShaderNodeTexWave')
    tex_l.inputs['Scale'].default_value = 220.0
    bmp_l = l_nodes.new('ShaderNodeBump')
    bmp_l.inputs['Strength'].default_value = 0.12
    bmp_l.inputs['Distance'].default_value = 0.001
    l_links.new(tex_l.outputs['Fac'], bmp_l.inputs['Height'])
    l_links.new(bmp_l.outputs['Normal'], l_bsdf.inputs['Normal'])

    mat_inner, _, _, _ = create_mat("Mat_Inner_Collar", cp['inner'], cp['inner_roughness'])
    mat_eyelet, _, _, _ = create_mat("Mat_Eyelets", cp['eyelet'], 0.18, cp['eyelet_metal'])
    mat_ped, p_nodes, p_links, p_bsdf = create_mat("Mat_Pedestal", cp['pedestal'], cp['pedestal_roughness'])

    mats = {
        'sole': mat_sole, 'upper': mat_upper, 'suede': mat_suede,
        'silver': mat_silver, 'lace': mat_lace, 'inner': mat_inner,
        'eyelet': mat_eyelet, 'pedestal': mat_ped
    }

    # =============================================================
    # PARAMETRIC FOOT LAST FUNCTIONS
    # =============================================================
    # Foot length from heel y=-0.115 to toe y=+0.125 (total 240mm last)
    def foot_half_width(y):
        # Realistic skate shoe half-width at longitudinal station y
        if y > 0.040: # Forefoot / Toe box
            t = (0.125 - y) / (0.125 - 0.040)
            t = max(0.0, min(1.0, t))
            # Rounds off at the toe apex
            return 0.045 * (t ** 0.45)
        elif y > -0.030: # Waist & arch transition
            t = (y + 0.030) / (0.040 + 0.030)
            return 0.034 + 0.011 * t
        else: # Heel cup
            t = (y + 0.115) / (-0.030 + 0.115)
            t = max(0.0, min(1.0, t))
            return 0.030 * (t ** 0.5)

    def get_sole_z(y):
        # Natural toe spring upward curve
        if y > 0.030:
            frac = (y - 0.030) / 0.095
            z_bot = 0.011 * (frac ** 1.8)
        else:
            z_bot = 0.000
        # Cupsole height: 18mm heel tapering to 14mm toe
        t_len = (y + 0.115) / 0.240
        t_len = max(0.0, min(1.0, t_len))
        sole_h = 0.018 - 0.004 * t_len
        return z_bot, sole_h, z_bot + sole_h

    # =============================================================
    # 1. CUPSOLE (`Sneaker_Sole`)
    # =============================================================
    sole_mesh = bpy.data.meshes.new("Sole_Mesh")
    sole_obj = bpy.data.objects.new("Sneaker_Sole", sole_mesh)
    bpy.context.collection.objects.link(sole_obj)
    sole_obj.data.materials.append(mats['sole'])

    bm_s = bmesh.new()

    # Generate 32 longitudinal stations along the sole
    N_Y = 28
    y_stations = [-0.115 + (0.125 - (-0.115)) * (i / (N_Y - 1)) for i in range(N_Y)]
    
    # Sidewall profile rings
    # For each y station, define lateral (+X) and medial (-X) points
    # Profile: Bottom, Mid-Rib, Top-Rim-Outer, Top-Rim-Inner, Cup-Bed
    r_bot_l, r_bot_m = [], []
    r_mid_l, r_mid_m = [], []
    r_rim_out_l, r_rim_out_m = [], []
    r_rim_in_l, r_rim_in_m = [], []
    r_bed_l, r_bed_m = [], []

    for y in y_stations:
        hw = foot_half_width(y)
        z_b, sh, z_r = get_sole_z(y)

        # Subtle asymmetry: medial arch slightly narrower at waist
        w_lat = hw * 1.03
        w_med = hw * (0.95 if -0.05 < y < 0.02 else 1.01)

        r_bot_l.append(bm_s.verts.new(( w_lat * 1.03, y, z_b)))
        r_bot_m.append(bm_s.verts.new((-w_med * 1.03, y, z_b)))

        r_mid_l.append(bm_s.verts.new(( w_lat * 1.01, y, z_b + sh * 0.55)))
        r_mid_m.append(bm_s.verts.new((-w_med * 1.01, y, z_b + sh * 0.55)))

        r_rim_out_l.append(bm_s.verts.new(( w_lat * 1.00, y, z_r)))
        r_rim_out_m.append(bm_s.verts.new((-w_med * 1.00, y, z_r)))

        r_rim_in_l.append(bm_s.verts.new(( w_lat * 0.93, y, z_r)))
        r_rim_in_m.append(bm_s.verts.new((-w_med * 0.93, y, z_r)))

        r_bed_l.append(bm_s.verts.new(( w_lat * 0.91, y, z_r - 0.004)))
        r_bed_m.append(bm_s.verts.new((-w_med * 0.91, y, z_r - 0.004)))

    bm_s.verts.ensure_lookup_table()

    # Build sole sidewall quads and top rim quads
    for i in range(N_Y - 1):
        i1 = i + 1
        # Lateral sidewall
        bm_s.faces.new((r_bot_l[i], r_bot_l[i1], r_mid_l[i1], r_mid_l[i]))
        bm_s.faces.new((r_mid_l[i], r_mid_l[i1], r_rim_out_l[i1], r_rim_out_l[i]))
        bm_s.faces.new((r_rim_out_l[i], r_rim_out_l[i1], r_rim_in_l[i1], r_rim_in_l[i]))
        bm_s.faces.new((r_rim_in_l[i], r_rim_in_l[i1], r_bed_l[i1], r_bed_l[i]))

        # Medial sidewall
        bm_s.faces.new((r_bot_m[i1], r_bot_m[i], r_mid_m[i], r_mid_m[i1]))
        bm_s.faces.new((r_mid_m[i1], r_mid_m[i], r_rim_out_m[i], r_rim_out_m[i1]))
        bm_s.faces.new((r_rim_out_m[i1], r_rim_out_m[i], r_rim_in_m[i], r_rim_in_m[i1]))
        bm_s.faces.new((r_rim_in_m[i1], r_rim_in_m[i], r_bed_m[i], r_bed_m[i1]))

        # Outsole bottom surface
        bm_s.faces.new((r_bot_l[i1], r_bot_l[i], r_bot_m[i], r_bot_m[i1]))
        # Cupsole interior bed surface
        bm_s.faces.new((r_bed_l[i], r_bed_l[i1], r_bed_m[i1], r_bed_m[i]))

    # Cap toe end (i = N_Y - 1)
    bm_s.faces.new((r_bot_l[-1], r_bot_m[-1], r_mid_m[-1], r_mid_l[-1]))
    bm_s.faces.new((r_mid_l[-1], r_mid_m[-1], r_rim_out_m[-1], r_rim_out_l[-1]))
    bm_s.faces.new((r_rim_out_l[-1], r_rim_out_m[-1], r_rim_in_m[-1], r_rim_in_l[-1]))
    bm_s.faces.new((r_rim_in_l[-1], r_rim_in_m[-1], r_bed_m[-1], r_bed_l[-1]))

    # Cap heel end (i = 0)
    bm_s.faces.new((r_bot_m[0], r_bot_l[0], r_mid_l[0], r_mid_m[0]))
    bm_s.faces.new((r_mid_m[0], r_mid_l[0], r_rim_out_l[0], r_rim_out_m[0]))
    bm_s.faces.new((r_rim_out_m[0], r_rim_out_l[0], r_rim_in_l[0], r_rim_in_m[0]))
    bm_s.faces.new((r_rim_in_m[0], r_rim_in_l[0], r_bed_l[0], r_bed_m[0]))

    bm_s.to_mesh(sole_mesh)
    bm_s.free()
    for p in sole_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 2. CONTINUOUS SCULPTED UPPER (`Sneaker_Upper`)
    # Complete, continuous hull with throat chasm and ankle collar
    # =============================================================
    upper_mesh = bpy.data.meshes.new("Upper_Mesh")
    upper_obj = bpy.data.objects.new("Sneaker_Upper", upper_mesh)
    bpy.context.collection.objects.link(upper_obj)
    upper_obj.data.materials.append(mats['upper'])  # 0: Leather
    upper_obj.data.materials.append(mats['inner'])  # 1: Padded lining

    bm_u = bmesh.new()

    # Upper cross section loops at each longitudinal station y
    # Stations:
    # 0..11: Heel & Quarter (y from -0.115 to -0.010)
    # 12..17: Eyestay Throat Zone (y from -0.010 to 0.045)
    # 18..27: Vamp & Toe Box (y from 0.045 to 0.125)
    
    # Store vertices per station:
    # For throat zone & quarters:
    # [welt_l, mid_l, crest_l, in_l, floor_m, in_m, crest_m, mid_m, welt_m]
    # For vamp zone:
    # [welt_l, mid_l, top_l, dome_c, top_m, mid_m, welt_m]

    vamp_rings = []
    throat_rings = []

    for i, y in enumerate(y_stations):
        hw = foot_half_width(y)
        _, _, z_r = get_sole_z(y)
        
        # Welt starts 3.5mm down INSIDE cupsole bed
        z_welt = z_r - 0.0035
        wl = hw * 0.915
        wm = hw * (0.915 if y > 0.02 else 0.88)

        if y > 0.045: # VAMP DOME REGION
            # Smooth rounded toe dome
            t_v = (y - 0.045) / (0.125 - 0.045)
            z_crest = z_r + 0.028 - 0.010 * (t_v ** 1.5)
            z_mid = z_r + 0.014
            
            v_wl  = bm_u.verts.new(( wl,          y, z_welt))
            v_ml  = bm_u.verts.new(( wl * 0.92,   y, z_mid))
            v_tl  = bm_u.verts.new(( wl * 0.55,   y, z_crest * 0.96))
            v_dc  = bm_u.verts.new(( 0.0,         y, z_crest))
            v_tm  = bm_u.verts.new((-wm * 0.55,   y, z_crest * 0.96))
            v_mm  = bm_u.verts.new((-wm * 0.92,   y, z_mid))
            v_wm  = bm_u.verts.new((-wm,          y, z_welt))
            vamp_rings.append((v_wl, v_ml, v_tl, v_dc, v_tm, v_mm, v_wm))

        else: # THROAT & COLLAR REGION
            # Ankle collar height
            if y < -0.050: # Heel collar rolls up to Achilles notch
                t_h = (-0.050 - y) / (-0.050 - (-0.115))
                z_collar = z_r + 0.038 + 0.012 * (1.0 - (t_h - 0.5)**2 * 4 if t_h < 1.0 else 0)
                # Eyestays meet at rear heel seam
                hw_top = hw * 0.82
            else: # Throat region where laces sit
                t_t = (y + 0.050) / (0.045 + 0.050)
                z_collar = z_r + 0.032 + 0.006 * math.sin(t_t * math.pi)
                # Eyestays narrow inward to exactly 13mm from center!
                hw_top = 0.013 + 0.005 * (1.0 - t_t)

            z_mid = z_r + (z_collar - z_r) * 0.50

            v_wl = bm_u.verts.new(( wl,         y, z_welt))
            v_ml = bm_u.verts.new(( wl * 0.92,  y, z_mid))
            v_cl = bm_u.verts.new(( hw_top,     y, z_collar))
            # Inward roll of padded lining
            v_il = bm_u.verts.new(( hw_top * 0.70, y, z_collar - 0.014))
            v_fl = bm_u.verts.new(( 0.0,           y, z_r - 0.002))
            v_im = bm_u.verts.new((-hw_top * 0.70, y, z_collar - 0.014))
            v_cm = bm_u.verts.new((-hw_top,        y, z_collar))
            v_mm = bm_u.verts.new((-wm * 0.92,  y, z_mid))
            v_wm = bm_u.verts.new((-wm,         y, z_welt))
            throat_rings.append((v_wl, v_ml, v_cl, v_il, v_fl, v_im, v_cm, v_mm, v_wm))

    bm_u.verts.ensure_lookup_table()

    # Loft vamp rings
    for s in range(len(vamp_rings) - 1):
        r0 = vamp_rings[s]
        r1 = vamp_rings[s + 1]
        for k in range(6):
            bm_u.faces.new((r0[k], r1[k], r1[k + 1], r0[k + 1])).material_index = 0

    # Cap toe front tip
    rt = vamp_rings[-1]
    bm_u.faces.new((rt[0], rt[1], rt[5], rt[6])).material_index = 0
    bm_u.faces.new((rt[1], rt[2], rt[4], rt[5])).material_index = 0
    bm_u.faces.new((rt[2], rt[3], rt[4])).material_index = 0

    # Loft throat & collar rings
    for s in range(len(throat_rings) - 1):
        r0 = throat_rings[s]
        r1 = throat_rings[s + 1]
        # Outer lateral wall
        bm_u.faces.new((r0[0], r1[0], r1[1], r0[1])).material_index = 0
        bm_u.faces.new((r0[1], r1[1], r1[2], r0[2])).material_index = 0
        # Lateral collar padded roll
        bm_u.faces.new((r0[2], r1[2], r1[3], r0[3])).material_index = 1
        bm_u.faces.new((r0[3], r1[3], r1[4], r0[4])).material_index = 1

        # Medial collar padded roll
        bm_u.faces.new((r0[4], r1[4], r1[5], r0[5])).material_index = 1
        bm_u.faces.new((r0[5], r1[5], r1[6], r0[6])).material_index = 1
        # Outer medial wall
        bm_u.faces.new((r0[6], r1[6], r1[7], r0[7])).material_index = 0
        bm_u.faces.new((r0[7], r1[7], r1[8], r0[8])).material_index = 0

    # Cap heel rear seam (s = 0)
    rh = throat_rings[0]
    bm_u.faces.new((rh[0], rh[8], rh[7], rh[1])).material_index = 0
    bm_u.faces.new((rh[1], rh[7], rh[6], rh[2])).material_index = 0
    bm_u.faces.new((rh[2], rh[6], rh[5], rh[3])).material_index = 1
    bm_u.faces.new((rh[3], rh[5], rh[4])).material_index = 1

    # Bridge the throat boundary to the front vamp ring!
    rv = vamp_rings[0]
    rt_front = throat_rings[-1]
    # Lateral bridge
    bm_u.faces.new((rt_front[0], rv[0], rv[1], rt_front[1])).material_index = 0
    bm_u.faces.new((rt_front[1], rv[1], rv[2], rt_front[2])).material_index = 0
    # Center throat opening bridge (vamp notch meets throat floor)
    bm_u.faces.new((rt_front[2], rv[2], rv[3], rt_front[4])).material_index = 0
    bm_u.faces.new((rt_front[4], rv[3], rv[4], rt_front[6])).material_index = 0
    # Medial bridge
    bm_u.faces.new((rt_front[6], rv[4], rv[5], rt_front[7])).material_index = 0
    bm_u.faces.new((rt_front[7], rv[5], rv[6], rt_front[8])).material_index = 0

    bm_u.to_mesh(upper_mesh)
    bm_u.free()
    sub_u = upper_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_u.levels = 1
    for p in upper_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 3. MASTERPIECE TONGUE (`Sneaker_Tongue`)
    # Wide, puffy foam tongue nestled tightly under eyestays
    # =============================================================
    tongue_mesh = bpy.data.meshes.new("Tongue_Mesh")
    tongue_obj = bpy.data.objects.new("Sneaker_Tongue", tongue_mesh)
    bpy.context.collection.objects.link(tongue_obj)
    tongue_obj.data.materials.append(mats['upper'])  # 0: Outer leather/nylon
    tongue_obj.data.materials.append(mats['inner'])  # 1: Soft backing
    tongue_obj.data.materials.append(mats['silver']) # 2: Chrome badge

    bm_t = bmesh.new()
    T_STEPS = 16
    t_loops = []

    # Tongue runs along instep from y=+0.046 down to y=-0.028
    for i in range(T_STEPS):
        u = i / (T_STEPS - 1)
        ty = 0.046 - 0.074 * u
        # Height follows the foot instep up to the ankle crest
        tz = 0.032 + 0.038 * (u ** 0.85) + 0.003 * math.sin(u * math.pi)
        
        # Tongue half-width: 19mm at root, 23mm at crest (width 38-46mm)
        # Eyestay distance is only 26mm, so the tongue ALWAYS extends 6-10mm under the eyestays!
        tw = 0.019 + 0.005 * u
        p_th = 0.0060 + 0.0015 * math.sin(u * math.pi)

        # 8-point cross section
        p0 = bm_t.verts.new((-tw,        ty, tz))
        p1 = bm_t.verts.new((-tw * 0.65, ty, tz + p_th * 0.75))
        p2 = bm_t.verts.new(( 0.0,        ty, tz + p_th))
        p3 = bm_t.verts.new(( tw * 0.65, ty, tz + p_th * 0.75))
        p4 = bm_t.verts.new(( tw,        ty, tz))
        p5 = bm_t.verts.new(( tw * 0.70, ty - 0.002, tz - p_th * 0.80))
        p6 = bm_t.verts.new(( 0.0,        ty - 0.002, tz - p_th))
        p7 = bm_t.verts.new((-tw * 0.70, ty - 0.002, tz - p_th * 0.80))
        t_loops.append((p0, p1, p2, p3, p4, p5, p6, p7))

    bm_t.verts.ensure_lookup_table()

    # Cap root face (u=0)
    r_root = t_loops[0]
    bm_t.faces.new((r_root[0], r_root[1], r_root[2], r_root[3], r_root[4], r_root[5], r_root[6], r_root[7])).material_index = 1

    # Loft tongue tube
    for s in range(T_STEPS - 1):
        r0 = t_loops[s]
        r1 = t_loops[s + 1]
        for k in range(8):
            knxt = (k + 1) % 8
            mat_idx = 0 if k in [0, 1, 2, 3, 4] else 1
            bm_t.faces.new((r0[k], r1[k], r1[knxt], r0[knxt])).material_index = mat_idx

    # Cap top crest face (u=1.0)
    r_top = t_loops[-1]
    bm_t.faces.new(reversed(r_top)).material_index = 0

    # Woven Branded Patch on Tongue
    lbl_y = -0.012
    lbl_z = 0.065
    lw = 0.012
    lh = 0.009
    l0 = bm_t.verts.new((-lw, lbl_y - lh, lbl_z + 0.006))
    l1 = bm_t.verts.new((-lw, lbl_y + lh, lbl_z + 0.006))
    l2 = bm_t.verts.new(( lw, lbl_y + lh, lbl_z + 0.006))
    l3 = bm_t.verts.new(( lw, lbl_y - lh, lbl_z + 0.006))
    bm_t.faces.new((l0, l1, l2, l3)).material_index = 1

    # Miniature chrome emblem badge
    bw = 0.006
    bh = 0.003
    b0 = bm_t.verts.new((-bw, lbl_y - bh, lbl_z + 0.007))
    b1 = bm_t.verts.new((-bw, lbl_y + bh, lbl_z + 0.007))
    b2 = bm_t.verts.new(( bw, lbl_y + bh, lbl_z + 0.007))
    b3 = bm_t.verts.new(( bw, lbl_y - bh, lbl_z + 0.007))
    bm_t.faces.new((b0, b1, b2, b3)).material_index = 2

    bm_t.to_mesh(tongue_mesh)
    bm_t.free()
    sub_t = tongue_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_t.levels = 1
    for p in tongue_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 4. SUEDE OVERLAYS & CHROME WAVE (`Sneaker_Design_Layers`)
    # Mudguard toe wrap, quarter panels, heel counter, chrome swoosh
    # =============================================================
    design_mesh = bpy.data.meshes.new("Design_Layers_Mesh")
    design_obj = bpy.data.objects.new("Sneaker_Design_Layers", design_mesh)
    bpy.context.collection.objects.link(design_obj)
    design_obj.data.materials.append(mats['suede'])  # 0: Suede
    design_obj.data.materials.append(mats['silver']) # 1: Chrome Silver

    bm_d = bmesh.new()

    # Toe Mudguard Wrap (y from 0.075 to 0.125)
    # Wraps around the front of the shoe with a raised stitch lip
    mg_rings = []
    mg_y = [y for y in y_stations if y >= 0.075]
    for y in mg_y:
        hw = foot_half_width(y)
        _, _, z_r = get_sole_z(y)
        z_welt = z_r - 0.003
        wl = hw * 0.925
        wm = hw * 0.925
        z_mid = z_r + 0.015
        
        m_wl = bm_d.verts.new(( wl,         y, z_welt))
        m_ml = bm_d.verts.new(( wl * 0.93,  y, z_mid))
        m_tl = bm_d.verts.new(( wl * 0.60,  y, z_mid + 0.008))
        m_tc = bm_d.verts.new(( 0.0,        y, z_mid + 0.010))
        m_tm = bm_d.verts.new((-wm * 0.60,  y, z_mid + 0.008))
        m_mm = bm_d.verts.new((-wm * 0.93,  y, z_mid))
        m_wm = bm_d.verts.new((-wm,         y, z_welt))
        mg_rings.append((m_wl, m_ml, m_tl, m_tc, m_tm, m_mm, m_wm))

    bm_d.verts.ensure_lookup_table()
    for s in range(len(mg_rings) - 1):
        r0 = mg_rings[s]
        r1 = mg_rings[s + 1]
        for k in range(6):
            bm_d.faces.new((r0[k], r1[k], r1[k + 1], r0[k + 1])).material_index = 0

    # Cap toe front tip
    rmt = mg_rings[-1]
    bm_d.faces.new((rmt[0], rmt[1], rmt[5], rmt[6])).material_index = 0
    bm_d.faces.new((rmt[1], rmt[2], rmt[4], rmt[5])).material_index = 0
    bm_d.faces.new((rmt[2], rmt[3], rmt[4])).material_index = 0

    # Lateral & Medial Eyestay Quarter Panels (y from -0.010 to 0.065)
    # Suede strips along the eyelet throat
    for side in [1.0, -1.0]:
        es_y = [0.055, 0.040, 0.025, 0.010, -0.005, -0.020]
        p_out, p_in = [], []
        for y in es_y:
            hw = foot_half_width(y)
            _, _, z_r = get_sole_z(y)
            t_t = (y + 0.020) / (0.055 + 0.020)
            z_col = z_r + 0.033 + 0.005 * math.sin(t_t * math.pi)
            
            x_in  = side * 0.012
            x_out = side * (hw * 0.70)
            p_in.append(bm_d.verts.new((x_in,  y, z_col + 0.001)))
            p_out.append(bm_d.verts.new((x_out, y, z_col - 0.004)))

        bm_d.verts.ensure_lookup_table()
        for s in range(len(es_y) - 1):
            if side > 0:
                bm_d.faces.new((p_out[s], p_out[s + 1], p_in[s + 1], p_in[s])).material_index = 0
            else:
                bm_d.faces.new((p_out[s + 1], p_out[s], p_in[s], p_in[s + 1])).material_index = 0

    # Heel Counter Wrap (y from -0.115 to -0.060)
    hc_rings = []
    hc_y = [y for y in y_stations if y <= -0.060]
    for y in hc_y:
        hw = foot_half_width(y)
        _, _, z_r = get_sole_z(y)
        z_welt = z_r - 0.003
        wl = hw * 0.925
        wm = hw * 0.900
        z_top = z_r + 0.026
        
        h_wl = bm_d.verts.new(( wl,        y, z_welt))
        h_ml = bm_d.verts.new(( wl * 0.93, y, z_top * 0.55))
        h_tl = bm_d.verts.new(( wl * 0.75, y, z_top))
        h_tm = bm_d.verts.new((-wm * 0.75, y, z_top))
        h_mm = bm_d.verts.new((-wm * 0.93, y, z_top * 0.55))
        h_wm = bm_d.verts.new((-wm,        y, z_welt))
        hc_rings.append((h_wl, h_ml, h_tl, h_tm, h_mm, h_wm))

    bm_d.verts.ensure_lookup_table()
    for s in range(len(hc_rings) - 1):
        r0 = hc_rings[s]
        r1 = hc_rings[s + 1]
        for k in range(5):
            bm_d.faces.new((r0[k], r1[k], r1[k + 1], r0[k + 1])).material_index = 0

    # 3D Chrome Wave / Swoop (Tightly seated onto the quarter surface)
    for side in [1.0, -1.0]:
        w_in, w_out = [], []
        W_SEGS = 12
        for s in range(W_SEGS):
            u = s / (W_SEGS - 1)
            wy = 0.030 - u * 0.085
            hw = foot_half_width(wy)
            _, _, z_r = get_sole_z(wy)
            
            # Follows the authentic quarter surface closely!
            dip = 0.003 * math.sin(u * math.pi) if u < 0.5 else 0.0
            swoop = 0.024 * (u ** 1.6)
            wz = z_r + 0.012 - dip + swoop
            w_th = 0.0050 + 0.0025 * math.sin(u * math.pi)

            # Placed firmly on the quarter leather surface
            x_base = side * (hw * 0.88 + 0.001)
            x_tip  = side * (hw * 0.88 + 0.0035)

            w_in.append(bm_d.verts.new((x_base, wy, wz)))
            w_out.append(bm_d.verts.new((x_tip,  wy, wz + w_th)))

        bm_d.verts.ensure_lookup_table()
        for s in range(W_SEGS - 1):
            if side > 0:
                bm_d.faces.new((w_in[s], w_in[s + 1], w_out[s + 1], w_out[s])).material_index = 1
            else:
                bm_d.faces.new((w_in[s + 1], w_in[s], w_out[s], w_out[s + 1])).material_index = 1

    bm_d.to_mesh(design_mesh)
    bm_d.free()
    sub_d = design_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_d.levels = 1
    for p in design_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 5. AUTHENTIC SKATE LACES & BEVELED EYELETS (`Sneaker_Laces`)
    # Tightly bridged across eyestays and resting on tongue
    # =============================================================
    lace_mesh = bpy.data.meshes.new("Laces_Mesh")
    lace_obj = bpy.data.objects.new("Sneaker_Laces", lace_mesh)
    bpy.context.collection.objects.link(lace_obj)
    lace_obj.data.materials.append(mats['lace'])
    lace_obj.data.materials.append(mats['eyelet'])

    bm_l = bmesh.new()

    lace_coords = [
        ( 0.044, 0.038, 0.014),
        ( 0.028, 0.044, 0.014),
        ( 0.012, 0.049, 0.014),
        (-0.004, 0.054, 0.014),
        (-0.018, 0.060, 0.014),
    ]

    # Metallic Eyelets directly on the eyestay margins
    for ly, lz, span in lace_coords:
        for side in [-1.0, 1.0]:
            cx = side * span
            cy = ly
            cz = lz + 0.001
            SEGS_E = 10
            er_out = 0.0024
            er_in  = 0.0014
            r_o, r_i = [], []
            for k in range(SEGS_E):
                ang = k * (2.0 * math.pi / SEGS_E)
                rx = math.cos(ang)
                ry = math.sin(ang)
                r_o.append(bm_l.verts.new((cx + rx * er_out, cy + ry * er_out, cz + 0.0004)))
                r_i.append(bm_l.verts.new((cx + rx * er_in,  cy + ry * er_in,  cz - 0.0004)))
            for k in range(SEGS_E):
                knxt = (k + 1) % SEGS_E
                bm_l.faces.new((r_o[k], r_o[knxt], r_i[knxt], r_i[k])).material_index = 1

    # Puffy Fat Skate Laces Bar Crossing (13mm span, perfectly spanning eyelets)
    for ly, lz, span in lace_coords:
        lw = 0.0042
        th = 0.0022
        lz_e = lz + 0.0025

        vl    = bm_l.verts.new((-span,         ly - lw, lz_e))
        vcl1  = bm_l.verts.new((-span * 0.45,  ly - lw, lz_e + 0.0020))
        vcr1  = bm_l.verts.new(( span * 0.45,  ly - lw, lz_e + 0.0020))
        vr    = bm_l.verts.new(( span,         ly - lw, lz_e))

        vl_f  = bm_l.verts.new((-span,         ly + lw, lz_e))
        vcl_f = bm_l.verts.new((-span * 0.45,  ly + lw, lz_e + 0.0020))
        vcr_f = bm_l.verts.new(( span * 0.45,  ly + lw, lz_e + 0.0020))
        vr_f  = bm_l.verts.new(( span,         ly + lw, lz_e))

        vl_t  = bm_l.verts.new((-span,         ly - lw, lz_e + th))
        vcl_t = bm_l.verts.new((-span * 0.45,  ly - lw, lz_e + th + 0.0020))
        vcr_t = bm_l.verts.new(( span * 0.45,  ly - lw, lz_e + th + 0.0020))
        vr_t  = bm_l.verts.new(( span,         ly - lw, lz_e + th))

        vl_ft  = bm_l.verts.new((-span,        ly + lw, lz_e + th))
        vcl_ft = bm_l.verts.new((-span * 0.45, ly + lw, lz_e + th + 0.0020))
        vcr_ft = bm_l.verts.new(( span * 0.45, ly + lw, lz_e + th + 0.0020))
        vr_ft  = bm_l.verts.new(( span,        ly + lw, lz_e + th))

        bm_l.faces.new((vl_t,   vcl_t,  vcl_ft, vl_ft)).material_index = 0
        bm_l.faces.new((vcl_t,  vcr_t,  vcr_ft, vcl_ft)).material_index = 0
        bm_l.faces.new((vcr_t,  vr_t,   vr_ft,  vcr_ft)).material_index = 0

        bm_l.faces.new((vl_ft,  vcl_ft, vcl_f,  vl_f)).material_index = 0
        bm_l.faces.new((vcl_ft, vcr_ft, vcr_f,  vcl_f)).material_index = 0
        bm_l.faces.new((vcr_ft, vr_ft,  vr_f,   vcr_f)).material_index = 0

        bm_l.faces.new((vl,     vcl1,   vcl_t,  vl_t)).material_index = 0
        bm_l.faces.new((vcl1,   vcr1,   vcr_t,  vcl_t)).material_index = 0
        bm_l.faces.new((vcr1,   vr,     vr_t,   vcr_t)).material_index = 0

    # Tied Knot & Bow at Collar
    ky = -0.020
    kz = 0.063
    kw = 0.0050
    kn0 = bm_l.verts.new((-kw, ky - kw, kz))
    kn1 = bm_l.verts.new((-kw, ky + kw, kz))
    kn2 = bm_l.verts.new(( kw, ky + kw, kz))
    kn3 = bm_l.verts.new(( kw, ky - kw, kz))
    kn4 = bm_l.verts.new((-kw * 0.8, ky - kw * 0.8, kz + 0.004))
    kn5 = bm_l.verts.new((-kw * 0.8, ky + kw * 0.8, kz + 0.004))
    kn6 = bm_l.verts.new(( kw * 0.8, ky + kw * 0.8, kz + 0.004))
    kn7 = bm_l.verts.new(( kw * 0.8, ky - kw * 0.8, kz + 0.004))
    bm_l.faces.new((kn0, kn1, kn2, kn3)).material_index = 0
    bm_l.faces.new((kn4, kn5, kn6, kn7)).material_index = 0
    bm_l.faces.new((kn0, kn4, kn5, kn1)).material_index = 0
    bm_l.faces.new((kn1, kn5, kn6, kn2)).material_index = 0
    bm_l.faces.new((kn2, kn6, kn7, kn3)).material_index = 0
    bm_l.faces.new((kn3, kn7, kn4, kn0)).material_index = 0

    # Left & Right Bow Loops
    for side in [-1.0, 1.0]:
        lx = side * 0.014
        ly = ky - 0.005
        lz = kz + 0.005
        lp0 = bm_l.verts.new((side * 0.003, ky, kz + 0.002))
        lp1 = bm_l.verts.new((lx,           ly, lz))
        lp2 = bm_l.verts.new((lx * 1.2,     ly + 0.004, lz - 0.002))
        lp3 = bm_l.verts.new((side * 0.003, ky + 0.002, kz + 0.001))
        bm_l.faces.new((lp0, lp1, lp2, lp3)).material_index = 0

        # Hanging aglet
        ax = side * 0.015
        ay = ky + 0.010
        az = kz - 0.012
        ag0 = bm_l.verts.new((side * 0.003, ky, kz + 0.001))
        ag1 = bm_l.verts.new((ax,           ay, az))
        ag2 = bm_l.verts.new((ax + side * 0.0012, ay, az - 0.006))
        ag3 = bm_l.verts.new((side * 0.003, ky, kz))
        bm_l.faces.new((ag0, ag1, ag2, ag3)).material_index = 0

    bm_l.to_mesh(lace_mesh)
    bm_l.free()
    for p in lace_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 6. STANDALONE ARCHITECTURAL PEDESTAL (`Sneaker_Pedestal`)
    # =============================================================
    ped_mesh = bpy.data.meshes.new("Pedestal_Mesh")
    ped_obj = bpy.data.objects.new("Sneaker_Pedestal", ped_mesh)
    bpy.context.collection.objects.link(ped_obj)
    ped_obj.data.materials.append(mats['pedestal'])

    bm_p = bmesh.new()
    P_SEGS = 40
    ped_r = 0.165
    c_top = bm_p.verts.new((0.0, 0.005, 0.000))
    c_bot = bm_p.verts.new((0.0, 0.005, -0.018))
    r_top, r_bot = [], []
    for i in range(P_SEGS):
        ang = i * (2.0 * math.pi / P_SEGS)
        px = math.cos(ang) * ped_r
        py = math.sin(ang) * ped_r + 0.005
        r_top.append(bm_p.verts.new((px, py, 0.000)))
        r_bot.append(bm_p.verts.new((px * 1.025, py, -0.018)))

    bm_p.verts.ensure_lookup_table()
    for i in range(P_SEGS):
        inxt = (i + 1) % P_SEGS
        bm_p.faces.new((c_top, r_top[i], r_top[inxt]))
        bm_p.faces.new((r_top[i], r_bot[i], r_bot[inxt], r_top[inxt]))
        bm_p.faces.new((c_bot, r_bot[inxt], r_bot[i]))

    bm_p.to_mesh(ped_mesh)
    bm_p.free()
    for p in ped_mesh.polygons:
        p.use_smooth = True

    # -------------------------------------------------------------
    # ORIENTATION FOR GLTF / THREE.JS:
    # Rotate 180 degrees around Z so the toe permanently faces forward (+Z in glTF)
    # -------------------------------------------------------------
    all_parts = [sole_obj, upper_obj, design_obj, tongue_obj, lace_obj, ped_obj]
    for target in all_parts:
        target.rotation_euler[2] += math.pi
        bpy.context.view_layer.objects.active = target
        target.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False
    )
    print(f"[OK] Exported Masterpiece Skate Sneaker: {out_glb_path}")

if __name__ == "__main__":
    out_dir = r"public/models"
    os.makedirs(out_dir, exist_ok=True)
    out_glb = os.path.join(out_dir, "test_perfect_sneaker.glb")
    build_perfect_sneaker(out_glb)
