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
  url = "http://lasp.colorado.edu/lisird/tss/sorce_ssi.csv?&time>=2010-01-01&time<2010-02-01",
  localfile = "data"):
    
  # download with urllib
  response = urllib2.urlopen(url)

  # save the file locally
  fp = open(localfile, "w")
  fp.write(response.read())
  
  # close handles
  fp.close()
  response.close()
  
  
def get_date(prompt):
  # get valid user input and return as formatted string
  dt_input = raw_input(prompt)
  try:
    dt = datetime.strptime(dt_input, '%Y-%m-%d')
  except ValueError:
    print "Incorrect format, please enter the date as YYYY-MM-DD."
    return get_date(prompt)
    
  return dt.strftime('%Y-%m-%d')
  
  
def hw4():
  # if data does not exist, fetch it
  localfile = "data"
  if not localfile in os.listdir('.'):
    # format user date input into target url
    dt_start = get_date("Enter beginning date(YYYY-MM-DD): ")
    dt_end = get_date("Enter non-inclusive ending date(YYYY-MM-DD): ")
    url = "http://lasp.colorado.edu/lisird/tss/sorce_ssi.csv?&time>=" + dt_start + "&time<" + dt_end
    
    print "Warning: file " + localfile + " not found; retrieving from the web"
    fetch_file(url)
  
  # load table into multi dimensional array, [[day, wavelength, flux]...]
  table = loadtxt("data", skiprows = (1), usecols = (0,1,2), delimiter = ",")
  
  # group flux readings into rows according to unique days, throwout NaN readings
  flux = []
  days = unique(table[:,0])
  waves = unique(table[:,1])
  for day in days:
    flux.append([row[2] for row in table if row[0] == day and not isnan(row[2])])

  #Creates an array of zeros. 
  flux2=zeros(shape=(len(flux),len(flux[0])))
    
  #Now I'm taking that array, and turning the corresponding entries from flux into floats
  for i in range(len(flux)):
    for j in range(len(flux[i])):
      flux2[i,j]=float(flux[i][j])
    
  #Empty array for the series of integrals
  Qo2=[]
    
  #Defining Constants
  h=6.626e-34
  c=2.99792458e8
    
  for a in flux2:
    #a is an array of intensities at each wavelength. h and c scale the integral.
    Qo2.append(integ.simps((waves*10.0**-9)*a/(h*c),x=waves))
    
    
  deltaQo2=(Qo2/mean(Qo2))-1
    
  print("Average value of Q(o2): " + str(mean(Qo2)) )
  print("Delta Q: 25th Percentile = " + str(percentile(deltaQo2, 25)) + ", 75th percentile = " +
  str(percentile(deltaQo2, 75)))
  
  #TODO: 7 onwards. Also, figure out the order-of-magnitude issue with our percentiles. Also, DeltaQO2 is plotted it looks wonky. 
  
