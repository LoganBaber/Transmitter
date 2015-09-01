import numpy as np
import matplotlib.pyplot as pp
import math
import cmath
from matplotlib import animation

#This function takes in a complex value for the incident electric Field, and a RF voltage.
#It returns the electric fields at several points in the MZ interferometer. 
#				       '''B1'''									    '''B3'''
#                --- Ein*sqrt(2) --- phase shift: exp(+jVotal/Vpi) -----------
#              /                                                              \
#  '''Ein''' -                                                                  --    ''' Eout'''
#              \                                                              /
#                --- Ein*sqrt(2) --- phase shift: exp(-jVotal/Vpi) -----------
#															         '''B4'''
def machZenerTF(Ein, Vrf):

	#Initilize constants
	Vdc = 0
	Vpi = 1
	
	Vtotal = Vrf + Vdc
	phi = Vtotal/Vpi
	B1 = Ein/2
	B2 = Ein/2
	B3 = B1*cmath.exp(1j*float(np.pi*(phi/2)))
	B4 = B2*cmath.exp(-1j*float(np.pi*(phi/2)))
	Eout = B3+B4
			
	return Eout, B1, B3, B4
	
#This function takes in a complex value for the incident electric Field, and two RF voltages (One for each arm).
#It returns the electric fields at several points in the MZ interferometer. 
#										       '''I1'''									    '''I3'''
#						                --- Ein*sqrt(2) --- phase shift: exp(+jVotal/Vpi) -----------
# 						             /                                                              \
# 				  ------- '''Iin''' -                                                                  ----  '''Iout''' -- 
# 				 /		             \                                                              /						\
#  				/	            	  --- Ein*sqrt(2) --- phase shift: exp(-jVotal/Vpi) -----------							 \
#			   /																		   '''I4'''							  \
#	'''Ein''' -																				                  		            -----  '''Eout'''
#				\					       '''Q1'''									       '''Q3'''							  /
#   			 \ 			             --- Ein*sqrt(2) --- phase shift: exp(+jVotal/Vpi) -----------						 /
#  				  \	            	  /                                                               \						/
#  				    ------ '''Qin''' -                                                                  ---- '''Qout''' --
#  						              \                                                               /
#  						                --- Ein*sqrt(2) --- phase shift: exp(-jVotal/Vpi) -----------
#																					         '''Q4'''

def dualPolMZM(Ein, IVrf, QVrf, PVrf):
	
	#Initilize constants
	Vdc = 0
	
	IVtotal = IVrf + Vdc
	QVtotal = QVrf + Vdc
	
	Iphi = np.pi*IVtotal
	Qphi = np.pi*QVtotal
	
	Iin = Ein/2
	Qin = Ein/2
	
	Iout = machZenerTF(Iin, IVtotal)[0]
	Qout = machZenerTF(Qin, QVtotal)[0]*cmath.exp(1j*PVrf)
	
	Eout = Iout+Qout
	
	return Eout, Iout, Qout
	
def dualElectricFields(Iv, Qv):
	t = np.linspace(-np.pi*2, np.pi*2, 100)
	Pv = np.pi/2
	Ein = []
	Eout = []
	Iout = []
	Qout = []

	for count, val in enumerate(t):
	
		Ein.append(cmath.exp(1j*val))
		Eout.append(dualPolMZM(Ein[-1], Iv, Qv, Pv)[0])
		Iout.append(dualPolMZM(Ein[-1], Iv, Qv, Pv)[1])
		Qout.append(dualPolMZM(Ein[-1], Iv, Qv, Pv)[2])
		
	return t, np.real(Ein), np.real(Eout), np.real(Iout), np.real(Qout)

	
#This function creates an electric field in time, and calls the machZenerTF to create the output electricFields in time.
def electricFields(v):

	t = np.linspace(-np.pi*2, np.pi*2, 100)
	Ein = []
	Eout = []
	B1 = []
	B3 = []
	B4 = []

	for count, val in enumerate(t):
	
		Ein.append(cmath.exp(1j*val))
		Eout.append(machZenerTF(Ein[-1], v)[0])
		B1.append(machZenerTF(Ein[-1], v)[1])
		B3.append(machZenerTF(Ein[-1], v)[2])
		B4.append(machZenerTF(Ein[-1], v)[3])
		
	return t, np.real(Ein), np.real(Eout), np.real(B1), np.real(B3), np.real(B4)
	
def mzTFPlot(Ein):
	range = np.linspace(-5, 5, 1000)
	a = []
	for v in range:
		a.append(machZenerTF(Ein, v)[0])
	
	pp.subplot(1, 2, 1)
	pp.plot(range, np.real(a)**2/np.real(Ein)**2)
	pp.ylabel('Normalised Intensity')
	pp.xlabel('Voltage (v)')
	
	pp.subplot(1, 2, 2)
	pp.plot(range, np.real(a)/np.real(Ein))
	pp.ylabel('Normalised Electric Field Amplitude')
	pp.xlabel('Voltage (v)')
	
	pp.show()
	
