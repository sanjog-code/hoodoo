import bpy
import bmesh
import math
import os

def create_hyperrealistic_skate_sneaker(out_glb_path, texture_path=None):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    mesh = bpy.data.meshes.new("Sneaker_Mesh")
    obj = bpy.data.objects.new("Sneaker_Model", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    
    bm = bmesh.new()
    
    # -------------------------------------------------------------
    # 1. 32 LONGITUDINAL CROSS-SECTIONS ALONG Y (Foot Last Loft)
    # Length: 285mm (-0.130 to +0.155)
    # -------------------------------------------------------------
    STATIONS = 32
    y_stations = [-0.130 + s * (0.285 / (STATIONS - 1)) for s in range(STATIONS)]
    
    def get_station_profile(s, y):
        t = (y + 0.130) / 0.285
        t = max(0.0, min(1.0, t))
        
        # 1. Toe Spring & Heel Rocker
        if t > 0.58:
            frac = (t - 0.58) / 0.42
            z_bot = 0.016 * (frac ** 1.8) # 16mm toe spring
        elif t < 0.08:
            z_bot = 0.003 * (1.0 - t / 0.08) # heel rocker
        else:
            z_bot = 0.000
            
        # Cupsole height (26mm at heel to 18mm at toe)
        sole_h = 0.026 - 0.008 * t
        z_mid = z_bot + sole_h
        
        # 2. Foot Half-Widths (Medial x_m < 0, Lateral x_l > 0)
        # Rounded radial caps at heel (t < 0.10) and toe (t > 0.90)
        taper_heel = math.sin(t / 0.10 * math.pi * 0.5) if t < 0.10 else 1.0
        taper_toe = math.sin((1.0 - t) / 0.10 * math.pi * 0.5) if t > 0.90 else 1.0
        
        if t < 0.22: # Heel cup
            w = 0.038 * (0.75 + 0.25 * (t / 0.22))
            x_m = -w * 0.96 * taper_heel
            x_l =  w * 1.00 * taper_heel
        elif t < 0.50: # Arch / Waist
            f = (t - 0.22) / 0.28
            x_m = -(0.038 - 0.013 * math.sin(f * math.pi))
            x_l =  (0.039 + 0.003 * math.sin(f * math.pi))
        elif t < 0.82: # Ball of foot
            f = (t - 0.50) / 0.32
            x_m = -(0.024 + 0.026 * math.sin(f * math.pi * 0.75))
            x_l =  (0.043 + 0.011 * math.sin(f * math.pi * 0.75))
        else: # Toe box
            f = (t - 0.82) / 0.18
            w_m = 0.050 * max(0.01, 1.0 - (f ** 1.3)) * taper_toe
            w_l = 0.054 * max(0.01, 1.0 - (f ** 1.3)) * taper_toe
            x_m = -w_m
            x_l =  w_l
            
        # 3. Heights for Footwear Upper Components
        if t < 0.25: # Heel counter tab
            f = t / 0.25
            z_top = z_mid + 0.060 - 0.008 * f
            zone = 'collar'
        elif t < 0.48: # Ankle collar dip
            f = (t - 0.25) / 0.23
            z_top = z_mid + 0.052 - 0.012 * math.sin(f * math.pi)
            zone = 'collar'
        elif t < 0.72: # Eyestay panels flanking open throat gap
            f = (t - 0.48) / 0.24
            z_top = z_mid + 0.042 - 0.014 * f
            zone = 'throat'
        else: # Domed toe box (Vamp)
            f = (t - 0.72) / 0.28
            z_top = z_mid + 0.026 * (1.0 - (f ** 1.3)) + 0.004
            zone = 'vamp'
            
        return z_bot, z_mid, z_top, x_m, x_l, zone

    rings = []
    for s, y in enumerate(y_stations):
        z_bot, z_mid, z_top, x_m, x_l, zone = get_station_profile(s, y)
        dz = z_top - z_mid
        
        v0 = bm.verts.new((0.0, y, z_bot))
        v1 = bm.verts.new((x_m * 1.04, y, z_bot))
        v2 = bm.verts.new((x_m * 1.00, y, z_mid))
        
        v3 = bm.verts.new((x_m * 0.95, y, z_mid + dz * 0.35))
        v4 = bm.verts.new((x_m * 0.88, y, z_mid + dz * 0.70))
        
        if zone == 'collar':
            v5 = bm.verts.new((x_m * 0.72, y, z_top))
            v6 = bm.verts.new((x_l * 0.72, y, z_top))
        elif zone == 'throat':
            v5 = bm.verts.new((-0.009, y, z_top))
            v6 = bm.verts.new(( 0.009, y, z_top))
        else: # vamp
            v5 = bm.verts.new((x_m * 0.45, y, z_top + 0.002))
            v6 = bm.verts.new((x_l * 0.45, y, z_top + 0.002))
            
        v7 = bm.verts.new((x_l * 0.88, y, z_mid + dz * 0.70))
        v8 = bm.verts.new((x_l * 0.95, y, z_mid + dz * 0.35))
        v9 = bm.verts.new((x_l * 1.00, y, z_mid))
        v10 = bm.verts.new((x_l * 1.04, y, z_bot))
        v11 = bm.verts.new((0.0, y, z_mid - 0.002))
        
        rings.append((v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, zone))
        
    bm.verts.ensure_lookup_table()
    
    # Bridge stations along length with outward-facing normals
    for s in range(STATIONS - 1):
        r0 = rings[s]
        r1 = rings[s + 1]
        zone0 = r0[12]
        zone1 = r1[12]
        
        # 1. Outsole bottom
        bm.faces.new((r0[0], r1[0], r1[1], r0[1])) # medial bot
        bm.faces.new((r0[0], r0[10], r1[10], r1[0])) # lateral bot
        
        # 2. Cupsole foxing sidewalls
        bm.faces.new((r0[1], r1[1], r1[2], r0[2])) # medial sole wall
        bm.faces.new((r0[9], r1[9], r1[10], r0[10])) # lateral sole wall (correct outward normal)
        
        # 3. Upper walls (shelf -> lower -> mid -> crest)
        bm.faces.new((r0[2], r1[2], r1[3], r0[3])) # medial lower
        bm.faces.new((r0[3], r1[3], r1[4], r0[4])) # medial mid
        bm.faces.new((r0[4], r1[4], r1[5], r0[5])) # medial crest
        
        bm.faces.new((r0[8], r1[8], r1[9], r0[9])) # lateral lower (correct outward normal)
        bm.faces.new((r0[7], r1[7], r1[8], r0[8])) # lateral mid (correct outward normal)
        bm.faces.new((r0[6], r1[6], r1[7], r0[7])) # lateral crest (correct outward normal)
        
        # 4. Top deck closure for Vamp
        if zone0 == 'vamp' and zone1 == 'vamp':
            bm.faces.new((r0[5], r1[5], r1[6], r0[6]))
        elif zone0 == 'throat' and zone1 == 'vamp':
            bm.faces.new((r0[5], r1[5], r1[6], r0[6]))
            
    # Cap heel end (station 0) with clean quad fan
    r_h = rings[0]
    bm.faces.new((r_h[1], r_h[0], r_h[10], r_h[9], r_h[8], r_h[7], r_h[6], r_h[5], r_h[4], r_h[3], r_h[2]))
    
    # Cap toe tip end (station -1)
    r_t = rings[-1]
    bm.faces.new((r_t[0], r_t[1], r_t[2], r_t[3], r_t[4], r_t[5], r_t[6], r_t[7], r_t[8], r_t[9], r_t[10]))
    
    # -------------------------------------------------------------
    # 2. PUFFY PADDED TONGUE (Emerges from vamp, curves up proud of collar)
    # -------------------------------------------------------------
    T_STEPS = 8
    tongue_rings = []
    for i in range(T_STEPS):
        frac = i / (T_STEPS - 1)
        ty = 0.048 - frac * 0.096
        tz = 0.044 + frac * 0.060 + 0.005 * math.sin(frac * math.pi)
        tw = 0.021 + 0.002 * math.sin(frac * math.pi)
        
        vt_l = bm.verts.new((-tw, ty, tz + 0.003))
        vt_c = bm.verts.new((0.0, ty, tz + 0.006))
        vt_r = bm.verts.new(( tw, ty, tz + 0.003))
        vb_r = bm.verts.new(( tw * 0.85, ty - 0.002, tz - 0.003))
        vb_c = bm.verts.new((0.0, ty - 0.002, tz - 0.004))
        vb_l = bm.verts.new((-tw * 0.85, ty - 0.002, tz - 0.003))
        tongue_rings.append((vt_l, vt_c, vt_r, vb_r, vb_c, vb_l))
        
    bm.verts.ensure_lookup_table()
    for s in range(T_STEPS - 1):
        r0 = tongue_rings[s]
        r1 = tongue_rings[s + 1]
        bm.faces.new((r0[0], r1[0], r1[1], r0[1]))
        bm.faces.new((r0[1], r1[1], r1[2], r0[2]))
        bm.faces.new((r0[2], r1[2], r1[3], r0[3]))
        bm.faces.new((r0[5], r1[5], r1[0], r0[0]))
        bm.faces.new((r0[3], r1[3], r1[4], r0[4]))
        bm.faces.new((r0[4], r1[4], r1[5], r0[5]))
    bm.faces.new((tongue_rings[-1][0], tongue_rings[-1][1], tongue_rings[-1][2],
                  tongue_rings[-1][3], tongue_rings[-1][4], tongue_rings[-1][5]))
                  
    # Woven Tongue Label ("HOODOO")
    lbl_y = -0.026
    lbl_z = 0.098
    lv0 = bm.verts.new((-0.012, lbl_y - 0.008, lbl_z + 0.003))
    lv1 = bm.verts.new((-0.012, lbl_y + 0.008, lbl_z + 0.003))
    lv2 = bm.verts.new(( 0.012, lbl_y + 0.008, lbl_z + 0.003))
    lv3 = bm.verts.new(( 0.012, lbl_y - 0.008, lbl_z + 0.003))
    bm.faces.new((lv0, lv1, lv2, lv3))
    
    # -------------------------------------------------------------
    # 3. 5 FAT WHITE SKATE LACES (Crisp elevated crossover geometry)
    # -------------------------------------------------------------
    lace_configs = [
        (0.034, 0.056),
        (0.016, 0.068),
        (-0.002, 0.078),
        (-0.018, 0.088),
        (-0.032, 0.098),
    ]
    for ly, lz in lace_configs:
        lw = 0.0042 # half width
        th = 0.0022 # thickness
        
        lv0 = bm.verts.new((-0.015, ly - lw, lz))
        lv1 = bm.verts.new((-0.015, ly + lw, lz))
        lv2 = bm.verts.new(( 0.015, ly + lw, lz))
        lv3 = bm.verts.new(( 0.015, ly - lw, lz))
        
        lv0_t = bm.verts.new((-0.015, ly - lw, lz + th))
        lv1_t = bm.verts.new((-0.015, ly + lw, lz + th))
        lv2_t = bm.verts.new(( 0.015, ly + lw, lz + th))
        lv3_t = bm.verts.new(( 0.015, ly - lw, lz + th))
        
        bm.faces.new((lv0_t, lv1_t, lv2_t, lv3_t))
        bm.faces.new((lv0, lv3, lv2, lv1))
        bm.faces.new((lv0, lv1, lv1_t, lv0_t))
        bm.faces.new((lv2, lv3, lv3_t, lv2_t))
        bm.faces.new((lv1, lv2, lv2_t, lv1_t))
        bm.faces.new((lv3, lv0, lv0_t, lv3_t))
        
    # -------------------------------------------------------------
    # 4. SIGNATURE BRUSHED SILVER WAVE LOGO OVERLAY
    # -------------------------------------------------------------
    wave_pts = [
        (0.96, -0.060, 0.046),
        (0.97, -0.035, 0.052),
        (0.97, -0.010, 0.044),
        (0.96,  0.015, 0.048),
        (0.95,  0.035, 0.042),
    ]
    for sign in [1.0, -1.0]:
        w_bot = []
        w_top = []
        for xr, wy, wz in wave_pts:
            w_bot.append(bm.verts.new((sign * 0.038 * xr, wy, wz)))
            w_top.append(bm.verts.new((sign * 0.038 * xr, wy, wz + 0.007)))
        bm.verts.ensure_lookup_table()
        for k in range(len(wave_pts) - 1):
            if sign > 0:
                bm.faces.new((w_bot[k], w_bot[k+1], w_top[k+1], w_top[k]))
            else:
                bm.faces.new((w_bot[k], w_top[k], w_top[k+1], w_bot[k+1]))
                
    # -------------------------------------------------------------
    # 5. ATELIER DISPLAY PEDESTAL (Concrete/stone disc)
    # -------------------------------------------------------------
    PED_SEGS = 32
    ped_rad = 0.170
    center_ped_t = bm.verts.new((0.0, 0.01, -0.004))
    center_ped_b = bm.verts.new((0.0, 0.01, -0.022))
    ped_top = [bm.verts.new((math.cos(i*2*math.pi/PED_SEGS)*ped_rad, math.sin(i*2*math.pi/PED_SEGS)*ped_rad + 0.01, -0.004)) for i in range(PED_SEGS)]
    ped_bot = [bm.verts.new((math.cos(i*2*math.pi/PED_SEGS)*ped_rad*1.03, math.sin(i*2*math.pi/PED_SEGS)*ped_rad*1.03 + 0.01, -0.022)) for i in range(PED_SEGS)]
    
    bm.verts.ensure_lookup_table()
    for i in range(PED_SEGS):
        nxt = (i + 1) % PED_SEGS
        bm.faces.new((center_ped_t, ped_top[i], ped_top[nxt]))
        bm.faces.new((ped_top[i], ped_bot[i], ped_bot[nxt], ped_top[nxt]))
        bm.faces.new((center_ped_b, ped_bot[nxt], ped_bot[i]))
        
    # -------------------------------------------------------------
    # 6. SEAMLESS UV MAPPING
    # -------------------------------------------------------------
    uv_layer = bm.loops.layers.uv.new("UVMap")
    for face in bm.faces:
        for loop in face.loops:
            v = loop.vert
            u = max(0.0, min(1.0, (v.co.x + 0.08) / 0.16))
            v_uv = max(0.0, min(1.0, (v.co.y + 0.13) / 0.29))
            loop[uv_layer].uv = (u, v_uv)
            
    bm.to_mesh(mesh)
    bm.free()
    
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 1
    subsurf.render_levels = 2
    
    mat = bpy.data.materials.new(name="Sneaker_Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.88, 0.85, 0.82, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.55
        bsdf.inputs['Metallic'].default_value = 0.02
        if texture_path and os.path.exists(texture_path):
            tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
            tex_image.image = bpy.data.images.load(texture_path)
            mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
            
    obj.data.materials.append(mat)
    
    os.makedirs(os.path.dirname(os.path.abspath(out_glb_path)), exist_ok=True)
    bpy.ops.export_scene.gltf(filepath=out_glb_path, export_format='GLB', use_selection=True, export_apply=True)
    print(f"Exported hyperrealistic skate sneaker to {out_glb_path}")
    return obj

def test_render_sneaker(out_png):
    create_hyperrealistic_skate_sneaker("public/models/kicks_p9.glb")
    
    bpy.ops.object.light_add(type='SUN', location=(2.0, 2.5, 3.5))
    sun = bpy.context.active_object
    sun.data.energy = 4.0
    sun.data.color = (1.0, 0.98, 0.95)

    bpy.ops.object.light_add(type='POINT', location=(-1.5, -1.2, 1.8))
    fill = bpy.context.active_object
    fill.data.energy = 60.0
    fill.data.color = (0.75, 0.85, 1.0)

    bpy.ops.object.camera_add(location=(0.38, 0.38, 0.22))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(72), 0, math.radians(135))
    bpy.context.scene.camera = cam

    scene = bpy.context.scene
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    print('Rendered fixed sneaker to', out_png)

if __name__ == '__main__':
    out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
    out_png = os.path.join(out_dir, "test_render_hyper_sneaker_v5.png")
    test_render_sneaker(out_png)
