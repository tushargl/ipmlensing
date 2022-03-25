import cv2
import numpy as np
import math



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





class CRUX_STAR(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.ra = 0
		self.dec = 0
		self.pm_ra = 1
		self.pm_dec = 1

	def move(self,x,y):
		self.x = x
		self.y = y
	def set_in_sky(self,ra,dec):
		self.ra = float(ra)
		self.dec = float(dec)
	def pma(self,pm_ra,pm_dec):
		self.pm_ra = float(pm_ra)
		self.pm_dec = float(pm_dec)
	def future_pos(self,timestamp):
		# print(self.ra)
		# print(self.dec)
		# print(self.x_v)
		# print(self.y_v)
		# print(timestamp)
		f_ra = self.ra + self.pm_ra*timestamp*0.001
		f_dec = self.dec + self.pm_dec*timestamp*0.001
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





		return (self.pm_ra,self.pm_dec)
	def __str__(self):
		return "RA: {:.10f} :  DEC :{:.10f} ".format(self.ra,self.dec)




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

	# def calibrate(self):
	def draw(self,timestamp):
		# self.centring(timestamp)
		height = self.height
		width = self.width

		img = np.zeros((height, width, 3), np.uint8)
		# img[:, :] = [255, 255, 255]


		row, col = 512, 512
		cv2.circle(img,(col, row), 500, (255,255,255), 1)


		decs = self.fov_dec
		ras = self.fov_ra


		line_thickness = 2

		for i in range(int(decs)):
			h_of_dec = self.height/decs
			x1 = 0
			y1 = int(i* h_of_dec)
			x2 = 1024
			y2 = int(i* h_of_dec)
			cv2.line(img, (x1, y1), (x2, y2), (255,255,255), thickness=line_thickness)
			curr_dec = self.dec_target - (decs/2)/3600*i
			cv2.putText(img,curr_dec, 
			    (x1, y1), 
			    font, 
			    fontScale,
			    fontColor,
			    thickness,
			    lineType)



		for i in range(int(ras)):
			w_of_ra = self.width/ras
			x1 = int(i* w_of_ra)
			y1 = 0
			x2 = int(i* w_of_ra)
			y2 = 1024
			cv2.line(img, (x1, y1), (x2, y2), (255,255,255), thickness=line_thickness)





		for star in self.stars:
			proj = self.projectStar(star,timestamp)
			cv2.circle(img,proj, 5, (255,255,255), -1)
			# img = star.plot_self(img,timestamp)
		return img
	def draw_full(self):
		# self.centring(timestamp)
		timestamp = 0
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


		line_thickness = 2

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





		for star in self.stars:
			proj = self.projectStar(star,timestamp)
			cv2.circle(img,proj, 5, (255,255,255), -1)

			# unit_movement = star.norm_movement()
			unit_movement = star.scaled_movement(10)

			pm_proj = (int(proj[0] + unit_movement[0]*100), int(proj[1] + unit_movement[1]*100))


			cv2.line(img, proj, pm_proj, (0,255,0), thickness=line_thickness)
			# img = star.plot_self(img,timestamp)
		return img
	def projectStar(self,star,timestamp):
		# s_cen = self.

		star_future_ra,star_future_dec = star.future_pos(timestamp) 
		ra_diff = star_future_ra - self.ra_target
		dec_diff = star_future_dec - self.dec_target



		cen_ = (self.width/2,self.height/2)

		star_x = cen_[0] + ra_diff*self.pp_ra
		star_y = cen_[1] + dec_diff*self.pp_dec


		ret_cen = (int(star_x),int(star_y))
		print(ret_cen)
		return ret_cen
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


		print(min_ra,max_ra)
		print(min_dec,max_dec)

		self.ra_target = min_ra + max_ra
		self.dec_target = min_dec + max_dec


		ra_span = max_ra - min_ra
		dec_span = max_dec - min_dec


		self.fov_ra = ra_span*1.5
		self.fov_dec = dec_span*1.5



		# ra_span = 2
		# dec_span =2 

		# avg_span = ra_span/2 + dec_span/2

		self.ra_target /= 2
		self.dec_target /= 2

		# self.fov = avg_span

		self.pp_ra = self.width/self.fov_ra
		self.pp_dec = self.height/self.fov_dec

		print("**>>>\t\t\t>>>***CENTERED EYEPIECE")
		print("**>>>\t\t\t>>>***MIN_RA MAX_RA",min_ra,max_ra)
		print("**>>>\t\t\t>>>***MIN_DEC MAX_DEC",min_dec,max_dec)
		print("**>>>\t\t\t>>>***FOV RA: ", self.fov_ra)
		print("**>>>\t\t\t>>>***FOV DEC: ", self.fov_dec)
		print("**>>>\t\t\t>>>***PP RA: " , self.pp_ra)
		print("**>>>\t\t\t>>>***PP DEC: " , self.pp_dec)
	def add_star(self,star):
		self.stars.append(star)
		print(star)
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
