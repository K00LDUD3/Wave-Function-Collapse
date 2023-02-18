from PIL import Image
import numpy as np
import random
import math
import matplotlib.pyplot as plt
from utility import GetBin, GetByteMask, GetInt
import logging


inp_img = Image.open("Sample.png")
img_bw = inp_img.convert("L")
img_arr = np.array(img_bw)


# variables
img_info_list = []
rows, cols = 10, 10
Map = np.full((rows, cols), -1).tolist()
# st -> Sample Tile
st_w = 2
st_h = 2
st_rows = int(inp_img.size[0]/st_w)
st_cols = int(inp_img.size[1]/st_h)

#Creating patches 2x2 
img_info_list = np.full((st_rows, st_cols, 2, 2), -1)
tile_img_list = []
tile_img_bytes = []
for i in range(st_rows):
    for j in range(st_cols):
        img_info_list[i][j][0][0] = img_arr[i*2][j*2]
        img_info_list[i][j][0][1] = img_arr[i*2][j*2+1]
        img_info_list[i][j][1][0] = img_arr[i*2+1][j*2]
        img_info_list[i][j][1][1] = img_arr[i*2+1][j*2+1]
        temp = Image.fromarray(img_info_list[i][j].astype('uint8')).convert("1")
        tile_img_bytes.append(GetByteMask(np.interp(img_info_list[i][j], [0,255],[0,3]).astype(int)))
        tile_img_list.append(temp)

#Displaying the tile set
f, axarr = plt.subplots(st_rows, st_cols)
plt.subplots_adjust(wspace=0,hspace=0)
for i in range(st_rows):
    for j in range(st_cols):
        axarr[i,j].imshow(tile_img_list[i*st_rows+j], interpolation='none')
        plt.axis('off')
# plt.show()

print(tile_img_bytes)

# Assigning valid neighbor sockets
valid_sockets = np.full((st_rows, st_cols), -1).tolist()
for i in range(st_rows):
    for j in range(st_cols):
        n_cells = [[(i-1)%st_rows,j], [i, (j+1)%st_cols], [(i+1)%st_rows,j], [i, (j-1)%st_cols]]
        valid_sockets[i][j] = ''
        for dir, [x,y] in enumerate(n_cells):
            mask = tile_img_bytes[x*st_rows + y]
            mask = GetBin(int(mask),length=8)
            req_mask = mask[(dir+4)%8]+mask[(dir+6)%8]
            print(mask[(dir+4)%8],mask[(dir+6)%8])
            print(req_mask)
            valid_sockets[i][j] = valid_sockets[i][j] + req_mask
        valid_sockets[i][j] = GetInt(valid_sockets[i][j])    
        print(f'{valid_sockets=}')


#Sub funcs
def MinEntropy():
    return

#Algorithm
def Propogate():
    #find minimum entropy
    #Set current cell sockets
    #Set neighbor cell sockets
    #Eliminate neighbor cell sockets
    return
