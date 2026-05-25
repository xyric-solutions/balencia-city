"""
QA Dark-First Test -- Zero all emissions, render, verify architectural readability.
Then restore emissions.
"""
import bpy
import math
import os

OUTPUT_DIR = '/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/interior/drafts'

# Store original emission values
original_emissions = {}
for mat in bpy.data.materials:
    if mat.name == 'Dots Stroke':
        continue
    if not mat.node_tree:
        continue
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            strength = node.inputs['Emission Strength'].default_value
            original_emissions[mat.name] = strength
            # Zero out emission
            node.inputs['Emission Strength'].default_value = 0.0
            break

print("=== DARK FIRST TEST ===")
print(f"Zeroed emissions for {len(original_emissions)} materials:")
for name, val in original_emissions.items():
    print(f"  {name}: {val} -> 0.0")

# Set up a simple neutral sun for dark-first test
# Add a dim sun light pointing down
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
test_sun = bpy.context.active_object
test_sun.name = 'QA_TestSun'
test_sun.data.energy = 0.5  # Very dim -- just enough to see forms
test_sun.data.color = (1.0, 1.0, 1.0)  # Neutral white
test_sun.rotation_euler = (math.radians(45), 0, math.radians(30))

# Set up render for screenshot
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 50

# Use the existing camera
cam = None
for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        cam = obj
        break

if cam:
    scene.camera = cam
    # Render dark-first test
    scene.render.filepath = os.path.join(OUTPUT_DIR, 'qa_dark_first_test_s11.png')
    scene.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    print(f"Dark-first test rendered to: {scene.render.filepath}")
else:
    print("WARNING: No camera found, cannot render dark-first test")

# Check if sage color appears in base colors of base/detail materials
print("\n=== BASE COLOR VERIFICATION ===")
for mat in bpy.data.materials:
    if mat.name == 'Dots Stroke':
        continue
    if not mat.node_tree:
        continue
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            bc = node.inputs['Base Color'].default_value
            ec = node.inputs['Emission Color'].default_value
            print(f"  {mat.name}:")
            print(f"    base_color: ({bc[0]:.4f}, {bc[1]:.4f}, {bc[2]:.4f})")
            print(f"    emission_color: ({ec[0]:.4f}, {ec[1]:.4f}, {ec[2]:.4f})")
            # Check if sage (#6EE7B7) appears in base color of base/detail
            if mat.name in ('base', 'detail'):
                g_dominant = bc[1] > bc[0] * 2 and bc[1] > 0.1
                if g_dominant:
                    print(f"    *** FAIL: Sage-like green detected in {mat.name} base color!")
                else:
                    print(f"    OK: No sage in base color")
            break

# Remove test sun
bpy.data.objects.remove(test_sun, do_unlink=True)

# Restore original emissions
for mat in bpy.data.materials:
    if mat.name in original_emissions:
        if not mat.node_tree:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                node.inputs['Emission Strength'].default_value = original_emissions[mat.name]
                break

print("\n=== EMISSIONS RESTORED ===")
for name, val in original_emissions.items():
    print(f"  {name}: restored to {val}")

print("\n=== DARK FIRST TEST COMPLETE ===")
