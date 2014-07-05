import numpy as np
import matplotlib.pyplot as plt
import random

def get_randColor():
	#RETURN A EXADECIMAL RANDOM COLOR ie #ff45e2
	r = lambda: random.randint(0, 255)
	return '#%02X%02X%02X' % (r(), r(), r())

def percentage_row(matrix, style='row'):
	mc = matrix.copy()
	if style != 'row':
		mc = mc.T
	#computing sum row by row
	return mc / mc.sum(axis=1).reshape(-1, 1)
	
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
		#if (os.path.exists(srcTable) = True and os.path.lexists(srcInfo) = True and os.path.lexists(srcMetrics) = True and os.path.lexists(srcFeatureList) = True and os.path.lexists(srcStability) = True):
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
		percentageData = percentage_row(self.data1)
		width = 0.8
		bottom = [0] * self.samplesCount
		colors = [0] * self.bacteriaCount
		rangeNum = np.arange(self.bacteriaCount + 1)
		n = 0
		for i in percentageData:
			if n != 0:
				#sum the botton at the last bottom
				cont = 0
				while cont < self.samplesCount + 1:
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
		#definition of the columns of the file
		colRep = 0
		colMMC = 1
		colMMCmin = 2
		colMMCmax = 3
		colSENS = 4
		colSENSmin = 5
		colSENSmax = 6
		colSPEC = 7
		colSPECmin = 8
		colSPECmax = 9
		colPPV = 10
		colPPVmin = 11
		colPPVmax = 12
		colNPV = 13
		colNPVmin = 14
		colNPVmax = 15
		colAUC = 16
		colAUCmin = 17
		colAUCmax = 18
		colACC = 19
		colACCmin = 20
		colACCmax = 21
		colDOR = 22
		colDORmin = 23
		colDORmax = 24
		numData = 3694 #number of analysis
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
		#definition of the array
		arrRep = np.zeros(numData + 1)
		arrMCC = np.zeros(numData + 1)
		arrMCCerr = np.zeros(numData + 1)
		arrSENS = np.zeros(numData + 1)
		arrSENSerr = np.zeros(numData + 1)
		arrSPEC = np.zeros(numData + 1)
		arrSPECerr = np.zeros(numData + 1)
		arrPPV = np.zeros(numData + 1)
		arrPPVerr = np.zeros(numData + 1)
		arrNPV = np.zeros(numData + 1)
		arrNPVerr = np.zeros(numData + 1)
		arrAUC = np.zeros(numData + 1)
		arrAUCerr = np.zeros(numData + 1)
		arrACC = np.zeros(numData + 1)
		arrACCerr = np.zeros(numData + 1)
		#arrDOR = np.zeros(numData + 1)
		#arrDORerr = np.zeros(numData + 1)
		n = 0
		for i in rowData:
			arr = i
			arrRep[n] = arr[colRep]
			arrMCC[n] = arr[colMMC]
			arrMCCerr[n] = (arr[colMMCmax] - arr[colMMCmin])/2
			arrSENS[n] = arr[colSENS]
			arrSENSerr[n] = (arr[colSENSmax] - arr[colSENSmin])/2
			arrSPEC[n] = arr[colSPEC]
			arrSPECerr[n] = (arr[colSPECmax] - arr[colSPECmin])/2
			arrPPV[n] = arr[colPPV]
			arrPPVerr[n] = (arr[colPPVmax] - arr[colPPVmin])/2
			arrNPV[n] = arr[colNPV]
			arrNPVerr[n] = (arr[colNPVmax] - arr[colNPVmin])/2
			arrAUC[n] = arr[colAUC]
			arrAUCerr[n] = (arr[colAUCmax] - arr[colAUCmin])/2
			arrACC[n] = arr[colACC]
			arrACCerr[n] = (arr[colACCmax] - arr[colACCmin])/2
			#arrDOR[n] = arr[colDOR]
			#arrDORerr[n] = (arr[colDORmax] - arr[colDORmin])/2
			n += 1
		plt.errorbar(arrRep, arrMCC, xerr=0, yerr=arrMCCerr)
		plt.xlim((0.5, numData + 1))
		plt.subplot().set_xscale("log")
		plt.savefig('graphs/MCC_metricsplot' + str(style), format = 'png')
		plt.clf()
		plt.errorbar(arrRep, arrSENS, xerr=0, yerr=arrSENSerr, color = 'red')
		plt.xlim((0.5, numData + 1))
		plt.subplot().set_xscale("log")
		plt.savefig('graphs/SENS_metricsplot' + str(style), format = 'png')
		plt.clf()
		plt.errorbar(arrRep, arrSPEC, xerr=0, yerr=arrSPECerr, color = 'green')
		plt.xlim((0.5, numData + 1))
		plt.subplot().set_xscale("log")
		plt.savefig('graphs/SPEC_metricsplot' + str(style), format = 'png')
		plt.clf()
		plt.errorbar(arrRep, arrPPV, xerr=0, yerr=arrPPVerr, color = 'black')
		plt.xlim((0.5, numData + 1))
		plt.subplot().set_xscale("log")
		plt.savefig('graphs/PPV_metricsplot' + str(style), format = 'png')
		plt.clf()
		plt.errorbar(arrRep, arrNPV, xerr=0, yerr=arrNPVerr, color = 'purple')
		plt.xlim((0.5, numData + 1))
		plt.subplot().set_xscale("log")
		plt.savefig('graphs/NPV_metricsplot' + str(style), format = 'png')
		plt.clf()
		plt.errorbar(arrRep, arrAUC, xerr=0, yerr=arrAUCerr, color = 'orange')
		plt.xlim((0.5, numData + 1))
		plt.subplot().set_xscale("log")
		plt.savefig('graphs/AUC_metricsplot' + str(style), format = 'png')
		plt.clf()
		plt.errorbar(arrRep, arrACC, xerr=0, yerr=arrACCerr, color = 'brown')
		plt.xlim((0.5, numData + 1))
		plt.subplot().set_xscale("log")
		plt.savefig('graphs/ACC_metricsplot' + str(style), format = 'png')
		plt.clf()
		#plt.errorbar(arrRep, arrDOR, xerr=0, yerr=arrDORerr)
		#plt.xlim((0.5, numData + 1))
		#plt.subplot().set_xscale("log")
		#plt.savefig('graphs/DOR_metricsplot' + str(style), format = 'png')
		#plt.clf()
'''
	def classbacteriahistogramm():
		#calculate the number of classes
		
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
'''

if __name__ == "__main__":


	a=BacteriaGraph('fakedata/percentagebacteria.txt', 'fakedata/P2', 'fakedata/metrics.txt')
	a.metricsplot(3)
	a.metricsplot(2)
	a.metricsplot(4)
	a.metricsplot(1)
	#a.percentagehistogramm()
