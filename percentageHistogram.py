"""
data1	:	data imported from the fle (Bacteria x Sample)
data2	:	data inverted (Samples x Bacteria)
info1	:	the data of information of the patients (Samples x Info)
info2	:	info trasposed (Info x Samples)
	:	columns of the data
"""

#position of the file with the data
#pathTableFile = '/home/stefano/P1'
#pathInfoFile = '/home/stefano/P2'
# Hlist('/home/stefano/P1', '/home/stefano/P2')

import numpy as np
import matplotlib.pyplot as plt
import random

pathT = 'fakedata/P1'
#pathMetric = 'home/stefano/Metric'
pathI = 'fakedata/P2'
#data of the relative abundance
data1 = np.loadtxt(pathT)
data2 = data1.T
samples = data1.shape[0]
bacteria = data1.shape[1]
#information of the patients
info1 = np.loadtxt(pathI)
info2 = info1.T
infos = info1.shape[1]
colID, colFM, colAge = 0, 1, 2
infoMatrix = ((samples, 3))

#the metric part analysis



def Hlist():
	#CREATION OF THE PERCENTAGE HISTOGRAMM OF THE DATA WITH RANDOM COLORS
	rangeNum = np.arange(1, samples + 1, 1)
	width = 0.8
	bottom = [0] * samples
	colors = [0] * bacteria
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
    	plt.xlabel('Samples')
	plt.ylabel('Bacteria')
	plt.title('Histogramm of bacteria percentage')	
	plt.show()

def get_randColor():
	#RETURN A EXADECIMAL RANDOM COLOR ie #ff45e2
	r = lambda: random.randint(0, 255)
	return '#%02X%02X%02X' % (r(), r(), r())


