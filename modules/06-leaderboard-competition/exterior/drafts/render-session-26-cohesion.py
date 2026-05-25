import importlib.util
import os
import sys

import bpy
from mathutils import Vector


ROOT = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3"
MODULE = os.path.join(ROOT, "modules/06-leaderboard-competition")
SCREENSHOTS = os.path.join(MODULE, "screenshots")
APPROVED_GLB = os.path.join(MODULE, "exterior/approved/leaderboard-ext.glb")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


lighting = load_module("balencia_lighting_s26_cohesion", os.path.join(ROOT, "shared/lighting-rig.py"))


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_shot(filename, camera_loc, target, lens=22):
    cam_data = bpy.data.cameras.new(filename.replace(".png", "_Camera"))
    cam = bpy.data.objects.new(filename.replace(".png", "_Camera"), cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = camera_loc
    cam.data.lens = lens
    cam.data.clip_start = 0.1
    cam.data.clip_end = 300
    look_at(cam, target)
    bpy.context.scene.camera = cam
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.image_settings.file_format = "PNG"
    path = os.path.join(SCREENSHOTS, filename)
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


bpy.ops.wm.read_factory_settings(use_empty=True)
lighting.setup_viewport_lighting()

imports = [
    ("sia", os.path.join(ROOT, "modules/00-sia-tower/exterior/approved/sia-tower-ext.glb"), (0, 0, 0)),
    ("fitness", os.path.join(ROOT, "modules/01-fitness/exterior/approved/fitness-ext.glb"), (25, 25, 0)),
    ("yoga", os.path.join(ROOT, "modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb"), (35, 10, 0)),
    ("finance", os.path.join(ROOT, "modules/03-finance/exterior/approved/finance-ext.glb"), (35, -5, 0)),
    ("knowledgebase", os.path.join(ROOT, "modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb"), (30, -20, 0)),
    ("chat", os.path.join(ROOT, "modules/05-chat-communication/exterior/approved/chat-ext.glb"), (18, -34, 0)),
    ("leaderboard", APPROVED_GLB, (-8, -44, 0)),
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

output = render_shot("s26_cohesion_all7.png", (82, -122, 78), (12, -16, 9), 22)
print(f"S26_COHESION_SCREENSHOT={output}")
