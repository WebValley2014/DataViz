"""
data1	:	data imported from the fle (Bacterias x Sample)
data2	:	data inverted (Samples x Bacterias)
rows	:	rows of the data
cols	:	columns of the data
"""

#position of the file with the data
#pathTableFile = '/home/stefano/P1'
#pathInfoFile = '/home/stefano/P2'
# Hlist('/home/stefano/P1', '/home/stefano/P2')

import numpy as np
import matplotlib.pyplot as plt
import random

'''
SET DATA
	#data of the relative abundance
	data1 = np.loadtxt(pathT)
	data2 = data1.T
	samples = data1.shape[0]
	bacterias = data1.shape[1]
	#information of the patients
	info = np.loadtxt(pathI)
'''

def Hlist(pathT, pathI):
	#data of the relative abundance
	data1 = np.loadtxt(pathT)
	data2 = data1.T
	samples = data1.shape[0]
	bacterias = data1.shape[1]
	#information of the patients
	info = np.loadtxt(pathI)
	#---start of the programm
	rangeNum = np.arange(1, samples + 1, 1)
	width = 0.8
	bottom = [0] * samples
	colors = [0] * bacterias
	n = 0
	for i in data2:
		if n != 0:
			#sum the botton at the last bottom
			cont = 0
			while cont < samples:
	        		bottom[cont] = bottom[cont] + hist[cont]
				cont += 1
		hist = i
		#random color for the histogramm
		randColor = get_randColor()
		colors[n] = randColor
		plt.bar(rangeNum - 0.5, hist, width, color = randColor, bottom = bottom)
		n += 1
    		
	plt.show()

def get_randColor():
	r = lambda: random.randint(0, 255)
	return '#%02X%02X%02X' % (r(),r(),r()) 


