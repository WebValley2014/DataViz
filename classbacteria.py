import numpy as np
import matplotlib.pyplot as plt
import random

def get_randColor():
	#RETURN A EXADECIMAL RANDOM COLOR ie #ff45e2
	r = lambda: random.randint(0, 255)
	return '#%02X%02X%02X' % (r(), r(), r())

def percentage_row(matrix, style='row'):
	if style != 'row':
		matrix = matrix.T
	percentageData = matrix
	row = percentageData.shape[0]
	sumLine = 0
	for i in matrix:
		arr = i
		#sum row j
		print '---'
		for j in arr:
			sumLine = sumLine + int(j)
		print sumLine
		#convert line j in the percentage number, in var 'percentageData'
		for m1, m2 in matrix, percentageData:
			n = 0
			for k1, k2 in m1, m2:
				k2 = k1 / sumLine
	return percentageData

class BacteriaGraph(object):
	"""
	the srcTable need a format samples X bacteria.
	this class can be used for receive, as a output,
	some graphics which analyze the data:
	*percentagehistogramm:
		from the table it can create the percentage 
		of the presence of the bacteria for each sample
	*metricsplot:
		from the metrics it create a plot that shows 
		the precision of the results of the machine 
		learning. "Style" can be 1, for only the first 
		10 misurations, 2, for 100, 3, for 1000, 
		or 4, for all.
	*classbacteriahistogramm:
		from the class.txt it produce a histogramm which 
		represent the average of the percentage of 
		the bacteria for each class
	"""
	def __init__(self, srcTable='sourcetable.txt', srcClass='sourceclass.txt', srcMetrics='sourcemetrics.txt', srcFeatureList='sourcefeaturelist.txt', srcStability='sourcestability.txt'):
		self.srcTable = srcTable
		self.srcClass = srcClass
		self.srcMetrics = srcMetrics
		self.srcFeatureList = srcFeatureList
		self.srcStability = srcStability
		self._loadData()
	def _loadData(self):
		#if (os.path.lexists(srcTable) = True and os.path.lexists(srcInfo) = True and os.path.lexists(srcMetrics) = True and os.path.lexists(srcFeatureList) = True and os.path.lexists(srcStability) = True):
			self.data1 = np.loadtxt(self.srcTable)
			self.data2 = self.data1.T
			self.samplesCount = self.data1.shape[0]
			self.bacteriaCount = self.data1.shape[1]
			self.metrics = np.loadtxt(self.srcMetrics, skiprows = 2)
			self.classes = np.loadtxt(self.srcClass) 
		#else:
			#raise Exception("wrong source file insert")		
	def percentagehistogramm(self):
		#CREATION OF THE PERCENTAGE HISTOGRAMM OF THE DATA WITH RANDOM COLORS
		#clculate the percentage
		
		width = 0.8
		bottom = [0] * self.samplesCount
		colors = [0] * self.bacteriaCount
		n = 0
		for i in percentageData:
			if n != 0:
				#sum the botton at the last bottom
				cont = 0
				while cont < self.samplesCount:
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
		plt.savefig('histplot', format = 'png')
	def metricsplot(self, style=1):
		self.style = style
		colRep = 0
		colMMC = 1
		colMMCmin = 2
		colMMCmax = 3
		numData = 3694 #numero di analisi
		rowData = self.metrics
		if style == 1:
			rowData = self.metrics[:10]
			numData = 10
		elif style == 2:
			rowData = self.metrics[:100]
			numData = 100
		elif style == 3:
			rowData = self.metrics[:1000]
			numData = 1000
		arrMCC = np.zeros(numData + 1)
		arrMCCerr = np.zeros(numData + 1)
		arrRep = np.zeros(numData + 1)
		n = 0
		for i in rowData:
			arr = i
			arrRep[n] = arr[colRep]
			arrMCC[n] = arr[colMMC]
			arrMCCerr[n] = (arr[colMMCmax] - arr[colMMCmin])/2
			n += 1
		plt.errorbar(arrRep, arrMCC, xerr=0, yerr=arrMCCerr)
		plt.xlim((0.5, numData + 1))
		plt.subplot().set_xscale("log")
		plt.savefig('graphs/metricsplot' + str(style), format = 'png')
		plt.clf()
	def classbacteriahistogramm():
		#calculate the number of classes
		arrCases = []
		try:
			n = 0
			for i in self.classes:
				test = True
				for j in arrCases:
					if j == i:
						test = False
						break
				if test == True:
					arrCases.append[i]
		except:
			arrCases[0] = self.classes[0]
		numCases = len(arrCases)
		#calculate the average of the presence of bacteria
		avBacteria = np.zeros((self.bacteriaCount, numCases))
		for i in self.classes:
			pass

if __name__ == "__main__":


	a=BacteriaGraph('fakedata/percentagebacteria.txt', 'fakedata/P2', 'fakedata/metrics.txt')
	a.metricsplot(3)
	#a.metricsplot(2)
	#a.metricsplot(4)
	#a.metricsplot(1)
	a.percentagehistogramm()
