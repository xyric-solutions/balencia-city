"""
Session 19 -- Render screenshots for verification.
Two views: overview camera, and from open wall looking in.
"""

import bpy
import math
import os

MODULE_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/04-knowledgebase"
SCREENSHOTS_DIR = os.path.join(MODULE_DIR, "screenshots")
BLEND_FILE = os.path.join(MODULE_DIR, "interior", "drafts", "knowledgebase-int-draft-19.blend")

# Open the blend file
bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

from mathutils import Vector

# Ensure EEVEE for fast render
try:
    engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'ShaderNodeEeveeSpecular') else 'BLENDER_EEVEE'
    bpy.context.scene.render.engine = engine
except Exception:
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 50  # Half-res for speed

# --- Screenshot 1: From camera_target perspective ---
# Create a temporary camera looking at the scene from an isometric-ish angle

# Find camera_target empty
cam_target = bpy.data.objects.get("camera_target")
target_loc = cam_target.location if cam_target else Vector((0, 0, 3.6))

# Position camera at an angle looking at the target
cam_pos = Vector((-3.5, -4.0, 5.0))
cam_data = bpy.data.cameras.new(name="Screenshot_Camera")
cam_data.lens = 24  # Wide angle to capture the room
cam_data.clip_end = 200
cam_obj = bpy.data.objects.new("Screenshot_Camera", cam_data)
bpy.context.collection.objects.link(cam_obj)
cam_obj.location = cam_pos

# Point at target
direction = target_loc - cam_pos
cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

bpy.context.scene.camera = cam_obj

# Render screenshot 1
output_1 = os.path.join(SCREENSHOTS_DIR, "s19-int-overview.png")
bpy.context.scene.render.filepath = output_1
bpy.ops.render.render(write_still=True)
print(f"Screenshot 1 saved: {output_1}")

# --- Screenshot 2: From the open wall looking in ---
cam_obj.location = (0, -3.5, 2.5)
direction2 = Vector((0, 0, 4.5)) - cam_obj.location
cam_obj.rotation_euler = direction2.to_track_quat('-Z', 'Y').to_euler()

output_2 = os.path.join(SCREENSHOTS_DIR, "s19-int-from-entrance.png")
bpy.context.scene.render.filepath = output_2
bpy.ops.render.render(write_still=True)
print(f"Screenshot 2 saved: {output_2}")

# --- Screenshot 3: Top-down view ---
cam_obj.location = (0, 0, 12)
cam_obj.rotation_euler = (0, 0, 0)  # Look straight down

output_3 = os.path.join(SCREENSHOTS_DIR, "s19-int-topdown.png")
bpy.context.scene.render.filepath = output_3
bpy.ops.render.render(write_still=True)
print(f"Screenshot 3 saved: {output_3}")

# Clean up temp camera
bpy.data.objects.remove(cam_obj, do_unlink=True)

print("All screenshots rendered.")
