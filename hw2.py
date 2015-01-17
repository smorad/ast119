from numpy import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import struct
import sys
import subprocess

def make_data(filename='hw2.dat', ngrid=100):
	"Creates data and writes it to binary file"
	#Premature optimization is the root of all evil -D. Knuth
	#
	#Bitwise AND with 111...10, dropping 1's place if present
	#-sys.maxint-1 == min_int
	#ngrid = ngrid & (-sys.maxint-2)
	#Let's just use the modulo operator instead
	if ngrid % 2 != 0:
		ngrid -= 1
	print(ngrid)

	#2 lists with ngrid steps
	x = linspace(-2*pi, 2*pi, ngrid)
	y = linspace(-2*pi, 2*pi, ngrid)

	xx, yy = meshgrid(x, y)
	r = sqrt(xx**2 + yy**2)
	z = sin(r) / r

	#create binary file, write, then close it
	#using with open()... ensures the file will close if an exception is raised
	#and is generally considered better style
	with open(filename, 'wb') as fp:
		fp.write(array(ngrid))
		fp.write(x)
		fp.write(y)
		fp.write(z)

def hw2(filename='hw2.dat', ngrid=100):
	make_data(filename, ngrid)
	with open(filename, 'rb') as fp:
		#read in raw data, byte by byte
		ngrid_raw = fp.read(8)
		ngrid = struct.unpack('l', ngrid_raw)[0]
	
		#read in ngrid elements, unpack as f64
		xraw = fp.read(ngrid*8)
		x = array(struct.unpack('d'*ngrid, xraw))

		yraw = fp.read(ngrid*8)
		y = array(struct.unpack('d'*ngrid, yraw))

		#z is 2d, so read in ngrid^2 data
		zraw = fp.read(ngrid**2*8)
		z = array(struct.unpack('d'*ngrid**2, zraw))

		#make Z 2d
		z = reshape(z, (ngrid, ngrid))

		#plot Z
		xx, yy = meshgrid(x, y)
		fig = figure()
		ax = fig.add_subplot(111, projection='3d')
		surf = ax.plot_surface(xx, yy, z)
		draw()
