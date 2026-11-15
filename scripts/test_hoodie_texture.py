import bpy
import bmesh
import math
import os

def render_hoodie_with_texture():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath="public/assets/models/perfect_hoodie.glb")
    
    # Camera
    cam_data = bpy.data.cameras.new("TestCam")
    cam_data.lens = 50
    cam_obj = bpy.data.objects.new("TestCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = (0, -2.4, -0.05)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    
    # Lights
    light1_data = bpy.data.lights.new("KeyLight", 'AREA')
    light1_data.energy = 350
    light1_data.size = 2.0
    light1 = bpy.data.objects.new("KeyLight", light1_data)
    bpy.context.collection.objects.link(light1)
    light1.location = (1.5, -2.0, 1.5)
    light1.rotation_euler = (math.radians(55), math.radians(20), math.radians(-30))
    
    light2_data = bpy.data.lights.new("FillLight", 'AREA')
    light2_data.energy = 150
    light2 = bpy.data.objects.new("FillLight", light2_data)
    bpy.context.collection.objects.link(light2)
    light2.location = (-1.8, -1.8, 0.8)
    
    light3_data = bpy.data.lights.new("RimLight", 'AREA')
    light3_data.energy = 500
    light3 = bpy.data.objects.new("RimLight", light3_data)
    bpy.context.collection.objects.link(light3)
    light3.location = (0, 2.0, 1.2)
    light3.rotation_euler = (math.radians(-45), 0, math.radians(180))
    
    # Assign Texture to Hoodie
    tex_path = os.path.abspath("public/assets/collection/hero_asphalt.png")
    for obj in bpy.data.objects:
        if "Hoodie" in obj.name:
            mat = bpy.data.materials.new("FabricWithTexture")
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            bsdf = nodes.get("Principled BSDF")
            if bsdf and os.path.exists(tex_path):
                tex_node = nodes.new("ShaderNodeTexImage")
                tex_node.image = bpy.data.images.load(tex_path)
                mat.node_tree.links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
                bsdf.inputs['Roughness'].default_value = 0.85
            obj.data.materials.clear()
            obj.data.materials.append(mat)
            
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderEngineEEVEE_NEXT') else 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    bpy.context.scene.render.film_transparent = True
    out_path = os.path.abspath("public/assets/models/render_perfect_front.png")
    bpy.context.scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered front view to: {out_path}")
    
    # Angle view
    cam_obj.location = (1.5, -1.8, 0.3)
    cam_obj.rotation_euler = (math.radians(80), 0, math.radians(40))
    out_angle = os.path.abspath("public/assets/models/render_perfect_angle.png")
    bpy.context.scene.render.filepath = out_angle
    bpy.ops.render.render(write_still=True)
    print(f"Rendered angle view to: {out_angle}")

if __name__ == "__main__":
    render_hoodie_with_texture()
