import bpy

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)
bpy.context.view_layer.objects.active = None


grid = [i for i in range(-10,11,5)]

for x in grid:
    for y in grid:
        for z in grid:
            obj_loc = (x,y,z)
            bpy.ops.mesh.primitive_cube_add(location=obj_loc)
