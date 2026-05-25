"""
Session 9 — Final report: per-object triangle counts and material assignments.
"""
import bpy

total_tris = 0
mesh_report = []
for obj in sorted(bpy.data.objects, key=lambda o: o.name):
    if obj.type == 'MESH':
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh_eval = obj_eval.to_mesh()
        tris = sum(max(1, len(p.vertices) - 2) for p in mesh_eval.polygons)
        obj_eval.to_mesh_clear()

        mat_name = obj.data.materials[0].name if obj.data.materials else "NONE"
        mesh_report.append((obj.name, tris, mat_name))
        total_tris += tris

print("=== SESSION 9 FINAL REPORT ===")
print(f"{'Object':<30} {'Tris':>6} {'Material':<10}")
print("-" * 50)
for name, tris, mat in mesh_report:
    print(f"{name:<30} {tris:>6} {mat:<10}")
print("-" * 50)
print(f"{'TOTAL':<30} {total_tris:>6}")
print(f"Budget: 10,800 tris | Usage: {total_tris/10800*100:.1f}%")
print(f"\nObjects: {len(mesh_report)} mesh objects")
print(f"Materials used: {set(m for _, _, m in mesh_report)}")

# Count by material slot
mat_counts = {}
for _, tris, mat in mesh_report:
    mat_counts[mat] = mat_counts.get(mat, 0) + tris
print(f"\nTriangles by material:")
for mat, count in sorted(mat_counts.items(), key=lambda x: -x[1]):
    pct = count / total_tris * 100
    print(f"  {mat}: {count} ({pct:.1f}%)")
