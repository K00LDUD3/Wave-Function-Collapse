import numpy as np
from Info import tile_w, img_arr

class Prototype:
    code = -1

    def __init__(self, coors : tuple, rotation : int) -> None:
        # f = open("Prototypes.txt", "a")
        # st = []
        # st.append(str("="*20+f"{coors} {rotation=} CODE:{Prototype.code+1}"+"="*20)+"\n")
        self.x, self.y = coors #TOP LEFT CORNER PIXEL 
        
        #Getting image with corresponding rotation
        self.img = np.ndarray((tile_w, tile_w), dtype = int)
        for i in range(tile_w):
            for j in range(tile_w):
                self.img[i][j] = img_arr[self.x+i][self.y+j]
        self.img = np.rot90(self.img, -1 * rotation)

        #Getting sockets of neighbour cells
        self.n_sockets = np.full((4,tile_w), -1).tolist()
        self.n_sockets[0] = [img_arr[(self.x-1)%img_arr.shape[0]][index] for index in range(self.y, self.y+tile_w)]
        self.n_sockets[1] = [img_arr[index][(self.y+tile_w)%img_arr.shape[1]] for index in range(self.x, self.x+tile_w)]
        self.n_sockets[2] = [img_arr[(self.x+tile_w)%img_arr.shape[0]][index] for index in range(self.y, self.y+tile_w)][::-1]
        self.n_sockets[3] = [img_arr[index][(self.y-1)%img_arr.shape[1]] for index in range(self.x+tile_w-1, self.x-1, -1)]
        self.n_sockets = Prototype.Shift(self.n_sockets, rotation, -1)
        
        #Getting sockets of own cell
        self.own_sockets = np.full((4,tile_w), -1).tolist()
        self.own_sockets[0] = self.img[0].tolist()
        self.own_sockets[1] = [self.img[index][tile_w-1] for index in range(tile_w)]
        self.own_sockets[2] = self.img[tile_w-1][::-1].tolist()
        self.own_sockets[3] = [self.img[index][0] for index in range(0, tile_w)][::-1]

        # st.append(str(f"{self.own_sockets=}\n"))
        # st.append(str(f"{self.n_sockets=}\n"))

        # st.append("IMG:\n")
        for x in self.img:
            temp = "["
            for j in range(self.img.shape[1]):
                temp = temp+f"{x[j]},"
            temp = temp[0:len(temp)-1]+"]\n"
            # st.append(temp)
        
        pass
        # st.append(str("\'"*25+f" END "+"\'"*25)+"\n")
        # f.writelines(st)
        Prototype.code +=1
        # f.close()

    def Shift(arr: list, step : int, direction : int):
        """
        -1 shifts forward
        1 shifts backward
        """
        return arr[step*direction:] + arr[:step*direction]