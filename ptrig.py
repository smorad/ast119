from numpy import *
from matplotlib.pyplot import *

def makeplot(funcname,  wave, freq=None, spread=2*pi, dx=.01, ps=0, am=1):
	if(freq and wave):
		raise Exception("Wavelength and frequency are mutually exclusive")
	x = arange(0, spread, range)
	if(not freq):
		if funcname == 'sin':
			plot(x,am*sin(x)+ps)
		elif funcname == 'cos':
			plot(x, am*cos(x)+ps)
		elif funcname == 'tan':
			plot(x, am*tan(x)+ps)
		else:
			raise Exception("Invalid function")
	else:
		if funcname == 'sin':
			plot(x,am*sin(1/x)+ps)
		elif funcname == 'cos':
			plot(x, am*cos(1/x)+ps)
		elif funcname == 'tan':
			plot(x, am*tan(1/x)+ps)
		else:
			raise Exception("Invalid function")
