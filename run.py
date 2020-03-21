import numpy as np
import draw
import moves
from os import remove
from completeCube import complete, completeHash
from itertools import product
import imageio
from pygifsicle import optimize
from time import clock

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

def makeInstructions(startInst=None, startLen=1, maxLen=0):
    while startLen != maxLen:
        for x in product(possibleMoves, repeat=startLen):
            if startInst:
                if ''.join(x) == startInst:
                    startInst = None
            else:
                yield ''.join(x)
        startLen+=1

def makeImagesFromString(moveString):
    cycleCount = 0
    moveCount = 0
    filenames = []
    cube = complete
    currHash = ""
    draw.createImage(cube,f"output/{moveString}_{moveCount:06}.png")
    filenames.append(f"output/{moveString}_{moveCount:06}.png")
    moveCount+=1
    draw.createImage(cube,f"output/{moveString}_{moveCount:06}.png")
    filenames.append(f"output/{moveString}_{moveCount:06}.png")
    while currHash != completeHash:
        cycleCount+=1
        for move in moveString:
            moveCount+=1
            cube = moves.moves[move](cube)
            draw.createImage(cube,f"output/{moveString}_{moveCount:06}.png")
            filenames.append(f"output/{moveString}_{moveCount:06}.png")
        currHash = hashCube(cube)
    return filenames
    
def makeGifFromString(moveString):
    filenames = makeImagesFromString(moveString)
    with imageio.get_writer(f'output/{moveString}.gif', mode='I', fps=3) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image,)
    optimize(f'output/{moveString}.gif')
    for filename in filenames:
        remove(filename)
    return f'output/{moveString}.gif'

def numberCrunch(cont=True, maxLen=0):
    count=0
    instruct = ""
    try:
        if(cont):
            with open("output.log",'r') as f:
                for line in f:
                    instruct, _ = line.split("\t")
                    count+=1
        else:
            remove("output.log")
    except FileNotFoundError:
        pass
    with open("output.log",'a') as f:
        for count, x in enumerate(makeInstructions(instruct,maxLen=maxLen),start=count):
            if checkInstruction(x):
                res = calcCycleNumFromString(x)
            else:
                res = "Redundant"
            if count % 100 == 0:
                f.flush()
                print(f"{x}\t{count}\t{res}")
            f.write(f"{x}\t{res}\n")

def minimizeInstruction(moveString):
    while True:
        cube = complete
        hashTable = [(completeHash)]
        for moveIndex, move in enumerate(moveString):
            cube = moves.moves[move](cube)
            currHash = hashCube(cube)
            try:
                key = hashTable.index((currHash))
                moveString = moveString[:key] + moveString[moveIndex+1:]
                break
            except ValueError:
                hashTable.append((currHash))
        else:
            break
    return moveString

def checkInstruction(moveString):
    cube = complete
    hashTable = [(completeHash)]
    for moveIndex, move in enumerate(moveString):
        cube = moves.moves[move](cube)
        currHash = hashCube(cube)
        if currHash in hashTable:
            return False
        else:
            hashTable.append((currHash))
    return True

def highestCycleNumber():
    highest = ("",0)
    count = 0
    with open("output.log",'r') as f:
        for line in f:
            instruct, cycles = line.split("\t")
            count += 1
            if cycles == "Redundant\n":
                continue
            cycles = int(cycles)
            if cycles > highest[1]:
                highest = (instruct, cycles)
    return (highest[0], highest[1], count)

if __name__ == "__main__":
    numberCrunch()