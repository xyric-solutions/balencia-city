"""
Finance Tower — Retake screenshots after proportion fixes.
"""
import bpy
import math
from mathutils import Vector

cam = bpy.data.objects.get("Overview_Camera")

# Screenshot 1: Front Elevation
cam.location = (0, -25, 8)
target = Vector((0, 0, 8))
direction = target - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

bpy.context.scene.render.filepath = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s13_front_elevation.png"
bpy.ops.render.render(write_still=True)
print("Screenshot 1: Front elevation")

# Screenshot 2: 3/4 Angle
cam.location = (18, -18, 10)
target = Vector((0, 0, 7))
direction = target - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

bpy.context.scene.render.filepath = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s13_three_quarter.png"
bpy.ops.render.render(write_still=True)
print("Screenshot 2: 3/4 angle")

# Screenshot 3: Distance Overview (farther back, full building in frame)
cam.location = (0, -40, 12)
target = Vector((0, 0, 7))
direction = target - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

bpy.context.scene.render.filepath = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s13_distance_overview.png"
bpy.ops.render.render(write_still=True)
print("Screenshot 3: Distance overview")

print("All screenshots captured.")
