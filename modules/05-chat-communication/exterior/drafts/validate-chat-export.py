import json
import os

import bpy
from mathutils import Vector


GLB = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/05-chat-communication/exterior/approved/chat-ext.glb"
ALLOWED = {"base", "accent", "detail", "glass", "emissive", "energy", "holo"}


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def count_tris():
    total = 0
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.data.calc_loop_triangles()
            total += len(obj.data.loop_triangles)
    return total


def bbox():
    min_v = Vector((1e9, 1e9, 1e9))
    max_v = Vector((-1e9, -1e9, -1e9))
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for vertex in obj.data.vertices:
            v = obj.matrix_world @ vertex.co
            min_v.x = min(min_v.x, v.x)
            min_v.y = min(min_v.y, v.y)
            min_v.z = min(min_v.z, v.z)
            max_v.x = max(max_v.x, v.x)
            max_v.y = max(max_v.y, v.y)
            max_v.z = max(max_v.z, v.z)
    return {
        "min": [round(min_v.x, 4), round(min_v.y, 4), round(min_v.z, 4)],
        "max": [round(max_v.x, 4), round(max_v.y, 4), round(max_v.z, 4)],
    }


clear_scene()
bpy.ops.import_scene.gltf(filepath=GLB)
materials = sorted({
    mat.name.split(".")[0]
    for obj in bpy.data.objects
    if obj.type == "MESH"
    for mat in obj.data.materials
    if mat
})
metrics = {
    "mesh_objects": sum(1 for obj in bpy.data.objects if obj.type == "MESH"),
    "tris": count_tris(),
    "materials": materials,
    "rogue_materials": [mat for mat in materials if mat not in ALLOWED],
    "cameras": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
    "lights": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
    "bbox": bbox(),
    "glb_bytes": os.path.getsize(GLB),
}
print("CHAT_EXPORT_VALIDATION=" + json.dumps(metrics, indent=2))
