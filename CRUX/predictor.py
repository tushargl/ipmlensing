import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path

import matplotlib.path as mpath


import numpy as np

# import pygame 
import numpy as np
from sklearn.preprocessing import normalize



import itertools

import math


from whiteroom import Thing,Scene,Room

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
coords = list(itertools.islice(coords, 500))

coords = coords[1:]
print(coords)
























# _CUBE_1 = Thing(glutWireCube,(.1,))
# _CUBE_2 = Thing(glutWireCube,(.1,))
# _CUBE_2.locate(.1,.0,.0)


from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


_CELESTIAL_SPHERE_ = Thing(glutWireSphere,(.1,10,10))

SCENE_1 = Scene()

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



# iloc[1]

R = Room(SCENE_VIEW_FROM_EARTH)
R.update()
while 21:
    R.update()
    # for i in range(1000000):
    #     pass


