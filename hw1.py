#Import sciency libs
from numpy import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import time
from IPython import display

#Diffusion simulator
def hw1(nsteps=500, dx=.01, sigma=.1):
	#Create two list with step dx
	x = arange(-1, 1, dx)
	y = arange(-1, 1, dx)
	#Create mesh
	xx, yy = meshgrid(x, y)
	#T is our resultant 2d vector
	t = 1.0 / (2.0*pi*sigma**2) * exp(-(xx**2 + yy**2) / (2.0*sigma**2))
	
	#Zero first and last cols and rows
	t[0,:] = 0
	t[:,0] = 0
	t[-1,:] = 0
	t[:,-1] = 0

	#Initial graph
	fig = figure()
	ax = fig.add_subplot(111, projection='3d')
	surf = ax.plot_surface(xx, yy, t)
	ax.set_zlim([0, 1.0/(2.0*pi*sigma**2)])
	draw()

	#Execute nsteps times
	for i in range(nsteps):
		t[1:-1, 1:-1] = 0.2 * (t[1:-1,1:-1] + t[0:-2,1:-1] + 
			       t[2:,1:-1] + t[1:-1,0:-2] + 
			       t[1:-1,2:])
		#Replot each 10 iterations
		if(i%10 == 0):
			surf.remove()
			surf=ax.plot_surface(xx, yy, t)
			display.clear_output(wait=True)
			display.display(fig)
			ax.set_zlim([0, 1.0/(2.0*pi*sigma**2)])
			draw()
			time.sleep(0.1)
