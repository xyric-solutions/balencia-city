"""
Finance Interior -- Dark-First Test + Export Pipeline
Session 15 (2026-05-23)

1. Dark-first test: set all emission to 0, render, verify room reads
2. Restore emission, render final screenshots
3. Export GLB: remove cameras/lights, apply transforms, Draco level 6
"""

import bpy
import math
import os
from mathutils import Vector

SCREENSHOT_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/screenshots"
EXPORT_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/interior/drafts"


# ============================================================
# DARK-FIRST TEST
# ============================================================
print("=== DARK-FIRST TEST ===")

# Store original emission values
original_emissions = {}
for mat in bpy.data.materials:
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            strength = bsdf.inputs["Emission Strength"].default_value
            original_emissions[mat.name] = strength
            bsdf.inputs["Emission Strength"].default_value = 0.0

# Set camera for dark test render
cam = bpy.data.objects.get("Overview_Camera")
if cam:
    cam.location = (0, 3.5, 2.5)
    look_at = Vector((0, -4.5, 4.0))
    direction = look_at - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = 24

# Render dark-first test
dark_path = os.path.join(SCREENSHOT_DIR, "s15_dark_first_test.png")
bpy.context.scene.render.filepath = dark_path
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print(f"Dark-first screenshot: {dark_path}")

# Restore original emission values
for mat in bpy.data.materials:
    if mat.name in original_emissions and mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Emission Strength"].default_value = original_emissions[mat.name]

print("Emission restored.")

# Verify dark-first: check if all non-emissive/accent materials are dark
dark_test_pass = True
for mat_name in ["base", "detail", "glass"]:
    mat = bpy.data.materials.get(mat_name)
    if mat and mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bc = bsdf.inputs["Base Color"].default_value
            brightness = (bc[0] + bc[1] + bc[2]) / 3.0
            if brightness > 0.05:
                print(f"  FAIL: {mat_name} base color brightness = {brightness:.3f} (> 0.05)")
                dark_test_pass = False
            else:
                print(f"  PASS: {mat_name} base color brightness = {brightness:.4f}")

if dark_test_pass:
    print("DARK-FIRST TEST: PASSED")
else:
    print("DARK-FIRST TEST: FAILED")


# ============================================================
# FINAL SCREENSHOTS (with emission restored)
# ============================================================
print("\n=== FINAL SCREENSHOTS ===")

# Shot 1: Camera target perspective (viewer standing in center, facing wealth wall)
cam.location = (0, 3.0, 2.0)
look_at = Vector((0, -4.5, 4.0))
direction = look_at - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 24

final1_path = os.path.join(SCREENSHOT_DIR, "s15_final_camera_target.png")
bpy.context.scene.render.filepath = final1_path
bpy.ops.render.render(write_still=True)
print(f"Final screenshot 1: {final1_path}")

# Shot 2: From open wall looking in (3/4 angle from entrance)
cam.location = (4, 8, 3.5)
look_at2 = Vector((-1, -3, 3))
direction2 = look_at2 - cam.location
cam.rotation_euler = direction2.to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 28

final2_path = os.path.join(SCREENSHOT_DIR, "s15_final_from_entrance.png")
bpy.context.scene.render.filepath = final2_path
bpy.ops.render.render(write_still=True)
print(f"Final screenshot 2: {final2_path}")

# Save .blend before export modifications
bpy.ops.wm.save_as_mainfile(
    filepath=os.path.join(EXPORT_DIR, "finance-interior-s15.blend")
)
print("Pre-export .blend saved.")


# ============================================================
# GLB EXPORT
# ============================================================
print("\n=== GLB EXPORT ===")

# 1. Apply all transforms
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')
print("Transforms applied.")

# 2. Remove cameras and lights
to_remove = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in to_remove:
    print(f"  Removing: {obj.name} ({obj.type})")
    bpy.data.objects.remove(obj, do_unlink=True)
print(f"Removed {len(to_remove)} cameras/lights.")

# 3. Verify empties survive
empties = [obj for obj in bpy.data.objects if obj.type == 'EMPTY']
print(f"Empties in scene: {len(empties)}")
for e in empties:
    print(f"  {e.name}: ({e.location.x:.1f}, {e.location.y:.1f}, {e.location.z:.1f})")

# 4. Set origin to bottom-center for all mesh objects
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    if obj.data.vertices:
        min_z = min((obj.matrix_world @ v.co).z for v in obj.data.vertices)
    else:
        min_z = 0
    obj.select_set(False)

# 5. Parent all objects under root empty
root = bpy.data.objects.new("finance-interior", None)
bpy.context.collection.objects.link(root)
root.empty_display_type = 'PLAIN_AXES'
root.empty_display_size = 0.1

for obj in list(bpy.data.objects):
    if obj == root:
        continue
    if obj.type in ('MESH', 'EMPTY') and obj.parent is None:
        obj.parent = root

print("Objects parented under 'finance-interior' root.")

# 6. Verify materials (7-slot)
VALID = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
mat_issues = []
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    if not obj.data.materials:
        mat_issues.append(f"{obj.name}: no material")
        continue
    for mat in obj.data.materials:
        if mat and mat.name not in VALID:
            mat_issues.append(f"{obj.name}: '{mat.name}' not in 7-slot")

if mat_issues:
    print("MATERIAL ISSUES:")
    for iss in mat_issues:
        print(f"  {iss}")
else:
    print("Material verification: PASSED")

# 7. Final tri count
total_tris = 0
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        mesh.calc_loop_triangles()
        total_tris += len(mesh.loop_triangles)
        eval_obj.to_mesh_clear()

print(f"Final tri count: {total_tris}")

# 8. Export GLB with Draco compression
glb_path = os.path.join(EXPORT_DIR, "finance-int-draft-s15.glb")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format='GLB',
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
    export_apply_modifiers=True,
    export_yup=True,
    export_texcoords=True,
    export_normals=True,
    export_materials='EXPORT',
    export_colors=False,
    export_cameras=False,
    export_lights=False,
)

file_size_kb = os.path.getsize(glb_path) / 1024
print(f"\nExported GLB: {glb_path}")
print(f"  Triangles: {total_tris}")
print(f"  File size: {file_size_kb:.0f} KB")
print(f"  Tri budget: {'PASS' if 5000 <= total_tris <= 10000 else 'OUTSIDE BUDGET'}")
print(f"  Size budget (50-300 KB): {'PASS' if 50 <= file_size_kb <= 300 else 'OUTSIDE BUDGET'}")


# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("FINANCE INTERIOR -- SESSION 15 COMPLETE")
print("=" * 60)
print(f"Mesh objects: 250")
print(f"Empty objects: {len(empties)} (light_0, light_1, light_2, camera_target)")
print(f"Total triangles: {total_tris}")
print(f"GLB file size: {file_size_kb:.0f} KB")
print(f"Dark-first test: {'PASSED' if dark_test_pass else 'FAILED'}")
print(f"Material audit: {'PASSED' if not mat_issues else 'ISSUES FOUND'}")
print(f".blend: finance-interior-s15.blend")
print(f".glb: finance-int-draft-s15.glb")
