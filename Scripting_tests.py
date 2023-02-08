x = ">>> "

import bpy
import pickle
import math
import numpy as np
import random

#main variables
rows = 4
cols = 4
code_place = np.full((rows, cols), 11, dtype=int)
dir = {
    'n':0,
    'e':1,
    's':2,
    'w':3
}

#Creating all the prototypes
class MeshInfo:
    #getting mesh sauce
    mesh_data = {}
    with open("D:\Terrain-Generation-Blender\MeshData.bin", "rb") as f:
        mesh_data = pickle.load(f)
    print(x,mesh_data)

    code = 0
    def __init__(self, name: str, rotation_index: int):
        self.name = name #STR
        self.valid_sockets = MeshInfo.ShiftList(arr = MeshInfo.mesh_data[name]['sockets'], step = rotation_index) #LIST
        self.rot_ind = rotation_index
        print(x,self.valid_sockets)
        self.prob_factor = MeshInfo.mesh_data[name]['fac'] #FLOAT
        MeshInfo.code += 1 
        return
    
    def ShiftList(arr: list,step: int):
        new_arr = []
        for i in range(len(arr)):
            new_arr.append(arr[(i+step)%len(arr)])
        return new_arr

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
        print(x+"ALready removed")
RemoveCollection("Base Meshes")
RemoveCollection("Instances")

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
instances = bpy.data.collections.new(name="Instances")
bpy.context.scene.collection.children.link(instances)

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


#Creating prototypes
prototypes = {}

#STRAIGHTS
for i in range(2):
    prototypes['straight '+str(MeshInfo.code-1)] = MeshInfo(name='straight', rotation_index=i)
#NINETYS
for i in range(4):
    prototypes['ninety '+str(MeshInfo.code-1)] = MeshInfo(name='ninety', rotation_index=i)
#TEES
for i in range(4):
    prototypes['tee '+str(MeshInfo.code-1)] = MeshInfo(name='tee', rotation_index=i)
#PLANE
prototypes['plane '+str(MeshInfo.code-1)] = MeshInfo(name='plane', rotation_index=0)
#CROSS
prototypes['cross '+str(MeshInfo.code-1)] = MeshInfo(name='cross', rotation_index=0)

#Creating sockets (4D) and candidate (3D) list
candidates = np.full((rows, cols, len(prototypes)), [i for i in range(len(prototypes))], dtype=int) #The length of each 2D element will give the entropy of the cell
sockets = np.full((rows, cols, 4, 2), [1,2], dtype=int)


print(candidates)

for i in prototypes.keys():
    print(x,i)

def CreateInstance(code : int, loc : tuple, collection : str = "Instances",):
    name = ''
    rot_index = 0
    for i in prototypes:
        if int(i.split()[1]) == code:
            name = prototypes[i].name
            rot_index = prototypes[i].rot_ind

    instance = bpy.data.objects[name].copy()
    bpy.data.collections[collection].objects.link(instance)
    bpy.data.objects[instance.name].location = loc
    bpy.data.objects[instance.name].rotation_euler[2] = math.pi * rot_index * 90 / 180
    print(x+"Spawned Block "+name.upper()+", rotation: "+str(rot_index * 90)+", LOC"+str(loc))

def MinEntropy():
    #Getting least entropy length
    min_entropy = 11
    max_entropy = 11
    for i in range(candidates.shape[0]):
        for j in range(candidates.shape[1]):
                if len(candidates[i][j]) < min_entropy and len(candidates[i][j]) > 1:
                    min_entropy = len(candidates[i][j])
                if len(candidates[i][j]) > max_entropy:
                    max_entropy = len(candidates[i][j])
    
    #If maximum entropy (possibilites) is 1, then return -1
    if max_entropy == 1:
        return -1

    #Looking for first cell with minimum entropy
    for i in range(candidates.shape[0]):
        for j in range(candidates.shape[1]):
            if len(candidates[i][j]) == min_entropy:
                return (i,j)




def EliminateNeighbors(min_entropy):

    return
    

def ChooseRand(min_entropy_cell):
    candidates[min_entropy_cell[0]][min_entropy_cell[1]] = [random.choice(candidates[min_entropy_cell[0]][min_entropy_cell[1]])]
    


    return

def epoch():
    x = MinEntropy()
    if x == -1:
        return
    
    ChooseRand(x)
    EliminateNeighbors(x)
    epoch()


def GridSpawner():
    for i in range(code_place.shape[0]):
        for j in range(code_place.shape[1]):
            if code_place[i][j] >= 0:
                CreateInstance(code_place[i][j], (i*2, j*2,0))
    return
