"""
Finance Interior -- GLB Export Only
Session 15 -- Blender 5.x compatible export
"""

import bpy
import os
from mathutils import Vector

EXPORT_DIR = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/interior/drafts"

# ============================================================
# 1. Apply all transforms
# ============================================================
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.select_all(action='DESELECT')
print("Transforms applied.")

# ============================================================
# 2. Remove cameras and lights
# ============================================================
to_remove = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
for obj in to_remove:
    print(f"  Removing: {obj.name} ({obj.type})")
    bpy.data.objects.remove(obj, do_unlink=True)
print(f"Removed {len(to_remove)} cameras/lights.")

# ============================================================
# 3. Verify empties
# ============================================================
empties = [obj for obj in bpy.data.objects if obj.type == 'EMPTY']
print(f"Empties in scene: {len(empties)}")
for e in empties:
    print(f"  {e.name}: ({e.location.x:.1f}, {e.location.y:.1f}, {e.location.z:.1f})")

# ============================================================
# 4. Parent all objects under root empty
# ============================================================
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

# ============================================================
# 5. Material verification
# ============================================================
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

# ============================================================
# 6. Tri count
# ============================================================
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

# ============================================================
# 7. Export GLB -- Blender 5.x compatible parameters
# ============================================================
glb_path = os.path.join(EXPORT_DIR, "finance-int-draft-s15.glb")

# Get available export parameters for this Blender version
export_kwargs = {
    'filepath': glb_path,
    'export_format': 'GLB',
    'export_draco_mesh_compression_enable': True,
    'export_draco_mesh_compression_level': 6,
    'export_yup': True,
    'export_texcoords': True,
    'export_normals': True,
    'export_materials': 'EXPORT',
    'export_cameras': False,
    'export_lights': False,
    'export_apply': True,
}

bpy.ops.export_scene.gltf(**export_kwargs)

file_size_kb = os.path.getsize(glb_path) / 1024

print(f"\nExported GLB: {glb_path}")
print(f"  Triangles: {total_tris}")
print(f"  File size: {file_size_kb:.0f} KB")
print(f"  Tri budget (5K-10K): {'PASS' if 5000 <= total_tris <= 10000 else 'OUTSIDE'}")
print(f"  Size budget (50-300 KB): {'PASS' if 50 <= file_size_kb <= 300 else 'OUTSIDE'}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("FINANCE INTERIOR -- SESSION 15 EXPORT COMPLETE")
print("=" * 60)
mesh_count = sum(1 for o in bpy.data.objects if o.type == 'MESH')
empty_count = sum(1 for o in bpy.data.objects if o.type == 'EMPTY')
print(f"Mesh objects: {mesh_count}")
print(f"Empty objects: {empty_count}")
print(f"Total triangles: {total_tris}")
print(f"GLB file size: {file_size_kb:.0f} KB")
print(f".blend: finance-interior-s15.blend")
print(f".glb: finance-int-draft-s15.glb")
