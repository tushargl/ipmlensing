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


from blackroom import CRUX_STAR,CRUX_EYEPIECE
import cv2

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


basic_hpm_tops = STAR_ARR[:,[0 ,1 ,8 ,13,17]]
basic_bgs_tops = STAR_ARR[:,[19,25,26,27,28]]


motion_hpm_tops = STAR_ARR[:,[2 ,11,3 ,12,9 ,14,10,15]]



motion_bgs_tops = STAR_ARR[:,[21,22,23,24,29,30,31,32]]


# basic_bgs_tops = total_headings[:[0]]
# motion_bgs_tops = total_headings[:[0]]

def index_printer(l):
	for i in range(len(l)):
		# print(, end = " ")
		print(i,'\t',l[i])

def index2_printer(l,m = []):
	for i in range(len(l)):
		# print(, end = " ")
		print(i,'\t\t',l[i],'\t\t',m[i])


index_printer(total_headings)
index2_printer(basic_hpm_tops[0],basic_bgs_tops[0])
index2_printer(motion_hpm_tops[0],motion_bgs_tops[0])



# 1st pair 
star_gaia_fg_motion = motion_hpm_tops[1]
star_gaia_bg_motion = motion_bgs_tops[1]

# 0 RA 1 E_RA
# 2 DEC 3 E_DEC
# 4 PM_RA 5 E_PM_RA
# 6 PM_DEC 7 E_PM_DEC



for i in range(1,len(motion_hpm_tops)):
	star_gaia_fg_motion = motion_hpm_tops[i]
	star_gaia_bg_motion = motion_bgs_tops[i]


	s_fg = CRUX_STAR()

	s_fg.set_in_sky(star_gaia_fg_motion[0],star_gaia_fg_motion[2])
	s_fg.pma(star_gaia_fg_motion[4],star_gaia_fg_motion[6])

	s_bg = CRUX_STAR()

	s_bg.set_in_sky(star_gaia_bg_motion[0],star_gaia_bg_motion[2])
	s_bg.pma(star_gaia_bg_motion[4],star_gaia_bg_motion[6])




	EYE = CRUX_EYEPIECE()
	EYE.add_star(s_fg)
	EYE.add_star(s_bg)
	# EYE.centring(0)
	img = EYE.draw_full()
	cv2.imshow('eyepiece image',img)
	k = cv2.waitKey(10000) 

# for i in range(1000):
# 	tick = i*0.01
# 	# EYE.centring(tick)
# 	img = EYE.draw(tick)
# 	cv2.imshow('eyepiece image',img)
# 	k = cv2.waitKey(50) 
