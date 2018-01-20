import mysql.connector
from phpdocument import PHPDocument

conn = mysql.connector.connect(user='ashiswin', password='terror56', host='devostrum.no-ip.info')
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
	
	
	d = PHPDocument(t)
	
