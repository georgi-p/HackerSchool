import xlrd
import unicodecsv as csv
import sys
import os

# Creates a csv file from an xls file
# @skip determines how many of the first few rows of the xls file should be skipped
def Excel2CSV(ExcelFile, CSVFile, skip):
	# Open the given xls file and select the first sheet
	workbook = xlrd.open_workbook(ExcelFile)
	worksheet = workbook.sheet_by_index(0)

	# Create and open the csv file
	csvfile = open(CSVFile, 'wb')
	wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

	# Fill the data
	i = 0
	for rownum in xrange(worksheet.nrows):
		i += 1
		if i <= skip: continue
		wr.writerow(worksheet.row_values(rownum))

	# Close the csv file
	csvfile.close()

# Converts all the xls files in the current directory into csv files
def convertToCSV():
	# Get the current path
	full_path = os.path.realpath(__file__)
	path = os.path.dirname(full_path)

	# Go through all the xls files in the directory
	for subdir, dirs, files in os.walk(path):
		for file in files:
			filepath = subdir + os.sep + file

			if filepath.endswith(".xls"):
				excelfile = filepath
				csvfile = os.path.splitext(filepath)[0]+".csv"
				# Skip the first two rows if the file is "Ek_atte.xls", otherwise skip only the first one
				if excelfile.endswith("atte.xls"): Excel2CSV(excelfile, csvfile, 2)
				else: Excel2CSV(excelfile, csvfile, 1)
