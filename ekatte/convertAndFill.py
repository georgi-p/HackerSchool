import convertToCSV as conv
import fillDB as fill

# Convert all xls files to csv
conv.convertToCSV()
print "Conversion done"
print ""

# Import all the data into the database
fill.fillDB()
print "Importing data to database done"
print ""
