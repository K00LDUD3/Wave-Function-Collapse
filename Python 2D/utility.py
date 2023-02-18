import numpy as np

#Length of each individual pixel info is 2 bits
def GetByteMask(x : np.ndarray):
    print(x)
    mask = ''
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            temp = bin(x[i,j])[2:]
            for k in range(2-len(temp)):
                temp = '0'+temp
            mask += temp
    
    return (int(mask, base=2))
 
def GetBin(x : int, length = 2) -> str:
    x_b = bin(x)[2:]
    for k in range(length-len(x_b)):
        x_b = '0'+x_b
    return x_b

def GetInt(x):
    return int(x, base=2)