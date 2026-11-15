import bpy
import bmesh
import math
import os
import sys

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

    mat_sole, _, _, _ = create_mat("Mat_Sole", cp['sole'], cp.get('sole_roughness', 0.52))
    mat_upper, _, _, _ = create_mat("Mat_Upper_Leather", cp['vamp'], cp.get('vamp_roughness', 0.36))
    mat_suede, _, _, _ = create_mat("Mat_Suede_Overlay", cp['quarter'], cp.get('quarter_roughness', 0.94))
    mat_silver, _, _, _ = create_mat("Mat_Chrome_Wave", cp['silver'], 0.12, 0.96)
    mat_lace, _, _, _ = create_mat("Mat_Laces", cp['lace'], 0.68)
    mat_inner, _, _, _ = create_mat("Mat_Inner_Collar", cp['inner'], 0.96)
    mat_eyelet, _, _, _ = create_mat("Mat_Eyelets", cp['eyelet'], 0.20, 0.94)
    mat_ped, _, _, _ = create_mat("Mat_Pedestal", cp['pedestal'], 0.88)

    materials['sole'] = mat_sole
    materials['upper'] = mat_upper
    materials['suede'] = mat_suede
    materials['silver'] = mat_silver
    materials['lace'] = mat_lace
    materials['inner'] = mat_inner
    materials['eyelet'] = mat_eyelet
    materials['pedestal'] = mat_ped
    return materials

def test_render_last(out_glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cp = {
        'sole': (0.74, 0.48, 0.25, 1.0),
        'vamp': (0.92, 0.90, 0.86, 1.0),
        'quarter': (0.08, 0.045, 0.025, 1.0),
        'silver': (0.92, 0.94, 0.98, 1.0),
        'lace': (0.98, 0.98, 0.98, 1.0),
        'inner': (0.05, 0.05, 0.06, 1.0),
        'eyelet': (0.85, 0.87, 0.90, 1.0),
        'pedestal': (0.28, 0.28, 0.30, 1.0),
    }
    mats = build_sneaker_pbr_materials(cp)
    
    RINGS = 24
    SEGS = 16
    
    # 1. UPPER MESH
    up_mesh = bpy.data.meshes.new("Upper_Mesh")
    up_obj = bpy.data.objects.new("Sneaker_Upper", up_mesh)
    bpy.context.collection.objects.link(up_obj)
    up_obj.data.materials.append(mats['upper'])
    
    bm_u = bmesh.new()
    ring_verts = []
    
    for i in range(RINGS):
        u = i / (RINGS - 1)
        # Cosine distribution gives density at heel and toe
        y = -0.125 + 0.270 * (0.5 - 0.5 * math.cos(u * math.pi))
        t = (y + 0.125) / 0.270
        t = max(0.0, min(1.0, t))
        
        # 12mm toe spring
        if t > 0.60:
            frac = (t - 0.60) / 0.40
            z_bot = 0.012 * (frac ** 1.9)
        elif t < 0.08:
            z_bot = 0.0018 * (1.0 - t / 0.08)
        else:
            z_bot = 0.000
            
        sole_h = 0.0165 - 0.0035 * t
        z_rim = z_bot + sole_h
        
        r_heel = math.sqrt(max(0.01, 1.0 - ((0.12 - t) / 0.12) ** 2)) if t < 0.12 else 1.0
        r_toe = math.sqrt(max(0.01, 1.0 - ((t - 0.76) / 0.24) ** 2)) if t > 0.76 else 1.0
        
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
            
        if t < 0.20:
            f = t / 0.20
            z_top = z_rim + 0.052 - 0.008 * f
        elif t < 0.44:
            f = (t - 0.20) / 0.24
            z_top = z_rim + 0.044 - 0.010 * math.sin(f * math.pi * 0.5)
        elif t < 0.70:
            f = (t - 0.44) / 0.26
            z_top = z_rim + 0.034 - 0.007 * f
        else:
            f = (t - 0.70) / 0.30
            z_top = z_rim + 0.027 * math.cos(f * math.pi * 0.48)
            
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
        ring_verts.append(cur_ring)
        
    bm_u.verts.ensure_lookup_table()
    
    for i in range(RINGS - 1):
        r0 = ring_verts[i]
        r1 = ring_verts[i + 1]
        for k in range(SEGS):
            knxt = (k + 1) % SEGS
            bm_u.faces.new((r0[k], r0[knxt], r1[knxt], r1[k]))
            
    # Rear heel sphere cap
    c_heel = bm_u.verts.new((0.0, -0.125 - 0.006, 0.035))
    r_h = ring_verts[0]
    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm_u.faces.new((c_heel, r_h[knxt], r_h[k]))
        
    # Front toe dome cap
    c_toe = bm_u.verts.new((0.0, 0.145 + 0.006, 0.022))
    r_t = ring_verts[-1]
    for k in range(SEGS):
        knxt = (k + 1) % SEGS
        bm_u.faces.new((c_toe, r_t[k], r_t[knxt]))
        
    bm_u.to_mesh(up_mesh)
    bm_u.free()
    
    sub_u = up_obj.modifiers.new("Subsurf", type='SUBSURF')
    sub_u.levels = 1
    for p in up_mesh.polygons:
        p.use_smooth = True
        
    # 2. Rotate 180 deg around Z
    up_obj.rotation_euler[2] += math.pi
    bpy.context.view_layer.objects.active = up_obj
    up_obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    bpy.ops.export_scene.gltf(filepath=out_glb_path, export_format='GLB')
    print(f"[OK] Exported test last: {out_glb_path}")

if __name__ == "__main__":
    out_glb = r"public/models/test_modular_sneaker.glb"
    test_render_last(out_glb)
