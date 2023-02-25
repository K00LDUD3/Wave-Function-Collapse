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
        # print(img_info_list[i][j])

info.tile_img_list = tile_img_list
from Patterns_2 import Prototype

for i in range(st_rows):
    for j in range(st_cols):
        for rot_ind in range(4):
            patterns[Prototype.code] = Prototype([i,j], rot_ind)


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


#Algorithm
def MinEntropy():
    min_entropy = len(patterns.keys()) + 1
    cell = -1

    for i in range(rows):
        for j in range(cols):
            if len(candidates[i][j]) < min_entropy and not collapsed[i][j]:
                min_entropy = len(candidates[i][j])
                cell = [i,j]

    return cell

def CollapseTile(cell : list):
    x,y = cell
    try:
        code = random.choice(candidates[x][y])
        msg = "CALC"
    except:
        code = random.choice(list(patterns.keys()))
        msg = "RAND"
    print(f"C{cell} -- {code=} <{msg}>")

    
    candidates[x][y] = [code]
    collapsed[x][y] = True
    Map[x][y] = code

    return

def UpdateNCells(c_cell : list):
    # Neighbor cells:
    x,y = c_cell
    ncells = N,E,S,W = [[(x-1)%rows, y],[x,(y+1)%cols],[(x+1)%rows,y],[x,(y-1)%cols]]
    print(Map)
    print(f"{ncells = }")
    # Go thru candiates of neighbor cells
    # Adding the candidates to new list 
    new_candidates = []
    # Get necessary side
    for _dir,(r,c) in enumerate(ncells):
        if collapsed[r][c]:
            print(f"{r},{c} collapsed already, skip iter...\n")
            continue
        for candidate in candidates[r][c]:
            # Comparing sockets of candidate and required sockets
            candidate_edges = patterns[candidate].EdgePixels()
            candidate_edges_req = candidate_edges[(_dir+2)%4]
            # Compare with collapsed tiles neighbor
            if patterns[Map[x][y]].valid_sockets[_dir] == candidate_edges_req[::-1]:
                print(f"{patterns[Map[x][y]].valid_sockets[_dir]} --- MATCH: {_dir=}, {candidate=}, {candidate_edges=}")
                new_candidates.append(candidate)    
        candidates[r][c] = new_candidates.copy()
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
    if cell == -1:
        return
    # 2:
    CollapseTile(cell)

    # 3:
    UpdateNCells(cell)

    Propogate()
    return
Propogate()
def Plot():
    final_arr = np.ndarray((rows*st_w, cols*info.tile_w))
    for i in range(rows):
        for j in range(cols):
            if Map[i][j] == -1:
                continue
            temp = patterns[Map[i][j]].Img_inf.copy()
            for x in range(st_w):
                for y in range(info.tile_w):
                    final_arr[i*st_w + x][j*info.tile_w + y] = temp[x][y]
    final_arr = final_arr.astype(int)
    fimg = Image.fromarray(final_arr.astype('uint8'))
    fimg.show()
Plot()