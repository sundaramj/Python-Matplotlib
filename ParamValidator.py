import sys

if 2 > len(sys.argv) or 3 > len(sys.argv) or 4 > len(sys.argv): # validate file name if user has not entered display error message
	print("Please enter correct parameter")	
	exit()