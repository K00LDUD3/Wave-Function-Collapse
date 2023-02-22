"""
==========================
A socket based implementation with N,NE,E,SE,S,SW,W,NW
N,E,S,W will have three sockets (edge pixels)
NE,SE,NW,SW will have 1 socket (corner pixel)
Only black and white images... for now
==========================
"""


from PIL import Image
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from utility import GetBin, GetByteMask, GetInt
import Info as info

dirc = {0:"North", 1:"East",2:"South", 3:"West"}

inp_img = info.inp_img
img_bw = inp_img.convert("L")
img_arr = info.img_arr


# variables
img_info_list = []
rows, cols = info.map_size
Map = np.full((rows, cols), -1)
# st -> Sample Tile

st_w = info.tile_w
st_rows = info.st_rows
st_cols = info.st_cols
print(st_rows, st_cols, inp_img.size)


#Creating patches (st_w)X(st_h) and adding it to patterns dictionary
patterns = {}
img_info_list = np.full((st_rows, st_cols, st_w, st_w), -1)
tile_img_list = np.ndarray((st_rows, st_cols)).tolist()
for i in range(st_rows):
    for j in range(st_cols):
        #Extracting st_w x st_h patch
        for x in range(st_w):
            for y in range(st_w):
                img_info_list[i][j][x][y] = img_arr[i*st_w+x][j*st_w+y]
        temp = Image.fromarray(img_info_list[i][j].astype('uint8')).convert("1")
        tile_img_list[i][j] = temp
        print(img_info_list[i][j])

info.tile_img_list = tile_img_list
from Patterns_2 import Prototype

for i in range(st_rows):
    for j in range(st_cols):
        #getting neighbor cells coordinates from the tile set
        patterns[Prototype.code] = Prototype([i,j])
        pass


#Displaying the tile set
f, axarr = plt.subplots(st_rows, st_cols)
plt.subplots_adjust(wspace=0,hspace=0)
for i in range(st_rows):
    for j in range(st_cols):
        axarr[i,j].imshow(tile_img_list[i][j], interpolation='none')
        plt.axis('off')
# plt.show()

#VARS for algorithm
candidates = np.full((rows, cols, len(patterns.keys())), list(patterns.keys())).tolist()
collapsed = np.full((rows, cols), False, dtype=bool)

#returning cell with minimum possibilites and -1 if none
def MinEntropy():
    min_entr = len(patterns.keys())+1
    cell = -1
    for i in range(rows):
        for j in range(cols):
            if not collapsed[i][j] and min_entr > len(candidates[i][j]):
                cell = [i,j]
                min_entr = len(candidates[i][j])
    return cell
#Collapsing minimum entropy tile with weighted random sampling 
def CollapseTile(cell : list):
    #Getting highest probability factor for candidates that are valid
    candidate = -1
    prob = 0.0
    prob_facs = []
    for i in candidates[cell[0]][cell[1]]:
        prob_facs.append(patterns[i].prob_fac)
    # code = random.choices(candidates[cell[0]][cell[1]], weights=prob_facs, k=1)
    code = -1
    try:
        code = random.choice(candidates[cell[0]][cell[1]])
    except:
        
        #Get rotations of each cell and get random from one of them
        code = [i for i in list(patterns.keys())]
        #Getting collapsed neighbors sockets
        n_cells = [[(cell[0]-1)%rows,cell[1]], [cell[0], (cell[1]+1)%cols],[(cell[0]+1)%rows, cell[1]],[cell[0], (cell[1]-1)%cols]]
        sockets = []
        for i in range(len(n_cells)):
            if Map[n_cells[i][0]][n_cells[i][0]] >=0:
                sockets.append(patterns[Map[n_cells[i][0]][n_cells[i][1]]].edgePixels[(i+2)%4][::-1])
                print(sockets)
            else:
                sockets.append(-1)
        for i in range(len(code)):
            new_codes = []
            for j in sockets:
                if sockets[j] == -1:
                    continue
                for candidate in code:
                    if sockets[j] == patterns[candidate].edgePixels[j]:
                        new_codes.append(code[j])
            code = new_codes.copy()
        print(code)
        code = random.choice([i for i in list(patterns.keys())])
    candidates[cell[0]][cell[1]] = [code]
    
    #Setting cell to certain code
    Map[cell[0]][cell[1]] = code
    collapsed[cell[0]][cell[1]] = True
    return
def UpdateCandidates(cell):
    #Getting the current cell's 4 neighbor's edge and corner cells
    n_corner_cells = patterns[Map[cell[0]][cell[1]]].cornerNeighbors
    n_edge_cells = patterns[Map[cell[0]][cell[1]]].edgeNeighbors
    
    #list of neighbor cells in the Final MAP
    n_cells = [[(cell[0]-1)%rows,cell[1]], [cell[0], (cell[1]+1)%cols],[(cell[0]+1)%rows, cell[1]],[cell[0], (cell[1]-1)%cols]]
    
    #Iterating thru each of them in the order of NESW
    for _dir, n_cell in enumerate(n_cells):
        #IF collapsed, dont bother computing 
        if Map[n_cell[0]][n_cell[1]] >= 0:
            continue

        #Getting the direction tied neighbor of the collapsed cell from the TILESET list
        x = patterns[Map[cell[0]][cell[1]]].edgeNeighbors
        x = x[_dir]

        n_edge = patterns[x[0]*st_rows + x[1]].edgePixels
        n_edge = n_edge[(_dir+2)%4]
        new_candidates = []
        print("="*20+str(Map[cell[0]][cell[1]])+"="*20)
        print(f"{x=} {dirc[_dir]} Neighbor")
        print(f"Old candidates({n_cell[0]}{n_cell[1]}): {candidates[n_cell[0]][n_cell[1]]}")
        for candidate in candidates[n_cell[0]][n_cell[1]]:
            candidate_edge = (patterns[candidate].edgePixels)[(_dir+2)%4]
            if n_edge == candidate_edge:
                print(f"{n_edge=} vs {candidate_edge=} '------MATCH'")
                new_candidates.append(candidate)
        candidates[n_cell[0]][n_cell[1]] = new_candidates
        print(f"New candidates({n_cell[0]},{n_cell[1]}): {candidates[n_cell[0]][n_cell[1]]}")
    return
def Propogate():
    """
    1: Choose minimum entropy
    2: Collapse the tile if entropy is valid
    3: Set the neighbour cell sockets for EDGE and CORNERS
    4: Eliminate CANDIDATES which dont match in neighbour cells 
    """
    # 1:
    cell = MinEntropy()

    #2:
    if cell == -1:
        return
    CollapseTile(cell=cell)
    print(f"Curent CELL --- {cell[0]},{cell[1]}")
    print(Map)

    #3:
    UpdateCandidates(cell=cell)

    return
while not collapsed.all():
    Propogate()

def Plot():
    final_arr = np.ndarray((rows*st_w, cols*info.tile_w))
    for i in range(rows):
        for j in range(cols):
            temp = patterns[Map[i][j]].Img_inf.copy()
            for x in range(st_w):
                for y in range(info.tile_w):
                    final_arr[i*st_w + x][j*info.tile_w + y] = temp[x][y]
    final_arr = final_arr.astype(int)
    fimg = Image.fromarray(final_arr.astype('uint8'))
    fimg.show()
Plot()
# plt.savefig("tileset.png")