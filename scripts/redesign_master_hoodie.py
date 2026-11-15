import bpy
import bmesh
import math
import os

def create_photorealistic_fabric_texture(
    base_rgb=(28, 28, 30),
    chest_graphic_type="westside",
    back_graphic_type="lowrider",
    sleeve_graphic_type="paisley",
    out_path="public/assets/models/textures/test_tex.png"
):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import numpy as np

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    size = (2048, 2048)
    
    # 1. Base fabric with realistic cotton fleece micro-grain
    r, g, b = base_rgb
    base_arr = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    base_arr[:, :] = [r, g, b]
    
    # Micro-grain noise
    noise = np.random.normal(0, 5.0, (size[1], size[0], 1))
    fleece_arr = np.clip(base_arr.astype(float) + noise, 0, 255).astype(np.uint8)
    
    canvas = Image.fromarray(fleece_arr).convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    
    # 2. Authentic Ribbed Knit Texture on Hem (Bottom 1780 to 2048)
    for y in range(1780, 2048, 14):
        knit_col = (max(0, r - 16), max(0, g - 16), max(0, b - 16), 255)
        knit_light = (min(255, r + 14), min(255, g + 14), min(255, b + 14), 200)
        draw.line([(0, y), (2048, y)], fill=knit_col, width=5)
        draw.line([(0, y + 4), (2048, y + 4)], fill=knit_light, width=2)
        
    # Ribbed Knit on Sleeve Cuffs (Left: x in [80, 480], y in [1650, 1850]; Right: x in [1568, 1968])
    for x_start, x_end in [(80, 480), (1568, 1968)]:
        for y in range(1650, 1850, 12):
            draw.line([(x_start, y), (x_end, y)], fill=(max(0, r - 18), max(0, g - 18), max(0, b - 18), 255), width=4)
            draw.line([(x_start, y + 3), (x_end, y + 3)], fill=(min(255, r + 12), min(255, g + 12), min(255, b + 12), 180), width=2)

    # 3. Kangaroo Pocket Top Stitch & Side Seams (Front: U centered at 1024, V in [1280, 1720])
    p_x1, p_y1 = 620, 1280
    p_x2, p_y2 = 1428, 1750
    stitch_dark = (max(0, r - 22), max(0, g - 22), max(0, b - 22), 255)
    stitch_light = (min(255, r + 20), min(255, g + 20), min(255, b + 20), 160)
    
    # Shadow under pocket top lip
    draw.line([(p_x1, p_y1), (p_x2, p_y1)], fill=stitch_dark, width=6)
    draw.line([(p_x1, p_y1 - 3), (p_x2, p_y1 - 3)], fill=stitch_light, width=2)
    # Side entry diagonal stitch lines
    draw.line([(p_x1, p_y1), (p_x1 - 90, p_y2)], fill=stitch_dark, width=5)
    draw.line([(p_x2, p_y1), (p_x2 + 90, p_y2)], fill=stitch_dark, width=5)
    
    # 4. Sleeve Patterns (Paisley Bandana / Pinstripe)
    if sleeve_graphic_type == "paisley":
        def draw_paisley(cx, cy, s=1.0, col=(220, 220, 220, 160)):
            pts = [
                (cx, cy), (cx+16*s, cy-22*s), (cx+36*s, cy-14*s), (cx+40*s, cy+16*s),
                (cx+26*s, cy+36*s), (cx, cy+28*s), (cx-20*s, cy+16*s), (cx-14*s, cy-8*s)
            ]
            draw.polygon(pts, fill=col)
            draw.ellipse([cx+8*s, cy-2*s, cx+26*s, cy+16*s], fill=(r, g, b, 255))
            draw.line([(cx+36*s, cy-14*s), (cx+50*s, cy-36*s)], fill=col, width=int(3*s))
            
        p_col = (min(255, r + 45), min(255, g + 45), min(255, b + 45), 180)
        for y in range(700, 1550, 75):
            draw_paisley(280, y, s=0.9, col=p_col)
            draw_paisley(1768, y, s=0.9, col=p_col)

    # 5. Chest Graphic (Centered around x=1024, y=720)
    font_oe = None
    for fp in ["C:/Windows/Fonts/OLDENGL.TTF", "C:/Windows/Fonts/chum.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(fp):
            try:
                font_oe = ImageFont.truetype(fp, 76)
                break
            except Exception:
                pass
                
    text_color = (245, 240, 230, 230) if (0.299*r + 0.587*g + 0.114*b < 140) else (25, 25, 25, 230)
    
    if chest_graphic_type == "westside":
        txt = "WESTSIDE"
        if font_oe:
            bb = draw.textbbox((0, 0), txt, font=font_oe)
            tw = bb[2] - bb[0]
            draw.text((1024 - tw//2, 680), txt, font=font_oe, fill=text_color)
            
            # Subtle lowrider flourish underneath
            draw.arc([924, 765, 1124, 805], start=0, end=180, fill=text_color, width=3)
            draw.polygon([(1024, 800), (1032, 792), (1024, 784), (1016, 792)], fill=text_color)
    elif chest_graphic_type == "cultura":
        txt = "LA Cultura"
        if font_oe:
            bb = draw.textbbox((0, 0), txt, font=font_oe)
            tw = bb[2] - bb[0]
            # Left chest hit
            draw.text((780, 680), txt, font=font_oe, fill=text_color)
    elif chest_graphic_type == "noir":
        txt = "HOODOO NOIR"
        if font_oe:
            bb = draw.textbbox((0, 0), txt, font=font_oe)
            tw = bb[2] - bb[0]
            draw.text((1024 - tw//2, 680), txt, font=font_oe, fill=text_color)

    canvas.save(out_path, "PNG")
    print(f"Created realistic fabric texture: {out_path}")
    return out_path

def build_realistic_draped_hoodie(texture_path, out_glb_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Hoodie_Fabric_Body_Mesh")
    hoodie = bpy.data.objects.new("Hoodie_Fabric_Body", mesh)
    bpy.context.collection.objects.link(hoodie)
    bpy.context.view_layer.objects.active = hoodie
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. TORSO: RELAXED HEAVYWEIGHT STREETWEAR DRAPE
    # Proportions: Box-cut width 0.98m, Height 0.88m (authentic 1:1.1 drop ratio)
    # -------------------------------------------------------------
    SEGS = 20
    ring_specs = [
        # (z, x_rad, y_front, y_back)
        (-0.46, 0.40, 0.17, 0.16), # 0: Hem bottom (ribbed waistband)
        (-0.36, 0.43, 0.18, 0.17), # 1: Hem top
        (-0.24, 0.47, 0.22, 0.20), # 2: Lower belly / pocket base
        (-0.08, 0.50, 0.24, 0.21), # 3: Mid torso / pocket pouch
        ( 0.08, 0.51, 0.23, 0.20), # 4: Upper pocket seam
        ( 0.22, 0.52, 0.21, 0.19), # 5: Chest graphic level
        ( 0.34, 0.53, 0.20, 0.18), # 6: Armpit / armscye level
        ( 0.44, 0.54, 0.18, 0.16), # 7: Dropped shoulder seam
        ( 0.50, 0.22, 0.14, 0.13), # 8: Collar opening
    ]
    
    torso_rings = []
    for r_idx, (z, xr, yf, yb) in enumerate(ring_specs):
        r_verts = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            ca = math.cos(ang)
            sa = math.sin(ang)
            vx = ca * xr
            yr = yf if sa >= 0 else yb
            vy = sa * yr
            # Organic fold ripple
            if 1 <= r_idx <= 6:
                vy += 0.008 * math.sin(ang * 3.0) + 0.005 * math.cos(ang * 5.0)
            v = bm.verts.new((vx, vy, z))
            r_verts.append(v)
        torso_rings.append(r_verts)
        
    bm.verts.ensure_lookup_table()
    
    # Bridge torso rings
    for r in range(6):
        r0 = torso_rings[r]
        r1 = torso_rings[r + 1]
        for i in range(SEGS):
            i_next = (i + 1) % SEGS
            bm.faces.new((r0[i], r0[i_next], r1[i_next], r1[i]))
            
    # Armscye: Rings 6 -> 7 (Leave side holes for sleeves: indices 19,0,1,2 and 8,9,10,11)
    r6 = torso_rings[6]
    r7 = torso_rings[7]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        # Skip side arm openings
        if i in (19, 0, 1) or i_next in (19, 0, 1):
            continue
        if i in (9, 10, 11) or i_next in (9, 10, 11):
            continue
        bm.faces.new((r6[i], r6[i_next], r7[i_next], r7[i]))
        
    # Shoulders to collar: Rings 7 -> 8
    r8 = torso_rings[8]
    for i in range(SEGS):
        i_next = (i + 1) % SEGS
        bm.faces.new((r7[i], r7[i_next], r8[i_next], r8[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. RELAXED DOWNWARD-DRAPED SLEEVES
    # Naturally hanging along the sides (NOT sticking out!)
    # -------------------------------------------------------------
    sleeve_def = [
        # (x_cen, y_cen, z_cen, radius)
        (0.53,  0.00,  0.36, 0.150), # 0: Shoulder cap drop
        (0.51,  0.01,  0.18, 0.138), # 1: Upper arm
        (0.48,  0.02, -0.02, 0.126), # 2: Elbow drape fold
        (0.44,  0.01, -0.22, 0.114), # 3: Forearm
        (0.40, -0.01, -0.38, 0.096), # 4: Ribbed cuff
        (0.38, -0.01, -0.45, 0.090), # 5: Cuff hem
    ]
    
    SLEEVE_SEGS = 10
    for side_sign in (1.0, -1.0):
        s_rings = []
        for s_idx, (xc, yc, zc, rad) in enumerate(sleeve_def):
            s_ring = []
            for j in range(SLEEVE_SEGS):
                ang = j * (2.0 * math.pi / SLEEVE_SEGS)
                sx = side_sign * (xc + math.cos(ang) * rad)
                sy = yc + math.sin(ang) * rad
                sz = zc
                # Natural elbow crease
                if s_idx == 2 and math.cos(ang) * side_sign < 0:
                    sz += 0.025
                    sy -= 0.015
                v = bm.verts.new((sx, sy, sz))
                s_ring.append(v)
            s_rings.append(s_ring)
            
        for s in range(len(s_rings) - 1):
            s0 = s_rings[s]
            s1 = s_rings[s + 1]
            for j in range(SLEEVE_SEGS):
                j_next = (j + 1) % SLEEVE_SEGS
                bm.faces.new((s0[j], s0[j_next], s1[j_next], s1[j]))
                
        # Bridge to torso armhole
        s0 = s_rings[0]
        if side_sign > 0:
            arm_torso = [r7[18], r7[19], r7[0], r7[1], r7[2], r6[2], r6[1], r6[0], r6[19], r6[18]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((arm_torso[k], arm_torso[k_next], s0[k_next], s0[k]))
        else:
            arm_torso = [r7[8], r7[9], r7[10], r7[11], r7[12], r6[12], r6[11], r6[10], r6[9], r6[8]]
            for k in range(SLEEVE_SEGS):
                k_next = (k + 1) % SLEEVE_SEGS
                bm.faces.new((arm_torso[k_next], arm_torso[k], s0[k], s0[k_next]))
                
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 3. ORGANIC COWL-DRAPED HOOD
    # Drapes over collar and backward around neck with natural volume
    # -------------------------------------------------------------
    hood_specs = [
        # (z, y_cen, x_rad, y_rad)
        (0.51, -0.04, 0.23, 0.20), # Cowl base
        (0.59, -0.10, 0.25, 0.23), # Nape drape
        (0.67, -0.07, 0.23, 0.22), # Mid skull curve
        (0.72, -0.02, 0.20, 0.19), # Crown apex
        (0.69,  0.05, 0.17, 0.16), # Face opening lip
    ]
    
    HOOD_PTS = 10
    h_rings = []
    for h_idx, (hz, hyc, hrx, hry) in enumerate(hood_specs):
        h_ring = []
        for i in range(HOOD_PTS):
            t = i / (HOOD_PTS - 1)
            ang = math.pi * 0.12 + t * (math.pi * 1.76)
            hx = math.cos(ang) * hrx
            hy = hyc + math.sin(ang) * hry
            # Natural neck sag
            hsag = -0.018 * math.cos(t * math.pi)
            v = bm.verts.new((hx, hy, hz + hsag))
            h_ring.append(v)
        h_rings.append(h_ring)
        
    for h in range(len(h_rings) - 1):
        h0 = h_rings[h]
        h1 = h_rings[h + 1]
        for i in range(HOOD_PTS - 1):
            bm.faces.new((h0[i], h0[i+1], h1[i+1], h1[i]))
            
    # Bridge hood to collar ring r8
    h0 = h_rings[0]
    collar_map = [3, 2, 1, 0, 19, 18, 17, 16, 15, 13]
    for i in range(len(collar_map) - 1):
        bm.faces.new((r8[collar_map[i]], r8[collar_map[i+1]], h0[i+1], h0[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 4. 3D KANGAROO POUCH POCKET
    # Forward depth with diagonal side opening entries
    # -------------------------------------------------------------
    kp_verts = []
    for pz, py_off, px_span in [(-0.24, 0.040, 0.32), (-0.08, 0.060, 0.36), (0.08, 0.040, 0.30)]:
        row = []
        for c in range(7):
            t = (c / 6.0) - 0.5
            px = t * 2.0 * px_span
            arch = math.cos(t * math.pi)
            base_y = 0.21 + arch * 0.02
            py = base_y + py_off * arch
            v = bm.verts.new((px, py, pz))
            row.append(v)
        kp_verts.append(row)
        
    for r in range(2):
        for c in range(6):
            bm.faces.new((kp_verts[r][c], kp_verts[r][c+1], kp_verts[r+1][c+1], kp_verts[r+1][c]))
            
    r2 = torso_rings[2]
    r4 = torso_rings[4]
    for c in range(6):
        bm.faces.new((r2[5], r2[6] if c >= 3 else r2[4], kp_verts[0][c+1], kp_verts[0][c]))
        bm.faces.new((kp_verts[2][c], kp_verts[2][c+1], r4[6] if c >= 3 else r4[4], r4[5]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 5. COTTON DRAWSTRINGS
    # -------------------------------------------------------------
    for ds_sign in (1.0, -1.0):
        ds_pts = [
            (ds_sign * 0.040, 0.16, 0.46),
            (ds_sign * 0.048, 0.17, 0.34),
            (ds_sign * 0.044, 0.18, 0.22),
            (ds_sign * 0.038, 0.18, 0.12),
        ]
        prev_ring = []
        for p_co in ds_pts:
            ring = []
            for k in range(6):
                kang = k * (2.0 * math.pi / 6)
                cx = p_co[0] + math.cos(kang) * 0.007
                cy = p_co[1] + math.sin(kang) * 0.007
                cz = p_co[2]
                v = bm.verts.new((cx, cy, cz))
                ring.append(v)
            if prev_ring:
                for k in range(6):
                    k_nxt = (k + 1) % 6
                    bm.faces.new((prev_ring[k], prev_ring[k_nxt], ring[k_nxt], ring[k]))
            prev_ring = ring
            
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 6. UV UNWRAPPING (DIRECT CONFORMAL MAPPING)
    # -------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    min_x, max_x = -0.68, 0.68
    min_z, max_z = -0.52, 0.78
    span_x = max_x - min_x
    span_z = max_z - min_z
    
    for f in bm.faces:
        c = f.calc_center_median()
        is_front = c.y >= -0.02
        for l in f.loops:
            v = l.vert
            u_coord = (v.co.x - min_x) / span_x
            v_coord = (v.co.z - min_z) / span_z
            if is_front:
                l[uv_layer].uv = (1.0 - u_coord, v_coord)
            else:
                l[uv_layer].uv = (u_coord, v_coord)
                
    bm.to_mesh(mesh)
    bm.free()
    
    # Subdivision modifier for smooth organic cloth
    sub = hoodie.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 2
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    sol = hoodie.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.006
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    for p in hoodie.data.polygons:
        p.use_smooth = True
        
    # -------------------------------------------------------------
    # 7. ATELIER MANNEQUIN STAND
    # Sleek matte black presentation bust
    # -------------------------------------------------------------
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.075, depth=0.28, location=(0, -0.03, 0.48))
    m_neck = bpy.context.active_object
    m_neck.name = "Mannequin_Bust"
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.060, depth=0.025, location=(0, -0.03, 0.62))
    m_cap = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.022, depth=0.95, location=(0, 0, -0.46))
    m_pole = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.35, depth=0.035, location=(0, 0, -0.93))
    m_base = bpy.context.active_object
    
    bpy.ops.object.select_all(action='DESELECT')
    for m in [m_neck, m_cap, m_pole, m_base]:
        m.select_set(True)
    bpy.context.view_layer.objects.active = m_neck
    bpy.ops.object.join()
    mannequin = bpy.context.active_object
    mannequin.name = "Mannequin_Stand"
    
    for p in mannequin.data.polygons:
        p.use_smooth = True
        
    bpy.ops.object.select_all(action='SELECT')
    for obj in [hoodie, mannequin]:
        obj.location.z -= 0.08
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
    
    # Material setup
    mat_fabric = bpy.data.materials.new(name="Mat_Hoodie_Fabric")
    nodes_f = mat_fabric.node_tree.nodes
    bsdf_f = nodes_f.get("Principled BSDF")
    
    tex_abs = os.path.abspath(texture_path)
    if os.path.exists(tex_abs) and bsdf_f:
        tex_node = nodes_f.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(tex_abs)
        mat_fabric.node_tree.links.new(tex_node.outputs['Color'], bsdf_f.inputs['Base Color'])
        bsdf_f.inputs['Roughness'].default_value = 0.90
    hoodie.data.materials.append(mat_fabric)
    
    mat_mannequin = bpy.data.materials.new(name="Mat_Mannequin")
    bsdf_m = mat_mannequin.node_tree.nodes.get("Principled BSDF")
    if bsdf_m:
        bsdf_m.inputs['Base Color'].default_value = (0.05, 0.05, 0.06, 1.0)
        bsdf_m.inputs['Metallic'].default_value = 0.85
        bsdf_m.inputs['Roughness'].default_value = 0.25
    mannequin.data.materials.append(mat_mannequin)
    
    # Export GLB
    os.makedirs(os.path.dirname(out_glb_path), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True
    )
    print(f"Exported 3D Model: {out_glb_path}")
    return hoodie, mannequin

if __name__ == "__main__":
    tex = create_photorealistic_fabric_texture(
        base_rgb=(26, 26, 28),
        chest_graphic_type="westside",
        sleeve_graphic_type="paisley",
        out_path="public/assets/models/textures/tex_test_redesign.png"
    )
    build_realistic_draped_hoodie(
        tex,
        os.path.abspath("public/assets/models/test_redesign.glb")
    )
