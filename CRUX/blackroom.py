import cv2
import numpy as np




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

class CRUX_STAR(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.x_v = 1
		self.y_v = 1
		self.ra = 0
		self.dec = 0
	def move(self,x,y):
		self.x = x
		self.y = y
	def set_in_sky(self,ra,dec):
		self.ra = ra
		self.dec = dec
	def pma(self,xv,yv):
		self.x_v = xv
		self.y_v = yv
	def future_pos(self,timestamp):
		f_x = self.x + self.x_v*timestamp
		f_y = self.y + self.y_v*timestamp
		return (f_x,f_y)
	def plot_self(self,img,timestamp):
		cen = self.future_pos(timestamp) 
		cv2.circle(img,cen, 5, (255,255,255), -1)
		return img


class CRUX_EYEPIECE(object):
	def __init__(self):
		self.ra_target = 0
		self.dec_target = 0
		self.fov_in_arcsecond = 10
		self.stars = []
	def draw(self,timestamp):
		height, width = 1024, 1024
		img = np.zeros((height, width, 3), np.uint8)
		# img[:, :] = [255, 255, 255]


		row, col = 512, 512
		cv2.circle(img,(col, row), 500, (255,255,255), 1)
		for star in self.stars:
			proj = self.projectStar(star,timestamp)
			cv2.circle(img,proj, 5, (255,255,255), -1)
			# img = star.plot_self(img,timestamp)
		return img
	def projectStar(self,star,timestamp):
		# s_cen = self.
		ra_diff = star.ra - self.ra_target
		dec_diff = star.dec - self.dec_target

		return (ra_diff,dec_diff)

	def add_star(self,star):
		self.stars.append(star)
		return True


s1 = CRUX_STAR()
s1.move(200,300)
s1.pma(1,1)
s2 = CRUX_STAR()
s2.move(400,300)
s2.pma(-1,1)


EYE = CRUX_EYEPIECE()
EYE.add_star(s1)
EYE.add_star(s2)

for i in range(1000):
	img = EYE.draw(i)
	cv2.imshow('eyepiece image',img)
	k = cv2.waitKey(50) 



# 	img = plot2Stars(s1,s2,i)

# def _test():
#     assert add('1', '1') == 2

# if __name__ == '__main__':
#     _test()
#     
