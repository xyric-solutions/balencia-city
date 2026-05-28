"""
Balencia City v3 - Session 76 Knowledgebase material-slot fix.

Assigns the approved `detail` material slot to the one Knowledgebase exterior
mesh that imported without a material, then refreshes the approved and app GLBs.
No geometry, transforms, origins, or layout positions are changed.
"""

import json
import os
import shutil
from datetime import date

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Desktop/balencia-city-v3"
SOURCE_GLB = "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"
DRAFT_GLB = "modules/04-knowledgebase/exterior/drafts/knowledgebase-ext-v2-draft-s76-material-fix.glb"
APPROVED_GLB = "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"
APP_GLB = "apps/balencia/public/models/structures/04-knowledgebase/knowledgebase-ext.glb"
QA_JSON = "modules/04-knowledgebase/exterior/drafts/session76-material-slot-fix.json"
ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}


def abs_path(path):
    return os.path.join(ROOT, path)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for mesh in list(bpy.data.meshes):
        if not mesh.users:
            bpy.data.meshes.remove(mesh)
    for material in list(bpy.data.materials):
        if not material.users:
            bpy.data.materials.remove(material)


def mesh_objects():
    return [obj for obj in bpy.data.objects if obj.type == "MESH"]


def material_root(material):
    return material.name.split(".")[0] if material else ""


def count_tris(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    total = 0
    for obj in objects:
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        mesh.calc_loop_triangles()
        total += len(mesh.loop_triangles)
        eval_obj.to_mesh_clear()
    return total


def world_bbox(objects):
    points = []
    for obj in objects:
        for corner in obj.bound_box:
            points.append(obj.matrix_world @ Vector(corner))
    mins = [min(point[i] for point in points) for i in range(3)]
    maxs = [max(point[i] for point in points) for i in range(3)]
    size = [maxs[i] - mins[i] for i in range(3)]
    center = [(mins[i] + maxs[i]) / 2 for i in range(3)]
    return {
        "min": [round(value, 4) for value in mins],
        "max": [round(value, 4) for value in maxs],
        "size": [round(value, 4) for value in size],
        "center": [round(value, 4) for value in center],
    }


def ensure_detail_material():
    for material in bpy.data.materials:
        if material_root(material) == "detail":
            return material
    material = bpy.data.materials.new("detail")
    material.diffuse_color = (0.086, 0.086, 0.118, 1.0)
    return material


def assign_missing_detail_slots():
    detail = ensure_detail_material()
    fixed = []
    still_missing = []
    for obj in mesh_objects():
        if obj.data.materials and all(slot is not None for slot in obj.data.materials):
            continue
        if "detail" not in obj.name.lower():
            still_missing.append(obj.name)
            continue
        obj.data.materials.clear()
        obj.data.materials.append(detail)
        fixed.append(obj.name)
    if still_missing:
        raise RuntimeError(f"Unexpected non-detail meshes without material: {still_missing}")
    if not fixed:
        raise RuntimeError("No missing Knowledgebase detail material slot was found.")
    return fixed


def validate(path, fixed):
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=abs_path(path))
    objects = mesh_objects()
    missing_materials = [obj.name for obj in objects if not obj.data.materials or any(slot is None for slot in obj.data.materials)]
    material_roots = sorted({material_root(slot) for obj in objects for slot in obj.data.materials if slot})
    invalid_materials = sorted(root for root in material_roots if root not in ALLOWED_MATERIALS)
    roots = sorted(obj.name for obj in bpy.data.objects if obj.parent is None)
    cameras_lights = sorted(obj.name for obj in bpy.data.objects if obj.type in {"CAMERA", "LIGHT"})
    size_bytes = os.path.getsize(abs_path(path))
    qa = {
        "session": 76,
        "date": str(date.today()),
        "path": path,
        "fixed_objects": fixed,
        "object_count": len(objects),
        "tris": count_tris(objects),
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "bbox": world_bbox(objects),
        "material_roots": material_roots,
        "missing_materials": missing_materials,
        "invalid_materials": invalid_materials,
        "roots": roots,
        "cameras_lights": cameras_lights,
    }
    qa["passed"] = (
        qa["object_count"] > 0
        and not qa["missing_materials"]
        and not qa["invalid_materials"]
        and not qa["cameras_lights"]
        and roots == ["knowledgebase-ext"]
        and qa["bbox"]["min"][2] >= -0.02
    )
    with open(abs_path(QA_JSON), "w", encoding="utf-8") as handle:
        json.dump(qa, handle, indent=2)
    return qa


def main():
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=abs_path(SOURCE_GLB))
    fixed = assign_missing_detail_slots()
    bpy.ops.export_scene.gltf(
        filepath=abs_path(DRAFT_GLB),
        export_format="GLB",
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_yup=True,
        export_apply=True,
        export_texcoords=True,
        export_normals=True,
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
    )
    qa = validate(DRAFT_GLB, fixed)
    if not qa["passed"]:
        raise RuntimeError(f"Knowledgebase material-slot fix failed: {qa}")
    shutil.copy2(abs_path(DRAFT_GLB), abs_path(APPROVED_GLB))
    shutil.copy2(abs_path(DRAFT_GLB), abs_path(APP_GLB))
    print(json.dumps(qa, indent=2))


if __name__ == "__main__":
    main()
