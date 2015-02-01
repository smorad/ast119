# ASTR119
# HW4
# Team: Forrest Kerslager, Benjamin Smithers, Steven Morad, Kevin Rodriguez,
# Elliot Ghassemi

from numpy import *
from matplotlib.pyplot import *
import urllib2
import os
import struct
from datetime import datetime
from itertools import groupby

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
  for day in days:
    flux.append([row[2] for row in table if row[0] == day and not isnan(row[2])])

  # TODO: continue to step 4
