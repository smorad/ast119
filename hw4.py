# ASTR119
# HW4
# Team: Forrest Kerslager, Benjamin Smithers, Steven Morad, Kevin Rodriguez,
# Elliot Ghassemi

from numpy import *
from matplotlib.pyplot import *
import urllib2
import os
from datetime import datetime
import scipy.integrate as integ

def fetch_file(
  url = "http://lasp.colorado.edu/lisird/tss/sorce_ssi.csv?&time>=2010-01-01&time<2011-01-01",
  localfile = "data_2010-01-01_2011-01-01"):
    
  # Download with urllib
  response = urllib2.urlopen(url)

  # Save the file locally
  fp = open(localfile, "w")
  fp.write(response.read())
  
  # Close handles
  fp.close()
  response.close()
  
  
def validateInput(dt_input):
  # Check for valid user input and return true or false
  try:
    dt = datetime.strptime(dt_input, '%Y-%m-%d')
  except ValueError:
    return False
    
  return True
  
  
def hw4(dt_start = "2010-01-01", dt_end = "2011-01-01"):
  # Validate and format user date input
  if not validateInput(dt_start) or not validateInput(dt_end):
    print "Incorrect format, please enter the date as YYYY-MM-DD"
    return
    
  # If data does not exist, fetch it
  localfile = "data_" + dt_start + "_" + dt_end
  if not localfile in os.listdir('.'):
    print "Warning: file " + localfile + " not found; retrieving from the web"
    url = "http://lasp.colorado.edu/lisird/tss/sorce_ssi.csv?&time>=" + dt_start + "&time<" + dt_end
    fetch_file(url, localfile)
    print "File successfully retrieved"
    
  # Load table into multi dimensional array, [[day, wavelength, flux]...]
  table = loadtxt(localfile, skiprows = (1), usecols = (0,1,2), delimiter = ",")
  
  # Extract all unique days
  days = unique(table[:,0])
  wavelengths = unique(table[:,1])
  
  # Initializing data and constants
  flux = []
  h = 6.626e-34
  c = 3.0e8
  
  # Group flux readings into rows according to unique days
  # Each row of table has the format [day, wavelength, intensity]
  for day in days:
    fluxValues = []
    for row in table:
      if row[0] == day:
        # Calculate flux using intensity and wavelength
        fluxValues.append((row[2] * row[1] * (10.0**-9)) / (h * c))
    # Throw out days with NaN readings
    if not isnan(fluxValues).any():
      flux.append(fluxValues)
        
  # Empty array for the series of integrals
  Qo2 = []
    
  # Compute Qo2 for each day's flux calculations
  for readings in flux:
    Qo2.append(integ.simps(readings, x=wavelengths))

  # Print the mean Qo2, 25th, and 75th percentile of deltaQo2.
  deltaQo2 = (Qo2 / mean(Qo2)) - 1.0
  print("Average value of Q(o2): " + str(mean(Qo2)))
  print("Delta Q: 25th Percentile = " + str(percentile(deltaQo2, 25)) + ", 75th percentile = " +
  str(percentile(deltaQo2, 75)))
  
  # TODO: 7 onwards. 
