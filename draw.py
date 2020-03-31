import pyglet
from pyglet.gl import *
import math
import numpy as np
from completeCube import complete

def get_tex(file):
    tex = pyglet.image.load(file).get_texture()
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    return pyglet.graphics.TextureGroup(tex)

def add_block(x,y,z,colours,batch):
    #[0] = back, [1] = front, [2] = left, [3] = right, [4] = bottom, [5] = top

    X, Y, Z = x+1, y+1, z+1

    tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

    batch.add(4, GL_QUADS, colours[0],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords) 
    batch.add(4, GL_QUADS, colours[1],   ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords)

    batch.add(4, GL_QUADS, colours[2],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)
    batch.add(4, GL_QUADS, colours[3],   ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)

    batch.add(4, GL_QUADS, colours[4], ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)
    batch.add(4, GL_QUADS, colours[5],    ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)

def colourStringToTextureList(colourStr):
    colours = []
    for letter in colourStr:
        if letter == "R":
            colours.append(red)
        elif letter == "B":
            colours.append(blue)
        elif letter == "G":
            colours.append(green)
        elif letter == "Y":
            colours.append(yellow)
        elif letter == "O":
            colours.append(orange)
        elif letter == "W":
            colours.append(white)
        elif letter == "X":
            colours.append(black)
    return colours

def drawRubiks(cube, path):
    window = pyglet.window.Window(width=600, height=600, caption='Cube',resizable=True, visible=False)
    glClearColor(0.5,0.5,0.5,1)
    glEnable(GL_DEPTH_TEST)
    btch = pyglet.graphics.Batch()

    for i in range(3):
        for j in range(3):
            for k in range(3):
                colours = colourStringToTextureList(cube[i][j][k])
                add_block(i, j, k, colours, btch)

    @window.event
    def on_draw():
        window.clear()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, window.width/window.height, 0.05, 1000)

        glPushMatrix()
        glRotatef(-math.degrees(-math.asin(1/math.sqrt(3))),1,0,0)
        glRotatef(-45,0,1,0)
        glTranslatef(-4.5, -4.5, -4.5)

        btch.draw()
        glPopMatrix()
        pyglet.image.get_buffer_manager().get_color_buffer().save(path)
        window.close()

    try:
        pyglet.app.run()
    except AttributeError:
        pass

red = get_tex('tex/red.png')
blue = get_tex('tex/blue.png')
green = get_tex('tex/green.png')
yellow = get_tex('tex/yellow.png')
orange = get_tex('tex/orange.png')
white = get_tex('tex/white.png')
black = get_tex('tex/black.png')


if __name__ == '__main__':
    drawRubiks(complete, "test.png")
