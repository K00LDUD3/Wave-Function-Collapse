import numpy as np
from PIL import Image
import Info


class Prototype:
    code = -1
    def __init__(self, img, N, E, S, W) -> None:
        self.img = img
        self.N = [N]
        self.E = [E]
        self.S = [S]
        self.W = [W]
        Prototype.code += 1
        self.cd = Prototype.code
        pass
    
    @property
    def Img_inf(self):
        temp = np.array(self.img.convert("L"))
        return temp

    @property
    def EdgePixels(self):
        edges = []
        temp = self.Img_inf
        st_w, st_h = temp.shape
        #North
        edges.append(temp[0].tolist())
        #East
        edges.append(np.transpose(temp)[st_w-1].tolist())
        #South
        edges.append(temp[st_h-1].tolist()[::-1])
        #West
        edges.append(np.transpose(temp)[0].tolist()[::-1])
        return edges
    
    def Shift(self, step : int, direction : int):
        return self.EdgePixels[step*direction:] + self.EdgePixels[:step*direction]
