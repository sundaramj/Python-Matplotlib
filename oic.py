import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import CsvRead as CsvData #imported python file for CSV read 
import warnings
warnings.filterwarnings("ignore")

#below function is used to convert nan value to default interpolate value between of two numbers
def nan_helper(y):
    return np.isnan(y), lambda z: z.nonzero()[0]

# parameter: {filename}.py {savefilename} {filesize} {sourcecsvfile}.csv {table show[0,1]}
def salesGrowth(SaveFileType,LineType,FileFormat,TableShow = None):
	try:
		import ParamValidator as prmValid #validate parmas when run script from command line

		print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

		#ReadData = CsvData.readData() # read CSV data
		dataRead = CsvData.readData() # read CSV data multiple file		
		incr=1
		for ReadData in dataRead:				
			plt.rcParams["font.family"] = "Arial" # apply for whole chart

			now = datetime.datetime.now()
			curTime = now.strftime("%Y%m%d%H%M%S%f")
				
			#saveFileNameParam = sys.argv[1] #Read first param
			saveFileNameParam = ReadData['fileName'] #Read first param
			saveFileSizeParam = SaveFileType
			markerSize = 8 # Marker width size
			lineWidth = 2 # Line width value
			count = 0 # Loop start count
			dottedKey = 3 # define where we need a dotted key on which line
			titleName = 'Sales Growth'
			replaceCountWord = 'Count'
			savePath = "export_img/"
			saveFile = "_"+saveFileNameParam+".png"
			color = ['#2e91ad','#2e91ad','#2e91ad','#ff7800','#2e91ad'] #color code of line
			style = ['--','-','--','-',''] # line type
			marker = ['','','','o',''] # Marker type	
			legendLabel = ReadData['legendName'] # legend name
			legendLabel1 = ReadData['legendName'] # legend name
			legendLabel1 = [w.replace(replaceCountWord, '_nolegend_') for w in legendLabel1] # replace Count word with _nolegend_. not required to display Count in legend	
			#numberFontSize = 15.5
			
			if saveFileSizeParam == 'A4': #If A4 Size		
				InWidth	= 8.3
				InHeight = 11.7
				dpi = 150
				numberFontSize = 15.5
			elif saveFileSizeParam == 'A3': #If A3 Size	
				InWidth	= 11.7
				InHeight = 16.5
				dpi = 200
				numberFontSize = 18.5
			else: #Default fize size landscape		
				InWidth	= 10.5
				InHeight = 5.5
				dpi = 250
				numberFontSize = 10

			# Check if CSV file value is in percentage or not
			percentageExist = ReadData["perExist"]
			percentageFormat = '{:3.1f}'
			if percentageExist: percentageFormat = '{:3.1f}%'


			# -- Start Plot  --		
			plt.figure()
			ax = plt.subplot()
			ax.spines['right'].set_visible(False) #hide right line of chart
			ax.spines['top'].set_visible(False) #hide top line of chart

			x = np.array(list(range(len(ReadData['xAxisName'])))) # X values total count

			yAxisValue = ReadData['axisValue'] # Y values data from CSV		
			# added below to set Y axis value static & dynamic Start
			yMin = ReadData['yMin']
			yMax = ReadData['yMax']	
			y = np.array(yAxisValue)
			plt.ylim(int(yMin),int(yMax))			
			
			my_xticks = ReadData['xAxisName'] # X values data from CSV

			for i,j in zip(x,y[dottedKey]):	# added to display value on marker		
				ax.annotate(percentageFormat.format(j),xy=(i,j),horizontalalignment='right',verticalalignment='bottom',fontsize=numberFontSize)	#converted values into percentage value	
					
			from scipy import interpolate # interpolate is used to convert the streight line with curve
			legend_elements = []		
			for data in y:
				#interpolate value if found Nan value in array
				data = np.array(data)
				nans, xdata= nan_helper(data)
				data[nans]= np.interp(xdata(nans), xdata(~nans), data[~nans])
				# to set a curve line instead of streight line Start
				f = interpolate.interp1d(np.arange(len(data)), data, kind='cubic') # Interpolate Line
				xnew = np.arange(0, len(data)-1, 0.01)
				ynew = f(xnew)	
				# to set a curve line iprint(nstead of streight line End
				plt.plot(xnew, ynew, color=color[count],linestyle=style[count],markersize=markerSize,linewidth=lineWidth,label=legendLabel[count]) #Set plot final plot
				legend_elements.append(Line2D([0], [0],color=color[count],label=legendLabel1[count],linestyle=style[count],markersize=markerSize,linewidth=lineWidth,marker=marker[count])) #to set the legend	
				count = count+1 # Auto increament of loop
			
			plt.plot(y[dottedKey],color='#ff6100',linestyle='',markersize=markerSize,linewidth=lineWidth,marker='o'); # Add orange marker on line
			plt.legend(handles=legend_elements,bbox_to_anchor=(1, 0.8),prop={'size': numberFontSize,'weight':'bold'},labelspacing=2,frameon=False) # to set the legend
			vals = ax.get_yticks()
			ax.set_yticklabels([percentageFormat.format(x) for x in vals],fontsize=numberFontSize) # Converted values into percentage value
			
			# Display table or not based on parameter passed by user, by default table will display on graph, 0 -> dont display table, 1 -> Display table
			try:
				TableShow # Parameter which is entered by user
			except Exception as e:
				showTable = True # default display Table
			else:
				showTable = False
				if TableShow == 't': # if user enter 1 display table else dont display the table
					showTable = True
					showTable
			plt.xticks(x, my_xticks,fontsize=numberFontSize)
			
			if showTable: # True display Table
				# First Table start
				the_table = plt.table(cellText=y,colLabels=my_xticks,loc='bottom',colLoc='right',rowLoc='left')	
				
				the_table.set_fontsize(numberFontSize)
				the_table.scale(1,1)
				
				#Remove Border of table 1 cell
				for key, cell in the_table.get_celld().items():		
					cell.set_linewidth(0)
				# First Table end
				
				# right side table of company name start		
				my_xticks_1 = [titleName]
				legendLabel_1 = np.reshape(legendLabel, (-1, 1))	
				
				the_table1 = plt.table(cellText=legendLabel_1,colLabels=my_xticks_1,loc='bottom right',colLoc='bottom left',rowLoc='bottom left',animated=True)
				the_table1.auto_set_column_width([-1,0,1]) # set column width	
				the_table1.set_fontsize(numberFontSize)
				the_table1.scale(1,1)
				cells = the_table1.properties()["celld"]
				
				# row text left align
				cellLength = len(legendLabel) #lengtshowTableh of row
				for i in range(0,cellLength+1):
					cells[i, 0]._loc = 'left'		
				
				
				#Remove Border of table 2 cell
				for key, cell in the_table1.get_celld().items():
					cell.set_linewidth(0)
					
				# right side table of company name end
				
				plt.xticks([]) # remove x Axis values, already put value using table
							
			plt.title(titleName,loc='left',fontsize=22,fontweight="bold") # Set title 
				
			fig = plt.gcf()
			fig.set_size_inches(InWidth, InHeight)
			plt.subplots_adjust(bottom=0.25,right=0.74,top=0.92,hspace=0.25,wspace=0.35) #Margin size of plot
			plt.savefig(savePath+curTime+saveFile,dpi=dpi) #save image with DPI
			print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			incr=incr+1
			#plt.show()
	except Exception as e:	
		print("Something Went wrong! Unable to process your request.")
		print(e)
