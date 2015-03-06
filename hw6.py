# ASTR119
# HW6
# Team: Forrest Kerslager, Benjamin Smithers, Steven Morad, Kevin Rodriguez,
# Elliot Ghassemi

from numpy import *
from matplotlib.pyplot import *
  
def hw6(length=1.0,ncell=200,trun=500.0,tplot=20.0,heatradius=0.25,heatrate=2.0,theat=100.0,kappa=1e-4):
  # Determine the size space and time splices
  dx = length/ncell
  dt = dx**2 / 4*kappa

  # Initialize the temperature distibution
  temp_dist = numpy.zeros(shape=(ncell,ncell))
  
  
  # Not sure of step 4, just puttin my initial idea in for now
  heat_func = numpy.zeros(shape=(ncell,ncell))
  # From the hw6 specification, r is an array that represents an array of radii
  x = np.linspace(-length/2+dx/2, length/2-dx/2, ncell)
  y = np.linspace(-length/2+dx/2, length/2-dx/2, ncell)
  xx, yy = np.meshgrid(x, y, indexing='ij')
  r = np.sqrt(xx**2 + yy**2)
  
  # TODO continue at step 5 and double check step 4