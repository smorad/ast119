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

def simulate(e,pasa,steps=10,tplot=12):
    # Play values for the solar system. The velocity needs to actually be calculated.
    obj=[[array([4.41673502e+02,0.0]),array([0.0,2.87592295]),array([0.00,0.00]),1.989e30]]
    obj.append([array([-5.7910e+07,0.0]),array([0.0,-15.57838370e+05]),array([0.00,0.00]),0.3301e24])
    obj.append([array([-10.820e+07,0.0]),array([0.0,-11.27838370e+05]),array([0.00,0.00]),4.87e24])
    obj.append([array([-1.47101238e+08,0.0]),array([0.0,-9.57838370e+05]),array([0.00,0.00]),5.972e24])
    obj.append([array([-22.790e+07,0.0]),array([0.0,-7.67838370e+05]),array([0.00,0.00]),0.642e24])
    
    # Initialize particle lists for each particle. This data structure needs to be simplified.
    particle = {'x': [], 'y': []}
    for _ in range(len(obj)):
        particle['x'].append([])
        particle['y'].append([])
    
    # Step through simulation and build a list of all points to plot
    for timeCount in range(steps):
        calc_position(obj)
        calc_force(obj)
        calc_velocity(obj)
        
        # Only plot every tplot step of the simulation.
        if timeCount % tplot == 0:
            for i in range(len(obj)):
                particle['x'][i].append(obj[i][0][0])
                particle['y'][i].append(obj[i][0][1])
                
    # Play back the result of the simulation.
    #animate_plot(particle)
    return(42)

def draw_plot(results):
    i = []
    j = []
    z = []
    for a in range(len(results)):
        i.append(results[a][0])
        j.append(results[a][1])
        z.append(results[a][2])
    xi = linspace(min(i), max(i),15)
    yj = linspace(min(j), max(j),15)  
    X,Y = meshgrid(xi,yj)
    Z = ml.griddata(i,j,z,xi,yj)

    imshow(Z, aspect='auto', origin='lower', extent=(i[0],i[-1],j[0],j[-1]), cmap=cm.prism)
    colorbar()

def final(emin=0.0,emax=1.0,pmin=2.0,pmax=5.0):
    """ 
    Accepts optional values for the min and max values for e, 
    the eccentricity of the stars' orbits, and p, the ratio of the 
    planets semi-major axis to the star's semi-major axis.
    """
    e = linspace(emin, emax, 15)
    pasa = linspace(pmin, pmax, 15)
    
    results = []
    for i in e:
        for j in pasa:
            results.append(array([i, j, simulate(eccentricity=i, pasa=j)]))
            
    draw_plot(results)
