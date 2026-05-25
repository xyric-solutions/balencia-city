"""
Finance Tower (Module #03) — Screenshot Captures
Take 3 viewport screenshots from different angles for silhouette evaluation.
"""
import bpy
import math
from mathutils import Vector

# Get camera
cam = bpy.data.objects.get("Overview_Camera")
if not cam:
    print("ERROR: No Overview_Camera found")
else:
    # ============================================================
    # Screenshot 1: Front Elevation
    # ============================================================
    cam.location = (0, -25, 8)
    target = Vector((0, 0, 8))
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    # Set viewport shading to material preview
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    space.region_3d.view_perspective = 'CAMERA'
                    break

    bpy.context.scene.render.filepath = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s13_front_elevation.png"
    bpy.ops.render.render(write_still=True)
    print("Screenshot 1: Front elevation saved")

    # ============================================================
    # Screenshot 2: 3/4 Angle
    # ============================================================
    cam.location = (18, -18, 10)
    target = Vector((0, 0, 7))
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    bpy.context.scene.render.filepath = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s13_three_quarter.png"
    bpy.ops.render.render(write_still=True)
    print("Screenshot 2: 3/4 angle saved")

    # ============================================================
    # Screenshot 3: Distance Overview
    # ============================================================
    cam.location = (0, -45, 15)
    target = Vector((0, 0, 7))
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

    bpy.context.scene.render.filepath = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots/s13_distance_overview.png"
    bpy.ops.render.render(write_still=True)
    print("Screenshot 3: Distance overview saved")

    print("All 3 screenshots captured.")
