import bpy
import pickle
import numpy as np

#some pre-script commands idk: select all, delete, deselect, purging orphan objects, whatever..
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)
bpy.context.view_layer.objects.active = None

#Removing select collections 
def RemoveCollection(name):
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
        #print(_+"ALready removed")
        pass
collections_to_remove = ["Base Meshes", "Instances"]
for collection in collections_to_remove:
    RemoveCollection(collection)

#importing sauce and assigning it to a certain collection
def FetchMesh(name: str, path = "/Users/tanushsrivatsa/Work/Wave-Function-Collapse/Blender-2/Assets/") -> bpy.types.Object:
    bpy.ops.import_scene.obj(filepath=path+name.capitalize()+".obj", filter_glob="*.obj")
    mesh = bpy.context.selected_objects[0]
    mesh.name = name
    #print(_+"imported obj "+mesh.name+"\n")
    bpy.data.collections['Base Meshes'].objects.link(mesh)
    return mesh
    
    
base_collection = bpy.data.collections.new(name="Base Meshes")
bpy.context.scene.collection.children.link(base_collection)
instances = bpy.data.collections.new(name="Instances")
bpy.context.scene.collection.children.link(instances)

plane = FetchMesh(name="plane_with_mat")
bpy.data.collections['Collection'].objects.unlink(plane)

    
    
#Getting map array
Map = np.load("/Users/tanushsrivatsa/Work/Wave-Function-Collapse/Blender-2/MapArray.npy")
Map = np.interp(Map, [0,255],[0,1]).astype(int)
print(Map)




def GridSpawner():
    global plane
    for i in range(Map.shape[0]):
        for j in range(Map.shape[1]):
            if Map[i][j] == 1:
                instance = bpy.data.objects[plane.name].copy()
                bpy.data.collections["Instances"].objects.link(instance)
                bpy.data.objects[instance.name].location = (i*2, j*2,0)
    return
GridSpawner()

