import os
import mysql.connector
from phpdocument import PHPDocument

user = raw_input('Enter username: ')
password = raw_input('Enter password: ')
host = raw_input('Enter host: ')
conn = mysql.connector.connect(user=user, password=password, host=host)
cur = conn.cursor()
cur.execute('show databases')

databases = []
print "Select a database to export:"

i = 1;

for x in cur:
	databases.append(x[0])
	print str(i) + ". " + x[0]
	i += 1

selection = int(raw_input("Enter your selection: ")) - 1

if selection >= len(databases):
	print "Invalid selection!"
	quit()

conn.database = databases[selection]

if not os.path.exists(databases[selection]):
	os.mkdir(databases[selection])
	os.mkdir(databases[selection] + "/connectors")
	os.mkdir(databases[selection] + "/util")

cur.execute("show tables")

tables = []
for x in cur:
	tables.append(x[0])

for t in tables:
	print "Processing table " + t
	cur.execute("describe " + t)
	
	columns = []
	for x in cur:
		columns.append(x)
	
	d = PHPDocument(t, columns)
	
	connectorName = t.title() + "Connector"
	d.save(open(databases[selection] + '/connectors/' + connectorName + '.php', 'w'))
	
	print "Processed table " + t
