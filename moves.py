import numpy as np

LEFT_SLICE = 0
MIDDLE_SLICE = 1
RIGHT_SLICE = 2

BOTTOM_SLICE = 0
TOP_SLICE = 2

BACK_SLICE = 0
FRONT_SLICE = 2

BACK_FACE = 0
FRONT_FACE = 1
LEFT_FACE = 2
RIGHT_FACE = 3
BOTTOM_FACE = 4
TOP_FACE = 5

X_AXIS_FACE_TRANSLATION = [5,4,2,3,0,1]
Z_AXIS_FACE_TRANSLATION = [0,1,4,5,3,2]
Y_AXIS_FACE_TRANSLATION = [3,2,0,1,4,5]

def right_forward(source):
    return x_axis(source, True, False)

def right_reverse(source):
    return x_axis(source, True, True)

def left_forward(source):
    return x_axis(source, False, False)
    
def left_reverse(source):
    return x_axis(source, False, True)

def x_axis(source, right, reverse):
    side = RIGHT_SLICE if right else LEFT_SLICE
    target = np.copy(source)

    for k in range(3):
        for j in range(3):
            for i in range(6):
                if reverse:
                    target[side][2-j][k][X_AXIS_FACE_TRANSLATION[i]] = source[side][k][j][i]
                else:
                    target[side][k][j][i] = source[side][2-j][k][X_AXIS_FACE_TRANSLATION[i]]
            
    return target

def back_forward(source):
    return z_axis(source, True, False)

def back_reverse(source):
    return z_axis(source, True, True)

def front_forward(source):
    return z_axis(source, False, False)
    
def front_reverse(source):
    return z_axis(source, False, True)

def z_axis(source, back, reverse):
    side = BACK_SLICE if back else FRONT_SLICE
    target = np.copy(source)

    for k in range(3):
        for j in range(3):
            for i in range(6):
                if reverse:
                    target[2-j][k][side][Z_AXIS_FACE_TRANSLATION[i]] = source[k][j][side][i]
                else:
                    target[k][j][side][i] = source[2-j][k][side][Z_AXIS_FACE_TRANSLATION[i]]
            
    return target

def down_forward(source):
    return y_axis(source, True, False)

def down_reverse(source):
    return y_axis(source, True, True)

def up_forward(source):
    return y_axis(source, False, False)
    
def up_reverse(source):
    return y_axis(source, False, True)

def y_axis(source, down, reverse):
    side = BOTTOM_SLICE if down else TOP_SLICE
    target = np.copy(source)

    for k in range(3):
        for j in range(3):
            for i in range(6):
                if reverse:
                    target[2-j][side][k][Y_AXIS_FACE_TRANSLATION[i]] = source[k][side][j][i]
                else:
                    target[k][side][j][i] = source[2-j][side][k][Y_AXIS_FACE_TRANSLATION[i]]
            
    return target

moves = {
    'r': right_forward,
    'R': right_reverse,
    'l': left_reverse,
    'L': left_forward,
    'u': up_reverse,
    'U': up_forward,
    'd': down_forward,
    'D': down_reverse,
    'b': back_reverse,
    'B': back_forward,
    'f': front_forward,
    'F': front_reverse
}