import numpy as np
import matplotlib.pyplot as pp
import math
import cmath











if __name__ == '__main__':

	EinFreq = 1.935*10^14			#1550nm = 193.5THz
	EinAngF = 2*np.pi*EinFreq
	
	NumCycles = 1000
	
	

	x = np.linspace(-np.pi*2, np.pi*2, 100) 
	Vrf = []
	Vrf[:100] = 0
	
	Vdc = 0
	
	Ein= []
	Eout=[]
	B1 = []
	B2 = []
	B3 = []
	B4 = []
	B5 = []

	
	
	phi = np.pi * 0.5
	
	for count, val in enumerate(x):
		
		Vtotal = Vrf[count] + Vdc
		phi = np.pi * Vtotal
		Ein.append(cmath.exp(1j*val))
		B1.append(Ein[-1]/2)
		B2.append(Ein[-1]/2)
		B3.append(B1[-1]*cmath.exp(1j*float((phi/2))))
		B4.append(B2[-1]*cmath.exp(-1j*float((phi/2))))
		Eout.append(B3[-1]+B4[-1])
		
	
	#B4 = B2*cmath.exp(-phi*1j)
	##pp.plot(x, Vrf, label = 'RFinput')
	#print B3
	pp.plot(x, np.real(Ein), label='REin')
	#pp.plot(x, np.imag(Ein), label='IEin')
	#pp.plot(x, np.real(B1), label='RB1')
	#pp.plot(x, np.imag(B1), label='IB1')
	#pp.plot(x, np.real(B2), label='RB2')
	#pp.plot(x, np.imag(B2), label='IB2')
	
	#pp.plot(x, np.real(B3), label='RB3')
	#pp.plot(x, np.imag(B3), label='IB3')
	#pp.plot(x, np.real(B4), label='RB4')
	#pp.plot(x, np.imag(B4), label='IB4')
	
	pp.plot(x, np.real(Eout), label='Eout')
	
	pp.legend()
	
	pp.grid()
	pp.show()
	
	'''
	print 'started'
	x = np.linspace(-np.pi*2, np.pi*2, 201)
	phi = np.pi/6
	Ein = np.sin(x)
	print Ein
	
	
	
	B1 = np.sin(x+phi)
	B2 = Ein/math.sqrt(2)
	
	#print B1
	
	
	B3 = B1*cmath.exp(1j*phi)
	
	'''