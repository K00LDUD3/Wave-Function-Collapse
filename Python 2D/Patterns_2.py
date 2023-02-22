import numpy as np
from PIL import Image
from Info import tile_img_list, st_rows, st_cols, tile_w
# from Info import tile_width, tile_height, st_rows, st_cols, tile_img_list as tw, th, rows, cols, tileimglist
class Prototype:
    code = -1
    
    def __init__(self, coors : list) -> None:
        self.x, self.y = coors
        self.img = tile_img_list[self.x][self.y]
        self.edgeNeighbors = self.SetEdgeNeighbors()
        self.cornerNeighbors = self.SetCornerNeighbors()
        self.prob_fac = self.Img_inf.mean()/255
        Prototype.code += 1
        self.edgePixels = self.GetEdgePixels()
        self.cornerPixels = self.GetCornerPixels()



        self.cd = Prototype.code
        print("="*30+f" {self.x},{self.y} "+"="*30)
        print(self.CornerNeighbors, self.EdgeNeighbors)
        print(self.edgePixels)
        print(f"{self.cornerPixels =}")

    def SetEdgeNeighbors(self):
        # self.N = [(self.x*tile_w-1)%st_rows, self.y]
        # self.E = [self.x, (self.y*tile_w+1)%st_cols]
        # self.S = [(self.x*tile_w+1)%st_rows, self.y]
        # self.W = [self.x,(self.y*tile_w-1)%st_cols]

        self.N = [(self.x-1)%st_rows, self.y]
        self.E = [self.x, (self.y+1)%st_cols]
        self.S = [(self.x+1)%st_rows, self.y]
        self.W = [self.x,(self.y-1)%st_cols]
        return [self.N, self.E, self.S, self.W]

    def SetCornerNeighbors(self):
        self.NW = [(self.x*tile_w-1)%st_rows, (self.y*tile_w-1)%st_cols]
        self.NE = [(self.x*tile_w-1)%st_rows, (self.y*tile_w+1)%st_cols]
        self.SW = [(self.x*tile_w+1)%st_rows, (self.y*tile_w-1)%st_cols]
        self.SE = [(self.x*tile_w+1)%st_rows,(self.y*tile_w+1)%st_cols]
        return [self.NE, self.SE, self.SW, self.NW]

    @property
    def EdgeNeighbors(self):
        return [self.N, self.E, self.S, self.W]

    @property
    def CornerNeighbors(self):
        return [self.NE, self.SE, self.SW, self.NW]
    
    @property
    def Img_inf(self):
        return np.array(self.img.convert("L"))
        


    def GetEdgePixels(self):
        edges = []
        temp = self.Img_inf
        st_w, st_h = temp.shape
        #North
        edges.append(temp[0].tolist())
        #East
        edges.append(temp.transpose()[st_w-1].tolist())
        #South
        edges.append(temp[st_h-1].tolist()[::-1])
        #West
        edges.append(temp.transpose()[0].tolist()[::-1])
        return edges
    
    def GetCornerPixels(self):
        return [i[tile_w-1] for i in self.GetEdgePixels()]
        
    
    def Shift(self, step : int, direction : int):
        return self.edgePixels[step*direction:] + self.edgePixels[:step*direction]
