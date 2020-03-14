import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
import numpy as np

class Model:

    def get_tex(self,file):
        tex = pyglet.image.load(file).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def add_block(self,x,y,z,colours):
        #[0] = back, [1] = front, [2] = left, [3] = right, [4] = bottom, [5] = top

        X, Y, Z = x+1, y+1, z+1

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

        self.batch.add(4, GL_QUADS, colours[0],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords) # back
        self.batch.add(4, GL_QUADS, colours[1],   ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords) # front

        self.batch.add(4, GL_QUADS, colours[2],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)  # left
        self.batch.add(4, GL_QUADS, colours[3],   ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)  # right

        self.batch.add(4, GL_QUADS, colours[4], ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)  # bottom
        self.batch.add(4, GL_QUADS, colours[5],    ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)  # top

    def __init__(self, listOfCubes):
        #char [3][3][3][6]
        self.red = self.get_tex('tex/red.png')
        self.blue = self.get_tex('tex/blue.png')
        self.green = self.get_tex('tex/green.png')
        self.yellow = self.get_tex('tex/yellow.png')
        self.orange = self.get_tex('tex/orange.png')
        self.white = self.get_tex('tex/white.png')
        self.black = self.get_tex('tex/black.png')

        self.batch = pyglet.graphics.Batch()

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    colours = self.colourStringToTextureList(listOfCubes[i][j][k])
                    self.add_block(i, j, k, colours)

    def colourStringToTextureList(self, colourStr):
        colours = []
        for letter in colourStr:
            if letter == "R":
                colours.append(self.red)
            elif letter == "B":
                colours.append(self.blue)
            elif letter == "G":
                colours.append(self.green)
            elif letter == "Y":
                colours.append(self.yellow)
            elif letter == "O":
                colours.append(self.orange)
            elif letter == "W":
                colours.append(self.white)
            elif letter == "X":
                colours.append(self.black)
        return colours

    def draw(self):
        self.batch.draw()

class Player:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def mouse_motion(self, dx, dy):
        dx/= 8
        dy/= 8
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0]>90:
            self.rot[0] = 90
        elif self.rot[0] < -90:
            self.rot[0] = -90

    def update(self,dt,keys):
        sens = 0.1
        s = dt*10
        rotY = -self.rot[1]/180*math.pi
        dx, dz = s*math.sin(rotY), math.cos(rotY)
        if keys[key.W]:
            self.pos[0] += dx*sens
            self.pos[2] -= dz*sens
        if keys[key.S]:
            self.pos[0] -= dx*sens
            self.pos[2] += dz*sens
        if keys[key.A]:
            self.pos[0] -= dz*sens
            self.pos[2] -= dx*sens
        if keys[key.D]:
            self.pos[0] += dz*sens
            self.pos[2] += dx*sens
        if keys[key.SPACE]:
            self.pos[1] += s
        if keys[key.LSHIFT]:
            self.pos[1] -= s

class Window(pyglet.window.Window):

    def push(self,pos,rot):
        glPushMatrix()
        rot = self.player.rot
        pos = self.player.pos
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0], -pos[1], -pos[2])

    def Projection(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def Model(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set2d(self):
        self.Projection()
        gluPerspective(0, self.width, 0, self.height)
        self.Model()

    def set3d(self):
        self.Projection()
        gluPerspective(70, self.width/self.height, 0.05, 1000)
        self.Model()

    def setLock(self, state):
        self.lock = state
        self.set_exclusive_mouse(state)

    lock = False
    mouse_lock = property(lambda self:self.lock, setLock)

    def __init__(self, path, cube, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(300,200)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.path = path 
        pyglet.clock.schedule(self.update)

        self.model = Model(cube)
        self.player = Player((4.5,4.5,4.5),(-45,45))

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock: self.player.mouse_motion(dx,dy)

    def on_key_press(self, KEY, _MOD):
        if KEY == key.ESCAPE:
            self.close()
        elif KEY == key.E:
            self.mouse_lock = not self.mouse_lock

    def update(self, dt):
        self.player.update(dt, self.keys)

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        self.model.draw()
        glPopMatrix()
        pyglet.image.get_buffer_manager().get_color_buffer().save(self.path)
        self.close()


def createImage(cube, path):
    window = Window(cube=cube,path=path,width=600, height=600, caption='Cube',resizable=True)
    glClearColor(0.5,0.5,0.5,1)
    glEnable(GL_DEPTH_TEST)
    try:
        pyglet.app.run()
    except AttributeError:
        pass
