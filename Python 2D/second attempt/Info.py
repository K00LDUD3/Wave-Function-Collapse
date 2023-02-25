from PIL import Image
from numpy import array

inp_img = Image.open("caves3.png")
img_arr = array(inp_img.convert("L"))
map_size = [20,20]

#Tile set vars
tile_w = 3
st_rows, st_cols = inp_img.size[0] - tile_w + 1, inp_img.size[1] - tile_w + 1
print(st_rows, st_cols)