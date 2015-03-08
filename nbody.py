from numpy import *
from math import *
from matplotlib.pyplot import *
import scipy.constants as sc
from collections import OrderedDict
import time

"""
  Updates the position of all objects
"""
def calc_position(obj):
	for i in range(len(obj)):
		obj[i][0] += obj[i][1] 
  
"""
  Calculates the acceleration for all objects
"""
def calc_force(obj):
	for i in range(len(obj)):
		obj[i][2] = array([0.0,0.0])
		for j in range(len(obj)):
			if obj[i][3] != obj[j][3]:
				r = obj[j][0]-obj[i][0]
				obj[i][2] += ((sc.G*obj[j][3])/(np.linalg.norm(r)**2))*(r/np.linalg.norm(r))
  
"""
  Updates the velocity of all objects
"""
def calc_velocity(obj):
	for i in range(len(obj)):
		obj[i][1] += obj[i][2]

"""
  Plots the result of the simulation as an animation.
  This code needs to be cleaned up.
"""
def animate_plot(particle):
	fig = figure(1)
	for i in range(len(particle['x'][0])):
		cla()
		gca().set_aspect('equal')
		# These limits should actually be calculated
		xlim([-2.9e8, 2.9e8])
		ylim([-2.9e8, 2.9e8])
		for j in range(len(particle['x'])):
			plot(particle['x'][j][i], particle['y'][j][i],'o')
		draw()
		time.sleep(0.016)
		

#attempt 2 starts here
def calc_star_pos(star1, star2, step, ecc=1., tick_rate=50., distance=4e2):			
	"Move stars along a oval track"
	star1['x'] = cos(step/tick_rate) * distance * ecc
	star1['y'] = sin(step/tick_rate) * distance
	star2['x'] = cos(step/tick_rate + pi) * distance * ecc
	star2['y'] = sin(step/tick_rate + pi) * distance

def calc_planet_pos(star_list, planet_list, tstep=0.01):
	"Integrate each star on each planet"
	for planet in planet_list:
		for star in star_list:
			integrate(star, planet, tstep)
	
def integrate(star, planet, dt):
	"Calculate effects of gravity on the planet"
	#This is broken, I should fix it
	planet['x'] = (planet['x'] + planet['xvel'] * dt)
	planet['y'] = (planet['y'] + planet['yvel'] * dt)
	planet['xvel'] += planet['xacc'] * dt
	planet['yvel'] += planet['yacc'] * dt
	r = array([star['x'] - planet['x'], star['y'] - planet['y']])
	force = ((sc.G * star['mass'])/(np.linalg.norm(r)**2))*(r/np.linalg.norm(r))
	#use scalars to determine if accel is in negative or positive direction
	#scalars will be either +1 or -1
	scalar = {'x':1, 'y':1}
	for dim in scalar.keys():
		if star[dim] - planet[dim] < 0:
			scalar[dim] = -1
	planet['xacc'] = force[0] / star['mass'] * scalar['x'] * dt
	planet['yacc'] = force[1] / star['mass'] * scalar['y'] * dt
	print(planet['xacc'], planet['yacc'])
	

def nbody(steps=1000, tplot=12):
	# Play values for the solar system. The velocity needs to actually be calculated.
	figure()
	star1 = {'mass':1989e30}
	star2 = {'mass':1989e30}
	star_list = [star1, star2]
	planet1 = {'x':4.41e+03, 'y':0., 'xvel':0.0, 'yvel': 1, 'xacc':0., 'yacc':0., 'mass':1}
	planet_list = [planet1]
	for step in range(steps):
		calc_star_pos(star1, star2, step)  
		calc_planet_pos(star_list, planet_list)
		plot(star1['x'], star1['y'], 'ro')
		plot(star2['x'], star2['y'], 'go')
		plot(planet1['x'], planet1['y'], 'bo')
		draw()
#	obj=[[array([4.41673502e+02,0.0]),array([0.0,2.87592295]),array([0.00,0.00]),1.989e30]]
#	obj.append([array([-5.7910e+07,0.0]),array([0.0,-15.57838370e+05]),array([0.00,0.00]),0.3301e24])
#	obj.append([array([-10.820e+07,0.0]),array([0.0,-11.27838370e+05]),array([0.00,0.00]),4.87e24])
#	obj.append([array([-1.47101238e+08,0.0]),array([0.0,-9.57838370e+05]),array([0.00,0.00]),5.972e24])
#	obj.append([array([-22.790e+07,0.0]),array([0.0,-7.67838370e+05]),array([0.00,0.00]),0.642e24])
#	 
#	# Initialize particle lists for each particle. This data structure needs to be simplified.
#	particle = {'x': [], 'y': []}
#	for _ in range(len(obj)):
#		particle['x'].append([])
#		particle['y'].append([])
#	
#	# Step through simulation and build a list of all points to plot
#	for timeCount in range(steps):
#		calc_position(obj)
#		calc_force(obj)
#		calc_velocity(obj)
#		
#		# Only plot every tplot step of the simulation.
#		if timeCount % tplot == 0:
#			for i in range(len(obj)):
#				particle['x'][i].append(obj[i][0][0])
#				particle['y'][i].append(obj[i][0][1])
#				
#	# Play back the result of the simulation.
#	animate_plot(particle)
