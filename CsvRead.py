# Reading csv data for charts
import os
import csv
import DateTime
import matplotlib.pyplot as plt
import numpy as np

def readData():
	#readFileNameParam = sys.argv[1] #read CSV file	
	finalArr1 = []
	for readFileNameParam in os.listdir("file/"): # Read All the files inside file folder
		if readFileNameParam.endswith(".csv"): #Read only CSV file
			filename = 'file/'+readFileNameParam			
			csvRowCount	 = 0;	
			data = {}	
			arrFirst = []
			arrTwo = []
			arrThree = []
			arrFour = []
			arrFive = []
			arrSix = []
			arrSeven = []
			arrEight = []
			finalArr	= {}
			perExist = False	
			with open(filename,'rt') as file: # Read CSV file
				reader=csv.reader(file)
				data=list(reader)
				for csvRow in data:
					#Auto increament	
					csvRowCount = csvRowCount + 1 		
					if csvRowCount == 1:
						#X axis value escape last 3 row
						arrFirst = csvRow[:-5]
						arrSix = csvRow[:-4] 
						continue
					# All Legend name
					arrTwo.append(csvRow[len(csvRow) - 5])
					# cutomized Legend text
					arrFour.append(csvRow[len(csvRow) - 4]) 
					# chart title
					arrFive.append(csvRow[len(csvRow) - 3])
					
					#arrSeven.append(csvRow[len(csvRow[:1]) - 2])
					if csvRowCount == 2:
						# Y mincsvRow
						arrSeven = csvRow[len(csvRow) - 2]
						# Y max
						arrEight = csvRow[len(csvRow) - 1]
			 
					#to check value is in percentage format or normal format			
					if any("%" in str for str in csvRow): 
						# if percentage value exist in CSV file
						csvRowerarrSevenExist = True 
					# replace % from the value
					csvRow = [w.replace('%', '') for w in csvRow]			
					# Line multidimentional value			
					arrThree.append([np.nan if v is '' else v for v in csvRow[:-5]]) # replace blank value with none
				
				# Start - to get Y min & max value if user not set Y min or max value then find min max from array
				arrThree = [list(map(float, i)) for i in arrThree[:5]] # All the data
				totalVal = [list(map(float, i)) for i in arrThree[:4]] # skipped count row
				exceedYAxis = 3
				if arrSeven == "" or arrEight == "":									
					arrSeven = np.nanmin(totalVal) #Min value
					arrEight = np.nanmax(totalVal) #Max value		
					#get Y min Value
					if arrSeven >= 0:
						arrSeven = arrSeven+exceedYAxis
					else:
						arrSeven = arrSeven-exceedYAxis
					#get Y max Value
					if arrEight >= 0:
						arrEight = arrEight+exceedYAxis
					else:
						arrEight = arrEight-exceedYAxis
				# End - to get Y min & max value if user not set Y min or max value then find min max from array
								
				finalArr['xAxisName'] = arrFirst
				finalArr['legendName'] = arrTwo
				finalArr['axisValue'] = arrThree
				finalArr['axisfigtext'] = arrFour
				finalArr['title'] = arrFive  
				finalArr['perExist'] = perExist
				finalArr['tabletitle'] = arrSix
				finalArr['yMin'] = arrSeven
				finalArr['yMax'] = arrEight
				finalArr['fileName'] = readFileNameParam
				
				finalArr1.append(finalArr)
				#final return done
	return finalArr1 

## End of program
