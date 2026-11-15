import bpy
import bmesh
import math
import os

def create_masterpiece_sneaker(out_glb_path, color_profile=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)

    cp = {
        'sole': (0.74, 0.48, 0.25, 1.0),       # Raw Gum Rubber
        'sole_roughness': 0.50,
        'vamp': (0.92, 0.90, 0.86, 1.0),       # Bone Tumbled Leather
        'vamp_roughness': 0.35,
        'quarter': (0.08, 0.045, 0.025, 1.0),  # Deep Chocolate Suede
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
        'pedestal': (0.24, 0.25, 0.27, 1.0),   # Brutalist Concrete
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
    tex_s.inputs['Scale'].default_value = 320.0
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
    # ANATOMICAL SNEAKER LAST GEOMETRY FUNCTIONS
    # authentic skate silhouette: broad rounded toe box,
    # sculpted waist arch, supportive heel cup, 12mm toe spring
    # =============================================================
    # Coordinate system:
    # Y: -0.125m (heel) to +0.138m (toe) - Length = 263mm (~US Men's 9 skate last)
    # X: Medial (-X) to Lateral (+X) - Width = 70mm (heel) to 92mm (ball of foot)
    # Z: Ground (Z=0) upwards - Sole height = 18mm heel / 14mm toe
    # =============================================================

    def get_last_contour(t):
        """
        Returns (xm, xl, z_bot, sole_h, z_rim, z_top) at parameter t in [0.0 (heel), 1.0 (toe)]
        """
        # 1. Sole Bottom Z (Toe Spring & Heel Roll)
        if t > 0.58:
            # Gradual 12mm upward rocker toward toe
            frac = (t - 0.58) / 0.42
            z_bot = 0.012 * (frac ** 2.0)
        elif t < 0.08:
            z_bot = 0.002 * (1.0 - t / 0.08)
        else:
            z_bot = 0.000

        # 2. Vulcanized Cupsole Height
        sole_h = 0.018 - 0.004 * t
        z_rim = z_bot + sole_h

        # 3. Width Contours: Skate Dunk / Vans Last
        # Authentic asymmetric human foot profile
        if t < 0.20:
            # Heel cup
            f = t / 0.20
            # Rounded heel curve
            rh = math.sqrt(max(0.04, 1.0 - ((1.0 - f) ** 2)))
            xm = -(0.035 * rh)
            xl =  (0.036 * rh)
        elif t < 0.55:
            # Waist / Arch
            f = (t - 0.20) / 0.35
            xm = -(0.035 - 0.007 * math.sin(f * math.pi))
            xl =  (0.036 + 0.002 * math.sin(f * math.pi))
        elif t < 0.82:
            # Ball of Foot (widest area: ~92mm wide)
            f = (t - 0.55) / 0.27
            xm = -(0.032 + 0.012 * math.sin(f * math.pi * 0.95))
            xl =  (0.038 + 0.010 * math.sin(f * math.pi * 0.95))
        else:
            # Broad Skate Toe Box:
            # DOES NOT collapse to 0! Gently rounds off to a generous 62mm front bumper arc!
            f = (t - 0.82) / 0.18
            w_factor = 1.0 - 0.30 * (f ** 1.5)
            xm = -(0.043 * w_factor)
            xl =  (0.046 * w_factor)

        # 4. Upper Top Height
        if t < 0.22:
            # Heel collar
            f = t / 0.22
            z_top = z_rim + 0.052 - 0.010 * f
        elif t < 0.46:
            # Throat / instep
            f = (t - 0.22) / 0.24
            z_top = z_rim + 0.042 - 0.008 * math.sin(f * math.pi * 0.5)
        elif t < 0.72:
            # Vamp transition
            f = (t - 0.46) / 0.26
            z_top = z_rim + 0.034 - 0.007 * f
        else:
            # Toe dome
            f = (t - 0.72) / 0.28
            z_top = z_rim + 0.027 - 0.008 * (f ** 1.3)

        return xm, xl, z_bot, sole_h, z_rim, z_top

    # Sample 30 longitudinal stations
    N_STATIONS = 30
    stations = []
    for i in range(N_STATIONS):
        u = i / (N_STATIONS - 1)
        # Cosine clustering at heel and toe
        t = 0.5 - 0.5 * math.cos(u * math.pi)
        y = -0.125 + 0.263 * t
        xm, xl, z_bot, sole_h, z_rim, z_top = get_last_contour(t)
        stations.append({
            'i': i, 't': t, 'y': y,
            'xm': xm, 'xl': xl,
            'z_bot': z_bot, 'sole_h': sole_h,
            'z_rim': z_rim, 'z_top': z_top
        })

    # =============================================================
    # 1. STANDALONE RUBBER CUPSOLE OBJECT (`Sneaker_Sole`)
    # Realistic vulcanized sidewall, foxing line, top shelf, bottom tread
    # =============================================================
    sole_mesh = bpy.data.meshes.new("Sole_Mesh")
    sole_obj = bpy.data.objects.new("Sneaker_Sole", sole_mesh)
    bpy.context.collection.objects.link(sole_obj)
    sole_obj.data.materials.append(mats['sole'])

    bm_s = bmesh.new()
    s_rings = []

    for st in stations:
        y = st['y']
        z_bot = st['z_bot']
        z_rim = st['z_rim']
        xl_s = st['xl'] * 1.03
        xm_s = st['xm'] * 1.03

        # Bottom floor vertices
        vb_l = bm_s.verts.new((xl_s, y, z_bot))
        vb_c = bm_s.verts.new((0.0,  y, z_bot))
        vb_m = bm_s.verts.new((xm_s, y, z_bot))

        # Mid sidewall (recessed foxing line stripe at 62% height)
        zm_low = z_bot + (z_rim - z_bot) * 0.56
        zm_mid = z_bot + (z_rim - z_bot) * 0.62
        zm_hi  = z_bot + (z_rim - z_bot) * 0.68

        v_low_l = bm_s.verts.new((xl_s * 1.015, y, zm_low))
        v_low_m = bm_s.verts.new((xm_s * 1.015, y, zm_low))

        # Recessed foxing line (-1.2mm depth)
        v_fx_l = bm_s.verts.new((xl_s * 0.995, y, zm_mid))
        v_fx_m = bm_s.verts.new((xm_s * 0.995, y, zm_mid))

        v_hi_l = bm_s.verts.new((xl_s * 1.012, y, zm_hi))
        v_hi_m = bm_s.verts.new((xm_s * 1.012, y, zm_hi))

        # Top foxing rim outer
        vro_l = bm_s.verts.new((xl_s * 1.005, y, z_rim))
        vro_m = bm_s.verts.new((xm_s * 1.005, y, z_rim))

        # Top foxing shelf inner (welt inset)
        vri_l = bm_s.verts.new((xl_s * 0.945, y, z_rim))
        vri_m = bm_s.verts.new((xm_s * 0.945, y, z_rim))

        # Recessed footbed floor
        vf_l = bm_s.verts.new((xl_s * 0.940, y, z_rim - 0.0035))
        vf_c = bm_s.verts.new((0.0,          y, z_rim - 0.0035))
        vf_m = bm_s.verts.new((xm_s * 0.940, y, z_rim - 0.0035))

        s_rings.append({
            'vb': (vb_l, vb_c, vb_m),
            'v_low': (v_low_l, v_low_m),
            'v_fx': (v_fx_l, v_fx_m),
            'v_hi': (v_hi_l, v_hi_m),
            'vro': (vro_l, vro_m),
            'vri': (vri_l, vri_m),
            'vf': (vf_l, vf_c, vf_m),
        })

    bm_s.verts.ensure_lookup_table()

    # Loft sole sidewalls and floor
    for i in range(N_STATIONS - 1):
        s0 = s_rings[i]
        s1 = s_rings[i + 1]

        # Bottom floor
        bm_s.faces.new((s0['vb'][0], s1['vb'][0], s1['vb'][1], s0['vb'][1]))
        bm_s.faces.new((s0['vb'][1], s1['vb'][1], s1['vb'][2], s0['vb'][2]))

        # Lateral sidewall
        bm_s.faces.new((s0['vb'][0], s0['v_low'][0], s1['v_low'][0], s1['vb'][0]))
        bm_s.faces.new((s0['v_low'][0], s0['v_fx'][0], s1['v_fx'][0], s1['v_low'][0]))
        bm_s.faces.new((s0['v_fx'][0], s0['v_hi'][0], s1['v_hi'][0], s1['v_fx'][0]))
        bm_s.faces.new((s0['v_hi'][0], s0['vro'][0], s1['vro'][0], s1['v_hi'][0]))

        # Medial sidewall
        bm_s.faces.new((s0['vb'][2], s1['vb'][2], s1['v_low'][1], s0['v_low'][1]))
        bm_s.faces.new((s0['v_low'][1], s1['v_low'][1], s1['v_fx'][1], s0['v_fx'][1]))
        bm_s.faces.new((s0['v_fx'][1], s1['v_fx'][1], s1['v_hi'][1], s0['v_hi'][1]))
        bm_s.faces.new((s0['v_hi'][1], s1['v_hi'][1], s1['vro'][1], s0['vro'][1]))

        # Top shelf (welt)
        bm_s.faces.new((s0['vro'][0], s0['vri'][0], s1['vri'][0], s1['vro'][0]))
        bm_s.faces.new((s0['vro'][1], s1['vro'][1], s1['vri'][1], s0['vri'][1]))

        # Drop into footbed
        bm_s.faces.new((s0['vri'][0], s0['vf'][0], s1['vf'][0], s1['vri'][0]))
        bm_s.faces.new((s0['vri'][1], s1['vri'][1], s1['vf'][2], s0['vf'][2]))

        # Footbed floor
        bm_s.faces.new((s0['vf'][0], s1['vf'][0], s1['vf'][1], s0['vf'][1]))
        bm_s.faces.new((s0['vf'][1], s1['vf'][1], s1['vf'][2], s0['vf'][2]))

    # Heel closure (rounded multi-quad cap)
    sh = s_rings[0]
    y_h = stations[0]['y']
    c_h_b = bm_s.verts.new((0.0, y_h - 0.007, 0.001))
    c_h_m = bm_s.verts.new((0.0, y_h - 0.008, 0.010))
    c_h_ro = bm_s.verts.new((0.0, y_h - 0.007, 0.017))
    c_h_ri = bm_s.verts.new((0.0, y_h - 0.005, 0.017))
    c_h_f  = bm_s.verts.new((0.0, y_h - 0.004, 0.0135))

    bm_s.faces.new((sh['vb'][0], sh['vb'][1], c_h_b))
    bm_s.faces.new((sh['vb'][1], sh['vb'][2], c_h_b))
    bm_s.faces.new((sh['vb'][0], c_h_b, c_h_m, sh['v_low'][0]))
    bm_s.faces.new((sh['vb'][2], sh['v_low'][1], c_h_m, c_h_b))
    bm_s.faces.new((sh['v_low'][0], c_h_m, c_h_ro, sh['vro'][0]))
    bm_s.faces.new((sh['v_low'][1], sh['vro'][1], c_h_ro, c_h_m))
    bm_s.faces.new((sh['vro'][0], c_h_ro, c_h_ri, sh['vri'][0]))
    bm_s.faces.new((sh['vro'][1], sh['vri'][1], c_h_ri, c_h_ro))
    bm_s.faces.new((sh['vri'][0], c_h_ri, c_h_f, sh['vf'][0]))
    bm_s.faces.new((sh['vri'][1], sh['vf'][2], c_h_f, c_h_ri))
    bm_s.faces.new((sh['vf'][0], c_h_f, sh['vf'][1]))
    bm_s.faces.new((sh['vf'][2], sh['vf'][1], c_h_f))

    # Toe bumper closure (swept rounded arc)
    st = s_rings[-1]
    y_t = stations[-1]['y']
    c_t_b = bm_s.verts.new((0.0, y_t + 0.010, 0.014))
    c_t_m = bm_s.verts.new((0.0, y_t + 0.011, 0.019))
    c_t_ro = bm_s.verts.new((0.0, y_t + 0.010, 0.024))
    c_t_ri = bm_s.verts.new((0.0, y_t + 0.007, 0.024))
    c_t_f  = bm_s.verts.new((0.0, y_t + 0.005, 0.0205))

    bm_s.faces.new((st['vb'][0], st['vb'][1], c_t_b))
    bm_s.faces.new((st['vb'][1], st['vb'][2], c_t_b))
    bm_s.faces.new((st['vb'][0], c_t_b, c_t_m, st['v_low'][0]))
    bm_s.faces.new((st['vb'][2], st['v_low'][1], c_t_m, c_t_b))
    bm_s.faces.new((st['v_low'][0], c_t_m, c_t_ro, st['vro'][0]))
    bm_s.faces.new((st['v_low'][1], st['vro'][1], c_t_ro, c_t_m))
    bm_s.faces.new((st['vro'][0], c_t_ro, c_t_ri, st['vri'][0]))
    bm_s.faces.new((st['vro'][1], st['vri'][1], c_t_ri, c_t_ro))
    bm_s.faces.new((st['vri'][0], c_t_ri, c_t_f, st['vf'][0]))
    bm_s.faces.new((st['vri'][1], st['vf'][2], c_t_f, c_t_ri))
    bm_s.faces.new((st['vf'][0], c_t_f, st['vf'][1]))
    bm_s.faces.new((st['vf'][2], st['vf'][1], c_t_f))

    bm_s.to_mesh(sole_mesh)
    bm_s.free()
    for p in sole_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 2. STANDALONE UPPER (`Sneaker_Upper`)
    # Watertight leather foot last with broad rounded skate toe dome
    # and perforated vamp area
    # =============================================================
    upper_mesh = bpy.data.meshes.new("Upper_Mesh")
    upper_obj = bpy.data.objects.new("Sneaker_Upper", upper_mesh)
    bpy.context.collection.objects.link(upper_obj)
    upper_obj.data.materials.append(mats['upper'])
    upper_obj.data.materials.append(mats['inner'])

    bm_u = bmesh.new()
    up_rings = []
    SEGS = 18

    for st in stations:
        y = st['y']
        z_rim = st['z_rim']
        z_top = st['z_top']
        z_bot = st['z_bot']
        xl = st['xl']
        xm = st['xm']

        cur_r = []
        for k in range(SEGS):
            theta = k * (2.0 * math.pi / SEGS)
            sin_th = math.sin(theta)
            cos_th = math.cos(theta)

            vx = xl * sin_th if sin_th >= 0 else (-xm * sin_th)
            if cos_th >= 0:
                h_f = cos_th ** 1.35
                vz = z_rim + (z_top - z_rim) * h_f
            else:
                b_f = (-cos_th) ** 1.45
                vz = z_rim - (z_rim - z_bot) * b_f
            cur_r.append(bm_u.verts.new((vx, y, vz)))
        up_rings.append(cur_r)

    bm_u.verts.ensure_lookup_table()

    for i in range(N_STATIONS - 1):
        r0 = up_rings[i]
        r1 = up_rings[i + 1]
        for k in range(SEGS):
            knxt = (k + 1) % SEGS
            bm_u.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0

    # Spherical heel cap
    c_heel_u = bm_u.verts.new((0.0, stations[0]['y'] - 0.006, 0.035))
    r_hu = up_rings[0]
    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm_u.faces.new((c_heel_u, r_hu[knxt], r_hu[k])).material_index = 0

    # Broad rounded skate toe dome cap
    r_tu = up_rings[-1]
    y_front = stations[-1]['y']
    z_rim_f = stations[-1]['z_rim']
    z_top_f = stations[-1]['z_top']
    xl_f = stations[-1]['xl']
    xm_f = stations[-1]['xm']

    # Step 1: Intermediate rounded ring (+6mm forward, 80% radial width)
    ring_front_mid = []
    for k in range(SEGS):
        theta = k * (2.0 * math.pi / SEGS)
        sin_th = math.sin(theta)
        cos_th = math.cos(theta)
        vx = (xl_f * sin_th if sin_th >= 0 else (-xm_f * sin_th)) * 0.80
        if cos_th >= 0:
            vz = z_rim_f + (z_top_f - z_rim_f) * (cos_th ** 1.35) * 0.88
        else:
            vz = z_rim_f - 0.003
        ring_front_mid.append(bm_u.verts.new((vx, y_front + 0.006, vz)))

    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm_u.faces.new((r_tu[k], r_tu[knxt], ring_front_mid[knxt], ring_front_mid[k])).material_index = 0

    # Step 2: Front dome apex ring (+11mm forward, 45% radial width)
    ring_front_tip = []
    for k in range(SEGS):
        theta = k * (2.0 * math.pi / SEGS)
        sin_th = math.sin(theta)
        cos_th = math.cos(theta)
        vx = (xl_f * sin_th if sin_th >= 0 else (-xm_f * sin_th)) * 0.45
        if cos_th >= 0:
            vz = z_rim_f + (z_top_f - z_rim_f) * (cos_th ** 1.35) * 0.65
        else:
            vz = z_rim_f - 0.002
        ring_front_tip.append(bm_u.verts.new((vx, y_front + 0.010, vz)))

    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm_u.faces.new((ring_front_mid[k], ring_front_mid[knxt], ring_front_tip[knxt], ring_front_tip[k])).material_index = 0

    # Step 3: Dome center cap
    c_toe_center = bm_u.verts.new((0.0, y_front + 0.0125, z_rim_f + (z_top_f - z_rim_f) * 0.35))
    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm_u.faces.new((ring_front_tip[k], ring_front_tip[knxt], c_toe_center)).material_index = 0

    # Perforations in front vamp
    vamp_perfs = [
        (0.000, 0.106, 0.033),
        (-0.009, 0.102, 0.033), (0.009, 0.102, 0.033),
        (-0.016, 0.096, 0.034), (0.000, 0.096, 0.035), (0.016, 0.096, 0.034),
        (-0.010, 0.090, 0.036), (0.010, 0.090, 0.036),
        (0.000, 0.084, 0.037)
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
    # Suede Mudguard U-band, Eyestays, Quarter Panels, Heel Counter,
    # and 3D Polished Chrome Wave Badge
    # =============================================================
    design_mesh = bpy.data.meshes.new("Design_Layers_Mesh")
    design_obj = bpy.data.objects.new("Sneaker_Design_Layers", design_mesh)
    bpy.context.collection.objects.link(design_obj)
    design_obj.data.materials.append(mats['suede'])  # 0: Suede panels
    design_obj.data.materials.append(mats['silver']) # 1: Chrome Silver Wave

    bm_d = bmesh.new()

    # Generate offset outer and return vertices (+1.8mm proud)
    proud_rings = []
    base_rings = []
    for st in stations:
        y = st['y']
        z_rim = st['z_rim']
        z_top = st['z_top']
        z_bot = st['z_bot']
        xl = st['xl']
        xm = st['xm']
        off = 0.0018

        cur_p = []
        cur_b = []
        for k in range(SEGS):
            theta = k * (2.0 * math.pi / SEGS)
            sin_th = math.sin(theta)
            cos_th = math.cos(theta)

            vx_p = (xl + off) * sin_th if sin_th >= 0 else ((-xm + off) * sin_th)
            vx_b = xl * sin_th if sin_th >= 0 else (-xm * sin_th)

            if cos_th >= 0:
                h_f = cos_th ** 1.35
                vz_p = z_rim + (z_top - z_rim + off) * h_f
                vz_b = z_rim + (z_top - z_rim) * h_f
            else:
                b_f = (-cos_th) ** 1.45
                vz_p = z_rim - (z_rim - z_bot) * b_f
                vz_b = z_rim - (z_rim - z_bot) * b_f

            cur_p.append(bm_d.verts.new((vx_p, y, vz_p)))
            cur_b.append(bm_d.verts.new((vx_b, y, vz_b)))
        proud_rings.append(cur_p)
        base_rings.append(cur_b)

    bm_d.verts.ensure_lookup_table()

    # (A) SUEDE MUDGUARD TOE CAP (Stations 20 to 29)
    # Covers lower lateral (k in [2..6]), wraps around front, to lower medial (k in [12..16])
    # Leaving the top vamp (k in [17, 0, 1]) open as white tumbled leather!
    mg_indices = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    for i in range(20, N_STATIONS - 1):
        r0 = proud_rings[i]
        r1 = proud_rings[i + 1]
        for k in mg_indices:
            knxt = (k + 1) % SEGS
            if knxt in mg_indices or knxt == 16:
                bm_d.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0

    # Beveled return lip along top edge of mudguard
    for i in range(20, N_STATIONS - 1):
        # Lateral rim at k=2
        p0_l, p1_l = proud_rings[i][2], proud_rings[i + 1][2]
        b0_l, b1_l = base_rings[i][2], base_rings[i + 1][2]
        bm_d.faces.new((p0_l, b0_l, b1_l, p1_l)).material_index = 0

        # Medial rim at k=16
        p0_m, p1_m = proud_rings[i][16], proud_rings[i + 1][16]
        b0_m, b1_m = base_rings[i][16], base_rings[i + 1][16]
        bm_d.faces.new((p0_m, p1_m, b1_m, b0_m)).material_index = 0

    # Front cap wrap for the mudguard
    r_mg_f = proud_rings[-1]
    c_mg_tip = bm_d.verts.new((0.0, y_front + 0.010, z_rim_f + 0.008))
    for k in mg_indices:
        knxt = (k + 1) % SEGS
        if knxt in mg_indices:
            bm_d.faces.new((r_mg_f[k], r_mg_f[knxt], c_mg_tip)).material_index = 0

    # (B) SUEDE QUARTER PANELS (Stations 7 to 20)
    for i in range(7, 20):
        r0 = proud_rings[i]
        r1 = proud_rings[i + 1]
        # Lateral flank (k in [1, 2, 3, 4])
        for k in [1, 2, 3]:
            knxt = (k + 1) % SEGS
            bm_d.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0
        # Medial flank (k in [14, 15, 16, 17])
        for k in [14, 15, 16]:
            knxt = (k + 1) % SEGS
            bm_d.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0

    # (C) SUEDE HEEL COUNTER (Stations 0 to 7)
    for i in range(7):
        r0 = proud_rings[i]
        r1 = proud_rings[i + 1]
        for k in [1, 2, 3, 14, 15, 16, 17]:
            knxt = (k + 1) % SEGS
            bm_d.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0

    # Heel counter rear closure
    c_hc = bm_d.verts.new((0.0, stations[0]['y'] - 0.007, 0.035))
    r_hc0 = proud_rings[0]
    for k in [1, 2, 3, 14, 15, 16, 17]:
        knxt = (k + 1) % SEGS
        bm_d.faces.new((c_hc, r_hc0[knxt], r_hc0[k])).material_index = 0

    # (D) 3D POLISHED CHROME WAVE BADGE
    # Elegantly sculpted on lateral and medial quarters
    for side in [1.0, -1.0]:
        w_in_b, w_in_t, w_out_b, w_out_t = [], [], [], []
        wave_st = range(9, 20)
        for idx, s in enumerate(wave_st):
            u = idx / (len(wave_st) - 1)
            y = stations[s]['y']
            z_rim = stations[s]['z_rim']
            z_top = stations[s]['z_top']
            xl = stations[s]['xl']
            xm = stations[s]['xm']
            dz = z_top - z_rim

            wave_h = 0.36 + 0.32 * math.sin(u * math.pi * 1.5)
            z_w = z_rim + dz * wave_h
            thick_h = 0.0055 + 0.0045 * math.sin(u * math.pi)

            base_x = (xl + 0.0022) if side > 0 else (-xm - 0.0022)
            x_in  = base_x - side * 0.0003
            x_out = base_x + side * 0.0028

            w_in_b.append(bm_d.verts.new((x_in, y, z_w)))
            w_in_t.append(bm_d.verts.new((x_in, y, z_w + thick_h)))
            w_out_b.append(bm_d.verts.new((x_out, y, z_w)))
            w_out_t.append(bm_d.verts.new((x_out, y, z_w + thick_h)))

        bm_d.verts.ensure_lookup_table()
        for k in range(len(wave_st) - 1):
            if side > 0:
                f_f = bm_d.faces.new((w_out_b[k], w_out_b[k+1], w_out_t[k+1], w_out_t[k]))
                f_t = bm_d.faces.new((w_in_t[k], w_in_t[k+1], w_out_t[k+1], w_out_t[k]))
                f_b = bm_d.faces.new((w_out_b[k], w_out_b[k+1], w_in_b[k+1], w_in_b[k]))
            else:
                f_f = bm_d.faces.new((w_out_b[k], w_out_t[k], w_out_t[k+1], w_out_b[k+1]))
                f_t = bm_d.faces.new((w_in_t[k], w_out_t[k], w_out_t[k+1], w_in_t[k+1]))
                f_b = bm_d.faces.new((w_out_b[k], w_in_b[k], w_in_b[k+1], w_out_b[k+1]))
            f_f.material_index = 1
            f_t.material_index = 1
            f_b.material_index = 1

        if side > 0:
            bm_d.faces.new((w_in_b[0], w_in_t[0], w_out_t[0], w_out_b[0])).material_index = 1
            bm_d.faces.new((w_in_b[-1], w_out_b[-1], w_out_t[-1], w_in_t[-1])).material_index = 1
        else:
            bm_d.faces.new((w_in_b[0], w_out_b[0], w_out_t[0], w_in_t[0])).material_index = 1
            bm_d.faces.new((w_in_b[-1], w_in_t[-1], w_out_t[-1], w_out_b[-1])).material_index = 1

    bm_d.to_mesh(design_mesh)
    bm_d.free()
    for p in design_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 4. STANDALONE TONGUE (`Sneaker_Tongue`)
    # 12mm thick plush skate foam tongue nestled in throat
    # =============================================================
    tongue_mesh = bpy.data.meshes.new("Tongue_Mesh")
    tongue_obj = bpy.data.objects.new("Sneaker_Tongue", tongue_mesh)
    bpy.context.collection.objects.link(tongue_obj)
    tongue_obj.data.materials.append(mats['upper'])
    tongue_obj.data.materials.append(mats['inner'])

    bm_t = bmesh.new()
    T_SEGS = 18
    t_loops = []

    for i in range(T_SEGS):
        u = i / (T_SEGS - 1)
        ty = 0.052 - u * 0.076
        tz = 0.032 + u * 0.022 + 0.002 * math.sin(u * math.pi)
        tw = 0.015 + 0.006 * u
        p_thick = 0.0048

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
    lbl_z = 0.054
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
        ( 0.044, 0.034, 0.016),
        ( 0.027, 0.039, 0.017),
        ( 0.010, 0.044, 0.018),
        (-0.006, 0.049, 0.019),
        (-0.020, 0.054, 0.020),
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
        lw = 0.0042
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
    print(f"[OK] Exported Masterpiece Sneaker: {out_glb_path}")

if __name__ == "__main__":
    out_dir = r"public/models"
    os.makedirs(out_dir, exist_ok=True)
    out_glb = os.path.join(out_dir, "test_artisan_sneaker.glb")
    create_masterpiece_sneaker(out_glb)
