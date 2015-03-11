from numpy import *
from matplotlib.pyplot import *
import time



def hw6(length=1.0, ncell=200,trun=500.0,tplot=20.0,heatradius=.25,heatrate=2.0,theat=100.0,kappa=1.0e-4):

	#define our space steps based on lenth of plate and ncell
	dx = length/ncell
	#define time steps to meet decent approximation criteria 
	dt = dx**2/ (4*kappa)

	#set up empty temperature dist
	temp_dist = zeros((ncell,ncell))

	#set up empty heat function
	heat_func = zeros((ncell,ncell))

	#find the radial distances of all points on the plate 
	x = np.linspace(-length/2+dx/2, length/2-dx/2, ncell)
	y = np.linspace(-length/2+dx/2, length/2-dx/2, ncell)
	xx, yy = np.meshgrid(x, y, indexing='ij')
	r = np.sqrt(xx**2 + yy**2)

	#here we see which points on the plate are within "heatradius". 
	#only the points on the plate directly above the flame 
	#are assigned "heatrate"; the others remain zeros
	n=0
	m=0
	while m<r.shape[1]:
		if r[n,m] <= heatradius:
			heat_func[n,m] = heatrate
		n+=1
		if n==r.shape[0]:
			n=0
			m+=1

	t=0
	#create an array to store max temp values in over time
	maxt = zeros(trun/dt)
	while t< trun:
		
		#hold edges at zero
		temp_dist[0,:] = 0.0
		temp_dist[-1,:] = 0.0
		temp_dist[:,0] = 0.0
		temp_dist[:,-1] = 0.0

		#once we hit 100 seconds, turn off the flame
		if t< theat:
			temp_dist = temp_dist + heat_func*dt

		#diffuse the temperature for the whole 500 seconds
		temp_dist[1:-1,1:-1] = 0.2 * (temp_dist[1:-1,1:-1] + temp_dist[0:-2,1:-1] + temp_dist[2:,1:-1] + temp_dist[1:-1,0:-2] + temp_dist[1:-1,2:])
		maxt[t/dt]=amax(temp_dist)
		#print maxt[t/dt]
		t = t+dt

		#save the highest temp recorded ever for the 2nd plot 
		highesttemp=amax(maxt)

	clf()
	figure(1)
	plot(arange(0,len(maxt),1),maxt, lw=2)
	xlabel('Time')
	ylabel('Maximum Temperature')
	#axes().set_aspect('equal')
	draw()


	#now we go through the cycle again with a raster plot over time
	temp_dist = zeros((ncell,ncell))
	figure(2)
	imshow(temp_dist, aspect='equal',origin='lower',extent=(-length/2,length/2,-length/2,length/2),vmin=0,vmax=highesttemp)
	xlabel('x')
	ylabel('y')
	colorbar()
	title('Time = 0 sec')
	time.sleep(0.1)

	t=0
	while t< trun:
			
		#hold edges at zero
		temp_dist[0,:] = 0.0
		temp_dist[-1,:] = 0.0
		temp_dist[:,0] = 0.0
		temp_dist[:,-1] = 0.0

		#once we hit 100 seconds, turn off the flame
		if t< theat:
			temp_dist = temp_dist + heat_func*dt

		#diffuse the temperature for the whole 500 seconds
		temp_dist[1:-1,1:-1] = 0.2 * (temp_dist[1:-1,1:-1] + temp_dist[0:-2,1:-1] + temp_dist[2:,1:-1] + temp_dist[1:-1,0:-2] + temp_dist[1:-1,2:])

		if t%20==0:
			clf()
			imshow(temp_dist, aspect='equal',origin='lower',extent=(-length/2,length/2,-length/2,length/2),vmin=0,vmax=highesttemp)
			xlabel('x')
			ylabel('y')
			colorbar()
    		title('Time = %d sec'%t)
    		draw()
    		time.sleep(0.1)
		t = t+dt
		print t

#TODO: fix the plotting intervals (it's plotting every second instead of every twenty and idk why mod isn't working like i expect it to)
#check for errors and add notes so the TA can see what we doin
