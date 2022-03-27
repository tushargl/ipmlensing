import cv2
import numpy as np
import math
from quaternion import normalize
import random
import time    

def plot2Stars(s1,s2,timestamp):
	height, width = 1024, 1024
	img = np.zeros((height, width, 3), np.uint8)
	# img[:, :] = [255, 255, 255]


	row, col = 512, 512
	cv2.circle(img,(col, row), 500, (255,255,255), 1)

	c_1 = s1.future_pos(timestamp)
	c_2 = s2.future_pos(timestamp)

	cv2.circle(img,c_1, 5, (255,255,255), -1)
	cv2.circle(img,c_2, 5, (255,255,255), -1)

	return img

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 0.5
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2


def sqrt_dist(v1,v2):

	x_diff = v1[0] - v2[0]
	y_diff = v1[1] - v2[1]


	return math.sqrt(x_diff*x_diff + y_diff*y_diff)

def statictical_distance(cluster_1,cluster_2):
	# pass
	iters = 10
	dizt = 0
	for x in range(iters):
		v1 = random.choice(cluster_1)
		v2 = random.choice(cluster_2)
		d = sqrt_dist(v1,v2)
		dizt += d 
	dizt /= iters
	return dizt



class CRUX_STAR(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.ra = 0
		self.ra_err = 0
		self.dec = 0
		self.dec_err = 0
		self.pm_ra = 1
		self.pm_ra_err = 1
		self.pm_dec = 1
		self.pm_dec_err = 1

	def move(self,x,y):
		self.x = x
		self.y = y
	def set_in_sky(self,ra,dec):
		self.ra = float(ra)
		self.dec = float(dec)
	def set_motion_params(self,params):
		
		# POSITION

		self.ra 		= float(params[0])  #DEGREES -> DEGREES
		self.ra_err 	= float(params[1])/3600  #ARCSECOND -> DEGREES
		
		self.dec 		= float(params[2]) #DEGREES -> DEGREES
		self.dec_err 	= float(params[3])/3600 #ARCSECOND -> DEGREES
		

		# MOTION
		self.pm_ra 		= float(params[4])/1000 #MAS/yr -> AS/yr
		self.pm_ra_err 	= float(params[5])/100  #PERCENT -> UNITLESS
		

		self.pm_dec 	= float(params[6])/1000  #MAS/ys -> AS/ys
		self.pm_dec_err = float(params[7])/100  #PERCENT -> UNITLESS


	def pma(self,pm_ra,pm_dec):
		self.pm_ra = float(pm_ra)
		self.pm_dec = float(pm_dec)
	def future_pos(self,timestamp):
		# print(self.ra)
		# print(self.dec)
		# print(self.x_v)
		# print(self.y_v)
		# print(timestamp)

		# TIMESTAMP in YEARS

		# timestamp = timestamp

		f_ra = self.ra + self.pm_ra*timestamp
		f_dec = self.dec + self.pm_dec*timestamp
		return (f_ra,f_dec)
	def future_error(self,timestamp,e_margin = 10):
		# print(self.ra)
		# print(self.dec)
		# print(self.x_v )
		# print(self.y_v)
		# print(timestamp)

		# TIMESTAMP in YEARS

		# timestamp = timestamp


		# s_to_n 
		# s_to_n_ra

		error_percent = e_margin/100.

		ra_position_err_percent = np.random.normal(1.0,error_percent)
		ra_proper_motion_err_percent = np.random.normal(1.0,error_percent)
		dec_position_err_percent = np.random.normal(1.0,error_percent)
		dec_proper_motion_err_percent = np.random.normal(1.0,error_percent)

		# print("\n\n-----------ERRORRS-----------\t\t", end = '\n\n')

		# print("ra_err\t\t", end = '\t')
		# print("pm_ra_err\t\t", end = '\t')
		# print("dec_err\t\t", end = '\t')
		# print("pm_dec_err\t\t")

		# print(self.ra_err, end = '\t')
		# print(self.pm_ra_err, end = '\t')
		# print(self.dec_err, end = '\t')
		# print(self.pm_dec_err)

		# print("ra_position_err_percent", end = '\t')
		# print("ra_proper_motion_err_percent", end = '\t')
		# print("dec_position_err_percent", end = '\t')
		# print("dec_proper_motion_err_percent")

		# print(ra_position_err_percent, end = '\t')
		# print(ra_proper_motion_err_percent, end = '\t')
		# print(dec_position_err_percent, end = '\t')
		# print(dec_proper_motion_err_percent)

		# poss_ra = self.ra + ra_position_err_percent*self.ra_err
		# poss_dec = self.dec + dec_position_err_percent*self.ra_err
		# poss_ra = self.ra + ra_position_err_percent*self.ra_err
		# poss_dec = self.dec + dec_position_err_percent*self.ra_err

		poss_pm_ra = self.pm_ra*ra_proper_motion_err_percent
		poss_pm_dec = self.pm_dec*dec_proper_motion_err_percent



		# future_pos = self.future_pos(timestamp)

		# f_ra = poss_ra + poss_pm_ra*timestamp
		# f_dec = poss_dec + poss_pm_dec*timestamp


		f_ra = self.ra + poss_pm_ra*timestamp
		f_dec = self.dec + poss_pm_dec*timestamp

		# print("FUTURE ERROR: ",(f_ra,f_dec))
		return (f_ra,f_dec)
	def plot_self(self,img,timestamp):
		cen = self.future_pos(timestamp) 
		cv2.circle(img,cen, 5, (255,255,255), -1)
		return img
	def norm_movement(self):

		m_tot = math.sqrt(self.pm_ra*self.pm_ra + self.pm_dec*self.pm_dec)

		nm_ra = self.pm_ra/m_tot
		nm_dec = self.pm_dec/m_tot

		return (nm_ra,nm_dec)
	def scaled_movement(self,scale):

		m_tot = math.sqrt(self.pm_ra*self.pm_ra + self.pm_dec*self.pm_dec)

		nm_ra = self.pm_ra/m_tot
		nm_dec = self.pm_dec/m_tot





		return (nm_ra,nm_dec)
	def __str__(self):
		# return "RA: {:.10f} :  DEC :{:.10f} ".format(self.ra,self.dec)
		return "RA: {0} :  DEC :{1} \n".format(self.ra,self.dec)+"ra_err: {0} :  dec_err :{1} \n".format(self.ra_err,self.dec_err)+"pm_ra: {0} :  pm_dec :{1} \n".format(self.pm_ra,self.pm_dec)+"pm_ra_err: {0} :  pm_dec_err :{1} \n".format(self.pm_ra_err,self.pm_dec_err)




class CRUX_EYEPIECE(object):
	def __init__(self):
		self.ra_target = 0
		self.dec_target = 0
		self.fov_ra = 10
		self.fov_dec = 10
		self.stars = []
		self.height = 1024
		self.width = 1024
		self.pp_ra = 102.4
		self.pp_dec = 102.4
	def calculate_cluster_distance(self,timestamp,e_margin):
		# print("TIMESTAMP", timestamp)
		# print("ERROR MARGIN", e_margin)
		if not len(self.stars) == 2:
			return
		star_0 = self.stars[0]
		star_1 = self.stars[1]

		s0_proj = self.projectStar(star_0,timestamp)
		s0_proj_errors = self.projectErrors(star_0,timestamp,e_margin)

		s1_proj = self.projectStar(star_1,timestamp)
		s1_proj_errors = self.projectErrors(star_1,timestamp,e_margin)

		abs_dist = sqrt_dist(s0_proj,s1_proj)
		stat_dist = statictical_distance(s0_proj_errors,s1_proj_errors)
		return (abs_dist,stat_dist)		
	def predict_cluster_closest_approach(self,e_margin):
		if not len(self.stars) == 2:
			return

		last_dist = 100000000000
		last_stat_dist = 100000000000
		closest_timestamp = 0


		backtrace = False
		saturated = False

		new_time = 0
		time_delta = 0.0001
		time_decay = 0.7

		min_delta = 0.000001
		# time_

		max_lookups = 1000
		curr_lookup = 0

		# print("INTIAL TIMESTAMP: {f} , ABS_DIST: {f}, STAT_DIST: {f}",closest_timestamp,last_dist,last_stat_dist)
		while not saturated and curr_lookup < max_lookups:
			curr_lookup += 1
			new_time = new_time + time_delta
			abs_dist, stat_dist = self.calculate_cluster_distance(new_time,e_margin)

			# print("CUREENT LOOKUP: " , curr_lookup, end = "")
			# print("\t\tTIME -> ",new_time,"\tabs dist", abs_dist, "\tstat_dist",stat_dist)
			if abs_dist < last_dist or  stat_dist < last_stat_dist:
				closest_timestamp = new_time
				last_dist = abs_dist
				last_stat_dist = stat_dist
			else:
				if time_delta < min_delta:
					saturated = True
				else:
					if not backtrace:
						backtrace = True
						new_time = new_time - time_delta
						time_delta = -1*time_delta*time_decay
					else:
						backtrace = False
						new_time = new_time - time_delta
						time_delta = -1*time_delta*time_decay
			# print("@{:f} ->{:f} TIMESTAMP: NOW {:f} : CLOSEST {:f} , ABS_DIST: {:f}, STAT_DIST: {:f}".format(int(time.time()),curr_lookup,new_time,closest_timestamp,last_dist,last_stat_dist))

		return closest_timestamp,last_stat_dist



	def draw_full(self,timestamp = 10,e_margin = 40):
		# self.centring(timestamp)
		# timestamp = 10
		height = self.height
		width = self.width

		img = np.zeros((height, width, 3), np.uint8)
		# img[:, :] = [255, 255, 255]


		row, col = 512, 512
		cv2.circle(img,(col, row), 500, (255,255,255), 1)


		show_ra = 10
		show_decs = 10


		ra_divider = show_ra/self.fov_ra
		dec_divider = show_decs/self.fov_dec


		decs = self.fov_dec*dec_divider
		ras = self.fov_ra*ra_divider


		line_thickness = 1

		for i in range(int(decs)):
			n = i - decs/2 
			h_of_dec = self.height/decs
			x1 = 0
			y1 = int(i* h_of_dec)
			x2 = 1024
			y2 = int(i* h_of_dec)
			cv2.line(img, (x1, y1), (x2, y2), (255,255,255), thickness=line_thickness)
			line_dec = self.dec_target - decs/dec_divider*n
			curr_dec = "{:.10f}".format(line_dec)
			# print(curr_dec)
			cv2.putText(img,curr_dec, 
			    (x1, y1-10), 
			    font, 
			    fontScale,
			    fontColor,
			    thickness,
			    lineType)



		for i in range(int(ras)):
			n = i - ras/2 
			w_of_ra = self.width/ras
			x1 = int(i* w_of_ra)
			y1 = 0
			x2 = int(i* w_of_ra)
			y2 = 1024
			cv2.line(img, (x1, y1), (x2, y2), (255,255,255), thickness=line_thickness)
			line_ra = self.ra_target + self.fov_ra*n
			curr_ra = "{:.10f}".format(line_ra)
			# print(curr_ra)
			t_y = y1 + 30 +  50 * (i%2)
			cv2.putText(img,curr_ra, 
			    (x1, t_y), 
			    font, 
			    fontScale,
			    fontColor,
			    thickness,
			    lineType)


		# for i in range(int(ras)):
		# 	w_of_ra = self.width/ras
		# 	x1 = int(i* w_of_ra)
		# 	y1 = 0
		# 	x2 = int(i* w_of_ra)
		# 	y2 = 1024
		# 	cv2.line(img, (x1, y1), (x2, y2), (255,255,255), thickness=line_thickness)



		red = (255,0,0)
		green = (0,255,0)

		clolor = red
		alternate = 0

		for star in self.stars:
			proj = self.projectStar(star,0)
			cv2.circle(img,proj, 5, (255,255,255), -1)
			# cv2.circle(img,proj, 5, (255,255,255), -1)
			proj_errors = self.projectErrors(star,timestamp,e_margin)

			if alternate == 1:
				alternate = 0
				color = green
			else:
				alternate = 1
				color = red
					
			for err in proj_errors:
				# print("ERROR LINE")
				cv2.line(img, proj, err, (255,255,255), thickness=1)
				cv2.circle(img,err, 2, color, 3)
				# cv2.circle(img,err, 2, green, 3)



			# unit_movement = star.norm_movement()
			unit_movement = star.scaled_movement(1000)

			pm_after_years = timestamp

			del_ra = pm_after_years*star.pm_ra*self.fov_ra*unit_movement[0]
			del_dec = pm_after_years*star.pm_dec*self.fov_dec*unit_movement[0]


			pm_proj = (int(proj[0] + del_ra), int(proj[1] + del_dec))
			error_ellipse =  list(np.array([star.ra_err,star.dec_err]))
			error_ellipse =  (int(error_ellipse[0]*self.pp_ra),int(error_ellipse[1]*self.pp_dec))
			cv2.ellipse(img, proj, error_ellipse, 0,0.0, 360, (255,255,255), 1)
			# print("error ellipse",error_ellipse)
			# print("proper motion unit",unit_movement)
			# print("proper motion projected",pm_proj)
			cv2.line(img, proj, pm_proj, (0,255,0), thickness=line_thickness)
			# img = star.plot_self(img,timestamp)
		distt = self.calculate_cluster_distance(timestamp,e_margin)
		print(distt)

		return img
	# def projectPos(self,star,timestamp):

	def projectStar(self,star,timestamp):
		# s_cen = self.

		star_future_ra,star_future_dec = star.future_pos(timestamp) 
		ra_diff = star_future_ra - self.ra_target
		dec_diff = star_future_dec - self.dec_target



		cen_ = (self.width/2,self.height/2)

		star_x = cen_[0] + ra_diff*self.pp_ra
		star_y = cen_[1] + dec_diff*self.pp_dec


		ret_cen = (int(star_y),int(star_x))
		# print(ret_cen)
		return ret_cen
	def projectErrors(self,star,timestamp,e_margin = 20):
		# s_cen = self.
		s_num = 50

		ret_errs = []
		for i in range(s_num):
			star_error_ra,star_error_dec = star.future_error(timestamp,e_margin) 
			ra_diff = star_error_ra - self.ra_target
			dec_diff = star_error_dec - self.dec_target

			cen_ = (self.width/2,self.height/2)

			star_x = cen_[0] + ra_diff*self.pp_ra
			star_y = cen_[1] + dec_diff*self.pp_dec
			ret_errs.append((int(star_y),int(star_x)))

		# ret_cen = (int(star_x),int(star_y))
		# print(ret_errs)
		return ret_errs
	def centring(self,timestamp):
		if len(self.stars)< 2:
			return
		min_ra = 360
		min_dec = 90
		max_ra = 0
		max_dec = -90

		for star in self.stars:
			star_future_ra,star_future_dec = star.future_pos(timestamp) 
			if star_future_ra < min_ra:
				min_ra = star_future_ra
			if star_future_dec < min_dec:
				min_dec = star_future_dec
			if star_future_ra > max_ra:
				max_ra = star_future_ra
			if star_future_dec > max_dec:
				max_dec = star_future_dec


		# print(min_ra,max_ra)
		# print(min_dec,max_dec)

		self.ra_target = min_ra + max_ra
		self.dec_target = min_dec + max_dec


		ra_span = max_ra - min_ra
		dec_span = max_dec - min_dec

		self.fov_ra = ra_span
		self.fov_dec = dec_span


		if self.fov_ra > self.fov_dec:
			self.fov_dec = self.fov_ra
		else:
			self.fov_ra = self.fov_dec

		self.fov_ra = self.fov_ra*10.5
		self.fov_dec = self.fov_dec *10.5

		# ra_span = 2
		# dec_span =2 

		# avg_span = ra_span/2 + dec_span/2

		self.ra_target /= 2
		self.dec_target /= 2

		# self.fov = avg_span

		self.pp_ra = self.width/self.fov_ra
		self.pp_dec = self.height/self.fov_dec

		# print("**>>>\t\t\t>>>***CENTERED EYEPIECE")
		# print("**>>>\t\t\t>>>***MIN_RA MAX_RA",min_ra,max_ra)
		# print("**>>>\t\t\t>>>***MIN_DEC MAX_DEC",min_dec,max_dec)
		# print("**>>>\t\t\t>>>***FOV RA: ", self.fov_ra)
		# print("**>>>\t\t\t>>>***FOV DEC: ", self.fov_dec)
		# print("**>>>\t\t\t>>>***PP RA: " , self.pp_ra)
		# print("**>>>\t\t\t>>>***PP DEC: " , self.pp_dec)
	def add_star(self,star):
		self.stars.append(star)
		# print(star)
		self.centring(0)
		return True


# s1 = CRUX_STAR()
# s1.set_in_sky(100,10)
# s1.pma(1,1)
# s2 = CRUX_STAR()
# s2.pma(-1,1)


# EYE = CRUX_EYEPIECE()
# EYE.add_star(s1)
# EYE.add_star(s2)


# for i in range(1000):
# 	img = EYE.draw(i*0.1)
# 	cv2.imshow('eyepiece image',img)
# 	k = cv2.waitKey(50) 



# 	img = plot2Stars(s1,s2,i)

# def _test():
#     assert add('1', '1') == 2

# if __name__ == '__main__':
#     _test()
#     
