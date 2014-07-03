import numpy as np
import matplotlib.pyplot as plt
import random

class BacteriaGraph(object):
	"""
	
	"""
	def __init__(self, srcTable='sourcetable.txt', srcInfo='sourceinfo.txt', srcMetrics='sourcemetrics.txt', srcFeatureList='sourcefeaturelist.txt', srcStability='sourcestability.txt'):
		self.srcTable = srcTable
		self.srcInfo = srcInfo
		self.scrMetrics = srcMetrics
		self.scrFL = scrFeaturList
		self.srcStability = scrStability
		#FIXME
	def _loadData(self):
		self.data1 = np.loadtxt(self.srcTable)
		self.data2 = self.data1.T
		self.samplesCount = self.data1.shape[0]
		self.bacteriaCount = self.data1.shape[1]
	def percentagehistogramm(self):
		#CREATION OF THE PERCENTAGE HISTOGRAMM OF THE DATA WITH RANDOM COLORS
		rangeNum = np.arange(1, samplesCount + 1, 1)
		width = 0.8
		bottom = [0] * samplesCount
		colors = [0] * bacteriaCount
		n = 0
		for i in data2:
			if n != 0:
				#sum the botton at the last bottom
				cont = 0
				while cont < samplesCount:
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
