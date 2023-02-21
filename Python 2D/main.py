from PIL import Image
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from utility import GetBin, GetByteMask, GetInt
from Prototypes import Prototype
from cachetools import Cache, LRUCache


inp_img = Image.open("Sample7.png")
img_bw = inp_img.convert("L")
img_arr = np.array(img_bw)


# variables
img_info_list = []
rows, cols = 30, 30
Map = np.full((rows, cols), -1)
# st -> Sample Tile

st_w = 2
st_h = 2
st_rows = int(inp_img.size[0]/st_w)
st_cols = int(inp_img.size[1]/st_h)

#Creating patches 2x2 
img_info_list = np.full((st_rows, st_cols, st_w, st_h), -1)
tile_img_list = np.ndarray((st_rows, st_cols)).tolist()
tile_img_codes = np.ndarray((st_rows, st_cols)).tolist()
for i in range(st_rows):
    for j in range(st_cols):
        img_info_list[i][j][0][0] = img_arr[i*st_w][j*st_h]
        img_info_list[i][j][0][1] = img_arr[i*st_w][j*st_h+1]
        img_info_list[i][j][1][0] = img_arr[i*st_w+1][j*st_h]
        img_info_list[i][j][1][1] = img_arr[i*st_w+1][j*st_h+1]
        temp = Image.fromarray(img_info_list[i][j].astype('uint8')).convert("1")
        tile_img_list[i][j] = temp

def ImgMatch(img1, img2):
    return (np.array(img1) == np.array(img2)).all()

#Instantiating prototypes for each cell
protos = {}
for i in range(st_rows):
    for j in range(st_cols):
        #getting neighbor cells coordinates from the tile set
        N = [(i-1)%st_rows, j]
        E = [i, (j+1)%st_cols]
        S = [(i+1)%st_rows, j]
        W = [i,(j-1)%st_cols]

        #Checking if image matches with another existing image in the prototypes dictionary
        img = tile_img_list[i][j]
        flag = False
        match_key = ''
        for key in range(len(protos.keys())):
            if ImgMatch(img, protos[key].img):
                flag = True
                match_key = key
        if flag:
            protos[match_key].N.append(N)
            protos[match_key].E.append(E)
            protos[match_key].S.append(S)
            protos[match_key].W.append(W)
            tile_img_codes[i][j] = protos[match_key].cd
        else:
            protos[Prototype.code] = Prototype(tile_img_list[i][j], N, E, S, W)
            tile_img_codes[i][j] = Prototype.code
            print(tile_img_codes)
            print(protos[Prototype.code].Img_inf)
        

# print(protos[0].N)


#Displaying the tile set
f, axarr = plt.subplots(st_rows, st_cols)
plt.subplots_adjust(wspace=0,hspace=0)
for i in range(st_rows):
    for j in range(st_cols):
        axarr[i,j].imshow(tile_img_list[i][j], interpolation='none')
        plt.axis('off')


candidates = np.full((rows, cols, len(protos.keys())), list(protos.keys())).tolist()

#Sub funcs
def MinEntropy():
    min_entropy = len(protos.keys())+1
    min_entropy_cell = -1

    for i in range(rows):
        for j in range(cols):
            if min_entropy > len(candidates[i][j]) and Map[i,j] == -1:
                min_entropy_cell = [i,j]
                min_entropy = len(candidates[i][j])
    
    return min_entropy_cell

def FixTile(x,y):
    # print(candidates[x][y])
    Map[x,y] = random.choice(candidates[x][y])
def GetCodeFromCoor(l : list):
    #Gets coor from a list of coordinates
    x = list(set([tile_img_codes[i[0]][i[1]] for i in l]))
    print(f"{x=}")
    return x 

def UpdateNCandidates(c_cell : list):
    i,j = c_cell
    #getting neighbor cells coordinates from the tile set
    N = [(i-1)%rows, j]
    E = [i, (j+1)%cols]
    S = [(i+1)%rows, j]
    W = [i,(j-1)%cols]

    #Fetching code of current cell

    code = Map[i,j]
    x = protos[code]
    # candidates[N[0]][N[1]] = [x.N[0][0]][x.N[0][1]]
    temp = GetCodeFromCoor(x.N)
    _new = []
    for i in temp:
        if i in candidates[N[0]][N[1]]:
            _new.append(i)
    candidates[N[0]][N[1]] = temp.copy()

    temp = GetCodeFromCoor(x.E)
    _new = []
    for i in temp:
        if i in candidates[E[0]][E[1]]:
            _new.append(i)
    candidates[E[0]][E[1]] = temp.copy()

    temp = GetCodeFromCoor(x.S)
    _new = []
    for i in temp:
        if i in candidates[S[0]][S[1]]:
            _new.append(i)
    candidates[S[0]][S[1]] = temp.copy()

    temp = GetCodeFromCoor(x.W)
    _new = []
    for i in temp:
        if i in candidates[W[0]][W[1]]:
            _new.append(i)
    candidates[W[0]][W[1]] = temp.copy()
    return
#Algorithm

def Propogate():
    #find minimum entropy
    c_cell = MinEntropy()
    if c_cell == -1:
        return
    # print(f"CHOSEN CELL: {c_cell}")

    #Choosing random block
    FixTile(c_cell[0], c_cell[1])
    #Eliminate neighbor cells
    UpdateNCandidates(c_cell=c_cell)

    return
while MinEntropy() != -1:
    Propogate()
plt.show()

def Plot():
    final_arr = np.ndarray((rows*st_w, cols*st_h))
    for i in range(rows):
        for j in range(cols):
            temp = protos[Map[i][j]].Img_inf
            final_arr[i*st_w][j*st_h] = temp[0][0]
            final_arr[i*st_w][j*st_h+1] = temp[0][1]
            final_arr[i*st_w+1][j*st_h] = temp[1][0]
            final_arr[i*st_w+1][j*st_h+1] = temp[1][1]
    final_arr = final_arr.astype(int)
    print(final_arr)
    fimg = Image.fromarray(final_arr.astype('uint8'))
    fimg.show()
Plot()