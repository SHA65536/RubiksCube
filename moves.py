import numpy as np
import draw

LeftSlice = 0
MiddleSlice = 1
RightSlice = 2

BottomSlice = 0
TopSlice = 2

BackSlice = 0
FrontSlice = 2

BackFace = 0
FrontFace = 1
LeftFace = 2
RightFace = 3
BottomFace = 4
TopFace = 5

xAxisFaceTranslation = [5,4,2,3,0,1]
zAxisFaceTranslation = [0,1,4,5,3,2]
yAxisFaceTranslation = [3,2,0,1,4,5]

def rightForward(source):
    return xAxis(source, True, False)

def rightReverse(source):
    return xAxis(source, True, True)

def leftForward(source):
    return xAxis(source, False, False)
    
def leftReverse(source):
    return xAxis(source, False, True)

def xAxis(source, right, reverse):
    Side = RightSlice if right else LeftSlice
    target = np.copy(source)

    for k in range(3):
        for j in range(3):
            for i in range(6):
                if reverse:
                    target[Side][2-j][k][xAxisFaceTranslation[i]] = source[Side][k][j][i]
                else:
                    target[Side][k][j][i] = source[Side][2-j][k][xAxisFaceTranslation[i]]
            
    return target

def backForward(source):
    return zAxis(source, True, False)

def backReverse(source):
    return zAxis(source, True, True)

def frontForward(source):
    return zAxis(source, False, False)
    
def frontReverse(source):
    return zAxis(source, False, True)

def zAxis(source, back, reverse):
    Side = BackSlice if back else FrontSlice
    target = np.copy(source)

    for k in range(3):
        for j in range(3):
            for i in range(6):
                if reverse:
                    target[2-j][k][Side][zAxisFaceTranslation[i]] = source[k][j][Side][i]
                else:
                    target[k][j][Side][i] = source[2-j][k][Side][zAxisFaceTranslation[i]]
            
    return target

def downForward(source):
    return yAxis(source, True, False)

def downReverse(source):
    return yAxis(source, True, True)

def upForward(source):
    return yAxis(source, False, False)
    
def upReverse(source):
    return yAxis(source, False, True)

def yAxis(source, down, reverse):
    Side = BottomSlice if down else TopSlice
    target = np.copy(source)

    for k in range(3):
        for j in range(3):
            for i in range(6):
                if reverse:
                    target[2-j][Side][k][yAxisFaceTranslation[i]] = source[k][Side][j][i]
                else:
                    target[k][Side][j][i] = source[2-j][Side][k][yAxisFaceTranslation[i]]
            
    return target

moves = {
    'r': rightForward,
    'R': rightReverse,
    'l': leftReverse,
    'L': leftForward,
    'u': upReverse,
    'U': upForward,
    'd': downForward,
    'D': downReverse,
    'b': backReverse,
    'B': backForward,
    'f': frontForward,
    'F': frontReverse
}