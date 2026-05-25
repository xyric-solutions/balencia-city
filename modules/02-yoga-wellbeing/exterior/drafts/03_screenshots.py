"""
Session 9 — Yoga & Wellbeing: Take viewport screenshots from 3 angles.
Run: blender -b yoga-exterior-s09.blend -P 03_screenshots.py
"""
import bpy
import math
import os
from mathutils import Vector

SAVE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/exterior/drafts"

# Render settings for screenshots
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGB'
bpy.context.scene.render.image_settings.compression = 15

# Use EEVEE for speed
try:
    engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'ShaderNodeEeveeSpecular') else 'BLENDER_EEVEE'
    bpy.context.scene.render.engine = engine
except Exception:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# Configure EEVEE for better screenshots
eevee = bpy.context.scene.eevee
if hasattr(eevee, 'use_bloom'):
    eevee.use_bloom = True
if hasattr(eevee, 'use_ssr'):
    eevee.use_ssr = True
if hasattr(eevee, 'use_gtao'):
    eevee.use_gtao = True

# Define 3 camera angles
camera_setups = [
    {
        "name": "front_elevation",
        "location": (0, -14, 4),
        "target": (0, 0, 1.0),
        "description": "Front elevation — identifies proportion and horizontal spread"
    },
    {
        "name": "three_quarter",
        "location": (12, -8, 5),
        "target": (0, 0, 1.0),
        "description": "3/4 angle — reveals dome shapes and floating walkways"
    },
    {
        "name": "distance_overview",
        "location": (16, -14, 8),
        "target": (0, 0, 0.8),
        "description": "Distance view — tests recognition at thumbnail scale"
    },
]

cam = bpy.data.objects.get("Overview_Camera")
if not cam:
    cam_data = bpy.data.cameras.new(name="Overview_Camera")
    cam_data.lens_unit = 'FOV'
    cam_data.angle = math.radians(45)
    cam_data.clip_start = 0.1
    cam_data.clip_end = 200
    cam = bpy.data.objects.new("Overview_Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam

for setup in camera_setups:
    print(f"Rendering: {setup['name']} — {setup['description']}")

    cam.location = setup["location"]
    target = Vector(setup["target"])
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    filepath = os.path.join(SAVE_DIR, f"s09_{setup['name']}.png")
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"  Saved: {filepath}")

print("\nAll 3 screenshots rendered.")
