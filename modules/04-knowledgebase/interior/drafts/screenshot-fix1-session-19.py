"""
Screenshot script for Session 19 Fix 1 -- Knowledgebase Interior
Takes 3 screenshots from different angles.
"""
import bpy
import math
import os

MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")
BLEND_FILE = os.path.join(MODULE_DIR, "interior", "drafts", "knowledgebase-int-draft-19-fix1.blend")

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Load the blend file
bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

# Room dimensions
ROOM_W = 3.6
ROOM_D = 3.2
ROOM_H = 9.0

# Setup render settings
try:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
except TypeError:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 50  # Half res for speed
bpy.context.scene.render.film_transparent = False

# Set world background to dark
world = bpy.context.scene.world
if world and world.use_nodes:
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.039, 0.039, 0.059, 1.0)  # #0A0A0F

# Remove existing cameras
for obj in list(bpy.data.objects):
    if obj.type == 'CAMERA':
        bpy.data.objects.remove(obj, do_unlink=True)

# Screenshot configurations
screenshots = [
    {
        "name": "s19-fix1-int-overview",
        "location": (5.0, -4.0, 6.0),
        "target": (0, 0, ROOM_H * 0.4),
        "lens": 28,
    },
    {
        "name": "s19-fix1-int-from-entrance",
        "location": (0, -ROOM_D / 2 - 2.0, ROOM_H * 0.3),
        "target": (0, 0, ROOM_H * 0.4),
        "lens": 35,
    },
    {
        "name": "s19-fix1-int-topdown",
        "location": (0, 0, ROOM_H + 4.0),
        "target": (0, 0, ROOM_H * 0.5),
        "lens": 35,
    },
]

for config in screenshots:
    # Add camera
    bpy.ops.object.camera_add(location=config["location"])
    cam = bpy.context.active_object
    cam.name = f"cam_{config['name']}"
    cam.data.lens = config["lens"]
    cam.data.clip_start = 0.1
    cam.data.clip_end = 100

    # Point camera at target
    from mathutils import Vector
    target = Vector(config["target"])
    direction = target - Vector(config["location"])
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cam.rotation_euler = rot_quat.to_euler()

    # Set as active camera
    bpy.context.scene.camera = cam

    # Render
    filepath = os.path.join(SCREENSHOTS_DIR, f"{config['name']}.png")
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"  Rendered: {filepath}")

    # Remove camera after render
    bpy.data.objects.remove(cam, do_unlink=True)

print("=== All screenshots rendered ===")
