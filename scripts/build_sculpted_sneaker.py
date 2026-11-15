import bpy
import bmesh
import math
import os

def create_sculpted_sneaker(out_glb_path, color_profile=None):
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

    # -------------------------------------------------------------
    # Materials
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
    bmp_s.inputs['Strength'].default_value = 0.07
    bmp_s.inputs['Distance'].default_value = 0.001
    s_links.new(tex_s.outputs['Fac'], bmp_s.inputs['Height'])
    s_links.new(bmp_s.outputs['Normal'], s_bsdf.inputs['Normal'])

    mat_upper, u_nodes, u_links, u_bsdf = create_mat("Mat_Upper_Leather", cp['vamp'], cp['vamp_roughness'])
    tex_u = u_nodes.new('ShaderNodeTexVoronoi')
    tex_u.inputs['Scale'].default_value = 450.0
    bmp_u = u_nodes.new('ShaderNodeBump')
    bmp_u.inputs['Strength'].default_value = 0.04
    bmp_u.inputs['Distance'].default_value = 0.001
    u_links.new(tex_u.outputs['Distance'], bmp_u.inputs['Height'])
    u_links.new(bmp_u.outputs['Normal'], u_bsdf.inputs['Normal'])

    mat_suede, d_nodes, d_links, d_bsdf = create_mat("Mat_Suede_Overlay", cp['quarter'], cp['quarter_roughness'])
    tex_d = d_nodes.new('ShaderNodeTexNoise')
    tex_d.inputs['Scale'].default_value = 500.0
    bmp_d = d_nodes.new('ShaderNodeBump')
    bmp_d.inputs['Strength'].default_value = 0.12
    bmp_d.inputs['Distance'].default_value = 0.0015
    d_links.new(tex_d.outputs['Fac'], bmp_d.inputs['Height'])
    d_links.new(bmp_d.outputs['Normal'], d_bsdf.inputs['Normal'])

    mat_silver, _, _, _ = create_mat("Mat_Chrome_Wave", cp['silver'], cp['silver_roughness'], cp['silver_metal'])

    mat_lace, l_nodes, l_links, l_bsdf = create_mat("Mat_Laces", cp['lace'], cp['lace_roughness'])
    tex_l = l_nodes.new('ShaderNodeTexWave')
    tex_l.inputs['Scale'].default_value = 240.0
    bmp_l = l_nodes.new('ShaderNodeBump')
    bmp_l.inputs['Strength'].default_value = 0.14
    bmp_l.inputs['Distance'].default_value = 0.001
    l_links.new(tex_l.outputs['Fac'], bmp_l.inputs['Height'])
    l_links.new(bmp_l.outputs['Normal'], l_bsdf.inputs['Normal'])

    mat_inner, _, _, _ = create_mat("Mat_Inner_Collar", cp['inner'], cp['inner_roughness'])
    mat_eyelet, _, _, _ = create_mat("Mat_Eyelets", cp['eyelet'], 0.20, cp['eyelet_metal'])
    mat_ped, p_nodes, p_links, p_bsdf = create_mat("Mat_Pedestal", cp['pedestal'], cp['pedestal_roughness'])
    tex_p = p_nodes.new('ShaderNodeTexNoise')
    tex_p.inputs['Scale'].default_value = 150.0
    bmp_p = p_nodes.new('ShaderNodeBump')
    bmp_p.inputs['Strength'].default_value = 0.15
    bmp_p.inputs['Distance'].default_value = 0.002
    p_links.new(tex_p.outputs['Fac'], bmp_p.inputs['Height'])
    p_links.new(bmp_p.outputs['Normal'], p_bsdf.inputs['Normal'])

    mats = {
        'sole': mat_sole,
        'upper': mat_upper,
        'suede': mat_suede,
        'silver': mat_silver,
        'lace': mat_lace,
        'inner': mat_inner,
        'eyelet': mat_eyelet,
        'pedestal': mat_ped
    }

    # -------------------------------------------------------------
    # SNEAKER FOOT LAST DEFINITION
    # RINGS = 24 along length (-0.125m heel to +0.145m toe)
    # SEGS = 16 around cross-section
    # -------------------------------------------------------------
    RINGS = 24
    SEGS = 16

    y_coords = []
    for i in range(RINGS):
        u = i / (RINGS - 1)
        # Cosine distribution gives density at heel and toe
        y = -0.125 + 0.270 * (0.5 - 0.5 * math.cos(u * math.pi))
        y_coords.append(y)

    def calc_last_station(y):
        t = (y + 0.125) / 0.270
        t = max(0.0, min(1.0, t))

        # Sole bottom height with 12mm toe spring
        if t > 0.60:
            frac = (t - 0.60) / 0.40
            z_bot = 0.012 * (frac ** 1.9)
        elif t < 0.08:
            z_bot = 0.0018 * (1.0 - t / 0.08)
        else:
            z_bot = 0.000

        # Sole rim height: 17mm heel, 13mm toe
        sole_h = 0.017 - 0.004 * t
        z_rim = z_bot + sole_h

        # Widths: rounded heel, medial arch tuck, ball of foot, skate toe
        r_heel = math.sqrt(max(0.01, 1.0 - ((0.12 - t) / 0.12) ** 2)) if t < 0.12 else 1.0
        r_toe  = math.sqrt(max(0.01, 1.0 - ((t - 0.76) / 0.24) ** 2)) if t > 0.76 else 1.0

        if t < 0.25:
            xm = -0.035 * r_heel
            xl =  0.036 * r_heel
        elif t < 0.52:
            f = (t - 0.25) / 0.27
            xm = -(0.035 - 0.006 * math.sin(f * math.pi))
            xl =  (0.036 + 0.001 * math.sin(f * math.pi))
        elif t < 0.82:
            f = (t - 0.52) / 0.30
            xm = -(0.031 + 0.011 * math.sin(f * math.pi * 0.9))
            xl =  (0.037 + 0.010 * math.sin(f * math.pi * 0.9))
        else:
            xm = -0.042 * r_toe
            xl =  0.044 * r_toe

        # Heights
        if t < 0.20: # Heel collar & Achilles notch
            f = t / 0.20
            z_top = z_rim + 0.052 - 0.008 * f
        elif t < 0.44: # Collar dip / opening
            f = (t - 0.20) / 0.24
            z_top = z_rim + 0.044 - 0.010 * math.sin(f * math.pi * 0.5)
        elif t < 0.70: # Eyestay lace throat
            f = (t - 0.44) / 0.26
            z_top = z_rim + 0.034 - 0.007 * f
        else: # Toe vamp dome
            f = (t - 0.70) / 0.30
            z_top = z_rim + 0.027 * math.cos(f * math.pi * 0.48)

        return t, z_bot, z_rim, z_top, xm, xl

    # =============================================================
    # 1. STANDALONE SOLE OBJECT (Crisp Rubber Cupsole)
    # Built from the exact footprint perimeter of the last!
    # =============================================================
    sole_mesh = bpy.data.meshes.new("Sole_Mesh")
    sole_obj = bpy.data.objects.new("Sneaker_Sole", sole_mesh)
    bpy.context.collection.objects.link(sole_obj)
    sole_obj.data.materials.append(mat_sole)

    bm_s = bmesh.new()

    sole_rings = []
    for i, y in enumerate(y_coords):
        t, z_bot, z_rim, z_top, xm, xl = calc_last_station(y)
        # Expand slightly by 1.025 for cupsole outer sidewall
        xl_s = xl * 1.025
        xm_s = xm * 1.025

        # 4 vertices per station:
        # 1. Bottom floor
        # 2. Mid foxing stripe
        # 3. Outer rim top ledge
        # 4. Inner rim shelf
        vb_l = bm_s.verts.new((xl_s, y, z_bot))
        vb_c = bm_s.verts.new((0.0,  y, z_bot))
        vb_m = bm_s.verts.new((xm_s, y, z_bot))

        zm = z_bot + (z_rim - z_bot) * 0.58
        vm_l = bm_s.verts.new((xl_s * 1.008, y, zm))
        vm_m = bm_s.verts.new((xm_s * 1.008, y, zm))

        vro_l = bm_s.verts.new((xl_s * 0.995, y, z_rim))
        vro_m = bm_s.verts.new((xm_s * 0.995, y, z_rim))

        vri_l = bm_s.verts.new((xl_s * 0.940, y, z_rim))
        vri_m = bm_s.verts.new((xm_s * 0.940, y, z_rim))

        vf_l = bm_s.verts.new((xl_s * 0.935, y, z_rim - 0.0035))
        vf_c = bm_s.verts.new((0.0,          y, z_rim - 0.0035))
        vf_m = bm_s.verts.new((xm_s * 0.935, y, z_rim - 0.0035))

        sole_rings.append({
            'b': (vb_l, vb_c, vb_m),
            'm': (vm_l, vm_m),
            'ro': (vro_l, vro_m),
            'ri': (vri_l, vri_m),
            'f': (vf_l, vf_c, vf_m)
        })

    bm_s.verts.ensure_lookup_table()

    for i in range(RINGS - 1):
        s0 = sole_rings[i]
        s1 = sole_rings[i + 1]

        # Floor quads
        bm_s.faces.new((s0['b'][0], s1['b'][0], s1['b'][1], s0['b'][1]))
        bm_s.faces.new((s0['b'][1], s1['b'][1], s1['b'][2], s0['b'][2]))

        # Lateral sidewalls
        bm_s.faces.new((s0['b'][0], s0['m'][0], s1['m'][0], s1['b'][0]))
        bm_s.faces.new((s0['m'][0], s0['ro'][0], s1['ro'][0], s1['m'][0]))

        # Medial sidewalls
        bm_s.faces.new((s0['b'][2], s1['b'][2], s1['m'][1], s0['m'][1]))
        bm_s.faces.new((s0['m'][1], s1['m'][1], s1['ro'][1], s0['ro'][1]))

        # Top foxing rim shelf
        bm_s.faces.new((s0['ro'][0], s0['ri'][0], s1['ri'][0], s1['ro'][0]))
        bm_s.faces.new((s0['ro'][1], s1['ro'][1], s1['ri'][1], s0['ri'][1]))

        # Cavity inner drop wall
        bm_s.faces.new((s0['ri'][0], s0['f'][0], s1['f'][0], s1['ri'][0]))
        bm_s.faces.new((s0['ri'][1], s1['ri'][1], s1['f'][2], s0['f'][2]))

        # Footbed floor
        bm_s.faces.new((s0['f'][0], s1['f'][0], s1['f'][1], s0['f'][1]))
        bm_s.faces.new((s0['f'][1], s1['f'][1], s1['f'][2], s0['f'][2]))

    # Rounded heel cup closure (spherical fan)
    sh = sole_rings[0]
    c_heel_b = bm_s.verts.new((0.0, y_coords[0] - 0.006, 0.001))
    c_heel_m = bm_s.verts.new((0.0, y_coords[0] - 0.007, 0.010))
    c_heel_ro = bm_s.verts.new((0.0, y_coords[0] - 0.006, 0.017))
    c_heel_ri = bm_s.verts.new((0.0, y_coords[0] - 0.004, 0.017))
    c_heel_f = bm_s.verts.new((0.0, y_coords[0] - 0.003, 0.0135))

    bm_s.faces.new((sh['b'][0], sh['b'][1], c_heel_b))
    bm_s.faces.new((sh['b'][1], sh['b'][2], c_heel_b))
    bm_s.faces.new((sh['b'][0], c_heel_b, c_heel_m, sh['m'][0]))
    bm_s.faces.new((sh['b'][2], sh['m'][1], c_heel_m, c_heel_b))
    bm_s.faces.new((sh['m'][0], c_heel_m, c_heel_ro, sh['ro'][0]))
    bm_s.faces.new((sh['m'][1], sh['ro'][1], c_heel_ro, c_heel_m))
    bm_s.faces.new((sh['ro'][0], c_heel_ro, c_heel_ri, sh['ri'][0]))
    bm_s.faces.new((sh['ro'][1], sh['ri'][1], c_heel_ri, c_heel_ro))
    bm_s.faces.new((sh['ri'][0], c_heel_ri, c_heel_f, sh['f'][0]))
    bm_s.faces.new((sh['ri'][1], sh['f'][2], c_heel_f, c_heel_ri))
    bm_s.faces.new((sh['f'][0], c_heel_f, sh['f'][1]))
    bm_s.faces.new((sh['f'][2], sh['f'][1], c_heel_f))

    # Rounded toe bumper closure (spherical fan)
    st = sole_rings[-1]
    c_toe_b = bm_s.verts.new((0.0, y_coords[-1] + 0.006, 0.014))
    c_toe_m = bm_s.verts.new((0.0, y_coords[-1] + 0.007, 0.018))
    c_toe_ro = bm_s.verts.new((0.0, y_coords[-1] + 0.006, 0.024))
    c_toe_ri = bm_s.verts.new((0.0, y_coords[-1] + 0.004, 0.024))
    c_toe_f = bm_s.verts.new((0.0, y_coords[-1] + 0.003, 0.0205))

    bm_s.faces.new((st['b'][0], st['b'][1], c_toe_b))
    bm_s.faces.new((st['b'][1], st['b'][2], c_toe_b))
    bm_s.faces.new((st['b'][0], c_toe_b, c_toe_m, st['m'][0]))
    bm_s.faces.new((st['b'][2], st['m'][1], c_toe_m, c_toe_b))
    bm_s.faces.new((st['m'][0], c_toe_m, c_toe_ro, st['ro'][0]))
    bm_s.faces.new((st['m'][1], st['ro'][1], c_toe_ro, c_toe_m))
    bm_s.faces.new((st['ro'][0], c_toe_ro, c_toe_ri, st['ri'][0]))
    bm_s.faces.new((st['ro'][1], st['ri'][1], c_toe_ri, c_toe_ro))
    bm_s.faces.new((st['ri'][0], c_toe_ri, c_toe_f, st['f'][0]))
    bm_s.faces.new((st['ri'][1], st['f'][2], c_toe_f, c_toe_ri))
    bm_s.faces.new((st['f'][0], c_toe_f, st['f'][1]))
    bm_s.faces.new((st['f'][2], st['f'][1], c_toe_f))

    bm_s.to_mesh(sole_mesh)
    bm_s.free()
    for p in sole_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 2. STANDALONE UPPER (The Foot Last Leather Base)
    # Closed, anatomical foot volume with padded collar & perforated vamp
    # =============================================================
    upper_mesh = bpy.data.meshes.new("Upper_Mesh")
    upper_obj = bpy.data.objects.new("Sneaker_Upper", upper_mesh)
    bpy.context.collection.objects.link(upper_obj)
    upper_obj.data.materials.append(mats['upper'])
    upper_obj.data.materials.append(mats['inner'])

    bm_u = bmesh.new()
    up_rings = []

    for i, y in enumerate(y_coords):
        t, z_bot, z_rim, z_top, xm, xl = calc_last_station(y)

        # 16 vertices per radial ring
        cur_ring = []
        for k in range(SEGS):
            theta = k * (2.0 * math.pi / SEGS)
            sin_th = math.sin(theta)
            cos_th = math.cos(theta)

            vx = xl * sin_th if sin_th >= 0 else (-xm * sin_th)

            if cos_th >= 0:
                h_frac = cos_th ** 1.3
                vz = z_rim + (z_top - z_rim) * h_frac
            else:
                b_frac = (-cos_th) ** 1.4
                vz = z_rim - (z_rim - z_bot) * b_frac

            cur_ring.append(bm_u.verts.new((vx, y, vz)))
        up_rings.append(cur_ring)

    bm_u.verts.ensure_lookup_table()

    for i in range(RINGS - 1):
        r0 = up_rings[i]
        r1 = up_rings[i + 1]
        for k in range(SEGS):
            knxt = (k + 1) % SEGS
            bm_u.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0

    # Spherical heel cap
    c_heel_u = bm_u.verts.new((0.0, y_coords[0] - 0.005, 0.035))
    r_hu = up_rings[0]
    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm_u.faces.new((c_heel_u, r_hu[knxt], r_hu[k])).material_index = 0

    # Spherical toe dome cap
    c_toe_u = bm_u.verts.new((0.0, y_coords[-1] + 0.005, 0.022))
    r_tu = up_rings[-1]
    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm_u.faces.new((c_toe_u, r_tu[k], r_tu[knxt])).material_index = 0

    # Vamp micro-perforations (subtle dark punch holes)
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
        bm_u.faces.new((p0, p1, p2, p3)).material_index = 1

    bm_u.to_mesh(upper_mesh)
    bm_u.free()
    sub_u = upper_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_u.levels = 1
    for p in upper_mesh.polygons:
        p.use_smooth = True

    # =============================================================
    # 3. STANDALONE DESIGN LAYERS (Physical Suede Overlays & 3D Wave)
    # Modeled as proud surfaces +1.5mm over the upper with Solidify & Bevel
    # =============================================================
    design_mesh = bpy.data.meshes.new("Design_Layers_Mesh")
    design_obj = bpy.data.objects.new("Sneaker_Design_Layers", design_mesh)
    bpy.context.collection.objects.link(design_obj)
    design_obj.data.materials.append(mats['suede'])  # 0: Suede
    design_obj.data.materials.append(mats['silver']) # 1: Chrome Silver Wave

    bm_d = bmesh.new()

    # (A) Suede Mudguard (Toe Cap Overlay, rings 16 to 23)
    # Extracted around the toe perimeter with physical offset
    mg_rings = []
    for i in range(16, RINGS):
        y = y_coords[i]
        t, z_bot, z_rim, z_top, xm, xl = calc_last_station(y)
        off = 0.0018 # 1.8mm proud

        # Mudguard covers the lower and mid sides around the toe (k in [2, 3, 4, 12, 13, 14])
        mg_v = []
        for k in range(SEGS):
            theta = k * (2.0 * math.pi / SEGS)
            sin_th = math.sin(theta)
            cos_th = math.cos(theta)
            vx = (xl + off) * sin_th if sin_th >= 0 else ((-xm + off) * sin_th)

            if cos_th >= 0:
                h_frac = cos_th ** 1.3
                vz = z_rim + (z_top - z_rim) * h_frac
            else:
                b_frac = (-cos_th) ** 1.4
                vz = z_rim - (z_rim - z_bot) * b_frac

            mg_v.append(bm_d.verts.new((vx, y, vz)))
        mg_rings.append(mg_v)

    bm_d.verts.ensure_lookup_table()
    for i in range(len(mg_rings) - 1):
        r0 = mg_rings[i]
        r1 = mg_rings[i + 1]
        # Only create faces for the mudguard band (k = 2 to 5 and k = 11 to 14)
        for k in [2, 3, 4, 11, 12, 13]:
            knxt = (k + 1) % SEGS
            bm_d.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0

    # (B) Suede Quarter Panels (rings 6 to 17)
    qp_rings = []
    for i in range(6, 18):
        y = y_coords[i]
        t, z_bot, z_rim, z_top, xm, xl = calc_last_station(y)
        off = 0.0016

        qp_v = []
        for k in range(SEGS):
            theta = k * (2.0 * math.pi / SEGS)
            sin_th = math.sin(theta)
            cos_th = math.cos(theta)
            vx = (xl + off) * sin_th if sin_th >= 0 else ((-xm + off) * sin_th)

            if cos_th >= 0:
                h_frac = cos_th ** 1.3
                vz = z_rim + (z_top - z_rim) * h_frac
            else:
                b_frac = (-cos_th) ** 1.4
                vz = z_rim - (z_rim - z_bot) * b_frac

            qp_v.append(bm_d.verts.new((vx, y, vz)))
        qp_rings.append(qp_v)

    bm_d.verts.ensure_lookup_table()
    for i in range(len(qp_rings) - 1):
        r0 = qp_rings[i]
        r1 = qp_rings[i + 1]
        # Lateral quarter (k = 1 to 4)
        for k in [1, 2, 3]:
            knxt = (k + 1) % SEGS
            bm_d.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0
        # Medial quarter (k = 12 to 15)
        for k in [12, 13, 14]:
            knxt = (k + 1) % SEGS
            bm_d.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0

    # (C) Suede Heel Counter (rings 0 to 7)
    hc_rings = []
    for i in range(8):
        y = y_coords[i]
        t, z_bot, z_rim, z_top, xm, xl = calc_last_station(y)
        off = 0.0017

        hc_v = []
        for k in range(SEGS):
            theta = k * (2.0 * math.pi / SEGS)
            sin_th = math.sin(theta)
            cos_th = math.cos(theta)
            vx = (xl + off) * sin_th if sin_th >= 0 else ((-xm + off) * sin_th)

            if cos_th >= 0:
                h_frac = cos_th ** 1.3
                vz = z_rim + (z_top - z_rim) * h_frac
            else:
                b_frac = (-cos_th) ** 1.4
                vz = z_rim - (z_rim - z_bot) * b_frac

            hc_v.append(bm_d.verts.new((vx, y, vz)))
        hc_rings.append(hc_v)

    bm_d.verts.ensure_lookup_table()
    for i in range(len(hc_rings) - 1):
        r0 = hc_rings[i]
        r1 = hc_rings[i + 1]
        # Rear wrap (k in [1, 2, 3, 4, 12, 13, 14, 15])
        for k in [1, 2, 3, 12, 13, 14, 15]:
            knxt = (k + 1) % SEGS
            bm_d.faces.new((r0[k], r0[knxt], r1[knxt], r1[k])).material_index = 0

    # Spherical heel counter cap
    c_hc = bm_d.verts.new((0.0, y_coords[0] - 0.0068, 0.035))
    r_hc0 = hc_rings[0]
    for k in [1, 2, 3, 12, 13, 14, 15]:
        knxt = (k + 1) % SEGS
        bm_d.faces.new((c_hc, r_hc0[knxt], r_hc0[k])).material_index = 0

    # (D) 3D Gleaming Chrome Wave Badge on Lateral & Medial Sides
    for side in [1.0, -1.0]:
        w_in_b, w_in_t, w_out_b, w_out_t = [], [], [], []
        wave_rings = range(8, 17)
        for idx, s in enumerate(wave_rings):
            u = idx / (len(wave_rings) - 1)
            y = y_coords[s]
            t, z_bot, z_rim, z_top, xm, xl = calc_last_station(y)
            dz = z_top - z_rim

            wave_h = 0.38 + 0.30 * math.sin(u * math.pi * 1.5)
            z_w = z_rim + dz * wave_h
            thick_h = 0.006 + 0.005 * math.sin(u * math.pi)

            base_x = (xl + 0.0016) if side > 0 else (-xm - 0.0016)
            x_in  = base_x - side * 0.0003
            x_out = base_x + side * 0.0024

            w_in_b.append(bm_d.verts.new((x_in, y, z_w)))
            w_in_t.append(bm_d.verts.new((x_in, y, z_w + thick_h)))
            w_out_b.append(bm_d.verts.new((x_out, y, z_w)))
            w_out_t.append(bm_d.verts.new((x_out, y, z_w + thick_h)))

        bm_d.verts.ensure_lookup_table()
        for k in range(len(wave_rings) - 1):
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
        ty = 0.054 - u * 0.078
        tz = 0.033 + u * 0.042 + 0.003 * math.sin(u * math.pi)
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
    lbl_z = 0.073
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
    print(f"[OK] Exported Sculpted Sneaker: {out_glb_path}")

if __name__ == "__main__":
    out_dir = r"public/models"
    os.makedirs(out_dir, exist_ok=True)
    out_glb = os.path.join(out_dir, "test_sculpted_sneaker.glb")
    create_sculpted_sneaker(out_glb)
