import numpy as np

class Cube():
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

    def __init__(self):
        self.data = np.load('BaseCube.npy')
        self.complete_hash = [x for x in np.nditer(self.data)]

    @property
    def hash(self):
        return [x for x in np.nditer(self.data)]

    
