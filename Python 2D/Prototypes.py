import numpy as np
from cachetools import Cache, LRUCache
from PIL import Image

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

