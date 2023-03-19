from PIL import Image
import numpy as np
import random
import matplotlib.pyplot as plt
import Info as info
from Prototypes import Prototype
import pickle

inp_img = info.inp_img
img_bw = inp_img.convert("L")
img_arr = info.img_arr
Map = np.full(info.map_size, -1)
rows, cols = info.st_rows, info.st_cols
video_frames = []

#Creating patches (st_w)X(st_h) and adding it to patterns dictionary
patterns = {}
for i in range(rows):
    for j in range(cols):
        for _dir in range(4):
            patterns[Prototype.code] = Prototype((i*info.tile_w,j*info.tile_w), _dir)



#ALGORITHM STARTS HERE
collasped = np.full((info.map_size[0], info.map_size[1]), False, dtype=bool)
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
    collasped[x][y] = True

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
    video_frames.append(Map)
    print(Map)

    # 3:
    UpdateNeighbours(cell=cell)    
while not collasped.all():
    Propogate()
final_arr = ''




def Plot():
    global final_arr
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
    fimg.save("system.png")
Plot()
#Saving the map numpy array
# np.save("MapArray", final_arr)


"""
============================
============================
============================
some postprocessing
============================
============================
============================
"""
post_iterations = 0
POSITIVE = 0
NEGATIVE = 255
def PostProcessing(negate_coors : list):
    # post_iterations+=1
    
    img_preprocessed = final_arr
    print(img_preprocessed)

    covered = np.interp(img_preprocessed, [0,255], [1,0]).astype(int)
    print(f"[{covered=}]")
    post_img = np.full((img_preprocessed.shape), NEGATIVE)
    rows,cols = img_preprocessed.shape
    stack = []

    def GetForeground(img, coors):
        _ = input("")
        x,y = coors
        global POSITIVE
        if img[x][y] == POSITIVE:
            covered[x][y] = 1
            img[x][y] = NEGATIVE
        n_cells = [[x-1,y],[x,y+1],[x+1,y],[x,y-1]]
        for _dir, (r,c) in enumerate(n_cells):
            if not 0<=r<img_preprocessed.shape[0] or not 0<=c<img_preprocessed.shape[1] or covered[r][c]:
                # print(f"Removing {n_cells[_dir] = }")
                n_cells[_dir] = -1
                
        return n_cells, img




    flag = False
    start_coors = []
    for i in range(img_preprocessed.shape[0]):
        for j in range(img_preprocessed.shape[1]):
            if img_preprocessed[i][j] == POSITIVE and [i,j] not in negate_coors:
                start_coors =  [i,j]
                negate_coors.append([i,j])
                flag = True
                break
        if flag:
            break

    print(post_img)
    print(covered)


    stack = [start_coors]
    print(start_coors)
    while stack != []:
        n_cells, img_preprocessed = GetForeground(img_preprocessed,stack[-1])
        ro, co = stack.pop()
        post_img[ro][co] = POSITIVE
        n_cells_new = [val for val in n_cells if val!=-1]
        stack.extend(n_cells_new)
        print(stack)

    if np.count_nonzero(post_img != NEGATIVE) >= 0.15 * np.size(post_img):
        fimg = Image.fromarray(post_img.astype('uint8'))
        fimg.show()
        return
    else:
        PostProcessing(negate_coors)
        

# PostProcessing([])
# videofig(video_frames)