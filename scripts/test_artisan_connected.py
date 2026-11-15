import bpy
import bmesh
import math
import os

def create_connected_sneaker(out_glb_path, color_profile=None):
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

    # Authentic 36-vertex Skate Sneaker Last Perimeter
    perimeter_raw = [
        # 0: Toe Apex
        ( 0.000,  0.130),
        # 1..4: Lateral Toe Arc
        ( 0.015,  0.128),
        ( 0.027,  0.124),
        ( 0.036,  0.117),
        ( 0.042,  0.108),
        # 5..9: Lateral Ball of Foot
        ( 0.045,  0.096),
        ( 0.047,  0.080),
        ( 0.048,  0.060),  # Widest lateral ball
        ( 0.045,  0.040),
        ( 0.040,  0.020),
        # 10..13: Lateral Waist & Quarter
        ( 0.036,  0.000),
        ( 0.034, -0.025),
        ( 0.032, -0.050),
        ( 0.031, -0.075),
        # 14..17: Lateral Heel Transition
        ( 0.030, -0.090),
        ( 0.027, -0.104),
        ( 0.020, -0.114),
        ( 0.010, -0.119),
        # 18: Rear Heel Apex
        ( 0.000, -0.120),
        # 19..22: Medial Heel Arc
        (-0.010, -0.119),
        (-0.020, -0.114),
        (-0.027, -0.104),
        (-0.030, -0.090),
        # 23..26: Medial Waist & Arch Hollow
        (-0.029, -0.070),
        (-0.027, -0.045),
        (-0.024, -0.020),  # Sculpted arch
        (-0.025,  0.005),
        # 27..30: Medial Ball of Foot
        (-0.032,  0.030),
        (-0.041,  0.055),
        (-0.044,  0.075),  # Widest medial ball
        (-0.042,  0.095),
        # 31..35: Medial Toe Arc
        (-0.037,  0.110),
        (-0.030,  0.120),
        (-0.021,  0.126),
        (-0.011,  0.129),
        (-0.005,  0.1298),
    ]
    N_PERIM = len(perimeter_raw)

    def get_z_spec(x, y):
        # Toe spring
        if y > 0.020:
            frac = (y - 0.020) / 0.110
            z_bot = 0.012 * (frac ** 1.8)
        elif y < -0.090:
            frac = (-0.090 - y) / 0.030
            z_bot = 0.002 * frac
        else:
            z_bot = 0.000

        # Cupsole height
        t_len = (y + 0.120) / 0.250
        t_len = max(0.0, min(1.0, t_len))
        sole_h = 0.018 - 0.004 * t_len
        z_rim = z_bot + sole_h

        # Upper top height
        if y < -0.050: # Heel collar
            z_top = z_rim + 0.046 - 0.010 * ((y + 0.120) / 0.070)
        elif y < 0.045: # Ankle & throat
            z_top = z_rim + 0.034 + 0.006 * math.sin(((y + 0.050) / 0.095) * math.pi)
        else: # Toe box & vamp dome
            z_top = z_rim + 0.024 - 0.008 * ((y - 0.045) / 0.085)

        return z_bot, sole_h, z_rim, z_top

    # =============================================================
    # 1. CUPSOLE (`Sneaker_Sole`)
    # =============================================================
    sole_mesh = bpy.data.meshes.new("Sole_Mesh")
    sole_obj = bpy.data.objects.new("Sneaker_Sole", sole_mesh)
    bpy.context.collection.objects.link(sole_obj)
    sole_obj.data.materials.append(mats['sole'])

    bm_s = bmesh.new()

    s_bottom = []
    s_mid_low = []
    s_mid_fx = []
    s_mid_hi = []
    s_rim_out = []
    s_rim_in = []
    s_bed = []

    for k in range(N_PERIM):
        x, y = perimeter_raw[k]
        z_bot, sole_h, z_rim, _ = get_z_spec(x, y)

        s_bottom.append(bm_s.verts.new((x * 1.025, y * 1.015, z_bot)))
        s_mid_low.append(bm_s.verts.new((x * 1.020, y * 1.012, z_bot + sole_h * 0.52)))
        s_mid_fx.append(bm_s.verts.new((x * 0.995, y * 0.998, z_bot + sole_h * 0.60)))
        s_mid_hi.append(bm_s.verts.new((x * 1.015, y * 1.010, z_bot + sole_h * 0.68)))
        s_rim_out.append(bm_s.verts.new((x * 1.002, y * 1.002, z_rim)))
        s_rim_in.append(bm_s.verts.new((x * 0.942, y * 0.942, z_rim)))
        s_bed.append(bm_s.verts.new((x * 0.932, y * 0.932, z_rim - 0.0050)))

    bm_s.verts.ensure_lookup_table()

    for k in range(N_PERIM):
        knxt = (k + 1) % N_PERIM
        bm_s.faces.new((s_bottom[k], s_bottom[knxt], s_mid_low[knxt], s_mid_low[k]))
        bm_s.faces.new((s_mid_low[k], s_mid_low[knxt], s_mid_fx[knxt], s_mid_fx[k]))
        bm_s.faces.new((s_mid_fx[k], s_mid_fx[knxt], s_mid_hi[knxt], s_mid_hi[k]))
        bm_s.faces.new((s_mid_hi[k], s_mid_hi[knxt], s_rim_out[knxt], s_rim_out[k]))
        bm_s.faces.new((s_rim_out[k], s_rim_out[knxt], s_rim_in[knxt], s_rim_in[k]))
        bm_s.faces.new((s_rim_in[k], s_rim_in[knxt], s_bed[knxt], s_bed[k]))

    bm_s.faces.new((s_bottom[0], s_bottom[1], s_bottom[N_PERIM - 1]))
    bm_s.faces.new((s_bed[0], s_bed[N_PERIM - 1], s_bed[1]))

    for k in range(1, N_PERIM // 2 - 1):
        k_nxt = k + 1
        opp = N_PERIM - k
        opp_nxt = N_PERIM - k - 1
        bm_s.faces.new((s_bottom[k], s_bottom[k_nxt], s_bottom[opp_nxt], s_bottom[opp]))
        bm_s.faces.new((s_bed[k], s_bed[opp], s_bed[opp_nxt], s_bed[k_nxt]))

    bm_s.faces.new((s_bottom[17], s_bottom[18], s_bottom[19]))
    bm_s.faces.new((s_bed[17], s_bed[19], s_bed[18]))

    bm_s.to_mesh(sole_mesh)
    bm_s.free()
    for p in sole_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 2. CONTINUOUS SCULPTED UPPER (`Sneaker_Upper`)
    # Eyestays fold inward toward instep (13-14mm from center)
    # =============================================================
    upper_mesh = bpy.data.meshes.new("Upper_Mesh")
    upper_obj = bpy.data.objects.new("Sneaker_Upper", upper_mesh)
    bpy.context.collection.objects.link(upper_obj)
    upper_obj.data.materials.append(mats['upper'])  # 0: Leather
    upper_obj.data.materials.append(mats['inner'])  # 1: Padded lining

    bm_u = bmesh.new()

    u_welt = []
    u_wall_mid = []
    u_wall_top = []
    u_collar_in = []

    for k in range(N_PERIM):
        x, y = perimeter_raw[k]
        z_bot, sole_h, z_rim, z_top = get_z_spec(x, y)

        # Welt starts 3.5mm down INSIDE cupsole channel
        u_welt.append(bm_u.verts.new((x * 0.935, y * 0.935, z_rim - 0.0035)))
        zm = z_rim + (z_top - z_rim) * 0.48
        u_wall_mid.append(bm_u.verts.new((x * 0.905, y * 0.915, zm)))

        # TOP WALL:
        # For the throat eyestay stations (k in [7..12] and [24..29]), fold inward to x = +/- 0.0135!
        if 7 <= k <= 12: # Lateral Eyestay
            xt = 0.0135
            yt = y
            u_wall_top.append(bm_u.verts.new((xt, yt, z_top)))
            u_collar_in.append(bm_u.verts.new((xt * 0.70, yt, z_top - 0.014)))
        elif 24 <= k <= 29: # Medial Eyestay
            xt = -0.0135
            yt = y
            u_wall_top.append(bm_u.verts.new((xt, yt, z_top)))
            u_collar_in.append(bm_u.verts.new((xt * 0.70, yt, z_top - 0.014)))
        else: # Vamp toe box and heel collar
            u_wall_top.append(bm_u.verts.new((x * 0.835, y * 0.865, z_top)))
            u_collar_in.append(bm_u.verts.new((x * 0.740, y * 0.780, z_top - 0.016)))

    bm_u.verts.ensure_lookup_table()

    # Outer wall quads around full perimeter
    for k in range(N_PERIM):
        knxt = (k + 1) % N_PERIM
        bm_u.faces.new((u_welt[k], u_welt[knxt], u_wall_mid[knxt], u_wall_mid[k])).material_index = 0
        bm_u.faces.new((u_wall_mid[k], u_wall_mid[knxt], u_wall_top[knxt], u_wall_top[k])).material_index = 0

    # Vamp dome with smooth multi-arc curvature
    c_vamp_f = bm_u.verts.new((0.0, 0.095, 0.036)) # Front dome crest
    c_vamp_m = bm_u.verts.new((0.0, 0.070, 0.038)) # Mid dome crest
    c_throat = bm_u.verts.new((0.0, 0.048, 0.036)) # Throat notch apex

    # Front toe fan (32..35, 0..3)
    front_toe_pairs = [
        (32, 33), (33, 34), (34, 35), (35, 0), (0, 1), (1, 2), (2, 3)
    ]
    for k0, k1 in front_toe_pairs:
        bm_u.faces.new((u_wall_top[k0], u_wall_top[k1], c_vamp_f)).material_index = 0

    # Medial vamp transitions (30, 31, 32)
    bm_u.faces.new((u_wall_top[31], u_wall_top[32], c_vamp_f)).material_index = 0
    bm_u.faces.new((u_wall_top[31], c_vamp_f, c_vamp_m)).material_index = 0
    bm_u.faces.new((u_wall_top[30], u_wall_top[31], c_vamp_m)).material_index = 0
    bm_u.faces.new((u_wall_top[29], u_wall_top[30], c_vamp_m)).material_index = 0

    # Lateral vamp transitions (3, 4, 5, 6, 7)
    bm_u.faces.new((u_wall_top[3], u_wall_top[4], c_vamp_f)).material_index = 0
    bm_u.faces.new((u_wall_top[4], c_vamp_m, c_vamp_f)).material_index = 0
    bm_u.faces.new((u_wall_top[4], u_wall_top[5], c_vamp_m)).material_index = 0
    bm_u.faces.new((u_wall_top[5], u_wall_top[6], c_vamp_m)).material_index = 0
    bm_u.faces.new((u_wall_top[6], u_wall_top[7], c_vamp_m)).material_index = 0

    # Vamp crest to throat notch
    bm_u.faces.new((c_vamp_m, c_throat, u_wall_top[7])).material_index = 0
    bm_u.faces.new((u_wall_top[29], c_throat, c_vamp_m)).material_index = 0

    # Drop throat bridge into footbed interior so no camera can see gaps
    c_floor_front = bm_u.verts.new((0.0, 0.042, 0.016))
    bm_u.faces.new((c_throat, u_wall_top[7], c_floor_front)).material_index = 1
    bm_u.faces.new((c_throat, c_floor_front, u_wall_top[29])).material_index = 1

    # Collar interior lining (k: 7..29)
    for k in range(7, 29):
        knxt = k + 1
        bm_u.faces.new((u_wall_top[k], u_wall_top[knxt], u_collar_in[knxt], u_collar_in[k])).material_index = 1

    # Inner footbed floor
    c_inner_floor = bm_u.verts.new((0.0, -0.040, 0.016))
    for k in range(7, 29):
        knxt = k + 1
        bm_u.faces.new((u_collar_in[k], c_inner_floor, u_collar_in[knxt])).material_index = 1
    bm_u.faces.new((u_collar_in[7], c_floor_front, c_inner_floor)).material_index = 1
    bm_u.faces.new((u_collar_in[29], c_inner_floor, c_floor_front)).material_index = 1

    # Laser-cut vamp perforations (authentic 9-dot skate array)
    vamp_perfs = [
        ( 0.000, 0.106, 0.035),
        (-0.009, 0.100, 0.035), (0.009, 0.100, 0.035),
        (-0.016, 0.093, 0.036), (0.000, 0.093, 0.037), (0.016, 0.093, 0.036),
        (-0.010, 0.086, 0.038), (0.010, 0.086, 0.038),
        ( 0.000, 0.078, 0.039)
    ]
    for px, py, pz in vamp_perfs:
        pw = 0.0016
        p0 = bm_u.verts.new((px - pw, py - pw, pz + 0.0002))
        p1 = bm_u.verts.new((px + pw, py - pw, pz + 0.0002))
        p2 = bm_u.verts.new((px + pw, py + pw, pz + 0.0002))
        p3 = bm_u.verts.new((px - pw, py + pw, pz + 0.0002))
        bm_u.faces.new((p0, p1, p2, p3)).material_index = 1

    bm_u.to_mesh(upper_mesh)
    bm_u.free()
    sub_u = upper_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_u.levels = 1
    for p in upper_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 3. MASTERPIECE CONNECTED TONGUE (`Sneaker_Tongue`)
    # Wide puffy tongue (34-40mm wide) tucked under 27mm eyestays
    # =============================================================
    tongue_mesh = bpy.data.meshes.new("Tongue_Mesh")
    tongue_obj = bpy.data.objects.new("Sneaker_Tongue", tongue_mesh)
    bpy.context.collection.objects.link(tongue_obj)
    tongue_obj.data.materials.append(mats['upper'])  # 0: Outer
    tongue_obj.data.materials.append(mats['inner'])  # 1: Backing & patch
    tongue_obj.data.materials.append(mats['silver']) # 2: Chrome badge

    bm_t = bmesh.new()
    T_SEGS = 18
    t_loops = []

    # Tongue starts deep inside throat at y=0.048, z=0.024 under vamp
    for i in range(T_SEGS):
        u = i / (T_SEGS - 1)
        ty = 0.048 - 0.076 * u
        tz = 0.026 + 0.040 * (u ** 0.85) + 0.002 * math.sin(u * math.pi)
        
        # Tongue width: 18mm at root up to 21mm at crest (width 36-42mm)
        # Eyestays are at +/- 13.5mm (width 27mm), so tongue extends 4.5-7.5mm UNDER the eyestays!
        tw = 0.018 + 0.004 * u
        p_thick = 0.0065 + 0.0015 * math.sin(u * math.pi)

        # 8-point cross section for rich padded pillow profile
        p0 = bm_t.verts.new((-tw,        ty, tz))
        p1 = bm_t.verts.new((-tw * 0.65, ty, tz + p_thick * 0.75))
        p2 = bm_t.verts.new(( 0.0,        ty, tz + p_thick))
        p3 = bm_t.verts.new(( tw * 0.65, ty, tz + p_thick * 0.75))
        p4 = bm_t.verts.new(( tw,        ty, tz))
        p5 = bm_t.verts.new(( tw * 0.70, ty - 0.002, tz - p_thick * 0.80))
        p6 = bm_t.verts.new(( 0.0,        ty - 0.002, tz - p_thick))
        p7 = bm_t.verts.new((-tw * 0.70, ty - 0.002, tz - p_thick * 0.80))
        t_loops.append((p0, p1, p2, p3, p4, p5, p6, p7))

    bm_t.verts.ensure_lookup_table()

    # Cap bottom root face (u=0)
    r_root = t_loops[0]
    bm_t.faces.new((r_root[0], r_root[1], r_root[2], r_root[3], r_root[4], r_root[5], r_root[6], r_root[7])).material_index = 1

    # Loft tongue tube
    for s in range(T_SEGS - 1):
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
    l0 = bm_t.verts.new((-lw, lbl_y - lh, lbl_z + 0.0065))
    l1 = bm_t.verts.new((-lw, lbl_y + lh, lbl_z + 0.0065))
    l2 = bm_t.verts.new(( lw, lbl_y + lh, lbl_z + 0.0065))
    l3 = bm_t.verts.new(( lw, lbl_y - lh, lbl_z + 0.0065))
    bm_t.faces.new((l0, l1, l2, l3)).material_index = 1

    # Miniature chrome emblem badge
    bw = 0.006
    bh = 0.003
    b0 = bm_t.verts.new((-bw, lbl_y - bh, lbl_z + 0.0075))
    b1 = bm_t.verts.new((-bw, lbl_y + bh, lbl_z + 0.0075))
    b2 = bm_t.verts.new(( bw, lbl_y + bh, lbl_z + 0.0075))
    b3 = bm_t.verts.new(( bw, lbl_y - bh, lbl_z + 0.0075))
    bm_t.faces.new((b0, b1, b2, b3)).material_index = 2

    bm_t.to_mesh(tongue_mesh)
    bm_t.free()
    sub_t = tongue_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_t.levels = 1
    for p in tongue_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 4. SUEDE OVERLAYS & CHROME WAVE (`Sneaker_Design_Layers`)
    # Sits directly on upper with zero gaps, locked into sole welt
    # =============================================================
    design_mesh = bpy.data.meshes.new("Design_Layers_Mesh")
    design_obj = bpy.data.objects.new("Sneaker_Design_Layers", design_mesh)
    bpy.context.collection.objects.link(design_obj)
    design_obj.data.materials.append(mats['suede'])  # 0: Suede
    design_obj.data.materials.append(mats['silver']) # 1: Chrome Silver

    bm_d = bmesh.new()

    d_welt = []
    d_outer = []
    d_mid = []
    d_top = []

    for k in range(N_PERIM):
        x, y = perimeter_raw[k]
        z_bot, sole_h, z_rim, z_top = get_z_spec(x, y)
        off = 0.0012

        d_welt.append(bm_d.verts.new((x * 0.938, y * 0.938, z_rim - 0.0025)))
        d_outer.append(bm_d.verts.new((x * 0.944, y * 0.944, z_rim + 0.0002)))
        zm = z_rim + (z_top - z_rim) * 0.50
        d_mid.append(bm_d.verts.new((x * 0.915, y * 0.925, zm + off)))

        # Suede top follows the upper top with a clean 0.8mm offset
        if 7 <= k <= 12:
            xt = 0.0135
            d_top.append(bm_d.verts.new((xt, y, z_top + off)))
        elif 24 <= k <= 29:
            xt = -0.0135
            d_top.append(bm_d.verts.new((xt, y, z_top + off)))
        else:
            d_top.append(bm_d.verts.new((x * 0.840, y * 0.870, z_top + off)))

    bm_d.verts.ensure_lookup_table()

    # Mudguard Toe Cap (Stations 29..35, 0..7)
    mg_k = [29, 30, 31, 32, 33, 34, 35, 0, 1, 2, 3, 4, 5, 6, 7]
    for idx in range(len(mg_k) - 1):
        k0 = mg_k[idx]
        k1 = mg_k[idx + 1]
        bm_d.faces.new((d_welt[k0], d_welt[k1], d_outer[k1], d_outer[k0])).material_index = 0
        bm_d.faces.new((d_outer[k0], d_outer[k1], d_mid[k1], d_mid[k0])).material_index = 0

    # Mudguard return lip resting tightly onto vamp
    for idx in range(len(mg_k) - 1):
        k0 = mg_k[idx]
        k1 = mg_k[idx + 1]
        x0, y0 = perimeter_raw[k0]
        x1, y1 = perimeter_raw[k1]
        _, _, z_r0, z_t0 = get_z_spec(x0, y0)
        _, _, z_r1, z_t1 = get_z_spec(x1, y1)
        zm0 = z_r0 + (z_t0 - z_r0) * 0.48
        zm1 = z_r1 + (z_t1 - z_r1) * 0.48
        v_in0 = bm_d.verts.new((x0 * 0.906, y0 * 0.916, zm0 + 0.0006))
        v_in1 = bm_d.verts.new((x1 * 0.906, y1 * 0.916, zm1 + 0.0006))
        bm_d.faces.new((d_mid[k0], d_mid[k1], v_in1, v_in0)).material_index = 0

    # Quarters & Eyestays (Lateral 7..14, Medial 22..29)
    for k in range(7, 14):
        knxt = k + 1
        bm_d.faces.new((d_welt[k], d_welt[knxt], d_outer[knxt], d_outer[k])).material_index = 0
        bm_d.faces.new((d_outer[k], d_outer[knxt], d_mid[knxt], d_mid[k])).material_index = 0
        bm_d.faces.new((d_mid[k], d_mid[knxt], d_top[knxt], d_top[k])).material_index = 0

    for k in range(22, 29):
        knxt = k + 1
        bm_d.faces.new((d_welt[k], d_welt[knxt], d_outer[knxt], d_outer[k])).material_index = 0
        bm_d.faces.new((d_outer[k], d_outer[knxt], d_mid[knxt], d_mid[k])).material_index = 0
        bm_d.faces.new((d_mid[k], d_mid[knxt], d_top[knxt], d_top[k])).material_index = 0

    # Heel Counter Wrap (14..22)
    for k in range(14, 22):
        knxt = k + 1
        bm_d.faces.new((d_welt[k], d_welt[knxt], d_outer[knxt], d_outer[k])).material_index = 0
        bm_d.faces.new((d_outer[k], d_outer[knxt], d_mid[knxt], d_mid[k])).material_index = 0
        bm_d.faces.new((d_mid[k], d_mid[knxt], d_top[knxt], d_top[k])).material_index = 0

    # 3D Chrome Wave / Swoop (Fitted tightly onto the quarter suede surface)
    for side in [1.0, -1.0]:
        w_in, w_out = [], []
        W_SEGS = 12
        for s in range(W_SEGS):
            u = s / (W_SEGS - 1)
            wy = 0.035 - u * 0.090
            
            # Find interpolated quarter station x at wy
            t_w = max(0.0, min(1.0, (wy - (-0.055)) / (0.035 - (-0.055))))
            # Quarter width profile
            qw = (0.032 + 0.012 * t_w) * 0.915
            
            dip = 0.003 * math.sin(u * math.pi) if u < 0.5 else 0.0
            swoop = 0.024 * (u ** 1.6)
            wz = 0.025 - dip + swoop
            w_th = 0.0045 + 0.0020 * math.sin(u * math.pi)

            x_base = side * (qw + 0.0012)
            x_tip  = side * (qw + 0.0032)

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
    # Resting directly across the tongue, connecting to eyestays
    # =============================================================
    lace_mesh = bpy.data.meshes.new("Laces_Mesh")
    lace_obj = bpy.data.objects.new("Sneaker_Laces", lace_mesh)
    bpy.context.collection.objects.link(lace_obj)
    lace_obj.data.materials.append(mats['lace'])
    lace_obj.data.materials.append(mats['eyelet'])

    bm_l = bmesh.new()

    lace_coords = [
        ( 0.044, 0.038, 0.0135),
        ( 0.028, 0.044, 0.0135),
        ( 0.012, 0.049, 0.0135),
        (-0.004, 0.054, 0.0135),
        (-0.018, 0.060, 0.0135),
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

    # Puffy Fat Skate Laces Bar Crossing
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
    out_glb = os.path.join(out_dir, "test_connected_sneaker.glb")
    create_connected_sneaker(out_glb)
