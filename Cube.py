import numpy as np

class Cube():
    def __init__(self):
        self.data = np.load('BaseCube.npy')
        self.complete_hash = [x for x in np.nditer(self.data)]

    @property
    def hash(self):
        return [x for x in np.nditer(self.data)]
