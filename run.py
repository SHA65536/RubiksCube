import numpy as np
import draw
import moves
from completeCube import complete, completeHash
from itertools import combinations_with_replacement

possibleMoves = "rRlLuUdDfFbB"

def hashCube(cube):
    hashString = [x for x in np.nditer(cube)]
    return hashString

def calcCycleNumFromString(moveString):
    count = 0
    cube = complete
    currHash = ""
    while currHash != completeHash:
        count+=1
        for move in moveString:
            cube = moves.moves[move](cube)
        currHash = hashCube(cube)
    return count

def makeInstructions(start=1):
    while True:
        for x in combinations_with_replacement(possibleMoves,start):
            yield ''.join(x)
        start+=1


if __name__ == "__main__":
    with open("output.log",'w') as f:
        for count, x in enumerate(makeInstructions()):
            if count % 100 == 0:
                f.flush()
                print(x)
            f.write(f"{x}\t{calcCycleNumFromString(x)}\n")