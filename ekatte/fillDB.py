import csv
import MySQLdb

# Fills a table by given csv file name, table name, and number of columns
def fillTable(name, tname, count, cursor):
	csv_data = csv.reader(file(name))
	query ='INSERT INTO '+tname+' VALUES('

	i = 0
	while i<count-1:
		query += '"%s", '
		i += 1

	if i<count:
		query += '"%s")'
	else:
		query += ')'

	print query

	for row in csv_data:
		cursor.execute(query, row)

# Fills the helper table help_atte
def fillHelp_atte(cursor):
	csv_data = csv.reader(file('Ek_atte.csv'))
	for row in csv_data:
		query = 'INSERT INTO help_atte VALUES("'+row[0]+'", "'+row[1]+'", "'+row[2]+'", "'+row[3]+'", "'+row[4]+'", "'+row[5]+'", "'+row[6]+'", "'+row[7]+'", "'+row[8]+'", "'+row[9]+'", "'+row[10]+'", "'+row[11]+'")'
		cursor.execute(query)

# Fills table regioni
def fillReg(cursor):
	csv_data = csv.reader(file('Ek_reg2.csv'))
	for row in csv_data:
		query = 'INSERT INTO regioni VALUES("'+row[0]+'", "'+row[1]+'", "'+row[2]+'", "'+row[3]+'")'
		cursor.execute(query)

# Fills table oblasti
def fillObl(cursor):
	csv_data = csv.reader(file('Ek_obl.csv'))
	for row in csv_data:
		query = 'INSERT INTO oblasti VALUES("'+row[0]+'", "'+row[2]+'", "'+row[3]+'", "'+row[4]+'", "'+row[5]+'")'
		cursor.execute(query)

# Fills table obstini
def fillObst(cursor):
	csv_data = csv.reader(file('Ek_obst.csv'))
	for row in csv_data:
		subq = '(SELECT oblast FROM help_atte WHERE ekatte="'+row[1]+'")'
		query = 'INSERT INTO obstini VALUES("'+row[0]+'", "'+row[2]+'", '+subq+', "'+row[3]+'", "'+row[4]+'", "'+row[5]+'")'
		cursor.execute(query)

# Fills table kmetstva
def fillKmet(cursor):
	csv_data = csv.reader(file('Ek_kmet.csv'))
	for row in csv_data:
		subq = '(SELECT obstina FROM help_atte WHERE ekatte="'+row[2]+'")'
		query = 'INSERT INTO kmetstva VALUES("'+row[0]+'", "'+row[1]+'", '+subq+', "'+row[3]+'", "'+row[4]+'")'
		cursor.execute(query)

# Fills table selishta
def fillSel(cursor):
	csv_data = csv.reader(file('Ek_atte.csv'))
	for row in csv_data:
		query = 'INSERT INTO selishta VALUES("'+row[0]+'", "'+row[1]+'", "'+row[2]+'", "'+row[5]+'", "'+row[4]+'", "'+row[6]+'", "'+row[7]+'", "'+row[8]+'", "'+row[9]+'", "'+row[10]+'", "'+row[11]+'")'

		# If the foreign key kmetstva is not contained in the table kmetstva, set it to NULL
		try:
			cursor.execute(query)
		except Exception as e:
			if str(e)=="(1452, 'Cannot add or update a child row: a foreign key constraint fails (`ekattedb`.`selishta`, CONSTRAINT `selishta_ibfk_1` FOREIGN KEY (`kmetstvo`) REFERENCES `kmetstva` (`kmetstvo`) ON DELETE CASCADE ON UPDATE CASCADE)')":
				query = 'INSERT INTO selishta VALUES("'+row[0]+'", "'+row[1]+'", "'+row[2]+'", NULL, "'+row[4]+'", "'+row[6]+'", "'+row[7]+'", "'+row[8]+'", "'+row[9]+'", "'+row[10]+'", "'+row[11]+'")'
				cursor.execute(query)

# Fills the database
def fillDB():
	# Open connection
	mydb = MySQLdb.connect(host='localhost',
		user='root',
		passwd='password',
		db='ekattedb')

	# Adjust the charset
	mydb.set_character_set("utf8")
	cursor = mydb.cursor()
	cursor.execute("SET NAMES utf8;")
	cursor.execute("SET CHARACTER SET utf8;")
	cursor.execute("SET character_set_connection=utf8;")

	# Create a helper table help_atte in order to fill the columns oblasti in table obshtini
	cursor.execute("CREATE TABLE help_atte(ekatte varchar(7) PRIMARY KEY NOT NULL, t_v_m varchar(6), name varchar(30), oblast varchar(5), obstina varchar(7), kmetstvo varchar(10), kind varchar(3), category varchar(3), altitude varchar(3), document varchar(6), tsb varchar(4), abc varchar(6)) ENGINE=MyISAM DEFAULT CHARSET=utf8")

	# Fill all the tables
	fillHelp_atte(cursor)
	print "Done with help_atte"

	fillReg(cursor)
	print "Done with regioni"

	fillObl(cursor)
	print "Done with oblasti"

	fillObst(cursor)
	print "Done with obstini"

	fillKmet(cursor)
	print "Done with kmetstva"

	fillSel(cursor)
	print "Done with selishta"

	# Delete the helper table
	cursor.execute("DROP TABLE help_atte")

	#close the connection to the database.
	mydb.commit()
	cursor.close()
