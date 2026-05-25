"""
Session 11 -- Screenshots for Yoga Interior
Takes screenshots from multiple angles for QA review.
"""

import bpy
import math
import os

OUTPUT_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/interior/drafts"

# Ensure render settings
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGB'

# Get or create camera
cam = bpy.data.objects.get("Overview_Camera")
if not cam:
    cam_data = bpy.data.cameras.new(name="Overview_Camera")
    cam_data.lens = 35
    cam = bpy.data.objects.new("Overview_Camera", cam_data)
    bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

from mathutils import Vector

def aim_camera(location, target, lens=35):
    """Position camera and aim at target."""
    cam.location = location
    cam.data.lens = lens
    direction = Vector(target) - Vector(location)
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

def render_screenshot(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"[Screenshot] Saved: {filepath}")

# Screenshot 1: Front view from camera_target perspective
aim_camera(location=(0, -8, 3), target=(0, 0, 1.0), lens=35)
render_screenshot("s11_front_overview")

# Screenshot 2: 3/4 angle showing focal element and props
aim_camera(location=(6, -6, 4), target=(0, 0, 0.5), lens=35)
render_screenshot("s11_three_quarter")

# Screenshot 3: From the open window wall looking in
aim_camera(location=(0, 8, 2.5), target=(0, 0, 0.8), lens=28)
render_screenshot("s11_window_view_in")

# Screenshot 4: Top-down plan view
aim_camera(location=(0, 0, 12), target=(0, 0, 0), lens=50)
render_screenshot("s11_top_down")

print("[S11] All screenshots taken.")
