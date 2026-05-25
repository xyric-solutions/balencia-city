"""
Balencia City v3 — Export Pipeline
Per-object decimation preserving detail, then Draco-compressed GLB export.

Usage:
    import export_pipeline
    export_pipeline.export_glb(
        output_path="/path/to/output.glb",
        root_name="sia-tower",
        max_tris=25000,
    )
"""
import bpy
import os


VALID_MATERIAL_NAMES = {"base", "accent", "glass", "detail", "emissive", "energy", "holo"}
DETAIL_THRESHOLD = 500


def clear_scene():
    """Remove all objects, meshes, materials, and collections from scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)

    for block in bpy.data.meshes:
        if not block.users:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if not block.users:
            bpy.data.materials.remove(block)
    for block in bpy.data.cameras:
        if not block.users:
            bpy.data.cameras.remove(block)
    for block in bpy.data.lights:
        if not block.users:
            bpy.data.lights.remove(block)


def apply_all_transforms():
    """Apply location, rotation, and scale to all mesh objects."""
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.select_all(action='DESELECT')


def count_total_tris():
    """Count total triangles across all mesh objects."""
    total = 0
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            depsgraph = bpy.context.evaluated_depsgraph_get()
            eval_obj = obj.evaluated_get(depsgraph)
            mesh = eval_obj.to_mesh()
            total += len(mesh.loop_triangles) if hasattr(mesh, 'loop_triangles') else len(mesh.polygons)
            eval_obj.to_mesh_clear()
    return total


def decimate_per_object(max_total_tris):
    """
    Decimate each mesh object proportionally to hit the total triangle budget.
    Objects below DETAIL_THRESHOLD tris are preserved intact.
    """
    current_total = count_total_tris()
    if current_total <= max_total_tris:
        print(f"Already within budget: {current_total} tris <= {max_total_tris}")
        return

    target_ratio = max_total_tris / current_total
    print(f"Decimating: {current_total} tris -> target {max_total_tris} (ratio {target_ratio:.2f})")

    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue

        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = obj.evaluated_get(depsgraph)
        mesh = eval_obj.to_mesh()
        obj_tris = len(mesh.loop_triangles) if hasattr(mesh, 'loop_triangles') else len(mesh.polygons)
        eval_obj.to_mesh_clear()

        if obj_tris < DETAIL_THRESHOLD:
            continue

        obj_ratio = max(0.15, target_ratio * 0.9)

        mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
        mod.ratio = obj_ratio
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="Decimate")

    final_count = count_total_tris()
    print(f"After decimation: {final_count} tris")


def set_origin_bottom_center():
    """Set origin of all mesh objects to bottom-center."""
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        min_z = min((obj.matrix_world @ v.co).z for v in obj.data.vertices) if obj.data.vertices else 0
        obj.location.z -= min_z
        obj.select_set(False)


def parent_to_root(root_name):
    """Parent all mesh objects under a single empty root for clean hierarchy."""
    root = bpy.data.objects.new(root_name, None)
    bpy.context.collection.objects.link(root)
    root.empty_display_type = 'PLAIN_AXES'
    root.empty_display_size = 0.1

    for obj in bpy.data.objects:
        if obj == root:
            continue
        if obj.type in ('MESH', 'EMPTY') and obj.parent is None:
            obj.parent = root

    return root


def remove_cameras_and_lights():
    """Remove all cameras and lights (they should NOT be in exported GLBs)."""
    to_remove = [obj for obj in bpy.data.objects if obj.type in ('CAMERA', 'LIGHT')]
    for obj in to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)


def verify_materials():
    """Check that all mesh objects have materials from the 7-slot set."""
    issues = []
    for obj in bpy.data.objects:
        if obj.type != 'MESH':
            continue
        if not obj.data.materials:
            issues.append(f"{obj.name}: no materials assigned")
            continue
        for mat in obj.data.materials:
            if mat and mat.name not in VALID_MATERIAL_NAMES:
                issues.append(f"{obj.name}: material '{mat.name}' not in 7-slot set")

    if issues:
        print("MATERIAL WARNINGS:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("All materials valid (7-slot set)")
    return len(issues) == 0


def export_glb(output_path, root_name="building", max_tris=15000, max_size_kb=400):
    """
    Full export pipeline:
    1. Apply transforms
    2. Decimate per-object (NOT join-then-decimate)
    3. Set origins to bottom-center
    4. Remove cameras and lights
    5. Parent under root empty
    6. Verify materials (7-slot)
    7. Export as Draco-compressed GLB
    """
    print(f"\n=== Exporting {root_name} ===")

    apply_all_transforms()
    decimate_per_object(max_tris)
    set_origin_bottom_center()
    remove_cameras_and_lights()
    parent_to_root(root_name)
    verify_materials()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    bpy.ops.export_scene.gltf(
        filepath=output_path,
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

    file_size_kb = os.path.getsize(output_path) / 1024
    final_tris = count_total_tris()
    print(f"Exported: {output_path}")
    print(f"  Triangles: {final_tris}")
    print(f"  File size: {file_size_kb:.0f} KB")
    print(f"  Budget check: {'PASS' if final_tris <= max_tris else 'OVER BUDGET'}")
    print(f"  Size check: {'PASS' if file_size_kb <= max_size_kb else 'LARGE'}")

    return {"path": output_path, "tris": final_tris, "size_kb": file_size_kb}
