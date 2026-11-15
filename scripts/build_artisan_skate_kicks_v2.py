import bpy
import bmesh
import math
import os

def create_artisan_skate_kicks(out_glb_path, color_profile=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Color profile with defaults for P9 (Chicano Bone & Gum)
    cp = {
        'sole': (0.74, 0.48, 0.25, 1.0),       # Raw Gum Rubber
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

    # -------------------------------------------------------------
    # PBR Materials with Procedural Micro-Bump
    # -------------------------------------------------------------
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
    # AUTHENTIC SKATE SNEAKER LAST PERIMETER (36 Vertices)
    # =============================================================
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
    N_PERIM = len(perimeter_raw) # exactly 36 vertices

    def get_z_spec(x, y):
        # Toe spring: lifts upward 12mm at front toe
        if y > 0.020:
            frac = (y - 0.020) / 0.110
            z_bot = 0.012 * (frac ** 1.8)
        elif y < -0.090:
            frac = (-0.090 - y) / 0.030
            z_bot = 0.002 * frac
        else:
            z_bot = 0.000

        # Cupsole height: 18mm heel tapering to 14mm toe
        t_len = (y + 0.120) / 0.250
        t_len = max(0.0, min(1.0, t_len))
        sole_h = 0.018 - 0.004 * t_len
        z_rim = z_bot + sole_h

        # Upper top height
        if y < -0.050: # Heel collar
            z_top = z_rim + 0.048 - 0.012 * ((y + 0.120) / 0.070)
        elif y < 0.030: # Ankle & throat
            z_top = z_rim + 0.036 + 0.006 * math.sin(((y + 0.050) / 0.080) * math.pi)
        else: # Toe box & vamp dome
            z_top = z_rim + 0.026 - 0.008 * ((y - 0.030) / 0.100)

        return z_bot, sole_h, z_rim, z_top

    # =============================================================
    # 1. STANDALONE RUBBER CUPSOLE OBJECT (`Sneaker_Sole`)
    # Vertical sidewalls, crisp foxing line, top shelf, bottom floor
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
        # Recessed foxing stripe line
        s_mid_fx.append(bm_s.verts.new((x * 0.995, y * 0.998, z_bot + sole_h * 0.60)))
        s_mid_hi.append(bm_s.verts.new((x * 1.015, y * 1.010, z_bot + sole_h * 0.68)))
        # Top outer foxing rim
        s_rim_out.append(bm_s.verts.new((x * 1.002, y * 1.002, z_rim)))
        # Top welt shelf inner (inset 2.5mm)
        s_rim_in.append(bm_s.verts.new((x * 0.940, y * 0.940, z_rim)))
        # Recessed footbed floor
        s_bed.append(bm_s.verts.new((x * 0.935, y * 0.935, z_rim - 0.0035)))

    bm_s.verts.ensure_lookup_table()

    # Loft sidewalls
    for k in range(N_PERIM):
        knxt = (k + 1) % N_PERIM
        bm_s.faces.new((s_bottom[k], s_bottom[knxt], s_mid_low[knxt], s_mid_low[k]))
        bm_s.faces.new((s_mid_low[k], s_mid_low[knxt], s_mid_fx[knxt], s_mid_fx[k]))
        bm_s.faces.new((s_mid_fx[k], s_mid_fx[knxt], s_mid_hi[knxt], s_mid_hi[k]))
        bm_s.faces.new((s_mid_hi[k], s_mid_hi[knxt], s_rim_out[knxt], s_rim_out[k]))
        bm_s.faces.new((s_rim_out[k], s_rim_out[knxt], s_rim_in[knxt], s_rim_in[k]))
        bm_s.faces.new((s_rim_in[k], s_rim_in[knxt], s_bed[knxt], s_bed[k]))

    # Close bottom and footbed with center spine quads
    # Front triangle at toe
    bm_s.faces.new((s_bottom[0], s_bottom[1], s_bottom[N_PERIM - 1]))
    bm_s.faces.new((s_bed[0], s_bed[N_PERIM - 1], s_bed[1]))

    # Mid quads along spine
    for k in range(1, N_PERIM // 2 - 1):
        k_nxt = k + 1
        opp = N_PERIM - k
        opp_nxt = N_PERIM - k - 1
        bm_s.faces.new((s_bottom[k], s_bottom[k_nxt], s_bottom[opp_nxt], s_bottom[opp]))
        bm_s.faces.new((s_bed[k], s_bed[opp], s_bed[opp_nxt], s_bed[k_nxt]))

    # Rear triangle at heel
    bm_s.faces.new((s_bottom[17], s_bottom[18], s_bottom[19]))
    bm_s.faces.new((s_bed[17], s_bed[19], s_bed[18]))

    bm_s.to_mesh(sole_mesh)
    bm_s.free()
    for p in sole_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 2. STANDALONE UPPER (`Sneaker_Upper`)
    # Closed leather toe vamp dome + Open Ankle Collar with Velvet Lining
    # =============================================================
    upper_mesh = bpy.data.meshes.new("Upper_Mesh")
    upper_obj = bpy.data.objects.new("Sneaker_Upper", upper_mesh)
    bpy.context.collection.objects.link(upper_obj)
    upper_obj.data.materials.append(mats['upper'])  # 0: White Tumbled Leather
    upper_obj.data.materials.append(mats['inner'])  # 1: Dark Velvet Collar Lining

    bm_u = bmesh.new()

    u_shelf = []
    u_wall_mid = []
    u_wall_top = []
    u_collar_in = []

    for k in range(N_PERIM):
        x, y = perimeter_raw[k]
        z_bot, sole_h, z_rim, z_top = get_z_spec(x, y)

        # Base welt ring
        u_shelf.append(bm_u.verts.new((x * 0.940, y * 0.940, z_rim)))
        # Mid wall ring
        zm = z_rim + (z_top - z_rim) * 0.48
        u_wall_mid.append(bm_u.verts.new((x * 0.905, y * 0.915, zm)))
        # Upper collar / dome boundary ring
        u_wall_top.append(bm_u.verts.new((x * 0.835, y * 0.865, z_top)))
        # Inner collar roll (drops down into foot cavity)
        u_collar_in.append(bm_u.verts.new((x * 0.740, y * 0.780, z_top - 0.016)))

    bm_u.verts.ensure_lookup_table()

    # Loft side walls around entire perimeter
    for k in range(N_PERIM):
        knxt = (k + 1) % N_PERIM
        bm_u.faces.new((u_shelf[k], u_shelf[knxt], u_wall_mid[knxt], u_wall_mid[k])).material_index = 0
        bm_u.faces.new((u_wall_mid[k], u_wall_mid[knxt], u_wall_top[knxt], u_wall_top[k])).material_index = 0

    # (A) FRONT VAMP DOME CLOSURE:
    # Vamp spans indices k=30..35, 0..6 (the forefoot)
    vamp_k = [30, 31, 32, 33, 34, 35, 0, 1, 2, 3, 4, 5, 6]
    c_vamp = bm_u.verts.new((0.0, 0.085, 0.035))
    for idx in range(len(vamp_k) - 1):
        k0 = vamp_k[idx]
        k1 = vamp_k[idx + 1]
        bm_u.faces.new((u_wall_top[k0], u_wall_top[k1], c_vamp)).material_index = 0

    # (B) OPEN ANKLE COLLAR WITH VELVET INNER LINING:
    # Collar wraps around heel and ankle: k=6..30
    for k in range(6, 30):
        knxt = k + 1
        # Padded inner collar roll
        bm_u.faces.new((u_wall_top[k], u_wall_top[knxt], u_collar_in[knxt], u_collar_in[k])).material_index = 1

    # Inner footbed floor
    c_inner_floor = bm_u.verts.new((0.0, -0.040, 0.018))
    for k in range(6, 30):
        knxt = k + 1
        bm_u.faces.new((u_collar_in[k], c_inner_floor, u_collar_in[knxt])).material_index = 1

    # Perforations on toe vamp
    vamp_perfs = [
        ( 0.000, 0.106, 0.033),
        (-0.009, 0.100, 0.033), (0.009, 0.100, 0.033),
        (-0.016, 0.093, 0.034), (0.000, 0.093, 0.035), (0.016, 0.093, 0.034),
        (-0.010, 0.086, 0.036), (0.010, 0.086, 0.036),
        ( 0.000, 0.078, 0.037)
    ]
    for px, py, pz in vamp_perfs:
        pw = 0.0016
        p0 = bm_u.verts.new((px - pw, py - pw, pz - 0.0005))
        p1 = bm_u.verts.new((px + pw, py - pw, pz - 0.0005))
        p2 = bm_u.verts.new((px + pw, py + pw, pz - 0.0005))
        p3 = bm_u.verts.new((px - pw, py + pw, pz - 0.0005))
        bm_u.faces.new((p0, p1, p2, p3)).material_index = 1

    bm_u.to_mesh(upper_mesh)
    bm_u.free()
    sub_u = upper_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_u.levels = 1
    for p in upper_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 3. STANDALONE DESIGN LAYERS (`Sneaker_Design_Layers`)
    # Suede Mudguard U-cap, Eyestays, Quarter Panels, Heel Counter,
    # and 3D Polished Chrome Wave Emblem
    # =============================================================
    design_mesh = bpy.data.meshes.new("Design_Layers_Mesh")
    design_obj = bpy.data.objects.new("Sneaker_Design_Layers", design_mesh)
    bpy.context.collection.objects.link(design_obj)
    design_obj.data.materials.append(mats['suede'])  # 0: Suede panels
    design_obj.data.materials.append(mats['silver']) # 1: Chrome Silver Wave

    bm_d = bmesh.new()

    # Vertices offset proud by +1.8mm
    d_outer = []
    d_mid = []
    d_top = []

    for k in range(N_PERIM):
        x, y = perimeter_raw[k]
        z_bot, sole_h, z_rim, z_top = get_z_spec(x, y)
        off = 0.0018

        d_outer.append(bm_d.verts.new((x * 0.950, y * 0.950, z_rim + 0.0005)))
        zm = z_rim + (z_top - z_rim) * 0.50
        d_mid.append(bm_d.verts.new((x * 0.915, y * 0.925, zm + off)))
        d_top.append(bm_d.verts.new((x * 0.840, y * 0.870, z_top + off)))

    bm_d.verts.ensure_lookup_table()

    # (A) SUEDE MUDGUARD TOE CAP:
    # Runs around front toe bumper from k=29 (medial ball) through 0 to k=7 (lateral ball)
    mg_k = [29, 30, 31, 32, 33, 34, 35, 0, 1, 2, 3, 4, 5, 6, 7]
    for idx in range(len(mg_k) - 1):
        k0 = mg_k[idx]
        k1 = mg_k[idx + 1]
        bm_d.faces.new((d_outer[k0], d_outer[k1], d_mid[k1], d_mid[k0])).material_index = 0

    # Beveled return lip along top edge of mudguard
    for idx in range(len(mg_k) - 1):
        k0 = mg_k[idx]
        k1 = mg_k[idx + 1]
        x0, y0 = perimeter_raw[k0]
        x1, y1 = perimeter_raw[k1]
        _, _, z_r0, z_t0 = get_z_spec(x0, y0)
        _, _, z_r1, z_t1 = get_z_spec(x1, y1)
        # Inner return point
        zm0 = z_r0 + (z_t0 - z_r0) * 0.48
        zm1 = z_r1 + (z_t1 - z_r1) * 0.48
        v_in0 = bm_d.verts.new((x0 * 0.905, y0 * 0.915, zm0))
        v_in1 = bm_d.verts.new((x1 * 0.905, y1 * 0.915, zm1))
        bm_d.faces.new((d_mid[k0], d_mid[k1], v_in1, v_in0)).material_index = 0

    # (B) SUEDE QUARTER PANELS & EYESTAYS:
    # Lateral (k=7..14) and Medial (k=22..29)
    for k in range(7, 14):
        knxt = k + 1
        bm_d.faces.new((d_outer[k], d_outer[knxt], d_mid[knxt], d_mid[k])).material_index = 0
        bm_d.faces.new((d_mid[k], d_mid[knxt], d_top[knxt], d_top[k])).material_index = 0

    for k in range(22, 29):
        knxt = k + 1
        bm_d.faces.new((d_outer[k], d_outer[knxt], d_mid[knxt], d_mid[k])).material_index = 0
        bm_d.faces.new((d_mid[k], d_mid[knxt], d_top[knxt], d_top[k])).material_index = 0

    # (C) SUEDE HEEL COUNTER:
    # Heel cup (k=14..22)
    for k in range(14, 22):
        knxt = k + 1
        bm_d.faces.new((d_outer[k], d_outer[knxt], d_mid[knxt], d_mid[k])).material_index = 0
        bm_d.faces.new((d_mid[k], d_mid[knxt], d_top[knxt], d_top[k])).material_index = 0

    # (D) 3D POLISHED CHROME WAVE EMBLEM (West Coast Wave Badge):
    # Starts at midfoot (y = +0.035, z = 0.030), dips gently at (y = +0.010, z = 0.026),
    # and swoops gracefully up toward rear heel collar at (y = -0.065, z = 0.055)
    for side in [1.0, -1.0]:
        w_in_b, w_in_t, w_out_b, w_out_t = [], [], [], []
        W_SEGS = 14
        for s in range(W_SEGS):
            u = s / (W_SEGS - 1)
            # u=0: front (midfoot, y=+0.035), u=1: rear (heelward, y=-0.065)
            wy = 0.035 - u * 0.100

            # Dynamic upward swooping arc
            # u=0: 0.028, u=0.25: 0.026 (gentle dip), u=1.0: 0.056 (high collar tail)
            dip = 0.004 * math.sin(u * math.pi) if u < 0.5 else 0.0
            swoop = 0.028 * (u ** 1.6)
            wz = 0.028 - dip + swoop

            w_thick = 0.0055 + 0.0035 * math.sin(u * math.pi)

            # Lateral / medial offset conforming to upper curvature
            wx_base = (0.041 - 0.009 * u) if side > 0 else (-0.036 + 0.008 * u)
            
            x_in  = (wx_base + side * 0.0016)
            x_out = (wx_base + side * 0.0044)

            w_in_b.append(bm_d.verts.new((x_in, wy, wz)))
            w_in_t.append(bm_d.verts.new((x_in, wy, wz + w_thick)))
            w_out_b.append(bm_d.verts.new((x_out, wy, wz)))
            w_out_t.append(bm_d.verts.new((x_out, wy, wz + w_thick)))

        bm_d.verts.ensure_lookup_table()
        for s in range(W_SEGS - 1):
            if side > 0:
                bm_d.faces.new((w_out_b[s], w_out_b[s+1], w_out_t[s+1], w_out_t[s])).material_index = 1
                bm_d.faces.new((w_in_t[s], w_in_t[s+1], w_out_t[s+1], w_out_t[s])).material_index = 1
                bm_d.faces.new((w_out_b[s], w_out_b[s+1], w_in_b[s+1], w_in_b[s])).material_index = 1
            else:
                bm_d.faces.new((w_out_b[s], w_out_t[s], w_out_t[s+1], w_out_b[s+1])).material_index = 1
                bm_d.faces.new((w_in_t[s], w_out_t[s], w_out_t[s+1], w_in_t[s+1])).material_index = 1
                bm_d.faces.new((w_out_b[s], w_in_b[s], w_in_b[s+1], w_out_b[s+1])).material_index = 1

        # End caps
        if side > 0:
            bm_d.faces.new((w_in_b[0], w_in_t[0], w_out_t[0], w_out_b[0])).material_index = 1
            bm_d.faces.new((w_in_b[-1], w_out_b[-1], w_out_t[-1], w_in_t[-1])).material_index = 1
        else:
            bm_d.faces.new((w_in_b[0], w_out_b[0], w_out_t[0], w_in_t[0])).material_index = 1
            bm_d.faces.new((w_in_b[-1], w_in_t[-1], w_out_t[-1], w_out_b[-1])).material_index = 1

    bm_d.to_mesh(design_mesh)
    bm_d.free()
    sub_d = design_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_d.levels = 1
    for p in design_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 4. STANDALONE TONGUE (`Sneaker_Tongue`)
    # 12mm thick plush skate foam tongue nestled in throat
    # =============================================================
    tongue_mesh = bpy.data.meshes.new("Tongue_Mesh")
    tongue_obj = bpy.data.objects.new("Sneaker_Tongue", tongue_mesh)
    bpy.context.collection.objects.link(tongue_obj)
    tongue_obj.data.materials.append(mats['upper'])  # 0: Vamp material
    tongue_obj.data.materials.append(mats['inner'])  # 1: Dark label badge

    bm_t = bmesh.new()
    T_SEGS = 16
    t_loops = []

    for i in range(T_SEGS):
        u = i / (T_SEGS - 1)
        ty = 0.052 - u * 0.076
        tz = 0.035 + u * 0.026 + 0.002 * math.sin(u * math.pi)
        tw = 0.016 + 0.006 * u
        p_thick = 0.0050

        p0 = bm_t.verts.new((-tw,       ty, tz + p_thick * 0.6))
        p1 = bm_t.verts.new(( 0.0,       ty, tz + p_thick))
        p2 = bm_t.verts.new(( tw,       ty, tz + p_thick * 0.6))
        p3 = bm_t.verts.new(( tw * 0.8, ty - 0.003, tz - p_thick * 0.6))
        p4 = bm_t.verts.new(( 0.0,       ty - 0.003, tz - p_thick))
        p5 = bm_t.verts.new((-tw * 0.8, ty - 0.003, tz - p_thick * 0.6))
        t_loops.append((p0, p1, p2, p3, p4, p5))

    bm_t.verts.ensure_lookup_table()
    for s in range(T_SEGS - 1):
        r0 = t_loops[s]
        r1 = t_loops[s + 1]
        for k in range(6):
            knxt = (k + 1) % 6
            bm_t.faces.new((r0[k], r1[k], r1[knxt], r0[knxt])).material_index = 0

    bm_t.faces.new(reversed(t_loops[-1])).material_index = 0

    # Woven HooDoo brand label at upper tongue
    lbl_y = -0.014
    lbl_z = 0.060
    lw = 0.011
    lh = 0.008
    l0 = bm_t.verts.new((-lw, lbl_y - lh, lbl_z + 0.0055))
    l1 = bm_t.verts.new((-lw, lbl_y + lh, lbl_z + 0.0055))
    l2 = bm_t.verts.new(( lw, lbl_y + lh, lbl_z + 0.0055))
    l3 = bm_t.verts.new(( lw, lbl_y - lh, lbl_z + 0.0055))
    bm_t.faces.new((l0, l1, l2, l3)).material_index = 1

    bm_t.to_mesh(tongue_mesh)
    bm_t.free()
    sub_t = tongue_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_t.levels = 1
    for p in tongue_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 5. STANDALONE LACES & EYELETS (`Sneaker_Laces`)
    # Flat braided fat skate laces nestled snugly on the tongue
    # =============================================================
    lace_mesh = bpy.data.meshes.new("Laces_Mesh")
    lace_obj = bpy.data.objects.new("Sneaker_Laces", lace_mesh)
    bpy.context.collection.objects.link(lace_obj)
    lace_obj.data.materials.append(mats['lace'])
    lace_obj.data.materials.append(mats['eyelet'])

    bm_l = bmesh.new()

    lace_stations = [
        ( 0.044, 0.038, 0.017),
        ( 0.027, 0.044, 0.018),
        ( 0.010, 0.049, 0.019),
        (-0.006, 0.054, 0.020),
        (-0.020, 0.059, 0.021),
    ]

    for ly, lz, span in lace_stations:
        for side in [-1.0, 1.0]:
            cx = side * span
            cy = ly
            cz = lz + 0.002
            SEGS_E = 8
            er_out = 0.0026
            er_in  = 0.0016
            r_o, r_i = [], []
            for k in range(SEGS_E):
                ang = k * (2.0 * math.pi / SEGS_E)
                rx = math.cos(ang)
                ry = math.sin(ang)
                r_o.append(bm_l.verts.new((cx + rx * er_out, cy + ry * er_out, cz + 0.0005)))
                r_i.append(bm_l.verts.new((cx + rx * er_in,  cy + ry * er_in,  cz - 0.0004)))
            for k in range(SEGS_E):
                knxt = (k + 1) % SEGS_E
                bm_l.faces.new((r_o[k], r_o[knxt], r_i[knxt], r_i[k])).material_index = 1

    for ly, lz, span in lace_stations:
        lw = 0.0044
        th = 0.0022
        lz_e = lz + 0.003

        vl   = bm_l.verts.new((-span,        ly - lw, lz_e))
        vcl  = bm_l.verts.new((-span * 0.45, ly - lw, lz_e + 0.0020))
        vcr  = bm_l.verts.new(( span * 0.45, ly - lw, lz_e + 0.0020))
        vr   = bm_l.verts.new(( span,        ly - lw, lz_e))

        vl_f  = bm_l.verts.new((-span,        ly + lw, lz_e))
        vcl_f = bm_l.verts.new((-span * 0.45, ly + lw, lz_e + 0.0020))
        vcr_f = bm_l.verts.new(( span * 0.45, ly + lw, lz_e + 0.0020))
        vr_f  = bm_l.verts.new(( span,        ly + lw, lz_e))

        vl_t  = bm_l.verts.new((-span,        ly - lw, lz_e + th))
        vcl_t = bm_l.verts.new((-span * 0.45, ly - lw, lz_e + th + 0.0020))
        vcr_t = bm_l.verts.new(( span * 0.45, ly - lw, lz_e + th + 0.0020))
        vr_t  = bm_l.verts.new(( span,        ly - lw, lz_e + th))

        vl_ft  = bm_l.verts.new((-span,        ly + lw, lz_e + th))
        vcl_ft = bm_l.verts.new((-span * 0.45, ly + lw, lz_e + th + 0.0020))
        vcr_ft = bm_l.verts.new(( span * 0.45, ly + lw, lz_e + th + 0.0020))
        vr_ft  = bm_l.verts.new(( span,        ly + lw, lz_e + th))

        bm_l.faces.new((vl_t,  vcl_t,  vcl_ft, vl_ft)).material_index = 0
        bm_l.faces.new((vcl_t, vcr_t,  vcr_ft, vcl_ft)).material_index = 0
        bm_l.faces.new((vcr_t, vr_t,   vr_ft,  vcr_ft)).material_index = 0

        bm_l.faces.new((vl_ft, vcl_ft, vcl_f,  vl_f)).material_index = 0
        bm_l.faces.new((vcl_ft,vcr_ft, vcr_f,  vcl_f)).material_index = 0
        bm_l.faces.new((vcr_ft,vr_ft,  vr_f,   vcr_f)).material_index = 0

        bm_l.faces.new((vl,    vcl,    vcl_t,  vl_t)).material_index = 0
        bm_l.faces.new((vcl,   vcr,    vcr_t,  vcl_t)).material_index = 0
        bm_l.faces.new((vcr,   vr,     vr_t,   vcr_t)).material_index = 0

    bm_l.to_mesh(lace_mesh)
    bm_l.free()
    for p in lace_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 6. STANDALONE ARCHITECTURAL PEDESTAL (`Sneaker_Pedestal`)
    # Brutalist concrete plinth centered under sneaker
    # =============================================================
    ped_mesh = bpy.data.meshes.new("Pedestal_Mesh")
    ped_obj = bpy.data.objects.new("Sneaker_Pedestal", ped_mesh)
    bpy.context.collection.objects.link(ped_obj)
    ped_obj.data.materials.append(mats['pedestal'])

    bm_p = bmesh.new()
    P_SEGS = 40
    ped_r = 0.170
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
    print(f"[OK] Exported Artisan Skate Kicks: {out_glb_path}")

if __name__ == "__main__":
    out_dir = r"public/models"
    os.makedirs(out_dir, exist_ok=True)
    out_glb = os.path.join(out_dir, "test_artisan_sneaker.glb")
    create_artisan_skate_kicks(out_glb)
