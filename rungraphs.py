import sys
import oi as Oi #imported python file for oi read 
import oic as Oic #imported python file for oic read

SaveFileType = sys.argv[1] # svg
LineType = sys.argv[2] #s = Streight, i = Interpolate
FileFormat = sys.argv[3] #p=portrait, l=Landscape
try:
	TableShow = sys.argv[4] # t
except Exception as e:
	TableShow = 0
	
Oi.operatingIndex(SaveFileType,LineType,FileFormat,TableShow) # function to call oi.py file
Oic.salesGrowth(SaveFileType,LineType,FileFormat,TableShow) # function to call oic.py file
