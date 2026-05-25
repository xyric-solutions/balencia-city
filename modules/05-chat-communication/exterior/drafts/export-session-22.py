import importlib.util
import json
import os
import sys

import bpy
from mathutils import Matrix, Vector


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/05-chat-communication")
APPROVED = os.path.join(MODULE, "exterior/approved")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
CHAT_GLB = os.path.join(APPROVED, "chat-ext.glb")
ALLOWED_MATERIALS = {"base", "accent", "detail", "glass", "emissive", "energy"}

os.makedirs(APPROVED, exist_ok=True)
os.makedirs(SCREENSHOTS, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_export", os.path.join(ROOT, "shared/lighting-rig.py"))


def count_tris():
    total = 0
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.data.calc_loop_triangles()
            total += len(obj.data.loop_triangles)
    return total


def material_tris():
    totals = {}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        obj.data.calc_loop_triangles()
        mat = obj.data.materials[0].name if obj.data.materials else "NONE"
        mat = mat.split(".")[0]
        totals[mat] = totals.get(mat, 0) + len(obj.data.loop_triangles)
    return dict(sorted(totals.items()))


def mesh_count():
    return sum(1 for obj in bpy.data.objects if obj.type == "MESH")


def non_identity_transforms():
    issues = []
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        if any(abs(v) > 1e-5 for v in obj.location):
            issues.append(obj.name)
            continue
        if any(abs(v) > 1e-5 for v in obj.rotation_euler):
            issues.append(obj.name)
            continue
        if any(abs(v - 1) > 1e-5 for v in obj.scale):
            issues.append(obj.name)
    return issues


def material_base_name(material):
    return material.name.split(".")[0] if material else ""


def normalize_material_slots():
    fallback = bpy.data.materials.get("detail")
    if fallback is None:
        fallback = next((mat for mat in bpy.data.materials if material_base_name(mat) in ALLOWED_MATERIALS), None)
    if fallback is None:
        raise RuntimeError("No allowed Balencia material available for slot normalization")

    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        if not obj.data.materials:
            obj.data.materials.append(fallback)
        for index, material in enumerate(obj.data.materials):
            if material_base_name(material) not in ALLOWED_MATERIALS:
                obj.data.materials[index] = fallback

        used_slots = {polygon.material_index for polygon in obj.data.polygons}
        for index in reversed(range(len(obj.data.materials))):
            if index not in used_slots and len(obj.data.materials) > 1:
                obj.data.materials.pop(index=index)

    for material in list(bpy.data.materials):
        if material_base_name(material) not in ALLOWED_MATERIALS and material.users == 0:
            bpy.data.materials.remove(material)


def bbox():
    min_v = Vector((1e9, 1e9, 1e9))
    max_v = Vector((-1e9, -1e9, -1e9))
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        obj.data.update()
        for vertex in obj.data.vertices:
            v = obj.matrix_world @ vertex.co
            min_v.x = min(min_v.x, v.x)
            min_v.y = min(min_v.y, v.y)
            min_v.z = min(min_v.z, v.z)
            max_v.x = max(max_v.x, v.x)
            max_v.y = max(max_v.y, v.y)
            max_v.z = max(max_v.z, v.z)
    return {"min": [round(min_v.x, 4), round(min_v.y, 4), round(min_v.z, 4)], "max": [round(max_v.x, 4), round(max_v.y, 4), round(max_v.z, 4)]}


def bbox_vectors():
    min_v = Vector((1e9, 1e9, 1e9))
    max_v = Vector((-1e9, -1e9, -1e9))
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        obj.data.update()
        for vertex in obj.data.vertices:
            v = obj.matrix_world @ vertex.co
            min_v.x = min(min_v.x, v.x)
            min_v.y = min(min_v.y, v.y)
            min_v.z = min(min_v.z, v.z)
            max_v.x = max(max_v.x, v.x)
            max_v.y = max(max_v.y, v.y)
            max_v.z = max(max_v.z, v.z)
    return min_v, max_v


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_shot(filename, camera_loc, target, lens=38):
    cam_data = bpy.data.cameras.new("Cohesion_Camera")
    cam = bpy.data.objects.new("Cohesion_Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    cam_data.lens = lens
    cam_data.clip_end = 250
    look_at(cam, target)
    bpy.context.scene.camera = cam
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.filepath = os.path.join(SCREENSHOTS, filename)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)


def clear_scene():
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def export_chat():
    for obj in list(bpy.data.objects):
        if obj.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(obj, do_unlink=True)
        elif obj.type == "EMPTY":
            bpy.data.objects.remove(obj, do_unlink=True)

    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(obj.matrix_world.copy())
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)
        obj.parent = None

    normalize_material_slots()

    min_v, max_v = bbox_vectors()
    center_x = (min_v.x + max_v.x) / 2
    center_y = (min_v.y + max_v.y) / 2
    lift_z = -min_v.z
    correction = Matrix.Translation(Vector((-center_x, -center_y, lift_z)))
    for obj in [obj for obj in bpy.data.objects if obj.type == "MESH"]:
        obj.data.transform(correction)
        obj.data.update()
        obj.matrix_world = Matrix.Identity(4)

    root = bpy.data.objects.new("chat-ext", None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.25
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.parent = root

    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

    bpy.ops.export_scene.gltf(
        filepath=CHAT_GLB,
        export_format="GLB",
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_yup=True,
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
    )
    return {
        "mesh_objects": mesh_count(),
        "tris": count_tris(),
        "material_tris": material_tris(),
        "bbox": bbox(),
        "non_identity_transforms": non_identity_transforms(),
        "cameras": sum(1 for obj in bpy.data.objects if obj.type == "CAMERA"),
        "lights": sum(1 for obj in bpy.data.objects if obj.type == "LIGHT"),
        "glb_bytes": os.path.getsize(CHAT_GLB),
    }


def create_cohesion_screenshot():
    clear_scene()
    lighting.setup_viewport_lighting()
    imports = [
        ("sia", os.path.join(ROOT, "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb"), (0, 0, 0)),
        ("fitness", os.path.join(ROOT, "modules/01-fitness/exterior/approved/fitness-ext.glb"), (25, 25, 0)),
        ("yoga", os.path.join(ROOT, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb"), (35, 10, 0)),
        ("finance", os.path.join(ROOT, "modules/03-finance/exterior/approved/finance-ext.glb"), (35, -5, 0)),
        ("knowledgebase", os.path.join(ROOT, "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"), (30, -20, 0)),
        ("chat", CHAT_GLB, (18, -18, 0)),
    ]
    for label, path, loc in imports:
        if not os.path.exists(path):
            continue
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=path)
        for obj in [obj for obj in bpy.data.objects if obj not in before]:
            obj.location.x += loc[0]
            obj.location.y += loc[1]
            obj.location.z += loc[2]
            obj.name = f"{label}_{obj.name}"
    render_shot("s22b_cohesion_all6.png", (70, -92, 54), (18, -6, 8), 30)


metrics = {"final": export_chat()}
create_cohesion_screenshot()
print("SESSION22_EXPORT_METRICS=" + json.dumps(metrics, indent=2))
