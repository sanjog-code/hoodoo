import bpy
import bmesh
import math
import os

def build_sneaker_materials(cp):
    """Builds ultra-realistic PBR materials with procedural bump and micro-textures."""
    materials = {}

    def create_mat(name):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (400, 0)
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (100, 0)
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        return mat, nodes, links, bsdf

    # 1. Cupsole Rubber (Gum / Vulcanized Rubber with micro-texture & foxing groove bump)
    mat_sole, nodes, links, bsdf = create_mat("Mat_Sole")
    bsdf.inputs['Base Color'].default_value = cp['sole']
    bsdf.inputs['Roughness'].default_value = cp.get('sole_roughness', 0.55)
    tex_noise = nodes.new('ShaderNodeTexNoise')
    tex_noise.location = (-300, -100)
    tex_noise.inputs['Scale'].default_value = 250.0
    tex_noise.inputs['Detail'].default_value = 4.0
    tex_noise.inputs['Roughness'].default_value = 0.7
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-100, -100)
    bump.inputs['Strength'].default_value = 0.08
    bump.inputs['Distance'].default_value = 0.002
    links.new(tex_noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    materials['sole'] = mat_sole

    # 2. Tumbled Leather (Rich grain, subtle specular gloss)
    mat_upper, nodes, links, bsdf = create_mat("Mat_Upper_Leather")
    bsdf.inputs['Base Color'].default_value = cp['vamp']
    bsdf.inputs['Roughness'].default_value = cp.get('vamp_roughness', 0.36)
    tex_voro = nodes.new('ShaderNodeTexVoronoi')
    tex_voro.location = (-320, -120)
    tex_voro.inputs['Scale'].default_value = 350.0
    bump_l = nodes.new('ShaderNodeBump')
    bump_l.location = (-100, -120)
    bump_l.inputs['Strength'].default_value = 0.05
    bump_l.inputs['Distance'].default_value = 0.0015
    links.new(tex_voro.outputs['Distance'], bump_l.inputs['Height'])
    links.new(bump_l.outputs['Normal'], bsdf.inputs['Normal'])
    materials['upper'] = mat_upper

    # 3. Tactile Suede / Nubuck (High roughness, soft diffuse scattering)
    mat_suede, nodes, links, bsdf = create_mat("Mat_Suede_Overlay")
    bsdf.inputs['Base Color'].default_value = cp['quarter']
    bsdf.inputs['Roughness'].default_value = cp.get('quarter_roughness', 0.94)
    tex_noise_s = nodes.new('ShaderNodeTexNoise')
    tex_noise_s.location = (-300, -100)
    tex_noise_s.inputs['Scale'].default_value = 400.0
    tex_noise_s.inputs['Detail'].default_value = 6.0
    bump_s = nodes.new('ShaderNodeBump')
    bump_s.location = (-100, -100)
    bump_s.inputs['Strength'].default_value = 0.12
    bump_s.inputs['Distance'].default_value = 0.002
    links.new(tex_noise_s.outputs['Fac'], bump_s.inputs['Height'])
    links.new(bump_s.outputs['Normal'], bsdf.inputs['Normal'])
    materials['suede'] = mat_suede

    # 4. Polished Chrome HooDoo Wave Emblem (Mirror-like chrome finish)
    mat_silver, nodes, links, bsdf = create_mat("Mat_Chrome_Wave")
    bsdf.inputs['Base Color'].default_value = cp['silver']
    bsdf.inputs['Metallic'].default_value = cp.get('silver_metal', 0.96)
    bsdf.inputs['Roughness'].default_value = cp.get('silver_roughness', 0.14)
    if 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = (0.08, 0.09, 0.10, 1.0)
    materials['silver'] = mat_silver

    # 5. Fat Skate Laces (Braided cotton weave texture)
    mat_lace, nodes, links, bsdf = create_mat("Mat_Laces")
    bsdf.inputs['Base Color'].default_value = cp['lace']
    bsdf.inputs['Roughness'].default_value = cp.get('lace_roughness', 0.68)
    tex_wave = nodes.new('ShaderNodeTexWave')
    tex_wave.location = (-300, -100)
    tex_wave.inputs['Scale'].default_value = 180.0
    bump_w = nodes.new('ShaderNodeBump')
    bump_w.location = (-100, -100)
    bump_w.inputs['Strength'].default_value = 0.15
    bump_w.inputs['Distance'].default_value = 0.001
    links.new(tex_wave.outputs['Fac'], bump_w.inputs['Height'])
    links.new(bump_w.outputs['Normal'], bsdf.inputs['Normal'])
    materials['lace'] = mat_lace

    # 6. Padded Velvet Interior Collar Lining & Tongue Lining
    mat_inner, nodes, links, bsdf = create_mat("Mat_Inner_Collar")
    bsdf.inputs['Base Color'].default_value = cp['inner']
    bsdf.inputs['Roughness'].default_value = cp.get('inner_roughness', 0.96)
    materials['inner'] = mat_inner

    # 7. Brushed Metal Eyelet Rings
    mat_eyelet, nodes, links, bsdf = create_mat("Mat_Eyelets")
    bsdf.inputs['Base Color'].default_value = cp['eyelet']
    bsdf.inputs['Metallic'].default_value = cp.get('eyelet_metal', 0.92)
    bsdf.inputs['Roughness'].default_value = 0.22
    materials['eyelet'] = mat_eyelet

    # 8. Brutalist Architectural Concrete Pedestal
    mat_ped, nodes, links, bsdf = create_mat("Mat_Pedestal")
    bsdf.inputs['Base Color'].default_value = cp['pedestal']
    bsdf.inputs['Roughness'].default_value = cp.get('pedestal_roughness', 0.88)
    tex_ped_noise = nodes.new('ShaderNodeTexNoise')
    tex_ped_noise.location = (-300, -100)
    tex_ped_noise.inputs['Scale'].default_value = 120.0
    bump_ped = nodes.new('ShaderNodeBump')
    bump_ped.location = (-100, -100)
    bump_ped.inputs['Strength'].default_value = 0.18
    bump_ped.inputs['Distance'].default_value = 0.003
    links.new(tex_ped_noise.outputs['Fac'], bump_ped.inputs['Height'])
    links.new(bump_ped.outputs['Normal'], bsdf.inputs['Normal'])
    materials['pedestal'] = mat_ped

    return materials


def create_masterpiece_modular_sneaker(out_glb_path, color_profile=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # -------------------------------------------------------------
    # Color Profiles
    # -------------------------------------------------------------
    cp = {
        'sole': (0.74, 0.48, 0.25, 1.0),       # Raw Gum Rubber
        'sole_roughness': 0.54,
        'vamp': (0.92, 0.90, 0.86, 1.0),       # Bone Tumbled Leather
        'vamp_roughness': 0.36,
        'quarter': (0.08, 0.045, 0.025, 1.0),  # Deep Chocolate Espresso Suede
        'quarter_roughness': 0.94,
        'silver': (0.92, 0.94, 0.98, 1.0),     # Polished Chrome Silver
        'silver_metal': 0.96,
        'silver_roughness': 0.14,
        'lace': (0.98, 0.98, 0.98, 1.0),       # Crisp White Fat Laces
        'lace_roughness': 0.68,
        'inner': (0.05, 0.05, 0.06, 1.0),      # Dark Velvet Padded Collar
        'inner_roughness': 0.96,
        'eyelet': (0.85, 0.87, 0.90, 1.0),     # High-luster Nickel Eyelets
        'eyelet_metal': 0.94,
        'pedestal': (0.30, 0.30, 0.32, 1.0),   # Concrete Plinth
        'pedestal_roughness': 0.88,
    }
    if color_profile:
        cp.update(color_profile)

    mats = build_sneaker_materials(cp)

    # -------------------------------------------------------------
    # SNEAKER CROSS-SECTIONAL LAST GEOMETRY
    # Length: 280mm (-0.130m heel to +0.150m toe)
    # -------------------------------------------------------------
    STATIONS = 36
    y_stations = [-0.130 + i * (0.280 / (STATIONS - 1)) for i in range(STATIONS)]

    def get_station_spec(y):
        t = (y + 0.130) / 0.280
        t = max(0.0, min(1.0, t))

        # 1. Sole Bottom Height & Realistic 12mm Toe Spring
        if t > 0.58:
            frac = (t - 0.58) / 0.42
            z_bot = 0.012 * (frac ** 1.85)
        elif t < 0.07:
            z_bot = 0.0018 * (1.0 - t / 0.07)
        else:
            z_bot = 0.000

        # Cupsole height: 18mm at heel tapering smoothly to 14mm at toe
        sole_h = 0.0185 - 0.0045 * t
        z_rim = z_bot + sole_h
        # Interior footbed: recessed 3.5mm down inside the cupsole rim
        z_bed = z_rim - 0.0035

        # 2. Width Contours: Ergonomic skate last
        r_heel = math.sqrt(max(0.01, 1.0 - ((0.11 - t) / 0.11) ** 2)) if t < 0.11 else 1.0
        r_toe = math.sqrt(max(0.01, 1.0 - ((t - 0.78) / 0.22) ** 2)) if t > 0.78 else 1.0

        if t < 0.25: # Heel
            xm = -0.036 * r_heel
            xl =  0.037 * r_heel
        elif t < 0.55: # Medial arch tuck & lateral waist
            f = (t - 0.25) / 0.30
            xm = -(0.036 - 0.005 * math.sin(f * math.pi))
            xl =  (0.037 + 0.001 * math.sin(f * math.pi))
        elif t < 0.84: # Ball of foot flare
            f = (t - 0.55) / 0.29
            xm = -(0.033 + 0.011 * math.sin(f * math.pi * 0.85))
            xl =  (0.039 + 0.010 * math.sin(f * math.pi * 0.85))
        else: # Toe dome
            xm = -0.043 * r_toe
            xl =  0.045 * r_toe

        # 3. Upper Height & Throat profile
        if t < 0.20: # Heel collar & Achilles notch
            f = t / 0.20
            z_top = z_rim + 0.052 - 0.008 * f
            throat_w = 0.024 - 0.003 * f
            has_throat = False
        elif t < 0.42: # Collar dip & opening
            f = (t - 0.20) / 0.22
            z_top = z_rim + 0.044 - 0.009 * math.sin(f * math.pi * 0.5)
            throat_w = 0.021 - 0.007 * f
            has_throat = (t >= 0.28)
        elif t < 0.68: # Eyestay lace throat
            f = (t - 0.42) / 0.26
            z_top = z_rim + 0.035 - 0.007 * f
            throat_w = 0.014 - 0.002 * f
            has_throat = True
        else: # Front vamp / toe box
            f = (t - 0.68) / 0.32
            z_top = z_rim + 0.027 * math.cos(f * math.pi * 0.48)
            throat_w = 0.0
            has_throat = False

        return {
            't': t, 'y': y, 'z_bot': z_bot, 'z_rim': z_rim, 'z_bed': z_bed,
            'z_top': z_top, 'xm': xm, 'xl': xl, 'throat_w': throat_w, 'has_throat': has_throat
        }

    stations = [get_station_spec(y) for y in y_stations]

    # =============================================================
    # PART 1: STANDALONE SOLE OBJECT (Crisp Foxing Rim, Tread, Lip)
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
        xl = d['xl'] * 1.020
        xm = d['xm'] * 1.020

        vb_l = bm_s.verts.new((xl, y, zb))
        vb_c = bm_s.verts.new((0.0, y, zb))
        vb_m = bm_s.verts.new((xm, y, zb))

        z_groove = zb + (zr - zb) * 0.55
        vg_l = bm_s.verts.new((xl * 1.010, y, z_groove))
        vg_m = bm_s.verts.new((xm * 1.010, y, z_groove))

        vr_o_l = bm_s.verts.new((xl * 0.995, y, zr))
        vr_o_m = bm_s.verts.new((xm * 0.995, y, zr))

        vr_i_l = bm_s.verts.new((xl * 0.950, y, zr))
        vr_i_m = bm_s.verts.new((xm * 0.950, y, zr))

        vf_l = bm_s.verts.new((xl * 0.945, y, zbed))
        vf_c = bm_s.verts.new((0.0, y, zbed))
        vf_m = bm_s.verts.new((xm * 0.945, y, zbed))

        sole_cross_sections.append({
            'b': (vb_l, vb_c, vb_m),
            'g': (vg_l, vg_m),
            'ro': (vr_o_l, vr_o_m),
            'ri': (vr_i_l, vr_i_m),
            'f': (vf_l, vf_c, vf_m)
        })

    bm_s.verts.ensure_lookup_table()

    for s in range(STATIONS - 1):
        s0 = sole_cross_sections[s]
        s1 = sole_cross_sections[s + 1]

        bm_s.faces.new((s0['b'][0], s1['b'][0], s1['b'][1], s0['b'][1]))
        bm_s.faces.new((s0['b'][1], s1['b'][1], s1['b'][2], s0['b'][2]))

        bm_s.faces.new((s0['b'][0], s0['g'][0], s1['g'][0], s1['b'][0]))
        bm_s.faces.new((s0['g'][0], s0['ro'][0], s1['ro'][0], s1['g'][0]))

        bm_s.faces.new((s0['b'][2], s1['b'][2], s1['g'][1], s0['g'][1]))
        bm_s.faces.new((s0['g'][1], s1['g'][1], s1['ro'][1], s0['ro'][1]))

        bm_s.faces.new((s0['ro'][0], s0['ri'][0], s1['ri'][0], s1['ro'][0]))
        bm_s.faces.new((s0['ro'][1], s1['ro'][1], s1['ri'][1], s0['ri'][1]))

        bm_s.faces.new((s0['ri'][0], s0['f'][0], s1['f'][0], s1['ri'][0]))
        bm_s.faces.new((s0['ri'][1], s1['ri'][1], s1['f'][2], s0['f'][2]))

        bm_s.faces.new((s0['f'][0], s1['f'][0], s1['f'][1], s0['f'][1]))
        bm_s.faces.new((s0['f'][1], s1['f'][1], s1['f'][2], s0['f'][2]))

    sh = sole_cross_sections[0]
    bm_s.faces.new((sh['b'][0], sh['g'][0], sh['ro'][0], sh['ri'][0], sh['f'][0],
                    sh['f'][1], sh['f'][2], sh['ri'][1], sh['ro'][1], sh['g'][1],
                    sh['b'][2], sh['b'][1]))

    st = sole_cross_sections[-1]
    y_front = stations[-1]['y'] + 0.007
    zb_tip = stations[-1]['z_bot'] + 0.004
    zr_tip = stations[-1]['z_rim'] + 0.001
    tb_b  = bm_s.verts.new((0.0, y_front, zb_tip))
    tb_g  = bm_s.verts.new((0.0, y_front + 0.0015, zb_tip + (zr_tip - zb_tip) * 0.55))
    tb_ro = bm_s.verts.new((0.0, y_front, zr_tip))
    tb_ri = bm_s.verts.new((0.0, y_front - 0.0025, zr_tip))
    tb_f  = bm_s.verts.new((0.0, y_front - 0.0035, stations[-1]['z_bed']))

    bm_s.faces.new((st['b'][0], st['b'][1], tb_b))
    bm_s.faces.new((st['b'][1], st['b'][2], tb_b))
    bm_s.faces.new((st['b'][0], tb_b, tb_g, st['g'][0]))
    bm_s.faces.new((st['b'][2], st['g'][1], tb_g, tb_b))
    bm_s.faces.new((st['g'][0], tb_g, tb_ro, st['ro'][0]))
    bm_s.faces.new((st['g'][1], st['ro'][1], tb_ro, tb_g))
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
    # PART 2: STANDALONE UPPER LEATHER MESH (The Foot Last Base)
    # =============================================================
    upper_mesh = bpy.data.meshes.new("Upper_Mesh")
    upper_obj = bpy.data.objects.new("Sneaker_Upper", upper_mesh)
    bpy.context.collection.objects.link(upper_obj)
    upper_obj.data.materials.append(mats['upper']) # 0: Tumbled Leather
    upper_obj.data.materials.append(mats['inner']) # 1: Padded Velvet Lining

    bm_u = bmesh.new()
    upper_cross_sections = []

    for s, d in enumerate(stations):
        y = d['y']
        zbed = d['z_bed']
        zr = d['z_rim']
        zt = d['z_top']
        xl = d['xl'] * 0.945
        xm = d['xm'] * 0.945
        th_w = d['throat_w']
        has_th = d['has_throat']
        t = d['t']

        vu_b_l = bm_u.verts.new((xl, y, zbed))
        vu_b_m = bm_u.verts.new((xm, y, zbed))

        vu_m_l = bm_u.verts.new((xl * 0.98, y, zr + 0.001))
        vu_m_m = bm_u.verts.new((xm * 0.98, y, zr + 0.001))

        dz = zt - zr
        vu_u_l = bm_u.verts.new((xl * 0.88, y, zr + dz * 0.52))
        vu_u_m = bm_u.verts.new((xm * 0.88, y, zr + dz * 0.52))

        if has_th:
            vu_t_l = bm_u.verts.new(( th_w, y, zt))
            vu_t_m = bm_u.verts.new((-th_w, y, zt))
            vu_in_l = bm_u.verts.new(( th_w * 0.65, y, zt - 0.006))
            vu_in_m = bm_u.verts.new((-th_w * 0.65, y, zt - 0.006))
        elif t < 0.28:
            vu_t_l = bm_u.verts.new((xl * 0.68, y, zt))
            vu_t_m = bm_u.verts.new((xm * 0.68, y, zt))
            vu_in_l = bm_u.verts.new((xl * 0.44, y, zt - 0.010))
            vu_in_m = bm_u.verts.new((xm * 0.44, y, zt - 0.010))
        else:
            vu_t_l = bm_u.verts.new((xl * 0.38, y, zt + 0.001))
            vu_t_m = bm_u.verts.new((xm * 0.38, y, zt + 0.001))
            vu_in_l = None
            vu_in_m = None

        upper_cross_sections.append({
            'b': (vu_b_l, vu_b_m),
            'm': (vu_m_l, vu_m_m),
            'u': (vu_u_l, vu_u_m),
            't': (vu_t_l, vu_t_m),
            'in': (vu_in_l, vu_in_m),
            'has_th': has_th,
            'is_vamp': (t >= 0.68),
            't_val': t, 'y': y, 'zt': zt, 'xl': xl, 'xm': xm
        })

    bm_u.verts.ensure_lookup_table()

    for s in range(STATIONS - 1):
        u0 = upper_cross_sections[s]
        u1 = upper_cross_sections[s + 1]

        f_l0 = bm_u.faces.new((u0['b'][0], u0['m'][0], u1['m'][0], u1['b'][0]))
        f_l1 = bm_u.faces.new((u0['m'][0], u0['u'][0], u1['u'][0], u1['m'][0]))
        f_l2 = bm_u.faces.new((u0['u'][0], u0['t'][0], u1['t'][0], u1['u'][0]))
        for f in [f_l0, f_l1, f_l2]: f.material_index = 0

        f_m0 = bm_u.faces.new((u0['b'][1], u1['b'][1], u1['m'][1], u0['m'][1]))
        f_m1 = bm_u.faces.new((u0['m'][1], u1['m'][1], u1['u'][1], u0['u'][1]))
        f_m2 = bm_u.faces.new((u0['u'][1], u1['u'][1], u1['t'][1], u0['t'][1]))
        for f in [f_m0, f_m1, f_m2]: f.material_index = 0

        if (u0['is_vamp'] and u1['is_vamp']) or (u0['has_th'] and u1['is_vamp']):
            f_v = bm_u.faces.new((u0['t'][0], u0['t'][1], u1['t'][1], u1['t'][0]))
            f_v.material_index = 0

        if u0['in'][0] and u1['in'][0]:
            f_il = bm_u.faces.new((u0['t'][0], u1['t'][0], u1['in'][0], u0['in'][0]))
            f_im = bm_u.faces.new((u0['t'][1], u0['in'][1], u1['in'][1], u1['t'][1]))
            f_il.material_index = 1
            f_im.material_index = 1

    uh = upper_cross_sections[0]
    f_hc = bm_u.faces.new((uh['b'][0], uh['m'][0], uh['u'][0], uh['t'][0],
                           uh['t'][1], uh['u'][1], uh['m'][1], uh['b'][1]))
    f_hc.material_index = 0

    ut = upper_cross_sections[-1]
    y_apex = ut['y'] + 0.0065
    z_apex = ut['zt'] - 0.002
    v_apex_b = bm_u.verts.new((0.0, y_apex, stations[-1]['z_bed']))
    v_apex_m = bm_u.verts.new((0.0, y_apex + 0.001, stations[-1]['z_rim'] + 0.003))
    v_apex_t = bm_u.verts.new((0.0, y_apex, z_apex))

    bm_u.faces.new((ut['b'][0], ut['m'][0], v_apex_m, v_apex_b)).material_index = 0
    bm_u.faces.new((ut['b'][1], v_apex_b, v_apex_m, ut['m'][1])).material_index = 0
    bm_u.faces.new((ut['m'][0], ut['u'][0], v_apex_t, v_apex_m)).material_index = 0
    bm_u.faces.new((ut['m'][1], v_apex_m, v_apex_t, ut['u'][1])).material_index = 0
    bm_u.faces.new((ut['u'][0], ut['t'][0], ut['t'][1], ut['u'][1], v_apex_t)).material_index = 0

    vamp_perfs = [
        (0.000, 0.106, 0.033),
        (-0.009, 0.102, 0.033), (0.009, 0.102, 0.033),
        (-0.016, 0.096, 0.034), (0.000, 0.096, 0.035), (0.016, 0.096, 0.034),
        (-0.010, 0.090, 0.036), (0.010, 0.090, 0.036),
        (0.000, 0.084, 0.037)
    ]
    for px, py, pz in vamp_perfs:
        pw = 0.0015
        p0 = bm_u.verts.new((px - pw, py - pw, pz - 0.0005))
        p1 = bm_u.verts.new((px + pw, py - pw, pz - 0.0005))
        p2 = bm_u.verts.new((px + pw, py + pw, pz - 0.0005))
        p3 = bm_u.verts.new((px - pw, py + pw, pz - 0.0005))
        f_perf = bm_u.faces.new((p0, p1, p2, p3))
        f_perf.material_index = 1

    bm_u.to_mesh(upper_mesh)
    bm_u.free()
    sub_u = upper_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_u.levels = 1
    for p in upper_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # PART 3: STANDALONE DESIGN LAYERS (Physical Relief Overlays)
    # =============================================================
    design_mesh = bpy.data.meshes.new("Design_Layers_Mesh")
    design_obj = bpy.data.objects.new("Sneaker_Design_Layers", design_mesh)
    bpy.context.collection.objects.link(design_obj)
    design_obj.data.materials.append(mats['suede'])  # 0: Rich tactile suede
    design_obj.data.materials.append(mats['silver']) # 1: Polished mirror chrome

    bm_d = bmesh.new()

    # (A) Suede Quarter Panels (Stations 8 to 22)
    q_left = []
    q_right = []
    q_range = range(8, 23)
    for s in q_range:
        d = stations[s]
        y = d['y']
        zr = d['z_rim']
        zt = d['z_top']
        dz = zt - zr
        off = 0.0016

        xl = d['xl'] * 0.945 + off
        xm = d['xm'] * 0.945 - off

        ql_b = bm_d.verts.new((xl * 0.99, y, zr + 0.0008))
        ql_m = bm_d.verts.new((xl * 0.94, y, zr + dz * 0.48))
        ql_t = bm_d.verts.new((xl * 0.85, y, zr + dz * 0.88))

        qm_b = bm_d.verts.new((xm * 0.99, y, zr + 0.0008))
        qm_m = bm_d.verts.new((xm * 0.94, y, zr + dz * 0.48))
        qm_t = bm_d.verts.new((xm * 0.85, y, zr + dz * 0.88))

        q_left.append((ql_b, ql_m, ql_t))
        q_right.append((qm_b, qm_m, qm_t))

    bm_d.verts.ensure_lookup_table()
    for i in range(len(q_range) - 1):
        l0 = q_left[i]
        l1 = q_left[i + 1]
        bm_d.faces.new((l0[0], l0[1], l1[1], l1[0])).material_index = 0
        bm_d.faces.new((l0[1], l0[2], l1[2], l1[1])).material_index = 0

        r0 = q_right[i]
        r1 = q_right[i + 1]
        bm_d.faces.new((r0[0], r1[0], r1[1], r0[1])).material_index = 0
        bm_d.faces.new((r0[1], r1[1], r1[2], r0[2])).material_index = 0

    # (B) Suede Mudguard Toe Cap Wrap (Stations 22 to 35)
    mg_left = []
    mg_right = []
    mg_range = range(22, STATIONS)
    for s in mg_range:
        d = stations[s]
        y = d['y']
        zr = d['z_rim']
        zt = d['z_top']
        dz = zt - zr
        off = 0.0016

        xl = d['xl'] * 0.945 + off
        xm = d['xm'] * 0.945 - off

        ml_b = bm_d.verts.new((xl * 0.99, y, zr + 0.0008))
        ml_t = bm_d.verts.new((xl * 0.88, y, zr + dz * 0.40))

        mr_b = bm_d.verts.new((xm * 0.99, y, zr + 0.0008))
        mr_t = bm_d.verts.new((xm * 0.88, y, zr + dz * 0.40))

        mg_left.append((ml_b, ml_t))
        mg_right.append((mr_b, mr_t))

    bm_d.verts.ensure_lookup_table()
    for i in range(len(mg_range) - 1):
        l0 = mg_left[i]
        l1 = mg_left[i + 1]
        bm_d.faces.new((l0[0], l0[1], l1[1], l1[0])).material_index = 0

        r0 = mg_right[i]
        r1 = mg_right[i + 1]
        bm_d.faces.new((r0[0], r1[0], r1[1], r0[1])).material_index = 0

    d_tip = stations[-1]
    y_tip = d_tip['y'] + 0.007
    z_tip = d_tip['z_rim'] + 0.008
    vt_b = bm_d.verts.new((0.0, y_tip, d_tip['z_rim'] + 0.0008))
    vt_t = bm_d.verts.new((0.0, y_tip, z_tip))
    bm_d.faces.new((mg_left[-1][0], mg_left[-1][1], vt_t, vt_b)).material_index = 0
    bm_d.faces.new((mg_right[-1][0], vt_b, vt_t, mg_right[-1][1])).material_index = 0

    # (C) Suede Heel Counter Wrap (Stations 0 to 8)
    hc_left = []
    hc_right = []
    for s in range(9):
        d = stations[s]
        y = d['y']
        zr = d['z_rim']
        zt = d['z_top']
        dz = zt - zr
        off = 0.0015
        xl = d['xl'] * 0.945 + off
        xm = d['xm'] * 0.945 - off

        hl_b = bm_d.verts.new((xl * 0.99, y, zr + 0.0008))
        hl_t = bm_d.verts.new((xl * 0.84, y, zr + dz * 0.60))
        hr_b = bm_d.verts.new((xm * 0.99, y, zr + 0.0008))
        hr_t = bm_d.verts.new((xm * 0.84, y, zr + dz * 0.60))

        hc_left.append((hl_b, hl_t))
        hc_right.append((hr_b, hr_t))

    bm_d.verts.ensure_lookup_table()
    for i in range(8):
        l0 = hc_left[i]
        l1 = hc_left[i + 1]
        bm_d.faces.new((l0[0], l0[1], l1[1], l1[0])).material_index = 0

        r0 = hc_right[i]
        r1 = hc_right[i + 1]
        bm_d.faces.new((r0[0], r1[0], r1[1], r0[1])).material_index = 0

    bm_d.faces.new((hc_left[0][0], hc_left[0][1], hc_right[0][1], hc_right[0][0])).material_index = 0

    # (D) 3D Gleaming Chrome Wave Badge
    for side in [1.0, -1.0]:
        w_in_b = []
        w_in_t = []
        w_out_b = []
        w_out_t = []

        wave_stations = range(10, 22)
        for idx, s in enumerate(wave_stations):
            u = idx / (len(wave_stations) - 1)
            d = stations[s]
            zr = d['z_rim']
            zt = d['z_top']
            dz = zt - zr
            y = d['y']

            wave_h = 0.38 + 0.32 * math.sin(u * math.pi * 1.5)
            z_w = zr + dz * wave_h
            thick_h = 0.006 + 0.005 * math.sin(u * math.pi)

            base_x = (d['xl'] * 0.945 if side > 0 else d['xm'] * 0.945) + side * 0.0016
            x_in = base_x - side * 0.0004
            x_out = base_x + side * 0.0022

            w_in_b.append(bm_d.verts.new((x_in, y, z_w)))
            w_in_t.append(bm_d.verts.new((x_in, y, z_w + thick_h)))
            w_out_b.append(bm_d.verts.new((x_out, y, z_w)))
            w_out_t.append(bm_d.verts.new((x_out, y, z_w + thick_h)))

        bm_d.verts.ensure_lookup_table()
        for k in range(len(wave_stations) - 1):
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
    # PART 4: STANDALONE TONGUE OBJECT (Puffy Skate Tongue & Badge)
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
    # PART 5: STANDALONE LACES & EYELETS OBJECT
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
            r_o = []
            r_i = []
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
    # PART 6: STANDALONE BRUTALIST CONCRETE PEDESTAL
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
    r_top = []
    r_bot = []
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
    print(f"[OK] Exported Masterpiece Modular Sneaker: {out_glb_path}")

if __name__ == "__main__":
    out_dir = r"public/models"
    os.makedirs(out_dir, exist_ok=True)
    out_glb = os.path.join(out_dir, "test_modular_sneaker.glb")
    create_masterpiece_modular_sneaker(out_glb)
