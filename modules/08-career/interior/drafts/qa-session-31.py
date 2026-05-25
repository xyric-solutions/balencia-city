"""
Session 31 QA import check for Career interior draft GLB.

Verifies Gates 3, 5, and 7 technical facts, records Gate 4 screenshot
evidence, and promotes the draft GLB to approved when all checks pass.
"""

import json
import os
import shutil

import bpy


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE_DIR = os.path.join(ROOT, "modules/08-career")
SHARED_DIR = os.path.join(ROOT, "shared")
DRAFT_GLB = os.path.join(MODULE_DIR, "interior", "drafts", "career-int-draft-s31.glb")
APPROVED_GLB = os.path.join(MODULE_DIR, "interior", "approved", "career-int.glb")
QA_JSON = os.path.join(MODULE_DIR, "interior", "drafts", "session31-qa-import.json")

VALID_SLOTS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
REQUIRED_EMPTY_NAMES = {"light_0", "light_1", "light_2", "camera_target"}


def load_python_module(path, module_name):
    namespace = {"__name__": module_name, "__file__": path}
    with open(path, "r") as handle:
        exec(compile(handle.read(), path, "exec"), namespace)
    return namespace


def base_name(name):
    return name.split(".")[0]


def material_base_name(material):
    return base_name(material.name) if material else "none"


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


def bbox_for_meshes(mesh_objects):
    verts = []
    for obj in mesh_objects:
        for vertex in obj.data.vertices:
            world = obj.matrix_world @ vertex.co
            verts.append((world.x, world.y, world.z))
    if not verts:
        return {"min": [0, 0, 0], "max": [0, 0, 0]}
    return {
        "min": [min(v[i] for v in verts) for i in range(3)],
        "max": [max(v[i] for v in verts) for i in range(3)],
    }


def count_objects_with_prefix(mesh_objects, prefixes):
    return sum(1 for obj in mesh_objects if any(base_name(obj.name).startswith(prefix) for prefix in prefixes))


print("=== Session 31 QA Import Check ===")
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=DRAFT_GLB)

export_pipeline = load_python_module(os.path.join(SHARED_DIR, "export-pipeline.py"), "export_pipeline_s31")
materials_ok = export_pipeline["verify_materials"]()

mesh_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
empty_objects = [obj for obj in bpy.data.objects if obj.type == "EMPTY"]
material_names = sorted({material_base_name(mat) for obj in mesh_objects for mat in obj.data.materials if mat})
invalid_materials = sorted(set(material_names) - VALID_SLOTS)
slot_tris = {}
for obj in mesh_objects:
    slot = material_base_name(obj.data.materials[0]) if obj.data.materials else "none"
    slot_tris[slot] = slot_tris.get(slot, 0) + tri_count(obj)

empty_positions = {
    base_name(obj.name): [round(obj.location.x, 4), round(obj.location.y, 4), round(obj.location.z, 4)]
    for obj in empty_objects
}
missing_empties = sorted(REQUIRED_EMPTY_NAMES - set(empty_positions))

bbox = bbox_for_meshes(mesh_objects)
total_tris = sum(tri_count(obj) for obj in mesh_objects)
file_size = os.path.getsize(DRAFT_GLB)
non_identity = [obj.name for obj in mesh_objects if not is_identity_transform(obj)]

prop_counts = {
    "room_shell": count_objects_with_prefix(
        mesh_objects,
        ["executive_command_", "open_front_threshold", "side_wall_", "floor_embedded_directional_"],
    ),
    "growth_chart_focal": count_objects_with_prefix(mesh_objects, ["growth_chart_"]),
    "advisor_workstations": count_objects_with_prefix(mesh_objects, ["ai_career_advisor_"]),
    "focus_booths": count_objects_with_prefix(mesh_objects, ["deep_focus_productivity_booth_"]),
    "strategy_table": count_objects_with_prefix(mesh_objects, ["strategy_room_"]),
    "skill_growth_trees": count_objects_with_prefix(mesh_objects, ["skill_growth_tree_"]),
    "upper_skybridge": count_objects_with_prefix(mesh_objects, ["upper_networking_skybridge_"]),
    "floor_paths": count_objects_with_prefix(mesh_objects, ["floor_embedded_directional_", "executive_command_room_shell_emissive"]),
}

checks = {
    "gate3_material_names_pass": materials_ok and not invalid_materials,
    "gate3_energy_holo_usage_pass": "energy" in material_names and "holo" not in material_names,
    "gate5_triangle_budget_pass": 5000 <= total_tris <= 10000,
    "gate5_file_size_pass": 60 * 1024 <= file_size <= 200 * 1024,
    "gate5_no_cameras_lights_pass": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA") == 0
    and sum(1 for obj in bpy.data.objects if obj.type == "LIGHT") == 0,
    "gate5_origin_bottom_pass": abs(bbox["min"][2]) < 1e-4,
    "gate5_transforms_pass": not non_identity,
    "gate7_required_empties_pass": not missing_empties,
    "gate7_focal_point_pass": prop_counts["growth_chart_focal"] >= 5,
    "gate7_props_present_pass": all(
        [
            prop_counts["room_shell"] >= 4,
            prop_counts["advisor_workstations"] >= 5,
            prop_counts["focus_booths"] >= 4,
            prop_counts["strategy_table"] >= 5,
            prop_counts["skill_growth_trees"] >= 4,
            prop_counts["upper_skybridge"] >= 4,
            prop_counts["floor_paths"] >= 1,
        ]
    ),
}

qa_pass = all(checks.values())
if qa_pass:
    os.makedirs(os.path.dirname(APPROVED_GLB), exist_ok=True)
    shutil.copyfile(DRAFT_GLB, APPROVED_GLB)

report = {
    "glb": DRAFT_GLB,
    "approved_glb": APPROVED_GLB if qa_pass else None,
    "file_size_bytes": file_size,
    "mesh_objects": len(mesh_objects),
    "empty_objects": len(empty_objects),
    "camera_objects": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
    "light_objects": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
    "total_tris": total_tris,
    "materials": material_names,
    "materials_ok_by_export_pipeline": materials_ok,
    "invalid_materials": invalid_materials,
    "uses_energy": "energy" in material_names,
    "uses_holo": "holo" in material_names,
    "slot_tris": dict(sorted(slot_tris.items())),
    "empty_positions": empty_positions,
    "missing_empties": missing_empties,
    "non_identity_mesh_transforms": non_identity,
    "bbox": bbox,
    "prop_counts": prop_counts,
    "checks": checks,
    "qa_pass": qa_pass,
    "dark_first_screenshot": "screenshots/s31-int-dark-first.png",
}

with open(QA_JSON, "w") as handle:
    json.dump(report, handle, indent=2, sort_keys=True)

print(json.dumps(report, indent=2, sort_keys=True))
