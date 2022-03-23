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
    def move(self,x,y):
    	self.x = x
    	self.y = y
    def pma(self,xv,yv):
    	self.x_v = xv
    	self.y_v = yv
    def future_pos(self,timestamp):
    	f_x = self.x + self.x_v*timestamp
    	f_y = self.y + self.y_v*timestamp
    	return (f_x,f_y)

s1 = CRUX_STAR()
s1.move(200,300)
s1.pma(1,1)
s2 = CRUX_STAR()
s2.move(400,300)
s2.pma(-1,1)

for i in range(1000):
	img = plot2Stars(s1,s2,i)
	cv2.imshow('star image',img)
	k = cv2.waitKey(50) 

# def _test():
#     assert add('1', '1') == 2

# if __name__ == '__main__':
#     _test()
#     
