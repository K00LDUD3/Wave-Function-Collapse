_ = ">>> "
print("=======================================================")
import bpy
import pickle
import math
import numpy as np
import random

#main variables
rows = 10
cols = 10
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
    #print(x,mesh_data)

    code = 0
    def __init__(self, name: str, rotation_index: int):
        self.name = name #STR
        self.valid_sockets = MeshInfo.ShiftList(arr = MeshInfo.mesh_data[name]['sockets'], step = rotation_index) #LIST
        self.rot_ind = rotation_index
        #print(x,self.valid_sockets)
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
        print(_+"ALready removed")
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
    print(_+"imported obj "+mesh.name+"\n")
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
bpy.data.collections['Base Meshes'].hide_viewport = True



#Creating sockets (4D) and candidate (3D) list
candidates = np.full((rows, cols, len(prototypes)), [i for i in range(len(prototypes))], dtype=int).tolist() #The length of each 2D element will give the entropy of the cell
sockets = np.full((rows, cols, 4, 2), [0,1], dtype=int).tolist()
final_codes = np.full((rows, cols), -1)
#print(candidates)



'''
for i in prototypes.keys():
    print(x,i)
'''

def CreateInstance(code : int, loc : tuple, collection : str = "Instances"):
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
    print(_+"Spawned Block "+name.upper()+", rotation: "+str(rot_index * 90)+", LOC"+str(loc)+", CODE "+str(code))

def MinEntropy():
    #Getting least entropy length
    min_entropy = 12
    max_entropy = 11
    for i in range(len(candidates)):
        for j in range(len(candidates[0])):
                if len(candidates[i][j]) < min_entropy and len(candidates[i][j]) > 1:
                    min_entropy = len(candidates[i][j])
                if len(candidates[i][j]) > max_entropy:
                    max_entropy = len(candidates[i][j])
    #If maximum entropy (possibilites) is 1, then return -1
    if max_entropy == 1:
        return -1

    #Looking for first cell with minimum entropy
    for i in range(len(candidates)):
        for j in range(len(candidates[0])):
            if len(candidates[i][j]) == min_entropy:
                return (i,j)
    return -1


def EliminateNeighbors(c_cell):
    #Iterating thru all 4 directions and taking out select sockets
    # for i in dir:
    #     code = candidates[c_cell[0]][c_cell[1]][0]
    #     for k in prototypes:
    #         if int(k.split()[1]) == code:
    #             for j in range(4):
    #                 sockets[c_cell[0]][c_cell[1]][j] = [prototypes[k].valid_sockets[j]]
    print(_,sockets[c_cell[0]][c_cell[1]])
    return


def ChooseRandomTile(c_cell : list):
    choice = random.choice(candidates[c_cell[0]][c_cell[1]])
    candidates[c_cell[0]][c_cell[1]], final_codes[c_cell[0]][c_cell[1]] = [choice], choice
    print(_,"Random Choice: ",choice)
    print(_,"check updated cell: \n",candidates)
    return

def UpdateCurrentCellSockets(c_cell : list):
    code = final_codes[c_cell[0]][c_cell[1]]
    x,y = c_cell
    print(_," PRE_UPDATE sockets of ",x,",",y,"(",code,") : ",sockets[x][y])
    
    #Getting prototype name from code
    key = ''
    for i in prototypes:
        if i.split()[1] == str(code):
            key = i
            break
    c_cell_sockets = prototypes[key].valid_sockets
    
    #Updating "sockets" of current cell with c_cell_sockets
    for i in range(4):
        sockets[x][y][i] = [c_cell_sockets[i]] 
    
    print(_," POST_UPDATE sockets of ",x,",",y,": ",sockets[x][y])


def SetNeighborSockets(c_cell : list):
    x,y = c_cell
    #Get the neighbor cell coordinates in the order of NESW
    n_cells = [[x,y+1],[x+1,y],[x,y-1],[x-1,y]]
    #Make sure they are in bounds
    #Make sure they are not finalised
    #assigning invalid cells to -1 
    for i in range(len(n_cells)):
        r,c = n_cells[i]
        if r not in range(rows) or c not in range(cols):
            n_cells[i] = -1
        elif final_codes[r][c] >= 0:
            n_cells[i] = -1
    print(_,"Neighbors of c_cell: ",n_cells)
    
    #Iterate through valid neighbor cells using the DIR dictionary
    #Set the valid sockets of the neighbor cells to match with current cell
    for i in dir:
        if n_cells[dir[i]] == -1:
            continue
        r,c = n_cells[dir[i]]
        sockets[r][c][(dir[i]+2)%4] = [sockets[x][y][dir[i]]]
    return n_cells

def EliminateNeighborCells(c_cell : list, n_cells : list):
    c_cell_code = final_codes[c_cell[0]][c_cell[1]]
    c_cell_sockets = -1
    c_cell_key = -1
    for i in prototypes:
        if i.split()[1] == str(c_cell_code):
            c_cell_sockets = prototypes[i].valid_sockets
            c_cell_key = i
            break
    
    
    #Iterate through each neighbor cell
    for i in range(len(n_cells)):
        new_candidates = []
        if n_cells[i] == -1:
            continue 
        r,c = n_cells[i]
        n_candidates = candidates[r][c]
        c_cell_socket = c_cell_sockets[i]
        
        #Check if sockets in direction of current cell exists in each prototype
        #if not, del
        for n_code in n_candidates:
            for j in prototypes:
                if j.split()[1] == str(n_code):
                    if prototypes[j].valid_sockets[(i+2)%4] == c_cell_socket:
                        new_candidates.append(n_code)
        print(_+" NEW candidates for cell: ",n_cells[i],": ",new_candidates)
        candidates[r][c] = new_candidates
    pass
def epoch():
    c_cell = MinEntropy()
    print(_,"Chosen Cell: ",c_cell)
    if c_cell == -1:
        return
    
    ChooseRandomTile(c_cell)
    #Set c_cell sockets
    UpdateCurrentCellSockets(c_cell)
    #Eliminate neighbor sockets
    n_cells = SetNeighborSockets(c_cell)
    #Eliminate Neighbor cells
    EliminateNeighborCells(c_cell, n_cells)
    
    epoch()

epoch()

def GridSpawner():
    for i in range(final_codes.shape[0]):
        for j in range(final_codes.shape[1]):
            if final_codes[i][j] >= 0:
                CreateInstance(final_codes[i][j], (i*2, j*(2),0))
    return
GridSpawner()
print(_,"final Codes:\n",final_codes)