def mzTFPlotDual(Ein):
	range = np.linspace(-5, 5, 1000)
	a = []
	for Iv in [0, 1, 2, 3]:
		for Qv in range:
			a.append(dualPolMZM(Ein, Iv, Qv, 0)[0])
		
		pp.subplot(1, 2, 1)
		pp.plot(range, np.real(a)**2/np.real(Ein)**2)
		pp.ylabel('Normalised Intensity')
		pp.xlabel('Voltage (v)')
		
		pp.subplot(1, 2, 2)
		pp.plot(range, np.real(a)/np.real(Ein))
		pp.ylabel('Normalised Electric Field Amplitude')
		pp.xlabel('Voltage (v)')
		
		pp.show()
		a = []
	
	
def efPlot():
	range = [0, 0.5, 1, 1.5, 2, 2.5]
	time = []
	Ein = []
	Eout = []
	B1 = []
	B3 = []
	B4 = []
	for v in range:
		a, b, c, d, e, f = electricFields(v)
		time.append(a)
		Ein.append(b)
		Eout.append(c)
		B1.append(d)
		B3.append(e)
		B4.append(f)
		
	pp.subplot(3, 2, 1)
	pp.plot(time[0], Ein[0])
	pp.plot(time[0], Eout[0])
	pp.plot(time[0], B3[0])
	pp.plot(time[0], B4[0])
	pp.ylabel('Normalised Electric Field')
	pp.xlabel('Time')
	
	pp.subplot(3, 2, 3)
	pp.plot(time[1], Ein[1])
	pp.plot(time[1], Eout[1])
	pp.plot(time[1], B3[1])
	pp.plot(time[1], B4[1])
	pp.ylabel('Normalised Electric Field')
	pp.xlabel('Time')
	
	pp.subplot(3, 2, 5)
	pp.plot(time[2], Ein[2])
	pp.plot(time[2], Eout[2])
	pp.plot(time[2], B3[2])
	pp.plot(time[2], B4[2])
	pp.ylabel('Normalised Electric Field')
	pp.xlabel('Time')
	
	pp.subplot(3, 2, 2)
	pp.plot(time[3], Ein[3])
	pp.plot(time[3], Eout[3])
	pp.plot(time[3], B3[3])
	pp.plot(time[3], B4[3])
	pp.ylabel('Normalised Electric Field')
	pp.xlabel('Time')
	
	pp.subplot(3, 2, 4)
	pp.plot(time[4], Ein[4])
	pp.plot(time[4], Eout[4])
	pp.plot(time[4], B3[4])
	pp.plot(time[4], B4[4])
	pp.ylabel('Normalised Electric Field')
	pp.xlabel('Time')
	
	pp.subplot(3, 2, 6)
	pp.plot(time[5], Ein[5])
	pp.plot(time[5], Eout[5])
	pp.plot(time[5], B3[5])
	pp.plot(time[5], B4[5])
	pp.ylabel('Normalised Electric Field')
	pp.xlabel('Time')
	
	pp.show()

	
def plotThings():
	fig = pp.figure()
	ax = fig.add_subplot(111)
	
	for v in np.linspace(0, 4, 200):
		ax.clear()
		time,Ein,Eout,B1,B3,B4, = electricFields(v)
		ax.plot(time, Ein)
		ax.plot(time, Eout)
		ax.plot(time, B3)
		ax.plot(time, B4)
		ax.text(4, -0.9, 'Voltage: {}'.format(round(v, 3)))
		pp.pause(0.01)
	pp.draw()
	
def plotOtherThings():
	fig = pp.figure()
	ax = fig.add_subplot(111)
	
	for Iv in np.linspace(0, 4, 50):
		for Qv in np.linspace(0, 4, 50):
			ax.clear()
			time,Ein,Eout,Iout, Qout = dualElectricFields(Iv,Qv)
			ax.plot(time, Ein)
			ax.plot(time, Eout)
			ax.plot(time, Iout)
			ax.plot(time, Qout)
			ax.text(6, -0.7, 'I voltage: {}'.format(round(Iv, 3)))
			ax.text(6, -0.9, 'Q voltage: {}'.format(round(Qv, 3)))
			pp.pause(0.001)
	pp.draw()
	
		
	

if __name__ == '__main__':
	#efPlot()
	#mzTFPlot(2+2j)
	#plotThings()
	plotOtherThings()
	#mzTFPlotDual(2+2j)
	
	
	
	'''for i in [0, 1, 2, 3, 4, 5, 6]:
		for j in [0, 1, 2, 3, 4, 5, 6]:
			a = dualPolMZM(2+2j, i, j)
			print a
	'''