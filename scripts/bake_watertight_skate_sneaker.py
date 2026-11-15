import bpy
import bmesh
import math
import os
import shutil

def build_watertight_skate_sneaker(texture_path, out_glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Sneaker_Mesh")
    sneaker = bpy.data.objects.new("Sneaker_Model", mesh)
    bpy.context.collection.objects.link(sneaker)
    bpy.context.view_layer.objects.active = sneaker
    
    bm = bmesh.new()
    
    # -----------------------------------------------------------------
    # 1. VULCANIZED RUBBER CUPSOLE & FOXING TAPE
    # Toe is at +Y, Heel is at -Y, Top is +Z, Lateral is +X, Medial is -X
    # -----------------------------------------------------------------
    sole_curve = [
        # (t, x_half_w, y_cen)
        (0.00, 0.075, -0.25), # Heel back
        (0.15, 0.085, -0.20), # Heel cup
        (0.35, 0.072, -0.08), # Arch waist
        (0.60, 0.105,  0.08), # Ball of foot
        (0.85, 0.095,  0.22), # Toe box base
        (1.00, 0.055,  0.28), # Toe tip
    ]
    
    # Rings for the sole: 0 (tread bottom), 1 (midsole foxing bottom), 2 (foxing tape top)
    sole_levels = [
        (-0.06, 1.02), # Level 0: Bottom rubber tread
        (-0.01, 1.00), # Level 1: Foxing tape line
        ( 0.04, 0.98), # Level 2: Top of midsole / upper seam
    ]
    
    SEGS = 20
    sole_rings = []
    for sz, s_scale in sole_levels:
        ring = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            
            # Map angle to foot curve parameter t
            t = 0.5 + 0.5 * sa
            # Find interpolated width
            hw = 0.08
            for idx in range(len(sole_curve) - 1):
                t0, w0, _ = sole_curve[idx]
                t1, w1, _ = sole_curve[idx + 1]
                if t0 <= t <= t1:
                    frac = (t - t0) / (t1 - t0)
                    hw = (w0 + frac * (w1 - w0)) * s_scale
                    break
                    
            y_pos = -0.25 + t * 0.53
            x_pos = ca * hw
            v = bm.verts.new((x_pos, y_pos, sz))
            ring.append(v)
        sole_rings.append(ring)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge sole rings
    for lvl in range(len(sole_levels) - 1):
        r0 = sole_rings[lvl]
        r1 = sole_rings[lvl + 1]
        for i in range(SEGS):
            i_next = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[i_next], r1[i_next], r1[i]))
            
    # Bottom tread cap
    r_bot = sole_rings[0]
    bm.faces.new(reversed(r_bot))
    
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 2. UPPER: TOE BOX, MUDGUARD & VAMP
    # -----------------------------------------------------------------
    upper_levels = [
        # (z, x_scale, y_shift)
        (0.08, 0.94, -0.01), # Lower upper perimeter
        (0.12, 0.88, -0.02), # Vamp & mudguard ridge
        (0.16, 0.80, -0.03), # Eyestay / collar base
        (0.20, 0.72, -0.04), # Padded ankle collar & tongue
    ]
    
    upper_rings = []
    prev_ring = sole_rings[2]
    for uz, uscale, uyshift in upper_levels:
        ring = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            t = 0.5 + 0.5 * sa
            
            hw = 0.08
            for idx in range(len(sole_curve) - 1):
                t0, w0, _ = sole_curve[idx]
                t1, w1, _ = sole_curve[idx + 1]
                if t0 <= t <= t1:
                    frac = (t - t0) / (t1 - t0)
                    hw = (w0 + frac * (w1 - w0)) * uscale
                    break
                    
            y_pos = -0.25 + t * 0.53 + uyshift
            x_pos = ca * hw
            
            # Raise tongue at front-center, lower collar at back
            z_mod = uz
            if 0.35 <= t <= 0.85 and abs(ca) < 0.4:
                # Tongue ridge
                z_mod += 0.035 * (1.0 - abs(ca)/0.4)
            elif t < 0.25 and uz >= 0.16:
                # Ankle collar dip
                z_mod -= 0.02
                
            v = bm.verts.new((x_pos, y_pos, z_mod))
            ring.append(v)
        upper_rings.append(ring)
        
    for lvl in range(len(upper_levels)):
        r0 = prev_ring
        r1 = upper_rings[lvl]
        for i in range(SEGS):
            i_next = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[i_next], r1[i_next], r1[i]))
        prev_ring = r1
        
    # Ankle foot opening / insole cap
    top_ring = upper_rings[-1]
    # Inset for insole opening
    insole_ring = []
    for v in top_ring:
        iv = bm.verts.new((v.co.x * 0.50, v.co.y * 0.90, v.co.z - 0.03))
        insole_ring.append(iv)
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        bm.faces.new((top_ring[i], top_ring[i_next], insole_ring[i_next], insole_ring[i]))
    bm.faces.new(insole_ring)
    
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 3. FAT COTTON SKATE LACES (Crossed across the eyestay)
    # -----------------------------------------------------------------
    lace_steps = [
        (0.045, 0.05, 0.13),
        (0.040, 0.00, 0.16),
        (0.036, -0.05, 0.19),
        (0.032, -0.10, 0.22),
    ]
    for lx, ly, lz in lace_steps:
        # Cross segment 1: left to right
        v0 = bm.verts.new((-lx, ly, lz))
        v1 = bm.verts.new(( lx, ly, lz + 0.008))
        v2 = bm.verts.new(( lx, ly - 0.015, lz + 0.008))
        v3 = bm.verts.new((-lx, ly - 0.015, lz))
        bm.faces.new((v0, v1, v2, v3))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -----------------------------------------------------------------
    # 4. UNIFIED DUAL-PANEL UV UNWRAPPING
    # Lateral profile (outer, x > 0) -> Left Half [0.0, 0.50]
    # Medial profile (inner, x <= 0) -> Right Half [0.50, 1.0]
    # -----------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    min_y, max_y = -0.28, 0.32
    min_z, max_z = -0.08, 0.26
    span_y = max_y - min_y
    span_z = max_z - min_z
    
    for f in bm.faces:
        c = f.calc_center_median()
        is_lateral = c.x >= 0.0
        for l in f.loops:
            v = l.vert
            # Map Y (heel to toe) to horizontal U, and Z (sole to collar) to vertical V
            u_norm = (v.co.y - min_y) / span_y
            v_norm = (v.co.z - min_z) / span_z
            u_norm = max(0.0, min(1.0, u_norm))
            v_norm = max(0.0, min(1.0, v_norm))
            
            if is_lateral:
                # Left half: [0.0, 0.50]
                l[uv_layer].uv = (u_norm * 0.50, v_norm)
            else:
                # Right half: [0.50, 1.0]
                l[uv_layer].uv = (0.50 + (1.0 - u_norm) * 0.50, v_norm)
                
    bm.to_mesh(mesh)
    bm.free()
    
    # Subdivision
    sub = sneaker.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    for p in sneaker.data.polygons:
        p.use_smooth = True
        
    # -----------------------------------------------------------------
    # 5. ATELIER SNEAKER DISPLAY PEDESTAL
    # High-end circular museum footwear platform
    # -----------------------------------------------------------------
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.36, depth=0.03, location=(0, 0.02, -0.075))
    pedestal = bpy.context.active_object
    pedestal.name = "Sneaker_Pedestal"
    
    for p in pedestal.data.polygons:
        p.use_smooth = True
        
    # -----------------------------------------------------------------
    # 6. MATERIALS & EXPORT
    # -----------------------------------------------------------------
    mat_upper = bpy.data.materials.new(name="Mat_Sneaker_Upper")
    nodes_u = mat_upper.node_tree.nodes
    bsdf_u = nodes_u.get("Principled BSDF")
    
    tex_abs = os.path.abspath(texture_path)
    if os.path.exists(tex_abs) and bsdf_u:
        tex_node = nodes_u.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(tex_abs)
        mat_upper.node_tree.links.new(tex_node.outputs['Color'], bsdf_u.inputs['Base Color'])
        bsdf_u.inputs['Roughness'].default_value = 0.75
    sneaker.data.materials.append(mat_upper)
    
    mat_ped = bpy.data.materials.new(name="Mat_Pedestal")
    bsdf_p = mat_ped.node_tree.nodes.get("Principled BSDF")
    if bsdf_p:
        bsdf_p.inputs['Base Color'].default_value = (0.05, 0.05, 0.06, 1.0)
        bsdf_p.inputs['Metallic'].default_value = 0.85
        bsdf_p.inputs['Roughness'].default_value = 0.25
    pedestal.data.materials.append(mat_ped)
    
    os.makedirs(os.path.dirname(out_glb_path), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True
    )
    print(f"Exported Sneaker GLB: {out_glb_path}")
    return sneaker, pedestal

kicks_to_bake = [
    {'id': 'p9',  'tex': 'public/assets/models/textures/tex_p9.png',  'out': 'public/assets/models/kicks_p9.glb'},
    {'id': 'p10', 'tex': 'public/assets/models/textures/tex_p10.png', 'out': 'public/assets/models/kicks_p10.glb'},
    {'id': 'p11', 'tex': 'public/assets/models/textures/tex_p11.png', 'out': 'public/assets/models/kicks_p11.glb'},
    {'id': 'p12', 'tex': 'public/assets/models/textures/tex_p12.png', 'out': 'public/assets/models/kicks_p12.glb'},
    {'id': 'p16', 'tex': 'public/assets/models/textures/tex_p16.png', 'out': 'public/assets/models/kicks_p16.glb'},
]

if __name__ == '__main__':
    for item in kicks_to_bake:
        print(f"Baking skate sneaker: {item['id']}...")
        build_watertight_skate_sneaker(item['tex'], os.path.abspath(item['out']))
    print("ALL SNEAKERS BAKED SUCCESSFULLY!")
