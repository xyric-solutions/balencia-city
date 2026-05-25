"""
Finance Tower — Save .blend file to drafts directory.
"""
import bpy

filepath = "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/03-finance/exterior/drafts/finance-exterior-s13.blend"
bpy.ops.wm.save_as_mainfile(filepath=filepath)
print(f"Saved: {filepath}")

# Final verification
mesh_count = sum(1 for obj in bpy.data.objects if obj.type == 'MESH')
curve_count = sum(1 for obj in bpy.data.objects if obj.type == 'CURVE')
light_count = sum(1 for obj in bpy.data.objects if obj.type == 'LIGHT')
camera_count = sum(1 for obj in bpy.data.objects if obj.type == 'CAMERA')

total_tris = 0
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh_eval = obj_eval.to_mesh()
        tris = sum(len(poly.vertices) - 2 for poly in mesh_eval.polygons)
        total_tris += tris
        obj_eval.to_mesh_clear()

mat_names = [m.name for m in bpy.data.materials if m.users > 0]

print(f"\nFinal scene summary:")
print(f"  Mesh objects: {mesh_count}")
print(f"  Curve objects: {curve_count}")
print(f"  Lights: {light_count}")
print(f"  Cameras: {camera_count}")
print(f"  Total mesh tris: {total_tris}")
print(f"  Materials in use: {mat_names}")
print(f"  Budget: {total_tris}/10800 = {total_tris/10800*100:.1f}%")
