import numpy as np
from PIL import Image
from Info import tile_img_list, st_rows, st_cols, tile_w
# from Info import tile_width, tile_height, st_rows, st_cols, tile_img_list as tw, th, rows, cols, tileimglist
class Prototype:
    code = -1
    
    def __init__(self, coors : list, rotation : int) -> None:
        #Setup
        print("="*20+f"{coors} ROT:{rotation} CODE:{Prototype.code+1}"+"="*20)
        self.x, self.y = coors
        self.rotation = rotation
        self.img = tile_img_list[coors[0]][coors[1]].rotate(rotation*(-90))
        self.Img_inf = np.array(self.img.convert("L"))

        print(self.Img_inf)

        #Getting edge neighbors and their pixels
        self.n_cells = []
        self.valid_sockets = []
        self.SetNeighbors()




        pass
        Prototype.code +=1
        print("="*20+"end"+"="*20)

    def SetNeighbors(self):
        #Getting neighbor images according to rotation
        self.N = np.array(tile_img_list[(self.x-1)%st_rows][self.y])
        self.E = np.array(tile_img_list[self.x][(self.y+1)%st_cols])
        self.S = np.array(tile_img_list[(self.x+1)%st_rows][self.y])
        self.W = np.array(tile_img_list[self.x][(self.y-1)%st_cols])
        self.n_cells = [self.N, self.E, self.S, self.W]

        # Getting edge pixel values
        self.valid_sockets.append(self.n_cells[0][tile_w-1])
        self.valid_sockets.append([self.n_cells[1][i][0] for i in range(tile_w)])
        self.valid_sockets.append(self.n_cells[2][0][::-1])
        self.valid_sockets.append([self.n_cells[3][i][tile_w-1] for i in range(tile_w)][::-1])
        self.valid_sockets = Prototype.Shift(np.interp(self.valid_sockets, [0,1], [0,255]).astype('uint8').tolist(), self.rotation, -1)
        print("Sockets: \n",self.valid_sockets)

    def Shift(arr: list, step : int, direction : int):
        """
        -1 shifts forward
        1 shifts backward
        """
        return arr[step*direction:] + arr[:step*direction]

    def EdgePixels(self):
        edges = []
        edges.append(self.Img_inf[0].tolist())
        edges.append([self.Img_inf[i][tile_w-1] for i in range(tile_w)])
        edges.append(self.Img_inf[tile_w-1][::-1].tolist())
        edges.append([self.Img_inf[i][0] for i in range(tile_w)][::-1])
        return edges