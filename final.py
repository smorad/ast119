from numpy import *
from matplotlib.pyplot import *
import scipy.constants as sc
from collections import OrderedDict
import matplotlib.mlab as ml
import time
import matplotlib.cm as cm

"""
  Updates the position of all objects
"""
def calc_position(obj,scale):
	for i in range(len(obj)):
		obj[i][0] += obj[i][1] * scale
  
"""
  Calculates the acceleration for all objects
"""
def calc_force(obj):
	for i in range(len(obj)):
		obj[i][2] = array([0.0,0.0])
		for j in range(len(obj)):
			if obj[i][4] != obj[j][4]:
				r = obj[j][0]-obj[i][0]
				obj[i][2] += ((sc.G*obj[j][3])/(np.linalg.norm(r)**2))*(r/np.linalg.norm(r))

"""
  Updates the velocity of all objects
"""
def calc_velocity(obj,scale):
	for i in range(len(obj)):
		obj[i][1] += obj[i][2] * scale

"""
  Plots the result of the simulation as an animation.
  This code needs to be cleaned up.
"""
def animate_plot(particle):
	fig = figure(1)
	
	
	
	for i in range(len(particle['x'][0])):
		cla()
		listofx= list(particle['x'][0])+list(particle['x'][1])+list(particle['x'][2])
		listofy= list(particle['y'][0])+list(particle['y'][1])+list(particle['y'][2])
		xlim([min(listofx), max(listofx)])
		ylim([min(listofy), max(listofy)])
		gca().set_aspect('equal')
		for j in range(len(particle['x'])):
			plot(particle['x'][j][i], particle['y'][j][i],'o')
		draw()
		time.sleep(0.016)

# Scale is your time step unit in seconds, default is in hours
def simulate(e,pasa,steps=50000,tplot=10,scale=3600):
	# Initialize variables for simulation bodies
	mStar = 1.989e30
	v0 = 0.5*sqrt((1.0+e)/(1.0-e)) * sqrt(sc.G*2.0*mStar/(0.5*sc.au))
	sa = 0.5*sc.au
	r0=(1-e)*sa/(2.0)
	#Define the initial conditions
	#Giving the planet a starting setup as if it were to enter a circular orbit around a 2Mstar point mass
	
	#(position, velocity, acceleration, mass, identifier)
	#Planet
	#Star1
	#Star2
	obj = [
			[array([0.5*pasa*sc.au,0.0]),array([0.0,sqrt(sc.G*2*mStar/(pasa*0.5*sc.au))]),array([0.00,0.00]), 5.97e24, 1],
			[array([r0, 0.0]), array([0.0, v0]), array([0.00, 0.00]), mStar, 2],
			[array([-1.0*r0, 0.0]), array([0.0, -1*v0]), array([0.00, 0.00]), mStar, 3]
		  ]
	
	# Initialize particle lists for each particle. This data structure needs to be simplified.
	# I, another preson, personally think the structure is fine.
	#	Well, yeah, it's weird. But, hey. It works!
	particle = {'x': [], 'y': []}
	for _ in range(len(obj)):
		particle['x'].append([])
		particle['y'].append([])
	
	# Step through simulation and build a list of all points to plot
	for timeCount in range(steps):
		#print(str(obj[1][1][0]) + "," + str(obj[1][1][1]) + " " + str(obj[2][1][0]) + "," + str(obj[2][1][1]) + " \n")
		calc_position(obj, scale)
		calc_force(obj)
		calc_velocity(obj, scale)
		
		# Only plot every tplot step of the simulation.
		if timeCount % tplot == 0:
			for i in range(len(obj)):
				particle['x'][i].append(obj[i][0][0])
				particle['y'][i].append(obj[i][0][1])
		
		dist = np.linalg.norm(obj[0][0])
		vEsc = sqrt(2*sc.G*2*mStar/dist)
		#print linalg.norm(obj[0][1]), Vesc, dist,(4*sc.au)
		if linalg.norm(obj[0][1]) > vEsc and dist > (0.5*sc.au*pasa):
			 return(timeCount)
			 
	# Play back the result of the simulation.
	#animate_plot(particle)
	
	return(steps)

def draw_plot(results, emin, emax, pmin, pmax):
	i = []
	j = []
	z = []
	for a in range(len(results)):
		i.append(results[a][0])
		j.append(results[a][1])
		z.append(results[a][2])
	xi = list(set(i))
	yj = list(set(j))
	
	Z=array(z).reshape(len(yj),len(xi))
	imshow(Z, aspect='auto', origin='lower', extent=(pmin,pmax,emin,emax), interpolation='nearest',cmap=cm.spectral)
	ylabel("Stellar Eccentricity")
	xlabel("Planet Semi Major / Stellar Semi Major")
	title("Hours survived for given eccentricity and ratio")
	colorbar()
	savefig('orbital_plot')
	draw()

def final(emin=0.0,emax=0.99,pmin=1.1,pmax=5.0,datadensity=30):
	"""
	Accepts optional values for the min and max values for e,
	the eccentricity of the stars' orbits, and p, the ratio of the
	planets semi-major axis to the star's semi-major axis.
	"""
	e = linspace(emin, emax, datadensity)
	pasa = linspace(pmin, pmax, datadensity)
	
	results = []
	for i in e:
		for j in pasa:
			results.append(array([i, j, simulate(e=i, pasa=j)]))
	#print results
	draw_plot(results, emin, emax, pmin, pmax)
