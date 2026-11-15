import bpy
import bmesh
import math
import os

def build_test_cylindrical_sleeves():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh = bpy.data.meshes.new("Tee_Mesh")
    obj = bpy.data.objects.new("Tee_Model", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bm = bmesh.new()
    
    # 1. Torso
    SEGS = 24
    torso_levels = [
        (-0.42, 0.248, 0.105, 0.095), # 0: Hem
        (-0.28, 0.244, 0.102, 0.092), # 1: Waist
        (-0.14, 0.250, 0.108, 0.096), # 2: Mid torso
        ( 0.04, 0.258, 0.114, 0.102), # 3: Lower chest
        ( 0.18, 0.265, 0.118, 0.104), # 4: Chest graphic center
        ( 0.30, 0.275, 0.114, 0.100), # 5: Armscye bottom
        ( 0.40, 0.295, 0.105, 0.092), # 6: Dropped shoulder seam
        ( 0.46, 0.190, 0.095, 0.082), # 7: Shoulder slope
        ( 0.49, 0.098, 0.078, 0.068), # 8: Collar base
        ( 0.52, 0.094, 0.074, 0.064), # 9: Collar top
    ]
    
    torso_rings = []
    for z, xr, yf, yb in torso_levels:
        ring = []
        for i in range(SEGS):
            ang = i * (2.0 * math.pi / SEGS)
            vx = math.cos(ang) * xr
            vy = (yf if math.sin(ang) <= 0 else yb) * math.sin(ang)
            ring.append(bm.verts.new((vx, vy, z)))
        torso_rings.append(ring)
        
    bm.verts.ensure_lookup_table()
    for r in range(5):
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((torso_rings[r][i], torso_rings[r][inxt], torso_rings[r+1][inxt], torso_rings[r+1][i]))
            
    # Bridge rings 6 -> 7 -> 8 -> 9
    for r in range(6, len(torso_levels) - 1):
        for i in range(SEGS):
            inxt = (i + 1) % SEGS
            bm.faces.new((torso_rings[r][i], torso_rings[r][inxt], torso_rings[r+1][inxt], torso_rings[r+1][i]))
            
    # Bridge armscye ring 5 -> 6 (excluding arm opening gaps)
    # Left opening (+X): skip 22, 23, 0, 1, 2
    # Right opening (-X): skip 10, 11, 12, 13, 14
    for i in range(SEGS):
        inxt = (i + 1) % SEGS
        if i in (22, 23, 0, 1) or inxt in (23, 0, 1, 2): continue
        if i in (10, 11, 12, 13) or inxt in (11, 12, 13, 14): continue
        bm.faces.new((torso_rings[5][i], torso_rings[5][inxt], torso_rings[6][inxt], torso_rings[6][i]))
        
    # 2. Cylindrical Sleeves with Planar Cross-Sections
    ARM_SEGS = 16
    arm_angle = math.radians(22) # 22 deg from vertical
    sin_a = math.sin(arm_angle)
    cos_a = math.cos(arm_angle)
    
    # 4 stations: deltoid to elbow
    tee_stations = [
        (0.00, 0.115, 0.110), # Armscye root
        (0.08, 0.112, 0.108), # Upper bicep
        (0.17, 0.110, 0.105), # Mid bicep
        (0.25, 0.108, 0.102), # Sleeve hem opening
        (0.26, 0.105, 0.100), # 1cm hem fold
    ]
    
    for sign in [1.0, -1.0]:
        c_root_x = sign * 0.285
        c_root_y = 0.005
        c_root_z = 0.355
        
        # Basis vectors for perpendicular planar rings:
        # Depth vector U is along Y
        # Width vector W is perpendicular to arm axis in XZ plane
        # A = (sign * sin_a, 0, -cos_a)
        # W = (sign * cos_a, 0, sin_a)
        
        prev_ring = None
        for s_dist, rw, ry in tee_stations:
            cx = c_root_x + sign * (sin_a * s_dist)
            cy = c_root_y
            cz = c_root_z - (cos_a * s_dist)
            
            s_ring = []
            for k in range(ARM_SEGS):
                theta = k * (2.0 * math.pi / ARM_SEGS)
                ca = math.cos(theta)
                sa = math.sin(theta)
                
                # Displacement along perpendicular basis W and U
                vx = cx + sign * (ca * rw * cos_a)
                vy = cy + sa * ry
                vz = cz + (ca * rw * sin_a)
                s_ring.append(bm.verts.new((vx, vy, vz)))
                
            bm.verts.ensure_lookup_table()
            if prev_ring:
                for k in range(ARM_SEGS):
                    knxt = (k + 1) % ARM_SEGS
                    if sign > 0:
                        bm.faces.new((prev_ring[k], prev_ring[knxt], s_ring[knxt], s_ring[k]))
                    else:
                        bm.faces.new((prev_ring[k], s_ring[k], s_ring[knxt], prev_ring[knxt]))
            prev_ring = s_ring
            
    # Atelier Bust Stand
    stand_levels = [
        (-0.62, 0.150),
        (-0.46, 0.120),
        ( 0.42, 0.090),
        ( 0.56, 0.045),
        ( 0.60, 0.038),
    ]
    stand_rings = []
    for sz, sr in stand_levels:
        s_ring = []
        for i in range(16):
            ang = i * (2.0 * math.pi / 16)
            s_ring.append(bm.verts.new((math.cos(ang) * sr, math.sin(ang) * sr, sz)))
        stand_rings.append(s_ring)
        
    bm.verts.ensure_lookup_table()
    for s in range(len(stand_levels) - 1):
        for i in range(16):
            inxt = (i + 1) % 16
            bm.faces.new((stand_rings[s][i], stand_rings[s][inxt], stand_rings[s+1][inxt], stand_rings[s+1][i]))
    bm.faces.new(reversed(stand_rings[0]))
    bm.faces.new(stand_rings[-1])
    
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
    
    mat = bpy.data.materials.new(name="Tee_Fabric")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.88, 0.86, 0.84, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.88
    obj.data.materials.append(mat)
    
    return obj

def test_render(out_png):
    build_test_cylindrical_sleeves()
    bpy.ops.object.light_add(type='POINT', location=(0.0, -1.8, 0.5))
    key = bpy.context.active_object
    key.data.energy = 90.0

    bpy.ops.object.light_add(type='POINT', location=(1.5, 1.2, 1.5))
    fill = bpy.context.active_object
    fill.data.energy = 60.0

    bpy.ops.object.camera_add(location=(0, -2.2, 0.05))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = cam

    scene = bpy.context.scene
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.render.filepath = out_png
    bpy.ops.render.render(write_still=True)
    print('Rendered test cylindrical sleeves to', out_png)

if __name__ == '__main__':
    out_dir = r"C:\Users\sanjo\.gemini\antigravity\brain\234f9af8-00da-4e48-94a4-b01c33156985"
    out_png = os.path.join(out_dir, "test_render_cylindrical_sleeves.png")
    test_render(out_png)
