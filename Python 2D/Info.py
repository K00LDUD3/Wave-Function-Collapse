import pickle
from PIL import Image
from numpy import array

inp_img = Image.open("sample2.png")
img_arr = array(inp_img.convert("L"))
map_size = [6,6]

#Tile set vars
tile_w = 3
st_rows, st_cols = inp_img.size[0] - tile_w + 1, inp_img.size[1] - tile_w + 1
st_rows, st_cols = int(inp_img.size[0]//tile_w), int(inp_img.size[1]//tile_w)
print(st_rows, st_cols)