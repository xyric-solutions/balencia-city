"""
Session 23 QA import check for Chat & Communication interior draft GLB.
Imports the Draco-compressed GLB, verifies gates 3/5/7 technical facts,
and writes a JSON report for REVIEW.md.
"""

import json
import math
import os

import bpy


MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/05-chat-communication"
SHARED_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared"
DRAFT_GLB = os.path.join(MODULE_DIR, "interior", "drafts", "chat-int-draft-s23.glb")
QA_JSON = os.path.join(MODULE_DIR, "interior", "drafts", "session23-qa-import.json")


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


def tri_count(obj):
    if obj.type != "MESH":
        return 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    count = sum(len(poly.vertices) - 2 for poly in mesh.polygons)
    eval_obj.to_mesh_clear()
    return count


def is_identity_transform(obj):
    loc_ok = all(abs(v) < 1e-4 for v in obj.location)
    rot_ok = all(abs(v) < 1e-4 for v in obj.rotation_euler)
    scale_ok = all(abs(v - 1.0) < 1e-4 for v in obj.scale)
    return loc_ok and rot_ok and scale_ok


print("=== Session 23 QA Import Check ===")
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=DRAFT_GLB)

export_pipeline = load_python_module(os.path.join(SHARED_DIR, "export-pipeline.py"), "export_pipeline")
materials_ok = export_pipeline["verify_materials"]()

valid_slots = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
mesh_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
empty_objects = [obj for obj in bpy.data.objects if obj.type == "EMPTY"]
materials = sorted({mat.name for obj in mesh_objects for mat in obj.data.materials if mat})
invalid_materials = sorted(set(materials) - valid_slots)
slot_tris = {}
for obj in mesh_objects:
    slot = obj.data.materials[0].name if obj.data.materials else "none"
    slot_tris[slot] = slot_tris.get(slot, 0) + tri_count(obj)

verts = []
for obj in mesh_objects:
    for vertex in obj.data.vertices:
        world = obj.matrix_world @ vertex.co
        verts.append((world.x, world.y, world.z))

if verts:
    bbox = {
        "min": [min(v[i] for v in verts) for i in range(3)],
        "max": [max(v[i] for v in verts) for i in range(3)],
    }
else:
    bbox = {"min": [0, 0, 0], "max": [0, 0, 0]}

non_identity = [obj.name for obj in mesh_objects if not is_identity_transform(obj)]
empty_positions = {obj.name: [round(v, 4) for v in obj.location] for obj in empty_objects}
required_empties = {"light_0", "light_1", "light_2", "camera_target"}
missing_empties = sorted(required_empties - set(empty_positions))

report = {
    "glb": DRAFT_GLB,
    "file_size_bytes": os.path.getsize(DRAFT_GLB),
    "mesh_objects": len(mesh_objects),
    "empty_objects": len(empty_objects),
    "camera_objects": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
    "light_objects": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
    "total_tris": sum(tri_count(obj) for obj in mesh_objects),
    "materials": materials,
    "materials_ok_by_export_pipeline": materials_ok,
    "invalid_materials": invalid_materials,
    "uses_holo": "holo" in materials,
    "uses_energy": "energy" in materials,
    "slot_tris": slot_tris,
    "empty_positions": empty_positions,
    "missing_empties": missing_empties,
    "non_identity_mesh_transforms": non_identity,
    "bbox": bbox,
    "origin_bottom_center_pass": abs(bbox["min"][2]) < 1e-4,
    "budget_pass": 5000 <= sum(tri_count(obj) for obj in mesh_objects) <= 10000,
    "size_pass": 60 * 1024 <= os.path.getsize(DRAFT_GLB) <= 200 * 1024,
}

with open(QA_JSON, "w") as handle:
    json.dump(report, handle, indent=2, sort_keys=True)

print(json.dumps(report, indent=2, sort_keys=True))
