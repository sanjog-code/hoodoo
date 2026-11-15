import bpy
import bmesh
import math
import os

def render_hoodie_view():
    # Load or generate master hoodie
    # Let's inspect the test_hoodie.glb
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath="public/assets/models/test_tailored.glb")
    
    # Setup Camera
    cam_data = bpy.data.cameras.new("TestCam")
    cam_data.lens = 50 # 50mm telephoto
    cam_obj = bpy.data.objects.new("TestCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = (0, -2.4, 0.0)
    cam_obj.rotation_euler = (math.radians(90), 0, 0)
    
    # Setup Studio Lights
    light1_data = bpy.data.lights.new("KeyLight", 'AREA')
    light1_data.energy = 300
    light1_data.size = 2.0
    light1 = bpy.data.objects.new("KeyLight", light1_data)
    bpy.context.collection.objects.link(light1)
    light1.location = (1.5, -1.8, 1.8)
    light1.rotation_euler = (math.radians(55), math.radians(20), math.radians(-30))
    
    light2_data = bpy.data.lights.new("FillLight", 'AREA')
    light2_data.energy = 120
    light2_data.size = 2.0
    light2 = bpy.data.objects.new("FillLight", light2_data)
    bpy.context.collection.objects.link(light2)
    light2.location = (-1.8, -1.5, 0.8)
    
    light3_data = bpy.data.lights.new("RimLight", 'AREA')
    light3_data.energy = 450
    light3_data.size = 1.5
    light3 = bpy.data.objects.new("RimLight", light3_data)
    bpy.context.collection.objects.link(light3)
    light3.location = (0, 2.0, 1.5)
    light3.rotation_euler = (math.radians(-45), 0, math.radians(180))
    
    # Assign Charcoal Fleece Material to Hoodie
    for obj in bpy.data.objects:
        if "Hoodie" in obj.name:
            mat = bpy.data.materials.new("TestFleece")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs['Base Color'].default_value = (0.08, 0.08, 0.09, 1.0)
                bsdf.inputs['Roughness'].default_value = 0.85
            obj.data.materials.clear()
            obj.data.materials.append(mat)
        elif "Cylinder" in obj.name or "Mannequin" in obj.name:
            mat = bpy.data.materials.new("TestMetal")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs['Base Color'].default_value = (0.04, 0.04, 0.04, 1.0)
                bsdf.inputs['Metallic'].default_value = 0.9
                bsdf.inputs['Roughness'].default_value = 0.2
            obj.data.materials.clear()
            obj.data.materials.append(mat)
            
    # Render Settings
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'RenderEngineEEVEE_NEXT') else 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1024
    bpy.context.scene.render.resolution_y = 1024
    bpy.context.scene.render.film_transparent = True
    out_path = os.path.abspath("public/assets/models/render_tailored_front.png")
    bpy.context.scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print(f"Rendered front view to: {out_path}")
    
    # Render Angle View
    cam_obj.location = (1.6, -1.8, 0.4)
    cam_obj.rotation_euler = (math.radians(78), 0, math.radians(40))
    out_angle = os.path.abspath("public/assets/models/render_tailored_angle.png")
    bpy.context.scene.render.filepath = out_angle
    bpy.ops.render.render(write_still=True)
    print(f"Rendered angle view to: {out_angle}")

if __name__ == "__main__":
    render_hoodie_view()
