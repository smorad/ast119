from numpy import *
from matplotlib.pyplot import *
import urllib
import os

def fetch_file(
	url='https://sites.google.com/a/ucsc.edu/krumholz/teaching-and-courses/ast119_w15/homework-3/hw3.npy',
	localfile='hw3.npy'):

	urlp = urllib.urlopen(url)
	#download npy array
	rawdata = urlp.read()
	urlp.close()		
	with open(localfile, 'w') as fp:
		#numpy save array
		save(fp, rawdata)

def hw3():
	#if file doesnt exist download it
	if not os.path.isfile('hw3.npy'):
		print('File not found, retrieving from web.')
		fetch_file()

	with open('hw3.npy', 'rb') as fp:
		#numpy load array
		fdata = load(fp)

	#create two arrays equal to x and y dim of fdata
	x = linspace(-1, 1, len(fdata))
	y = linspace(-1, 1, len(fdata[0]))
	
	#plot
	figure(1)
	imshow(fdata , aspect='equal', origin = 'lower', extent = (-1, 1, -1, 1))
	colorbar()
	xlabel('x') 
	ylabel('y')
	draw()
	#write figure
	savefig('hw3a.png')

	#calculate means of arrays
	xmean = fdata.mean(0) 	
	ymean = fdata.mean(1)

	#find max
	xm = max(max(xmean), max(ymean))
