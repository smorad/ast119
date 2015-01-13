from numpy import *
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
import struct
import sys

def make_data(filename='hw2.dat', ngrid=100):
	"Creates data and writes it to binary file"
	#Premature optimization is the root of all evil -D. Knuth
	#
	#Bitwise AND with 111...10, dropping 1's place if present
	ngrid = ngrid & (sys.min_int-1)

	#2 lists with ngrid steps
	x = arange(-2*pi, 2*pi, ngrid)
	y = arange(-2*pi, 2*pi, ngrid)

	xx, yy = meshgrid(x, y)
	r = sqrt(xx**2 + yy**2)
	z = sin(r) / r

	#create binary file, write, then close it
	with open(filename) as fp:
		fp.write(array(ngrid))
		fp.write(x)
		fp.write(y)
		fp.write(z)
		

def hw2(filename='hw2.dat', ngrid=100):
	make_data(filename, ngrid)
	with open(filename) as fp:
		ngrid_raw = fp.read(8)
		ngrid = struct.unpack('l', ngrid_raw)[0]
