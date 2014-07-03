import numpy as np
import matplotlib.pyplot as plt
import random

class BacteriaGraph(object):
	"""
	this class can be used for receive, as a output,
	some graphics which analyze the data:
	*percentagehistogramm:
		from the table it can create the percentage 
		of the presence of the bacteria for each sample
	*metricsplot
		from the metrics it create a plot that shows 
		the precision of the results of the machine 
		learning. "Style" can be 1, for only the first 
		10 misurations, 2, for 100, 3, for 1000, 
		or 4, for all. 
	"""
	def __init__(self, srcTable='sourcetable.txt', srcInfo='sourceinfo.txt', srcMetrics='sourcemetrics.txt', srcFeatureList='sourcefeaturelist.txt', srcStability='sourcestability.txt'):
		self.srcTable = srcTable
		self.srcInfo = srcInfo
		self.scrMetrics = srcMetrics
		self.scrFL = scrFeaturList
		self.srcStability = scrStability
		loadData()
	def _loadData(self):
		#if (os.path.lexists(srcTable) = True and os.path.lexists(srcInfo) = True and os.path.lexists(srcMetrics) = True and os.path.lexists(srcFeatureList) = True and os.path.lexists(srcStability) = True):
			self.data1 = np.loadtxt(self.srcTable)
			self.data2 = self.data1.T
			self.samplesCount = self.data1.shape[0]
			self.bacteriaCount = self.data1.shape[1]
			self.metrics = np.loadtxt(self.srcMetrics)
		else:
			raise Exception("wrong source file insert")		
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
	def metricsplot(self, style=1):
		self.style = style
		colRep = 0
		colMMC = 1
		colMMCmin = 2
		colMMCmax = 3
		if style == 1:
			pass


if __name__ == "__main__":
	pass 





		
