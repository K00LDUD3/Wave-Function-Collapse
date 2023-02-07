import pickle

socket_data = {
    "straight": [1,0,1,0],
    "ninety": [1,1,0,0],
    "plane": [0,0,0,0],
    "cross": [1,1,1,1],
    "tee": [1,1,0,1]
}

with open("MeshData.bin","wb") as f:
    pickle.dump(socket_data, f)

## in the order of S,E,N,w