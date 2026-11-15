import bpy
import bmesh
import math
import os

def build_chunky_skate_sneaker(out_glb_path, texture_path=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Sneaker_Mesh")
    sneaker = bpy.data.objects.new("Sneaker_Model", mesh)
    bpy.context.collection.objects.link(sneaker)
    bpy.context.view_layer.objects.active = sneaker
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # Shoe Last Dimensions (in meters):
    # Length: ~0.28m, Heel: y=-0.13, Waist: y=-0.02, Ball: y=+0.06, Toe: y=+0.15
    # -------------------------------------------------------------
    def get_sole_half_widths(y):
        t = (y + 0.13) / 0.28 # 0 to 1
        t = max(0.0, min(1.0, t))
        if t < 0.22: # Heel
            f = t / 0.22
            w = 0.036 + 0.005 * math.sin(f * math.pi)
            return -w, w
        elif t < 0.48: # Waist / Arch
            f = (t - 0.22) / 0.26
            w_med = 0.036 - 0.011 * math.sin(f * math.pi)
            w_lat = 0.038 - 0.003 * math.sin(f * math.pi)
            return -w_med, w_lat
        elif t < 0.82: # Ball of foot
            f = (t - 0.48) / 0.34
            w_med = 0.025 + 0.025 * math.sin(f * math.pi * 0.75)
            w_lat = 0.035 + 0.016 * math.sin(f * math.pi * 0.75)
            return -w_med, w_lat
        else: # Toe taper
            f = (t - 0.82) / 0.18
            w_med = 0.050 * max(0.0, 1.0 - (f ** 1.3))
            w_lat = 0.051 * max(0.0, 1.0 - (f ** 1.2))
            return -w_med, w_lat

    def get_sole_heights(y):
        # Heel is higher (drop), toe tip rises (toe spring)
        t = (y + 0.13) / 0.28
        # Sole bottom z
        if t < 0.65:
            z_bot = 0.0
        else:
            frac = (t - 0.65) / 0.35
            z_bot = 0.015 * (frac ** 1.8) # Toe spring
            
        # Sole thickness: 28mm at heel, tapering to 20mm at ball/toe
        thickness = 0.028 - 0.008 * min(1.0, t / 0.60)
        z_top = z_bot + thickness
        return z_bot, z_top

    # Number of longitudinal stations along Y
    Y_SEGS = 18
    y_stations = [-0.13 + i * (0.28 / (Y_SEGS - 1)) for i in range(Y_SEGS)]
    
    # -------------------------------------------------------------
    # 1. CUPSOLE (Bottom Tread, Midsole Wall, Foxing Rim)
    # -------------------------------------------------------------
    # Create grid for sole bottom and sole top
    sole_bot_verts = {}
    sole_top_verts = {}
    
    for i, y in enumerate(y_stations):
        x_med, x_lat = get_sole_half_widths(y)
        z_bot, z_top = get_sole_heights(y)
        
        # 5 cross-section points across the sole:
        # 0: medial outer, 1: medial mid, 2: center, 3: lateral mid, 4: lateral outer
        sole_bot_verts[i] = []
        sole_top_verts[i] = []
        for xi in range(5):
            frac = xi / 4.0
            x = x_med + frac * (x_lat - x_med)
            vb = bm.verts.new((x, y, z_bot))
            vt = bm.verts.new((x, y, z_top))
            sole_bot_verts[i].append(vb)
            sole_top_verts[i].append(vt)
            
    bm.verts.ensure_lookup_table()
    
    # Skin the bottom sole tread (faces point down -Z)
    for i in range(Y_SEGS - 1):
        for xi in range(4):
            v0 = sole_bot_verts[i][xi]
            v1 = sole_bot_verts[i][xi + 1]
            v2 = sole_bot_verts[i + 1][xi + 1]
            v3 = sole_bot_verts[i + 1][xi]
            bm.faces.new((v0, v3, v2, v1))
            
    # Skin the outer sidewalls of the midsole (foxing tape)
    # Medial sidewall (xi = 0)
    for i in range(Y_SEGS - 1):
        vb0 = sole_bot_verts[i][0]
        vb1 = sole_bot_verts[i + 1][0]
        vt1 = sole_top_verts[i + 1][0]
        vt0 = sole_top_verts[i][0]
        bm.faces.new((vb0, vb1, vt1, vt0))
        
    # Lateral sidewall (xi = 4)
    for i in range(Y_SEGS - 1):
        vb0 = sole_bot_verts[i][4]
        vb1 = sole_bot_verts[i + 1][4]
        vt1 = sole_top_verts[i + 1][4]
        vt0 = sole_top_verts[i][4]
        bm.faces.new((vb0, vt0, vt1, vb1))
        
    # Heel back sidewall (i = 0)
    for xi in range(4):
        vb0 = sole_bot_verts[0][xi]
        vb1 = sole_bot_verts[0][xi + 1]
        vt1 = sole_top_verts[0][xi + 1]
        vt0 = sole_top_verts[0][xi]
        bm.faces.new((vb0, vt0, vt1, vb1))
        
    # Toe front sidewall (i = Y_SEGS - 1)
    for xi in range(4):
        vb0 = sole_bot_verts[Y_SEGS - 1][xi]
        vb1 = sole_bot_verts[Y_SEGS - 1][xi + 1]
        vt1 = sole_top_verts[Y_SEGS - 1][xi + 1]
        vt0 = sole_top_verts[Y_SEGS - 1][xi]
        bm.faces.new((vb0, vb1, vt1, vt0))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 2. UPPER: TOE BOX & VAMP (Y from +0.02 to +0.15)
    # Authentic rounded low-profile toe cap and arched vamp
    # -------------------------------------------------------------
    # Find stations for forefoot (y >= 0.01)
    forefoot_indices = [i for i, y in enumerate(y_stations) if y >= 0.005]
    
    toe_upper_verts = {}
    for i in forefoot_indices:
        y = y_stations[i]
        x_med, x_lat = get_sole_half_widths(y)
        _, z_top = get_sole_heights(y)
        t = (y + 0.13) / 0.28
        
        # Height of the toe dome above the sole:
        # At toe tip (t=1): ~22mm dome
        # At ball/vamp (t=0.65): ~38mm dome
        # At throat (t=0.48): ~48mm dome
        dome_h = 0.022 + 0.026 * (1.0 - (t - 0.48) / 0.52)
        
        toe_upper_verts[i] = []
        for xi in range(5):
            frac = xi / 4.0
            x = (x_med + frac * (x_lat - x_med)) * 0.94
            # Parabolic curve across X for rounded shoe dome
            arch = math.sin(frac * math.pi)
            z = z_top + dome_h * arch + 0.008
            v = bm.verts.new((x, y, z))
            toe_upper_verts[i].append(v)
            
    bm.verts.ensure_lookup_table()
    
    # Skin the toe box upper dome
    for idx in range(len(forefoot_indices) - 1):
        i0 = forefoot_indices[idx]
        i1 = forefoot_indices[idx + 1]
        for xi in range(4):
            v0 = toe_upper_verts[i0][xi]
            v1 = toe_upper_verts[i0][xi + 1]
            v2 = toe_upper_verts[i1][xi + 1]
            v3 = toe_upper_verts[i1][xi]
            bm.faces.new((v0, v1, v2, v3))
            
    # Connect toe box outer edges to sole top rim (mudguard sidewall)
    for idx in range(len(forefoot_indices) - 1):
        i0 = forefoot_indices[idx]
        i1 = forefoot_indices[idx + 1]
        # Medial side (xi = 0)
        v_sole0 = sole_top_verts[i0][0]
        v_sole1 = sole_top_verts[i1][0]
        v_upper1 = toe_upper_verts[i1][0]
        v_upper0 = toe_upper_verts[i0][0]
        bm.faces.new((v_sole0, v_sole1, v_upper1, v_upper0))
        
        # Lateral side (xi = 4)
        v_sole0 = sole_top_verts[i0][4]
        v_sole1 = sole_top_verts[i1][4]
        v_upper1 = toe_upper_verts[i1][4]
        v_upper0 = toe_upper_verts[i0][4]
        bm.faces.new((v_sole0, v_upper0, v_upper1, v_sole1))
        
    # Front tip mudguard closure
    tip_idx = forefoot_indices[-1]
    for xi in range(4):
        vs0 = sole_top_verts[tip_idx][xi]
        vs1 = sole_top_verts[tip_idx][xi + 1]
        vu1 = toe_upper_verts[tip_idx][xi + 1]
        vu0 = toe_upper_verts[tip_idx][xi]
        bm.faces.new((vs0, vs1, vu1, vu0))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 3. QUARTER PANELS & PADDED ANKLE COLLAR (Y from -0.13 to +0.01)
    # The sides wrap up to the collar rim, leaving an ankle opening
    # -------------------------------------------------------------
    rear_indices = [i for i, y in enumerate(y_stations) if y <= 0.01]
    
    # Collar rim vertices along the rear:
    # Achilles heel is at y = -0.13, rising to Z = 0.105
    # Ankle dip on sides at y = -0.06, dipping to Z = 0.082
    # Eyestay rise at y = 0.00, rising to Z = 0.092
    lat_collar_verts = {}
    med_collar_verts = {}
    
    for i in rear_indices:
        y = y_stations[i]
        x_med, x_lat = get_sole_half_widths(y)
        _, z_top = get_sole_heights(y)
        t_rear = (y + 0.13) / 0.14 # 0 at heel, 1 at throat
        
        # Anatomical collar height curve
        if t_rear < 0.25: # Heel counter
            z_col = z_top + 0.075 - 0.010 * (t_rear / 0.25)
        elif t_rear < 0.70: # Ankle bone dip
            f = (t_rear - 0.25) / 0.45
            z_col = z_top + 0.065 - 0.008 * math.sin(f * math.pi)
        else: # Eyestay throat rise
            f = (t_rear - 0.70) / 0.30
            z_col = z_top + 0.057 + 0.015 * f
            
        # Padded collar width (slightly narrower than sole)
        w_lat = x_lat * 0.88
        w_med = x_med * 0.88
        
        vl = bm.verts.new((w_lat, y, z_col))
        vm = bm.verts.new((w_med, y, z_col))
        lat_collar_verts[i] = vl
        med_collar_verts[i] = vm
        
    bm.verts.ensure_lookup_table()
    
    # Connect quarter panels: sole top -> collar rim
    for idx in range(len(rear_indices) - 1):
        i0 = rear_indices[idx]
        i1 = rear_indices[idx + 1]
        
        # Lateral quarter panel
        vs0 = sole_top_verts[i0][4]
        vs1 = sole_top_verts[i1][4]
        vc1 = lat_collar_verts[i1]
        vc0 = lat_collar_verts[i0]
        bm.faces.new((vs0, vc0, vc1, vs1))
        
        # Medial quarter panel
        vs0 = sole_top_verts[i0][0]
        vs1 = sole_top_verts[i1][0]
        vc1 = med_collar_verts[i1]
        vc0 = med_collar_verts[i0]
        bm.faces.new((vs0, vs1, vc1, vc0))
        
    # Heel back closure (i = 0)
    for xi in range(4):
        vs0 = sole_top_verts[0][xi]
        vs1 = sole_top_verts[0][xi + 1]
        # Top heel rim interpolated
        frac0 = xi / 4.0
        frac1 = (xi + 1) / 4.0
        vc0_x = med_collar_verts[0].co.x + frac0 * (lat_collar_verts[0].co.x - med_collar_verts[0].co.x)
        vc1_x = med_collar_verts[0].co.x + frac1 * (lat_collar_verts[0].co.x - med_collar_verts[0].co.x)
        vc0 = bm.verts.new((vc0_x, -0.13, lat_collar_verts[0].co.z))
        vc1 = bm.verts.new((vc1_x, -0.13, lat_collar_verts[0].co.z))
        bm.faces.new((vs0, vs1, vc1, vc0))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 4. HOLLOW ANKLE OPENING & INTERIOR INSOLE
    # Authentic opening into the shoe cavity
    # -------------------------------------------------------------
    # Rolled padded collar rim and insole floor
    insole_verts = []
    for i in rear_indices:
        y = y_stations[i]
        _, z_top = get_sole_heights(y)
        # Deep interior insole floor (z = z_top + 3mm)
        in_vl = bm.verts.new((lat_collar_verts[i].co.x * 0.55, y, z_top + 0.003))
        in_vm = bm.verts.new((med_collar_verts[i].co.x * 0.55, y, z_top + 0.003))
        
        # Connect collar rim down into interior cavity
        bm.faces.new((lat_collar_verts[i], in_vl, in_vm, med_collar_verts[i]))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 5. AUTHENTIC 3D PADDED SKATE TONGUE
    # Puffy skate tongue rising up and angled forward
    # -------------------------------------------------------------
    t_stations = [
        # (y, z, half_w, thick)
        ( 0.015, 0.065, 0.026, 0.006), # Base at throat
        (-0.010, 0.088, 0.028, 0.008), # Lower tongue
        (-0.035, 0.110, 0.029, 0.009), # Mid tongue
        (-0.055, 0.128, 0.028, 0.008), # Top tongue peak
    ]
    
    tongue_rings = []
    for ty, tz, tw, th in t_stations:
        # 4 vertices per slice
        v_tl = bm.verts.new((-tw, ty, tz + th*0.5))
        v_tr = bm.verts.new(( tw, ty, tz + th*0.5))
        v_br = bm.verts.new(( tw*0.85, ty - 0.005, tz - th*0.5))
        v_bl = bm.verts.new((-tw*0.85, ty - 0.005, tz - th*0.5))
        tongue_rings.append((v_tl, v_tr, v_br, v_bl))
        
    bm.verts.ensure_lookup_table()
    
    for s in range(len(t_stations) - 1):
        r0 = tongue_rings[s]
        r1 = tongue_rings[s + 1]
        bm.faces.new((r0[0], r0[1], r1[1], r1[0])) # Top
        bm.faces.new((r0[1], r0[2], r1[2], r1[1])) # Right
        bm.faces.new((r0[2], r0[3], r1[3], r1[2])) # Bottom
        bm.faces.new((r0[3], r0[0], r1[0], r1[3])) # Left
        
    # Cap tongue peak
    top_r = tongue_rings[-1]
    bm.faces.new((top_r[0], top_r[1], top_r[2], top_r[3]))
    
    # -------------------------------------------------------------
    # 6. AUTHENTIC 3D FAT SKATE LACES (4 Puffy 3D Cross Bars)
    # Chunky textured skate laces spanning between eyestays
    # -------------------------------------------------------------
    lace_bars = [
        # (y, z, width, thickness)
        ( 0.020, 0.068, 0.034, 0.0045), # Bottom lace
        ( 0.002, 0.086, 0.032, 0.0050), # 2nd lace
        (-0.016, 0.104, 0.030, 0.0052), # 3rd lace
        (-0.034, 0.120, 0.028, 0.0055), # Top lace
    ]
    
    for ly, lz, lw, lth in lace_bars:
        lb_v0 = bm.verts.new((-lw, ly, lz))
        lb_v1 = bm.verts.new(( lw, ly, lz))
        lb_v2 = bm.verts.new(( lw, ly - 0.007, lz))
        lb_v3 = bm.verts.new((-lw, ly - 0.007, lz))
        
        # Puffy crest of the fat lace
        lb_c0 = bm.verts.new((-lw * 0.90, ly - 0.0035, lz + lth))
        lb_c1 = bm.verts.new(( lw * 0.90, ly - 0.0035, lz + lth))
        
        bm.verts.ensure_lookup_table()
        bm.faces.new((lb_v0, lb_v1, lb_c1, lb_c0))
        bm.faces.new((lb_c0, lb_c1, lb_v2, lb_v3))
        
    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    
    # -------------------------------------------------------------
    # 7. SEAMLESS DUAL-PANEL UV MAPPING
    # -------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    
    for face in bm.faces:
        for loop in face.loops:
            v = loop.vert
            vx, vy, vz = v.co.x, v.co.y, v.co.z
            
            u_norm = max(0.0, min(1.0, (vy + 0.13) / 0.28))
            v_norm = max(0.0, min(1.0, vz / 0.14))
            
            if vx >= 0:
                loop[uv_layer].uv = (u_norm * 0.49, v_norm)
            else:
                loop[uv_layer].uv = (0.51 + (1.0 - u_norm) * 0.49, v_norm)
                
    bm.to_mesh(mesh)
    bm.free()
    
    # Smooth shading & subdivision modifier for organic curves
    for p in sneaker.data.polygons:
        p.use_smooth = True
        
    sub = sneaker.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    
    # -------------------------------------------------------------
    # 8. CIRCULAR DISPLAY PEDESTAL
    # -------------------------------------------------------------
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.20, depth=0.02, location=(0, 0.01, -0.010))
    pedestal = bpy.context.active_object
    pedestal.name = "Sneaker_Pedestal"
    for p in pedestal.data.polygons:
        p.use_smooth = True
        
    # -------------------------------------------------------------
    # 9. PBR MATERIALS
    # -------------------------------------------------------------
    mat_upper = bpy.data.materials.new(name="Mat_Sneaker_Upper")
    nodes_u = mat_upper.node_tree.nodes
    bsdf_u = nodes_u.get("Principled BSDF")
    
    if texture_path and os.path.exists(os.path.abspath(texture_path)) and bsdf_u:
        tex_node = nodes_u.new("ShaderNodeTexImage")
        tex_node.image = bpy.data.images.load(os.path.abspath(texture_path))
        mat_upper.node_tree.links.new(tex_node.outputs['Color'], bsdf_u.inputs['Base Color'])
        bsdf_u.inputs['Roughness'].default_value = 0.65
    sneaker.data.materials.append(mat_upper)
    
    mat_ped = bpy.data.materials.new(name="Mat_Pedestal")
    bsdf_p = mat_ped.node_tree.nodes.get("Principled BSDF")
    if bsdf_p:
        bsdf_p.inputs['Base Color'].default_value = (0.04, 0.04, 0.05, 1.0)
        bsdf_p.inputs['Metallic'].default_value = 0.90
        bsdf_p.inputs['Roughness'].default_value = 0.20
    pedestal.data.materials.append(mat_ped)
    
    bpy.ops.object.select_all(action='SELECT')
    os.makedirs(os.path.dirname(out_glb_path), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=out_glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True
    )
    print(f"Exported Chunky Skate Sneaker GLB: {out_glb_path}")
    return sneaker, pedestal

if __name__ == '__main__':
    kicks = [
        {'id': 'p9',  'tex': 'public/assets/models/textures/tex_p9.png',  'out': 'public/assets/models/kicks_p9.glb'},
        {'id': 'p10', 'tex': 'public/assets/models/textures/tex_p10.png', 'out': 'public/assets/models/kicks_p10.glb'},
        {'id': 'p11', 'tex': 'public/assets/models/textures/tex_p11.png', 'out': 'public/assets/models/kicks_p11.glb'},
        {'id': 'p12', 'tex': 'public/assets/models/textures/tex_p12.png', 'out': 'public/assets/models/kicks_p12.glb'},
        {'id': 'p16', 'tex': 'public/assets/models/textures/tex_p16.png', 'out': 'public/assets/models/kicks_p16.glb'},
    ]
    for k in kicks:
        build_chunky_skate_sneaker(os.path.abspath(k['out']), k['tex'])
    print("ALL REALISTIC SKATE SNEAKERS BAKED!")
