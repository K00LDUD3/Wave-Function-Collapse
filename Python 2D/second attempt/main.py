from PIL import Image
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import Info as info
from Prototypes import Prototype


inp_img = info.inp_img
img_bw = inp_img.convert("L")
img_arr = info.img_arr
Map = np.full(info.map_size, -1)
rows, cols = info.st_rows, info.st_cols

#Creating patches (st_w)X(st_h) and adding it to patterns dictionary
patterns = {}
for i in range(rows):
    for j in range(cols):
        for _dir in range(4):
            patterns[Prototype.code] = Prototype((i,j), _dir)
print(len(patterns.keys()))


#ALGORITHM STARTS HERE
candidates = np.full((info.map_size[0], info.map_size[1], len(patterns.keys())), list(patterns.keys())).tolist()
def MinEntropy():
    min_entropy = len(patterns.keys()) + 1
    cell = -1

    for i in range(info.map_size[0]):
        for j in range(info.map_size[1]):
            if len(candidates[i][j]) < min_entropy and Map[i][j] == -1:
                min_entropy = len(candidates[i][j])
                cell = (i,j)
    return cell

def CollapseTile(cell):
    x, y  = cell
    temp = candidates[x][y]
    try:
        code = random.choice(temp)
        msg = "CALC"
    except:
        code = random.choice(list(patterns.keys()))
        msg = "RAND"
    print(f"{msg} --- {code=}")
    Map[x][y] = code
    candidates[x][y] = [code]

def UpdateNeighbours(cell):
    x,y = cell
    n_cells = [[(x-1)%info.map_size[0], y],[x,(y+1)%info.map_size[1]],[(x+1)%info.map_size[0],y],[x,(y-1)%info.map_size[1]]]
    
    for _dir,rc_val in enumerate(n_cells):
        r,c = rc_val
        if Map[r][c] >= 0:
            continue
        new_candidates = []
        for candidate in candidates[r][c]:
            if patterns[candidate].n_sockets[(_dir+2)%4] == patterns[Map[x][y]].own_sockets[_dir][::-1]:
                new_candidates.append(candidate)
        candidates[r][c] = new_candidates.copy()
    
def Propogate():
    """
    1: Choose minimum entropy
    2: Collapse the tile if entropy is valid
    3: Set the neighbour cell sockets for EDGE and CORNERS
    4: Eliminate CANDIDATES which dont match in neighbour cells 
    """
    # 1:
    cell = MinEntropy()
    print(cell)
    
    # 2:
    if cell == -1:
        return
    CollapseTile(cell=cell)
    print(Map)

    # 3:
    UpdateNeighbours(cell=cell)
    
    Propogate()

Propogate()
def Plot():
    final_arr = np.ndarray((info.map_size[0]*info.tile_w, info.map_size[1]*info.tile_w))
    for i in range(info.map_size[0]):
        for j in range(info.map_size[1]):
            if Map[i][j] == -1:
                continue
            temp = patterns[Map[i][j]].img.copy()
            for x in range(info.tile_w):
                for y in range(info.tile_w):
                    final_arr[i*info.tile_w + x][j*info.tile_w + y] = temp[x][y]
    final_arr = final_arr.astype(int)
    fimg = Image.fromarray(final_arr.astype('uint8'))
    fimg.show()
Plot()