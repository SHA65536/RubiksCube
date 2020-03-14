import numpy as np
import draw



if __name__ == "__main__":
    testCube = np.array([
            [
                #Left Slice
                [
                    #Bottom Side
                    ["O","X","B","X","W","X"],["X","X","B","X","W","X"],["X","R","B","X","W","X"]
                ],
                [
                    #Middle Side
                    ["O","X","B","X","X","X"],["X","X","B","X","X","X"],["X","R","B","X","X","X"]
                ],
                [
                    #Top Side
                    ["O","X","B","X","W","Y"],["X","X","B","X","X","Y"],["X","R","B","X","X","Y"]
                ]
            ],
            [
                #Middle Slice
                [
                    #Bottom Side
                    ["O","X","X","X","W","X"],["X","X","X","X","W","X"],["X","R","X","X","W","X"]
                ],
                [
                    #Middle Side
                    ["O","X","X","X","X","X"],["X","X","X","X","X","X"],["X","R","X","X","X","X"]
                ],
                [
                    #Top Side
                    ["O","X","X","X","X","Y"],["X","X","X","X","X","Y"],["X","R","X","X","X","Y"]
                ]
            ],
            [
                #Right Slice
                [
                    #Bottom Side
                    ["O","X","X","G","W","X"],["X","X","X","G","W","X"],["X","R","X","G","W","X"]
                ],
                [
                    #Middle Side
                    ["O","X","X","G","X","X"],["X","X","X","G","X","X"],["X","R","X","G","X","X"]
                ],
                [
                    #Top Side
                    ["O","X","X","G","X","Y"],["X","X","X","G","X","Y"],["X","R","X","G","X","Y"]
                ]
            ]
        ])
    draw.createImage(testCube, "img.png")