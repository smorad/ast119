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
  # format user date input into target url
  dt_start = get_date("Enter beginning date(YYYY-MM-DD): ")
  dt_end = get_date("Enter non-inclusive ending date(YYYY-MM-DD): ")
  url = "http://lasp.colorado.edu/lisird/tss/sorce_ssi.csv?&time>=" + dt_start + "&time<" + dt_end

  # if data does not exist, fetch it
  localfile = "data"
  if not localfile in os.listdir('.'):
    print "Warning: file " + localfile + " not found; retrieving from the web"
    fetch_file(url)
  
  # step 2: TODO
