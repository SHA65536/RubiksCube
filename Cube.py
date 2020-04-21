import numpy as np

class RubiksCube():
    # RubiksCube class representing a cube.

    # These are constants for array access
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

    X_AXIS = 0
    Z_AXIS = 1
    Y_AXIS = 2

    # These represent the destination of faces after rotation.
    X_AXIS_FACE_TRANSLATION = [5,4,2,3,0,1]
    Z_AXIS_FACE_TRANSLATION = [0,1,4,5,3,2]
    Y_AXIS_FACE_TRANSLATION = [3,2,0,1,4,5]

    # This is a helper for executing algorithms

    # Each move corresponds to the settings that will 
    # perform that move with the rotate function.
    MOVE_DICT = {
        'r': (X_AXIS,RIGHT_SLICE,False),
        'R': (X_AXIS,RIGHT_SLICE,True),
        'l': (X_AXIS,LEFT_SLICE,True),
        'L': (X_AXIS,LEFT_SLICE,False),
        'u': (Y_AXIS,TOP_SLICE,True),
        'U': (Y_AXIS,TOP_SLICE,False),
        'd': (Y_AXIS,BOTTOM_SLICE,False),
        'D': (Y_AXIS,BOTTOM_SLICE,True),
        'b': (Z_AXIS,BACK_SLICE,True),
        'B': (Z_AXIS,BACK_SLICE,False),
        'f': (Z_AXIS,FRONT_SLICE,False),
        'F': (Z_AXIS,FRONT_SLICE,True),
    }

    def __init__(self):
        #Initialization makes a solved cube.
        self.data = np.load('BaseCube.npy')
        self.complete_hash = [x for x in np.nditer(self.data)]

    @property
    def hash(self):
        return [x for x in np.nditer(self.data)]

    def is_solved(self):
        return self.hash == self.complete_hash

    def apply_algorithm(self, algo_string):
        for move in algo_string:
            self.make_move(move)

    def make_move(self, move):
        if move not in RubiksCube.MOVE_DICT:
            raise ValueError("Invalid Move!")
        move_settings = RubiksCube.MOVE_DICT[move]
        self.rotate(move_settings[0], move_settings[1], move_settings[2],)

    def rotate(self, axis, side, reverse):
        #don't touch and it will work :D
        new = np.copy(self.data)
        if axis == 0:
            for k in range(3):
                for j in range(3):
                    for i in range(6):
                        if reverse:
                            new[side][2-j][k][self.X_AXIS_FACE_TRANSLATION[i]] = self.data[side][k][j][i]
                        else:
                            new[side][k][j][i] = self.data[side][2-j][k][self.X_AXIS_FACE_TRANSLATION[i]]
        elif axis == 1:
            for k in range(3):
                for j in range(3):
                    for i in range(6):
                        if reverse:
                            new[2-j][k][side][self.Z_AXIS_FACE_TRANSLATION[i]] = self.data[k][j][side][i]
                        else:
                            new[k][j][side][i] = self.data[2-j][k][side][self.Z_AXIS_FACE_TRANSLATION[i]]
        elif axis == 2:
            for k in range(3):
                for j in range(3):
                    for i in range(6):
                        if reverse:
                            new[2-j][side][k][self.Y_AXIS_FACE_TRANSLATION[i]] = self.data[k][side][j][i]
                        else:
                            new[k][side][j][i] = self.data[2-j][side][k][self.Y_AXIS_FACE_TRANSLATION[i]]
        self.data = new