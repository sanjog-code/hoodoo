import bpy
import bmesh
import math
import os

def build_sneaker_pbr_materials(cp):
    materials = {}
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

    # 1. Cupsole Rubber (with micro-stipple and foxing stripe bump)
    mat_sole, s_nodes, s_links, s_bsdf = create_mat("Mat_Sole", cp['sole'], cp.get('sole_roughness', 0.52))
    tex_s = s_nodes.new('ShaderNodeTexNoise')
    tex_s.inputs['Scale'].default_value = 350.0
    bmp_s = s_nodes.new('ShaderNodeBump')
    bmp_s.inputs['Strength'].default_value = 0.07
    bmp_s.inputs['Distance'].default_value = 0.001
    s_links.new(tex_s.outputs['Fac'], bmp_s.inputs['Height'])
    s_links.new(bmp_s.outputs['Normal'], s_bsdf.inputs['Normal'])
    materials['sole'] = mat_sole

    # 2. Tumbled Leather Upper (fine leather grain bump)
    mat_upper, u_nodes, u_links, u_bsdf = create_mat("Mat_Upper_Leather", cp['vamp'], cp.get('vamp_roughness', 0.36))
    tex_u = u_nodes.new('ShaderNodeTexVoronoi')
    tex_u.inputs['Scale'].default_value = 450.0
    bmp_u = u_nodes.new('ShaderNodeBump')
    bmp_u.inputs['Strength'].default_value = 0.04
    bmp_u.inputs['Distance'].default_value = 0.001
    u_links.new(tex_u.outputs['Distance'], bmp_u.inputs['Height'])
    u_links.new(bmp_u.outputs['Normal'], u_bsdf.inputs['Normal'])
    materials['upper'] = mat_upper

    # 3. Suede Overlays (soft tactile suede nap)
    mat_suede, d_nodes, d_links, d_bsdf = create_mat("Mat_Suede_Overlay", cp['quarter'], cp.get('quarter_roughness', 0.94))
    tex_d = d_nodes.new('ShaderNodeTexNoise')
    tex_d.inputs['Scale'].default_value = 500.0
    bmp_d = d_nodes.new('ShaderNodeBump')
    bmp_d.inputs['Strength'].default_value = 0.12
    bmp_d.inputs['Distance'].default_value = 0.0015
    d_links.new(tex_d.outputs['Fac'], bmp_d.inputs['Height'])
    d_links.new(bmp_d.outputs['Normal'], d_bsdf.inputs['Normal'])
    materials['suede'] = mat_suede

    # 4. Mirror Polished Chrome Wave Emblem
    mat_silver, _, _, _ = create_mat("Mat_Chrome_Wave", cp['silver'], cp.get('silver_roughness', 0.12), cp.get('silver_metal', 0.96))
    materials['silver'] = mat_silver

    # 5. Fat Skate Laces (Braided fabric weave bump)
    mat_lace, l_nodes, l_links, l_bsdf = create_mat("Mat_Laces", cp['lace'], cp.get('lace_roughness', 0.68))
    tex_l = l_nodes.new('ShaderNodeTexWave')
    tex_l.inputs['Scale'].default_value = 240.0
    bmp_l = l_nodes.new('ShaderNodeBump')
    bmp_l.inputs['Strength'].default_value = 0.14
    bmp_l.inputs['Distance'].default_value = 0.001
    l_links.new(tex_l.outputs['Fac'], bmp_l.inputs['Height'])
    l_links.new(bmp_l.outputs['Normal'], l_bsdf.inputs['Normal'])
    materials['lace'] = mat_lace

    # 6. Padded Velvet Lining
    mat_inner, _, _, _ = create_mat("Mat_Inner_Collar", cp['inner'], cp.get('inner_roughness', 0.96))
    materials['inner'] = mat_inner

    # 7. Brushed Nickel Eyelets
    mat_eyelet, _, _, _ = create_mat("Mat_Eyelets", cp['eyelet'], 0.20, cp.get('eyelet_metal', 0.94))
    materials['eyelet'] = mat_eyelet

    # 8. Brutalist Architectural Concrete Pedestal
    mat_ped, p_nodes, p_links, p_bsdf = create_mat("Mat_Pedestal", cp['pedestal'], cp.get('pedestal_roughness', 0.88))
    tex_p = p_nodes.new('ShaderNodeTexNoise')
    tex_p.inputs['Scale'].default_value = 150.0
    bmp_p = p_nodes.new('ShaderNodeBump')
    bmp_p.inputs['Strength'].default_value = 0.15
    bmp_p.inputs['Distance'].default_value = 0.002
    p_links.new(tex_p.outputs['Fac'], bmp_p.inputs['Height'])
    p_links.new(bmp_p.outputs['Normal'], p_bsdf.inputs['Normal'])
    materials['pedestal'] = mat_ped

    return materials

