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



# for i in range(1,len(motion_hpm_tops)):
# 	star_gaia_fg_motion = motion_hpm_tops[i]
# 	star_gaia_bg_motion = motion_bgs_tops[i]


# 	s_fg = CRUX_STAR()
# 	s_fg.set_motion_params(star_gaia_fg_motion)
	
# 	s_bg = CRUX_STAR()
# 	s_bg.set_motion_params(star_gaia_bg_motion)



# 	EYE = CRUX_EYEPIECE()
# 	EYE.add_star(s_fg)
# 	EYE.add_star(s_bg)
# 	# EYE.centring(0)
# 	img = EYE.draw_full()
# 	cv2.imshow('eyepiece image',img)
# 	k = cv2.waitKey(10000) 

# for i in range(1000):
# 	tick = i*0.01
# 	# EYE.centring(tick)
# 	img = EYE.draw(tick)
# 	cv2.imshow('eyepiece image',img)
# 	k = cv2.waitKey(50) 



# for i in range(1,len(motion_hpm_tops)):
star_gaia_fg_motion = motion_hpm_tops[1]
star_gaia_bg_motion = motion_bgs_tops[1]


s_fg = CRUX_STAR()
s_fg.set_motion_params(star_gaia_fg_motion)

s_bg = CRUX_STAR()
s_bg.set_motion_params(star_gaia_bg_motion)

EYE = CRUX_EYEPIECE()
EYE.add_star(s_fg)
EYE.add_star(s_bg)


INDEX = 1
DATE = 0
ERROR_SCOPE = 3


EVENT_LIST = []
TIME_LIST = []


def draw_SCOPE(INDEX,DATE,ERROR_PERCENT = 50):
	star_gaia_fg_motion = motion_hpm_tops[INDEX]
	star_gaia_bg_motion = motion_bgs_tops[INDEX]

	s_fg = CRUX_STAR()
	s_fg.set_motion_params(star_gaia_fg_motion)

	s_bg = CRUX_STAR()
	s_bg.set_motion_params(star_gaia_bg_motion)

	EYE = CRUX_EYEPIECE()
	EYE.add_star(s_fg)
	EYE.add_star(s_bg)

	img = EYE.draw_full(DATE,ERROR_PERCENT)
	cv2.imshow('eyepiece image',img)

def predict_and_draw_MICROLENS(INDEX,ERROR_PERCENT = 50):
	global DATE
	star_gaia_fg_motion = motion_hpm_tops[INDEX]
	star_gaia_bg_motion = motion_bgs_tops[INDEX]

	s_fg = CRUX_STAR()
	s_fg.set_motion_params(star_gaia_fg_motion)

	s_bg = CRUX_STAR()
	s_bg.set_motion_params(star_gaia_bg_motion)

	EYE = CRUX_EYEPIECE()
	EYE.add_star(s_fg)
	EYE.add_star(s_bg)

	timestamp,dist = EYE.predict_cluster_closest_approach(ERROR_SCOPE)
	print(timestamp)
	DATE = timestamp
	draw_SCOPE(INDEX,DATE,ERROR_SCOPE)

	# img = EYE.draw_full(DATE,ERROR_PERCENT)
	# cv2.imshow('eyepiece image',img)



# NEW_LIST = np.array([])

def predict_MICROLENS(INDEX,ERROR_PERCENT = 50):
	global DATE,EVENT_LIST
	star_gaia_fg_motion = motion_hpm_tops[INDEX]
	star_gaia_bg_motion = motion_bgs_tops[INDEX]

	s_fg = CRUX_STAR()
	s_fg.set_motion_params(star_gaia_fg_motion)

	s_bg = CRUX_STAR()
	s_bg.set_motion_params(star_gaia_bg_motion)

	EYE = CRUX_EYEPIECE()
	EYE.add_star(s_fg)
	EYE.add_star(s_bg)

	timestamp,dist = EYE.predict_cluster_closest_approach(ERROR_SCOPE)
	if dist < 10 and timestamp > 0:
		print("FOUND LENSING EVENT! @",INDEX)
		star_list = list(oneStarPair(INDEX))
		star_list.append(timestamp)
		EVENT_LIST.append(star_list)
		# TIME_LIST.append(timestamp)/




def date_change(val):
	global DATE
	DATE = val/365
	draw_SCOPE(INDEX,DATE,ERROR_SCOPE)

def error_change(val):
	global ERROR_SCOPE
	ERROR_SCOPE = val
	draw_SCOPE(INDEX,DATE,ERROR_SCOPE)


def set_index(val):
	global INDEX
	INDEX = int(val)
	draw_SCOPE(INDEX,DATE,ERROR_SCOPE)

def closest_approach(val):
	predict_and_draw_MICROLENS(INDEX,ERROR_SCOPE)


def predict(error):
	global INDEX,EVENT_LIST
	EVENT_LIST = []
	for i in range(1,len(STAR_DATAFRAME)):
		# INDEX = i
		predict_MICROLENS(i,error)
	headings = list(total_headings)
	headings.append('TIMESTAMP')
	print('headings')
	EVENT_FRAME = pd.DataFrame(EVENT_LIST, columns = headings)
	print(EVENT_FRAME)
	EVENT_FRAME.to_csv('future_microlensing_events.csv',index=False)


if len(sys.argv) < 3:
	img = EYE.draw_full(10)
	cv2.imshow('eyepiece image',img)

	windowName = 'controls'
	cv2.namedWindow('controls')
	cv2.createTrackbar('DATE', 'controls', 0, 100, date_change)
	cv2.createTrackbar('INDEX', 'controls', 1, 10000, set_index)
	cv2.createTrackbar('ERROR', 'controls', 1, 100, error_change)
	cv2.createTrackbar('PREDICT', 'controls', 0, 1, closest_approach)

	k = cv2.waitKey(0) 
	cv2.destroyAllWindows()
elif sys.argv[2] == 'predict':
	predict(0.1)
