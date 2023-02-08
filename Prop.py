import pickle

socket_data = {
    "straight": {
        "sockets":[1,0,1,0],
        "fac":0.6
    },
    "ninety": {
        "sockets":[0,1,1,0],
        "fac":0.5
    },
    "plane": {
        "sockets":[0,0,0,0],
        "fac":0.4
    },
    "cross": {
        "sockets":[1,1,1,1],
        "fac":0.2

    },
    "tee": {
        "sockets":[0,1,1,1],
        "fac":0.3
    }
}

with open("MeshData.bin","wb") as f:
    pickle.dump(socket_data, f)

## in the order of NESW