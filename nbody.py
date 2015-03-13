from numpy import *
from matplotlib.pyplot import *
import scipy.constants as sc
from collections import OrderedDict
import time

"""
  Updates the position of all objects
"""
def calc_position(obj, scale):
    for i in range(len(obj)):
        obj[i][0] += obj[i][1] * scale
  
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
def calc_velocity(obj, scale):
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
        gca().set_aspect('equal')
        # These limits should actually be calculated
        xlim([-2.9e11, 2.9e11])
        ylim([-2.9e11, 2.9e11])
        for j in range(len(particle['x'])):
            plot(particle['x'][j][i], particle['y'][j][i],'o')
        draw()
        time.sleep(0.016)
  
def nbody(steps=2111, tplot=12, scale=36000):
    # Play values for the solar system. The velocity needs to actually be calculated.
    obj=[[array([4.41673502e+2,0.0]),array([0.0,0.0]),array([0.00,0.00]),1.989e30]]
    obj.append([array([-5.7910e+10,0.0]),array([0.0,-4.7360e+4]),array([0.00,0.00]),3.301e23])
    obj.append([array([-1.0820e+11,0.0]),array([0.0,-3.5020e+4]),array([0.00,0.00]),4.87e24])
    obj.append([array([-1.4960e+11,0.0]),array([0.0,-2.9780e+4]),array([0.00,0.00]),5.972e24])
    obj.append([array([-2.27920e+11,0.0]),array([0.0,-2.4070e+4]),array([0.00,0.00]),0.642e24])

    # Initialize particle lists for each particle. This data structure needs to be simplified.
    particle = {'x': [], 'y': []}
    for _ in range(len(obj)):
        particle['x'].append([])
        particle['y'].append([])
    
    # Step through simulation and build a list of all points to plot
    for timeCount in range(steps):
        calc_position(obj, scale)
        calc_force(obj)
        calc_velocity(obj, scale)
        
        # Only plot every tplot step of the simulation.
        if timeCount % tplot == 0:
            for i in range(len(obj)):
                particle['x'][i].append(obj[i][0][0])
                particle['y'][i].append(obj[i][0][1])
                
    # Play back the result of the simulation.
    animate_plot(particle)
