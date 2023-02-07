x = ">>> "

import bpy
import pickle

#some pre-script commands idk: select all, delete, deselect, purging orphan objects, whatever..
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)
bpy.context.view_layer.objects.active = None

name = "Base Meshes"
remove_collection_objects = True

coll = bpy.data.collections.get(name)
try:

    if coll:
        if remove_collection_objects:
            obs = [o for o in coll.objects if o.users == 1]
            while obs:
                bpy.data.objects.remove(obs.pop())
                pass

        bpy.data.collections.remove(coll)
except:
    print(x+"ALready removed")

def del_collection(coll):
    for c in coll.children:
        del_collection(c)
    bpy.data.collections.remove(coll,do_unlink=True)

#NOTE: KEEP COLLECTION SELECTED

#importing sauce and assigning it to a certain collection
def FetchMesh(name: str, path = "D:\\Terrain-Generation-Blender\\Models\\") -> bpy.types.Object:
    bpy.ops.import_scene.obj(filepath=path+name.capitalize()+".obj", filter_glob="*.obj")
    mesh = bpy.context.selected_objects[0]
    mesh.name = name
    print(x+"imported obj "+mesh.name+"\n")
    bpy.data.collections['Base Meshes'].objects.link(mesh)
    return mesh


base_collection = bpy.data.collections.new(name="Base Meshes")
bpy.context.scene.collection.children.link(base_collection)

cross = FetchMesh(name="cross")
#bpy.data.collections['Base Meshes'].objects.link(cross)
bpy.data.collections['Collection'].objects.unlink(cross)


straight = FetchMesh(name="straight")
#bpy.data.collections['Base Meshes'].objects.link(straight)
bpy.data.collections['Collection'].objects.unlink(straight)

ninety = FetchMesh(name="ninety")
#bpy.data.collections['Base Meshes'].objects.link(ninety)
bpy.data.collections['Collection'].objects.unlink(ninety)

plane = FetchMesh(name="plane")
#bpy.data.collections['Base Meshes'].objects.link(plane)
bpy.data.collections['Collection'].objects.unlink(plane)

tee = FetchMesh(name="tee")
#bpy.data.collections['Base Meshes'].objects.link(tee)
bpy.data.collections['Collection'].objects.unlink(tee)

bpy.ops.object.select_all(action='DESELECT')


#getting mesh sauce
mesh_data = {}
with open("D:\Terrain-Generation-Blender\MeshData.bin", "rb") as f:
    mesh_data = pickle.load(f)
print(x,mesh_data)