def create_complete_masterpiece_sneaker(out_glb_path, color_profile=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)

    cp = {
        'sole': (0.74, 0.48, 0.25, 1.0),       # Raw Gum Rubber
        'sole_roughness': 0.52,
        'vamp': (0.92, 0.90, 0.86, 1.0),       # Bone Tumbled Leather
        'vamp_roughness': 0.36,
        'quarter': (0.08, 0.045, 0.025, 1.0),  # Deep Chocolate Espresso Suede
        'quarter_roughness': 0.94,
        'silver': (0.92, 0.94, 0.98, 1.0),     # Polished Chrome Silver
        'silver_metal': 0.96,
        'silver_roughness': 0.12,
        'lace': (0.98, 0.98, 0.98, 1.0),       # Crisp White Fat Laces
        'lace_roughness': 0.68,
        'inner': (0.05, 0.05, 0.06, 1.0),      # Dark Velvet Padded Collar
        'inner_roughness': 0.96,
        'eyelet': (0.85, 0.87, 0.90, 1.0),     # Nickel Eyelets
        'eyelet_metal': 0.94,
        'pedestal': (0.28, 0.28, 0.30, 1.0),   # Concrete Plinth
        'pedestal_roughness': 0.88,
    }
    if color_profile:
        cp.update(color_profile)

    mats = build_sneaker_pbr_materials(cp)

    # -------------------------------------------------------------
    # PARAMETRIC FOOT LAST (34 Longitudinal Stations)
    # y = -0.130m (heel) to +0.150m (toe)
    # -------------------------------------------------------------
    STATIONS = 34
    y_stations = [-0.130 + i * (0.280 / (STATIONS - 1)) for i in range(STATIONS)]

    def calc_station(y):
        t = (y + 0.130) / 0.280
        t = max(0.0, min(1.0, t))

        # 12mm Toe Spring
        if t > 0.60:
            frac = (t - 0.60) / 0.40
            z_bot = 0.012 * (frac ** 1.85)
        elif t < 0.08:
            z_bot = 0.0016 * (1.0 - t / 0.08)
        else:
            z_bot = 0.000

        # Cupsole height: 18mm heel tapering smoothly to 14mm toe
        sole_h = 0.018 - 0.004 * t
        z_rim = z_bot + sole_h
        z_bed = z_rim - 0.0035 # Footbed floor recessed inside sole

        # Width contours: Skate last
        r_heel = math.sqrt(max(0.01, 1.0 - ((0.12 - t) / 0.12) ** 2)) if t < 0.12 else 1.0
        r_toe  = math.sqrt(max(0.01, 1.0 - ((t - 0.76) / 0.24) ** 2)) if t > 0.76 else 1.0

        if t < 0.24: # Heel
            xm = -0.035 * r_heel
            xl =  0.036 * r_heel
        elif t < 0.52: # Arch / Waist
            f = (t - 0.24) / 0.28
            xm = -(0.035 - 0.005 * math.sin(f * math.pi))
            xl =  (0.036 + 0.001 * math.sin(f * math.pi))
        elif t < 0.82: # Ball of foot flare
            f = (t - 0.52) / 0.30
            xm = -(0.032 + 0.011 * math.sin(f * math.pi * 0.88))
            xl =  (0.038 + 0.010 * math.sin(f * math.pi * 0.88))
        else: # Broad skate toe cap
            xm = -0.042 * r_toe
            xl =  0.044 * r_toe

        # Upper height & throat width
        if t < 0.20: # Heel collar & Achilles notch
            f = t / 0.20
            z_top = z_rim + 0.054 - 0.008 * f
            throat_w = 0.024 - 0.003 * f
            has_throat = False
        elif t < 0.42: # Collar opening
            f = (t - 0.20) / 0.22
            z_top = z_rim + 0.046 - 0.009 * math.sin(f * math.pi * 0.5)
            throat_w = 0.021 - 0.007 * f
            has_throat = (t >= 0.28)
        elif t < 0.68: # Eyestay lace throat
            f = (t - 0.42) / 0.26
            z_top = z_rim + 0.036 - 0.007 * f
            throat_w = 0.014 - 0.002 * f
            has_throat = True
        else: # Front vamp toe box
            f = (t - 0.68) / 0.32
            z_top = z_rim + 0.027 * math.cos(f * math.pi * 0.48)
            throat_w = 0.0
            has_throat = False

        return {
            't_val': t, 'y': y, 'z_bot': z_bot, 'z_rim': z_rim, 'z_bed': z_bed,
            'z_top': z_top, 'xm': xm, 'xl': xl, 'throat_w': throat_w, 'has_throat': has_throat
        }

    stations = [calc_station(y) for y in y_stations]

    # =============================================================
    # 1. STANDALONE SOLE (Rubber Cupsole with Foxing Rim)
    # =============================================================
    sole_mesh = bpy.data.meshes.new("Sole_Mesh")
    sole_obj = bpy.data.objects.new("Sneaker_Sole", sole_mesh)
    bpy.context.collection.objects.link(sole_obj)
    sole_obj.data.materials.append(mats['sole'])

    bm_s = bmesh.new()
    sole_cross_sections = []

    for s, d in enumerate(stations):
        y = d['y']
        zb = d['z_bot']
        zr = d['z_rim']
        zbed = d['z_bed']
        xl = d['xl'] * 1.025
        xm = d['xm'] * 1.025

        # Sole floor
        vb_l = bm_s.verts.new((xl, y, zb))
        vb_c = bm_s.verts.new((0.0, y, zb))
        vb_m = bm_s.verts.new((xm, y, zb))

        # Mid foxing stripe
        zm = zb + (zr - zb) * 0.58
        vm_l = bm_s.verts.new((xl * 1.010, y, zm))
        vm_m = bm_s.verts.new((xm * 1.010, y, zm))

        # Outer rim ledge
        vro_l = bm_s.verts.new((xl * 0.995, y, zr))
        vro_m = bm_s.verts.new((xm * 0.995, y, zr))

        # Inner rim shelf (2.0mm rim wall)
        vri_l = bm_s.verts.new((xl * 0.940, y, zr))
        vri_m = bm_s.verts.new((xm * 0.940, y, zr))

        # Footbed cavity floor
        vf_l = bm_s.verts.new((xl * 0.935, y, zbed))
        vf_c = bm_s.verts.new((0.0, y, zbed))
        vf_m = bm_s.verts.new((xm * 0.935, y, zbed))

        sole_cross_sections.append({
            'b': (vb_l, vb_c, vb_m),
            'm': (vm_l, vm_m),
            'ro': (vro_l, vro_m),
            'ri': (vri_l, vri_m),
            'f': (vf_l, vf_c, vf_m)
        })

    bm_s.verts.ensure_lookup_table()

    for s in range(STATIONS - 1):
        s0 = sole_cross_sections[s]
        s1 = sole_cross_sections[s + 1]

        # Floor quads
        bm_s.faces.new((s0['b'][0], s1['b'][0], s1['b'][1], s0['b'][1]))
        bm_s.faces.new((s0['b'][1], s1['b'][1], s1['b'][2], s0['b'][2]))

        # Lateral sidewall
        bm_s.faces.new((s0['b'][0], s0['m'][0], s1['m'][0], s1['b'][0]))
        bm_s.faces.new((s0['m'][0], s0['ro'][0], s1['ro'][0], s1['m'][0]))

        # Medial sidewall
        bm_s.faces.new((s0['b'][2], s1['b'][2], s1['m'][1], s0['m'][1]))
        bm_s.faces.new((s0['m'][1], s1['m'][1], s1['ro'][1], s0['ro'][1]))

        # Top rim shelf
        bm_s.faces.new((s0['ro'][0], s0['ri'][0], s1['ri'][0], s1['ro'][0]))
        bm_s.faces.new((s0['ro'][1], s1['ro'][1], s1['ri'][1], s0['ri'][1]))

        # Cavity inner wall
        bm_s.faces.new((s0['ri'][0], s0['f'][0], s1['f'][0], s1['ri'][0]))
        bm_s.faces.new((s0['ri'][1], s1['ri'][1], s1['f'][2], s0['f'][2]))

        # Interior floor
        bm_s.faces.new((s0['f'][0], s1['f'][0], s1['f'][1], s0['f'][1]))
        bm_s.faces.new((s0['f'][1], s1['f'][1], s1['f'][2], s0['f'][2]))

    # Heel closure
    sh = sole_cross_sections[0]
    bm_s.faces.new((sh['b'][0], sh['m'][0], sh['ro'][0], sh['ri'][0], sh['f'][0],
                    sh['f'][1], sh['f'][2], sh['ri'][1], sh['ro'][1], sh['m'][1],
                    sh['b'][2], sh['b'][1]))

    # Front toe bumper closure
    st = sole_cross_sections[-1]
    y_ft = stations[-1]['y'] + 0.0075
    zb_t = stations[-1]['z_bot'] + 0.003
    zr_t = stations[-1]['z_rim'] + 0.001
    tb_b  = bm_s.verts.new((0.0, y_ft, zb_t))
    tb_m  = bm_s.verts.new((0.0, y_ft + 0.0015, zb_t + (zr_t - zb_t) * 0.58))
    tb_ro = bm_s.verts.new((0.0, y_ft, zr_t))
    tb_ri = bm_s.verts.new((0.0, y_ft - 0.0025, zr_t))
    tb_f  = bm_s.verts.new((0.0, y_ft - 0.0035, stations[-1]['z_bed']))

    bm_s.faces.new((st['b'][0], st['b'][1], tb_b))
    bm_s.faces.new((st['b'][1], st['b'][2], tb_b))
    bm_s.faces.new((st['b'][0], tb_b, tb_m, st['m'][0]))
    bm_s.faces.new((st['b'][2], st['m'][1], tb_m, tb_b))
    bm_s.faces.new((st['m'][0], tb_m, tb_ro, st['ro'][0]))
    bm_s.faces.new((st['m'][1], st['ro'][1], tb_ro, tb_m))
    bm_s.faces.new((st['ro'][0], tb_ro, tb_ri, st['ri'][0]))
    bm_s.faces.new((st['ro'][1], st['ri'][1], tb_ri, tb_ro))
    bm_s.faces.new((st['ri'][0], tb_ri, tb_f, st['f'][0]))
    bm_s.faces.new((st['ri'][1], st['f'][2], tb_f, tb_ri))
    bm_s.faces.new((st['f'][0], tb_f, st['f'][1]))
    bm_s.faces.new((st['f'][2], st['f'][1], tb_f))

    bm_s.to_mesh(sole_mesh)
    bm_s.free()
    for p in sole_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 2. STANDALONE UPPER (The Foot Last Leather Base)
    # =============================================================
    upper_mesh = bpy.data.meshes.new("Upper_Mesh")
    upper_obj = bpy.data.objects.new("Sneaker_Upper", upper_mesh)
    bpy.context.collection.objects.link(upper_obj)
    upper_obj.data.materials.append(mats['upper']) # 0: Tumbled leather
    upper_obj.data.materials.append(mats['inner']) # 1: Velvet padded collar

    bm_u = bmesh.new()
    upper_sections = []

    for s, d in enumerate(stations):
        y = d['y']
        zbed = d['z_bed']
        zr = d['z_rim']
        zt = d['z_top']
        xl = d['xl'] * 0.940
        xm = d['xm'] * 0.940
        th_w = d['throat_w']
        has_th = d['has_throat']
        t = d['t_val']

        ub_l = bm_u.verts.new((xl, y, zbed))
        ub_m = bm_u.verts.new((xm, y, zbed))

        um_l = bm_u.verts.new((xl * 0.98, y, zr + 0.001))
        um_m = bm_u.verts.new((xm * 0.98, y, zr + 0.001))

        dz = zt - zr
        uu_l = bm_u.verts.new((xl * 0.88, y, zr + dz * 0.52))
        uu_m = bm_u.verts.new((xm * 0.88, y, zr + dz * 0.52))

        if has_th:
            ut_l = bm_u.verts.new(( th_w, y, zt))
            ut_m = bm_u.verts.new((-th_w, y, zt))
            uin_l = bm_u.verts.new(( th_w * 0.65, y, zt - 0.006))
            uin_m = bm_u.verts.new((-th_w * 0.65, y, zt - 0.006))
        elif t < 0.28:
            ut_l = bm_u.verts.new((xl * 0.68, y, zt))
            ut_m = bm_u.verts.new((xm * 0.68, y, zt))
            uin_l = bm_u.verts.new((xl * 0.44, y, zt - 0.010))
            uin_m = bm_u.verts.new((xm * 0.44, y, zt - 0.010))
        else:
            ut_l = bm_u.verts.new((xl * 0.38, y, zt + 0.001))
            ut_m = bm_u.verts.new((xm * 0.38, y, zt + 0.001))
            uin_l = None
            uin_m = None

        upper_sections.append({
            'b': (ub_l, ub_m),
            'm': (um_l, um_m),
            'u': (uu_l, uu_m),
            't_verts': (ut_l, ut_m),
            'in_verts': (uin_l, uin_m),
            'has_th': has_th,
            'is_vamp': (t >= 0.68),
            't_val': t, 'y': y, 'zt': zt, 'xl': xl, 'xm': xm, 'zr': zr
        })

    bm_u.verts.ensure_lookup_table()

    for s in range(STATIONS - 1):
        u0 = upper_sections[s]
        u1 = upper_sections[s + 1]

        f_l0 = bm_u.faces.new((u0['b'][0], u0['m'][0], u1['m'][0], u1['b'][0]))
        f_l1 = bm_u.faces.new((u0['m'][0], u0['u'][0], u1['u'][0], u1['m'][0]))
        f_l2 = bm_u.faces.new((u0['u'][0], u0['t_verts'][0], u1['t_verts'][0], u1['u'][0]))
        for f in [f_l0, f_l1, f_l2]: f.material_index = 0

        f_m0 = bm_u.faces.new((u0['b'][1], u1['b'][1], u1['m'][1], u0['m'][1]))
        f_m1 = bm_u.faces.new((u0['m'][1], u1['m'][1], u1['u'][1], u0['u'][1]))
        f_m2 = bm_u.faces.new((u0['u'][1], u1['u'][1], u1['t_verts'][1], u0['t_verts'][1]))
        for f in [f_m0, f_m1, f_m2]: f.material_index = 0

        if (u0['is_vamp'] and u1['is_vamp']) or (u0['has_th'] and u1['is_vamp']):
            f_v = bm_u.faces.new((u0['t_verts'][0], u0['t_verts'][1], u1['t_verts'][1], u1['t_verts'][0]))
            f_v.material_index = 0

        if u0['in_verts'][0] and u1['in_verts'][0]:
            f_il = bm_u.faces.new((u0['t_verts'][0], u1['t_verts'][0], u1['in_verts'][0], u0['in_verts'][0]))
            f_im = bm_u.faces.new((u0['t_verts'][1], u0['in_verts'][1], u1['in_verts'][1], u1['t_verts'][1]))
            f_il.material_index = 1
            f_im.material_index = 1

    uh = upper_sections[0]
    f_hc = bm_u.faces.new((uh['b'][0], uh['m'][0], uh['u'][0], uh['t_verts'][0],
                           uh['t_verts'][1], uh['u'][1], uh['m'][1], uh['b'][1]))
    f_hc.material_index = 0

    ut = upper_sections[-1]
    y_apex = ut['y'] + 0.0065
    z_apex = ut['zt'] - 0.002
    va_b = bm_u.verts.new((0.0, y_apex, stations[-1]['z_bed']))
    va_m = bm_u.verts.new((0.0, y_apex + 0.001, stations[-1]['z_rim'] + 0.003))
    va_t = bm_u.verts.new((0.0, y_apex, z_apex))

    bm_u.faces.new((ut['b'][0], ut['m'][0], va_m, va_b)).material_index = 0
    bm_u.faces.new((ut['b'][1], va_b, va_m, ut['m'][1])).material_index = 0
    bm_u.faces.new((ut['m'][0], ut['u'][0], va_t, va_m)).material_index = 0
    bm_u.faces.new((ut['m'][1], va_m, va_t, ut['u'][1])).material_index = 0
    bm_u.faces.new((ut['u'][0], ut['t_verts'][0], ut['t_verts'][1], ut['u'][1], va_t)).material_index = 0

    # Toe box micro-perforations
    perfs = [
        (0.000, 0.106, 0.033),
        (-0.009, 0.102, 0.033), (0.009, 0.102, 0.033),
        (-0.016, 0.096, 0.034), (0.000, 0.096, 0.035), (0.016, 0.096, 0.034),
        (-0.010, 0.090, 0.036), (0.010, 0.090, 0.036),
        (0.000, 0.084, 0.037)
    ]
    for px, py, pz in perfs:
        pw = 0.0015
        p0 = bm_u.verts.new((px - pw, py - pw, pz - 0.0006))
        p1 = bm_u.verts.new((px + pw, py - pw, pz - 0.0006))
        p2 = bm_u.verts.new((px + pw, py + pw, pz - 0.0006))
        p3 = bm_u.verts.new((px - pw, py + pw, pz - 0.0006))
        bm_u.faces.new((p0, p1, p2, p3)).material_index = 1

    bm_u.to_mesh(upper_mesh)
    bm_u.free()
    sub_u = upper_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_u.levels = 1
    for p in upper_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 3. STANDALONE DESIGN LAYERS (Physical Suede Overlays & 3D Wave)
    # =============================================================
    design_mesh = bpy.data.meshes.new("Design_Layers_Mesh")
    design_obj = bpy.data.objects.new("Sneaker_Design_Layers", design_mesh)
    bpy.context.collection.objects.link(design_obj)
    design_obj.data.materials.append(mats['suede'])  # 0: Suede panels
    design_obj.data.materials.append(mats['silver']) # 1: Chrome Silver Wave

    bm_d = bmesh.new()

    # (A) Suede Mudguard (Toe Cap Overlay, stations 20 to 33)
    mg_l_in, mg_l_out, mg_m_in, mg_m_out = [], [], [], []
    mg_range = range(20, STATIONS)

    for s in mg_range:
        d = stations[s]
        y = d['y']
        zr = d['z_rim']
        zt = d['z_top']
        dz = zt - zr
        
        xl_b = d['xl'] * 0.940
        xm_b = d['xm'] * 0.940
        thk = 0.0016

        z_top_mg = zr + dz * 0.44
        mg_l_in.append((
            bm_d.verts.new((xl_b * 0.99, y, zr + 0.001)),
            bm_d.verts.new((xl_b * 0.88, y, z_top_mg))
        ))
        mg_l_out.append((
            bm_d.verts.new(((xl_b + thk) * 0.99, y, zr + 0.001)),
            bm_d.verts.new(((xl_b + thk) * 0.88, y, z_top_mg))
        ))

        mg_m_in.append((
            bm_d.verts.new((xm_b * 0.99, y, zr + 0.001)),
            bm_d.verts.new((xm_b * 0.88, y, z_top_mg))
        ))
        mg_m_out.append((
            bm_d.verts.new(((xm_b - thk) * 0.99, y, zr + 0.001)),
            bm_d.verts.new(((xm_b - thk) * 0.88, y, z_top_mg))
        ))

    bm_d.verts.ensure_lookup_table()

    for i in range(len(mg_range) - 1):
        lo0 = mg_l_out[i]
        lo1 = mg_l_out[i + 1]
        bm_d.faces.new((lo0[0], lo0[1], lo1[1], lo1[0])).material_index = 0
        li0 = mg_l_in[i]
        li1 = mg_l_in[i + 1]
        bm_d.faces.new((lo0[1], li0[1], li1[1], lo1[1])).material_index = 0

        mo0 = mg_m_out[i]
        mo1 = mg_m_out[i + 1]
        bm_d.faces.new((mo0[0], mo0[1], mo1[1], mo1[0])).material_index = 0
        mi0 = mg_m_in[i]
        mi1 = mg_m_in[i + 1]
        bm_d.faces.new((mo0[1], mo1[1], mi1[1], mi0[1])).material_index = 0

    d_tip = stations[-1]
    y_tip = d_tip['y'] + 0.0072
    z_tip = d_tip['z_rim'] + 0.0085
    thk = 0.0016
    vt_out_b = bm_d.verts.new((0.0, y_tip + thk, d_tip['z_rim'] + 0.001))
    vt_out_t = bm_d.verts.new((0.0, y_tip + thk, z_tip))
    vt_in_t  = bm_d.verts.new((0.0, y_tip, z_tip))

    bm_d.faces.new((mg_l_out[-1][0], mg_l_out[-1][1], vt_out_t, vt_out_b)).material_index = 0
    bm_d.faces.new((mg_m_out[-1][0], vt_out_b, vt_out_t, mg_m_out[-1][1])).material_index = 0
    bm_d.faces.new((mg_l_out[-1][1], mg_l_in[-1][1], vt_in_t, vt_out_t)).material_index = 0
    bm_d.faces.new((mg_m_out[-1][1], vt_out_t, vt_in_t, mg_m_in[-1][1])).material_index = 0

    # (B) Suede Quarter Panels (Stations 7 to 21)
    qp_range = range(7, 22)
    qp_l_in, qp_l_out, qp_m_in, qp_m_out = [], [], [], []

    for s in qp_range:
        d = stations[s]
        y = d['y']
        zr = d['z_rim']
        zt = d['z_top']
        dz = zt - zr
        thk = 0.0015
        xl_b = d['xl'] * 0.940
        xm_b = d['xm'] * 0.940

        z_t_qp = zr + dz * 0.88
        z_m_qp = zr + dz * 0.48
        qp_l_out.append((
            bm_d.verts.new(((xl_b + thk) * 0.99, y, zr + 0.001)),
            bm_d.verts.new(((xl_b + thk) * 0.94, y, z_m_qp)),
            bm_d.verts.new(((xl_b + thk) * 0.85, y, z_t_qp))
        ))
        qp_l_in.append((
            bm_d.verts.new((xl_b * 0.99, y, zr + 0.001)),
            bm_d.verts.new((xl_b * 0.85, y, z_t_qp))
        ))

        qp_m_out.append((
            bm_d.verts.new(((xm_b - thk) * 0.99, y, zr + 0.001)),
            bm_d.verts.new(((xm_b - thk) * 0.94, y, z_m_qp)),
            bm_d.verts.new(((xm_b - thk) * 0.85, y, z_t_qp))
        ))
        qp_m_in.append((
            bm_d.verts.new((xm_b * 0.99, y, zr + 0.001)),
            bm_d.verts.new((xm_b * 0.85, y, z_t_qp))
        ))

    bm_d.verts.ensure_lookup_table()
    for i in range(len(qp_range) - 1):
        lo0 = qp_l_out[i]
        lo1 = qp_l_out[i + 1]
        bm_d.faces.new((lo0[0], lo0[1], lo1[1], lo1[0])).material_index = 0
        bm_d.faces.new((lo0[1], lo0[2], lo1[2], lo1[1])).material_index = 0
        li0 = qp_l_in[i]
        li1 = qp_l_in[i + 1]
        bm_d.faces.new((lo0[2], li0[1], li1[1], lo1[2])).material_index = 0

        mo0 = qp_m_out[i]
        mo1 = qp_m_out[i + 1]
        bm_d.faces.new((mo0[0], mo0[1], mo1[1], mo1[0])).material_index = 0
        bm_d.faces.new((mo0[1], mo1[1], mo1[2], mo0[2])).material_index = 0
        mi0 = qp_m_in[i]
        mi1 = qp_m_in[i + 1]
        bm_d.faces.new((mo0[2], mo1[2], mi1[1], mi0[1])).material_index = 0

    # (C) Suede Heel Counter (Stations 0 to 8)
    hc_l_out, hc_m_out = [], []
    for s in range(8):
        d = stations[s]
        y = d['y']
        zr = d['z_rim']
        zt = d['z_top']
        dz = zt - zr
        thk = 0.0015
        xl_b = d['xl'] * 0.940
        xm_b = d['xm'] * 0.940
        z_t_hc = zr + dz * 0.65

        hc_l_out.append((
            bm_d.verts.new(((xl_b + thk) * 0.99, y, zr + 0.001)),
            bm_d.verts.new(((xl_b + thk) * 0.84, y, z_t_hc))
        ))
        hc_m_out.append((
            bm_d.verts.new(((xm_b - thk) * 0.99, y, zr + 0.001)),
            bm_d.verts.new(((xm_b - thk) * 0.84, y, z_t_hc))
        ))

    bm_d.verts.ensure_lookup_table()
    for i in range(7):
        l0 = hc_l_out[i]
        l1 = hc_l_out[i + 1]
        bm_d.faces.new((l0[0], l0[1], l1[1], l1[0])).material_index = 0
        r0 = hc_m_out[i]
        r1 = hc_m_out[i + 1]
        bm_d.faces.new((r0[0], r1[0], r1[1], r0[1])).material_index = 0

    bm_d.faces.new((hc_l_out[0][0], hc_l_out[0][1], hc_m_out[0][1], hc_m_out[0][0])).material_index = 0

    # (D) 3D Gleaming Chrome Wave Emblem
    for side in [1.0, -1.0]:
        w_in_b, w_in_t, w_out_b, w_out_t = [], [], [], []
        wave_st = range(9, 21)
        for idx, s in enumerate(wave_st):
            u = idx / (len(wave_st) - 1)
            d = stations[s]
            zr = d['z_rim']
            zt = d['z_top']
            dz = zt - zr
            y = d['y']

            wave_h = 0.38 + 0.30 * math.sin(u * math.pi * 1.5)
            z_w = zr + dz * wave_h
            thick_h = 0.006 + 0.005 * math.sin(u * math.pi)

            base_x = (d['xl'] * 0.940 if side > 0 else d['xm'] * 0.940) + side * 0.0015
            x_in = base_x - side * 0.0003
            x_out = base_x + side * 0.0022

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
    # 4. STANDALONE TONGUE (Puffy Skate Tongue with Woven Tag)
    # =============================================================
    tongue_mesh = bpy.data.meshes.new("Tongue_Mesh")
    tongue_obj = bpy.data.objects.new("Sneaker_Tongue", tongue_mesh)
    bpy.context.collection.objects.link(tongue_obj)
    tongue_obj.data.materials.append(mats['upper'])
    tongue_obj.data.materials.append(mats['inner'])

    bm_t = bmesh.new()
    T_SEGS = 16
    t_loops = []

    for i in range(T_SEGS):
        u = i / (T_SEGS - 1)
        ty = 0.052 - u * 0.076
        tz = 0.034 + u * 0.040 + 0.003 * math.sin(u * math.pi)
        tw = 0.016 + 0.006 * u
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

    lbl_y = -0.014
    lbl_z = 0.072
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
    # 5. STANDALONE LACES & EYELETS
    # =============================================================
    lace_mesh = bpy.data.meshes.new("Laces_Mesh")
    lace_obj = bpy.data.objects.new("Sneaker_Laces", lace_mesh)
    bpy.context.collection.objects.link(lace_obj)
    lace_obj.data.materials.append(mats['lace'])
    lace_obj.data.materials.append(mats['eyelet'])

    bm_l = bmesh.new()

    lace_stations = [
        ( 0.044, 0.040, 0.015),
        ( 0.027, 0.049, 0.016),
        ( 0.010, 0.058, 0.017),
        (-0.006, 0.066, 0.018),
        (-0.020, 0.074, 0.019),
    ]

    for ly, lz, span in lace_stations:
        for side in [-1.0, 1.0]:
            cx = side * span
            cy = ly
            cz = lz + 0.002
            SEGS = 8
            er_out = 0.0026
            er_in  = 0.0016
            r_o, r_i = [], []
            for k in range(SEGS):
                ang = k * (2.0 * math.pi / SEGS)
                rx = math.cos(ang)
                ry = math.sin(ang)
                r_o.append(bm_l.verts.new((cx + rx * er_out, cy + ry * er_out, cz + 0.0005)))
                r_i.append(bm_l.verts.new((cx + rx * er_in,  cy + ry * er_in,  cz - 0.0004)))
            for k in range(SEGS):
                knxt = (k + 1) % SEGS
                bm_l.faces.new((r_o[k], r_o[knxt], r_i[knxt], r_i[k])).material_index = 1

    for ly, lz, span in lace_stations:
        lw = 0.0042
        th = 0.0022
        lz_e = lz + 0.003

        vl   = bm_l.verts.new((-span,        ly - lw, lz_e))
        vcl  = bm_l.verts.new((-span * 0.45, ly - lw, lz_e + 0.0024))
        vcr  = bm_l.verts.new(( span * 0.45, ly - lw, lz_e + 0.0024))
        vr   = bm_l.verts.new(( span,        ly - lw, lz_e))

        vl_f  = bm_l.verts.new((-span,        ly + lw, lz_e))
        vcl_f = bm_l.verts.new((-span * 0.45, ly + lw, lz_e + 0.0024))
        vcr_f = bm_l.verts.new(( span * 0.45, ly + lw, lz_e + 0.0024))
        vr_f  = bm_l.verts.new(( span,        ly + lw, lz_e))

        vl_t  = bm_l.verts.new((-span,        ly - lw, lz_e + th))
        vcl_t = bm_l.verts.new((-span * 0.45, ly - lw, lz_e + th + 0.0024))
        vcr_t = bm_l.verts.new(( span * 0.45, ly - lw, lz_e + th + 0.0024))
        vr_t  = bm_l.verts.new(( span,        ly - lw, lz_e + th))

        vl_ft  = bm_l.verts.new((-span,        ly + lw, lz_e + th))
        vcl_ft = bm_l.verts.new((-span * 0.45, ly + lw, lz_e + th + 0.0024))
        vcr_ft = bm_l.verts.new(( span * 0.45, ly + lw, lz_e + th + 0.0024))
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
    # 6. STANDALONE BRUTALIST CONCRETE PEDESTAL
    # =============================================================
    ped_mesh = bpy.data.meshes.new("Pedestal_Mesh")
    ped_obj = bpy.data.objects.new("Sneaker_Pedestal", ped_mesh)
    bpy.context.collection.objects.link(ped_obj)
    ped_obj.data.materials.append(mats['pedestal'])

    bm_p = bmesh.new()
    P_SEGS = 36
    ped_r = 0.185
    c_top = bm_p.verts.new((0.0, 0.010, 0.000))
    c_bot = bm_p.verts.new((0.0, 0.010, -0.024))
    r_top, r_bot = [], []
    for i in range(P_SEGS):
        ang = i * (2.0 * math.pi / P_SEGS)
        px = math.cos(ang) * ped_r
        py = math.sin(ang) * ped_r + 0.010
        r_top.append(bm_p.verts.new((px, py, 0.000)))
        r_bot.append(bm_p.verts.new((px * 1.035, py, -0.024)))

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
    print(f"[OK] Exported Complete Masterpiece Sneaker: {out_glb_path}")

if __name__ == "__main__":
    out_dir = r"public/models"
    os.makedirs(out_dir, exist_ok=True)
    out_glb = os.path.join(out_dir, "test_complete_sneaker.glb")
    create_complete_masterpiece_sneaker(out_glb)
