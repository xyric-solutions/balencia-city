"""
Balencia City v3 - Session 74 focused Knowledgebase export cleanup.

Removes the reusable glyph master that was accidentally exported as a second
root, then refreshes the approved/app GLB and Session 74 metrics.
"""

import json
import os
import shutil
from datetime import date

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Desktop/balencia-city-v3"
SOURCE_GLB = "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"
DRAFT_GLB = "modules/04-knowledgebase/exterior/drafts/knowledgebase-ext-v2-draft-s74.glb"
APPROVED_GLB = "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"
APP_GLB = "apps/balencia/public/models/structures/04-knowledgebase/knowledgebase-ext.glb"
METRICS = "modules/04-knowledgebase/exterior/drafts/session74-v2-metrics.json"
QA_IMPORT = "modules/04-knowledgebase/exterior/drafts/session74-qa-import.json"
AUDIT_JSON = "assembly/audit/session-74-urban-polish.json"
AUDIT_MD = "assembly/audit/session-74-urban-polish.md"
ALLOWED_MATERIALS = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}


def abs_path(path):
    return os.path.join(ROOT, path)


def material_base_name(material):
    return material.name.split(".")[0] if material else ""


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        if not mesh.users:
            bpy.data.meshes.remove(mesh)
    for material in list(bpy.data.materials):
        if not material.users:
            bpy.data.materials.remove(material)


def mesh_objects():
    return [obj for obj in bpy.data.objects if obj.type == "MESH"]


def count_tris(objects=None):
    total = 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in objects or mesh_objects():
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        mesh.calc_loop_triangles()
        total += len(mesh.loop_triangles)
        eval_obj.to_mesh_clear()
    return total


def world_bbox(objects=None):
    points = []
    for obj in objects or mesh_objects():
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


def remove_helper_roots():
    for obj in list(bpy.data.objects):
        if "reusable_archive_glyph_master" in obj.name:
            bpy.data.objects.remove(obj, do_unlink=True)


def parent_under_clean_root():
    for obj in list(bpy.data.objects):
        if obj.name == "knowledgebase-ext":
            bpy.data.objects.remove(obj, do_unlink=True)
    root = bpy.data.objects.new("knowledgebase-ext", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in mesh_objects():
        obj.parent = root


def validate(path):
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=abs_path(path))
    objects = mesh_objects()
    materials = sorted({material_base_name(mat) for obj in objects for mat in obj.data.materials if mat})
    invalid_materials = sorted(slot for slot in materials if slot not in ALLOWED_MATERIALS)
    size_bytes = os.path.getsize(abs_path(path))
    qa = {
        "path": path,
        "object_count": len(objects),
        "tris": count_tris(objects),
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 1),
        "bbox": world_bbox(objects),
        "materials": materials,
        "invalid_materials": invalid_materials,
        "cameras_lights": [obj.name for obj in bpy.data.objects if obj.type in {"CAMERA", "LIGHT"}],
        "roots": [obj.name for obj in bpy.data.objects if obj.parent is None],
    }
    qa["passed"] = (
        qa["object_count"] > 0
        and 15000 <= qa["tris"] <= 20000
        and 100 * 1024 <= qa["size_bytes"] <= 400 * 1024
        and not qa["invalid_materials"]
        and not qa["cameras_lights"]
        and qa["roots"] == ["knowledgebase-ext"]
        and qa["bbox"]["min"][2] >= -0.02
    )
    with open(abs_path(QA_IMPORT), "w", encoding="utf-8") as handle:
        json.dump(qa, handle, indent=2)
    return qa


def update_metrics(qa):
    with open(abs_path(METRICS), "r", encoding="utf-8") as handle:
        metrics = json.load(handle)
    metrics["date"] = str(date.today())
    metrics["final_live_tris"] = qa["tris"]
    metrics["final_live_objects"] = qa["object_count"]
    metrics["final_tris"] = qa["tris"]
    metrics["final_objects"] = qa["object_count"]
    metrics["final_size_bytes"] = qa["size_bytes"]
    metrics["final_size_kb"] = qa["size_kb"]
    metrics["bbox"] = qa["bbox"]
    metrics["qa"] = qa
    metrics["budget"]["status"] = "APPROVED"
    with open(abs_path(METRICS), "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
    return metrics


def update_audit(metrics):
    with open(abs_path(AUDIT_JSON), "r", encoding="utf-8") as handle:
        audit = json.load(handle)
    for result in audit.get("results", []):
        if result.get("module") == "Knowledgebase":
            result["final_live_tris"] = metrics["final_live_tris"]
            result["final_live_objects"] = metrics["final_live_objects"]
            result["final_tris"] = metrics["final_tris"]
            result["final_objects"] = metrics["final_objects"]
            result["final_size_bytes"] = metrics["final_size_bytes"]
            result["final_size_kb"] = metrics["final_size_kb"]
            result["bbox"] = metrics["bbox"]
            result["qa"] = metrics["qa"]
    for item in audit.get("pre_audit", []):
        if item.get("id") == "knowledgebase":
            item["tris"] = metrics["qa"]["tris"]
            item["object_count"] = metrics["qa"]["object_count"]
            item["size_bytes"] = metrics["qa"]["size_bytes"]
            item["size_kb"] = metrics["qa"]["size_kb"]
            item["bbox"] = metrics["qa"]["bbox"]
            item["materials"] = metrics["qa"]["materials"]
            item["invalid_materials"] = metrics["qa"]["invalid_materials"]
    with open(abs_path(AUDIT_JSON), "w", encoding="utf-8") as handle:
        json.dump(audit, handle, indent=2)

    with open(abs_path(AUDIT_MD), "r", encoding="utf-8") as handle:
        report = handle.read()
    report = report.replace(
        "| Knowledgebase | 7,532 | 15,260 | 9 | 102.8 KB | Approved |",
        f"| Knowledgebase | 7,532 | {metrics['final_tris']:,} | {metrics['final_objects']} | {metrics['final_size_kb']} KB | Approved |",
    )
    with open(abs_path(AUDIT_MD), "w", encoding="utf-8") as handle:
        handle.write(report)


def main():
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=abs_path(SOURCE_GLB))
    remove_helper_roots()
    parent_under_clean_root()
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
    qa = validate(DRAFT_GLB)
    if not qa["passed"]:
        raise RuntimeError(f"Knowledgebase cleanup QA failed: {qa}")
    shutil.copy2(abs_path(DRAFT_GLB), abs_path(APPROVED_GLB))
    shutil.copy2(abs_path(DRAFT_GLB), abs_path(APP_GLB))
    metrics = update_metrics(qa)
    update_audit(metrics)
    print(json.dumps(qa, indent=2))


if __name__ == "__main__":
    main()
