import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path

import matplotlib.path as mpath


import numpy as np

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import math
# import pygame 
import numpy as np
from sklearn.preprocessing import normalize

from quaternion import Quaternion as qt


import itertools

import math

def XYZ_from_ra_dec(ra,dec,radius):
    x = radius * math.cos(ra) *math.sin(dec)
    y = radius * math.sin(ra) *math.sin(dec)
    z = radius * math.cos(dec)

    return (x,y,z)

# PROCESS



STAR_DATAFRAME = pd.read_csv(sys.argv[1], header=None)
print("/CRUX/LOG> LOADED DATAFRAME SHAPE:",STAR_DATAFRAME.shape)
# print(STAR_DATAFRAME.loc[[0]])

STAR_ARR = STAR_DATAFRAME.to_numpy()

print("/CRUX/LOG> NUMPY ARRAY SHAPE:",STAR_ARR.shape)
# print(STAR_ARR)

def oneStarPair(n):
    return STAR_ARR[n]


def oneStarColumn(m):
    return STAR_ARR[:,m]


total_headings = oneStarPair(0)
basic_hpm_tops = total_headings[:4]


print(total_headings)
print(basic_hpm_tops)

all_ra_hpm = oneStarColumn(2)
all_dec_hpm = oneStarColumn(3)

print(all_ra_hpm)
print(all_dec_hpm)

coords = zip(all_ra_hpm,all_dec_hpm)
# for x in range(0,10):
#     print(oneStarPair(x))
coords = list(itertools.islice(coords, 5000))

coords = coords[1:]
print(coords)






















position = [1,1,1]
heading = []
position = [position[0],position[1],position[2]]


class Haal(object):
    def __init__(self):
        self.rotation_Q = qt.from_axisangle(0.0,(0,0,1))
        self.position_P = [0,0,0]
    def locate(self,x,y,z):
        self.position_P = [x,y,z]

class Thing(object):
    def __init__(self,draw_function,draw_args):
        self.draw_function = draw_function
        self.draw_args = draw_args
        self.haal = Haal()
    def make(self):
        # Q_filterred = self.Q_filterred
        w, v = self.haal.rotation_Q.get_axisangle()
        w_degrees = w*180/math.pi
        location = self.haal.position_P
        glPushMatrix()
        glTranslatef(location[0],location[1],location[2])
        print(location)
        glRotatef(w_degrees,v[0],v[1],v[2])
        self.draw_function(*self.draw_args)
        glPopMatrix()
    def locate(self,x,y,z):
        self.haal.locate(x,y,z)

class Scene(object):
    def __init__(self):
        self.objects = []
        self.scenes = []
        self.scales = []
        self.coordinates = [0.,0.,0.]
    def add_object(self,thing):
        self.objects.append(thing)
    def add_scene(self,scene,x,y,z):
        self.scenes.append(scene)
        self.scales.append([x,y,z])
    def fix_position(self,coords):
        self.coordinates = coords
    def make_scene(self,depth=0):
        if depth > 10:
            return
        glPushMatrix()
        glTranslatef(self.coordinates[0],self.coordinates[1],self.coordinates[2])
        for o in self.objects:
            print(o)
            o.make()
        for s in range(len(self.scenes)):
            scale = self.scales[s]
            glPushMatrix()
            glScalef(scale[0],scale[1],scale[2])
            self.scenes[s].make_scene(depth+1)
            glPopMatrix()
        glPopMatrix()
# _CUBE_1 = Thing(glutWireCube,(.1,))
# _CUBE_2 = Thing(glutWireCube,(.1,))
# _CUBE_2.locate(.1,.0,.0)



_CELESTIAL_SPHERE_ = Thing(glutWireSphere,(.1,10,10))


def plane(x,y):
    glScalef(x,y,0.01)
    glutWireCube(1.)
# _PLANE_ = Thing(plane,(.2,.2))
# _PLANE_.locate()
SCENE_1 = Scene()
# SCENE_1.add_object(_CUBE_1)
SCENE_1.add_object(_CELESTIAL_SPHERE_)



for i in coords:
    x,y,z = XYZ_from_ra_dec(float(i[0]),float(i[1]),0.1)
    _STAR_  = Thing(glutSolidSphere,(.001,20,20))
    _STAR_.locate(x,y,z)
    SCENE_1.add_object(_STAR_)
    print(x,y,z)

    






# SCENE_1.add_object(_PLANE_)
SCENE_1.fix_position([0,0,0])

SCENE_VIEW_FROM_EARTH = Scene()
SCENE_VIEW_FROM_EARTH.add_scene(SCENE_1,1,1,1)

SCENE_TABLE = Scene()


class Room(object):
    def __init__(self):
        self.window_name = "Empty"
        self.camera_heading = [0,0,0]
        self.window_function()
    def update(self):
        self.draw_function()
    def look_at_scene(self):
        # glMatrixMode(GL_PROJECTION)
        d = math.sqrt(sum([x*x for x in position]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.,1.,d/100.,4*d)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(position[0],position[1],position[2],
          0,0,0,
          0,0,1)
    def draw_room(self):
        glPushMatrix()
        # glTranslatef(position[0],position[1],position[2])
        glutWireCube(1.0)
        glPopMatrix()
    def keyboard_funtion(self,*args):
        global position
        d = math.sqrt(sum([x*x for x in position]))
        key = str(args[0],'utf-8')
        print(key)
        if key == ' ':
            snap_zero = True
        if key == 'w':
            position = [position[0]*(1-0.1),position[1]*(1-0.1),position[2]*(1-0.1)]
        if key == 's':
            position = [position[0]*(1+0.1),position[1]*(1+0.1),position[2]*(1+0.1)]
        if key == 'd':
            position = np.add(position,np.cross(position,[0,0,1])*0.1)
        if key == 'a':
            position = np.subtract(position,np.cross(position,[0,0,1])*0.1)
        if key == 'r':
            position = [2,2,0]
        print(position)
    def draw_display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        color = [1.0,0.,0.,1.]
        self.look_at_scene()
        glPushMatrix()
        self.draw_room()
        SCENE_VIEW_FROM_EARTH.make_scene()
        glPopMatrix()
        glutSwapBuffers()
        return
    def window_function(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(300,300)
        glutCreateWindow(self.window_name)

        glClearColor(0.,0.,0.,1.)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glutKeyboardFunc(self.keyboard_funtion)
        glutDisplayFunc(self.draw_display)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(40.,1.,1.,40.)
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0,0,10,
                  0,0,0,
                  0,1,1)
        glPushMatrix()
        # glutMainLoop()
        return
    def draw_function(self):
        glutPostRedisplay()
        glutMainLoopEvent()

# iloc[1]

R = Room()
R.update()
while 21:
    R.update()
    # for i in range(1000000):
    #     pass


