import numpy as np
import draw
import moves
from completeCube import complete, completeHash

def hashCube(cube):
    hashString = ""
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(6):
                    hashString += cube[i][j][k][l]
    return hashString

if __name__ == "__main__":
    cube = complete
    currHash = ""
    cnt = 0
    while currHash != completeHash:
        draw.createImage(cube, f"output/{cnt:03}.png")
        cube = moves.upForward(cube)
        cnt+=1
        draw.createImage(cube, f"output/{cnt:03}.png")
        cube = moves.rightForward(cube)
        cnt+=1
        currHash = hashCube(cube)
    draw.createImage(cube, f"output/{cnt:03}.png")