import os
import mysql.connector
from phpdocument import PHPDocument

# Request for MySQL authentication details
user = raw_input('Enter MySQL username: ')
password = raw_input('Enter MySQL password: ')
host = raw_input('Enter host URL/IP Address: ')

# Connect to MySQL server (defaults to port 3306)
conn = mysql.connector.connect(user=user, password=password, host=host)

# Get database name list
cur = conn.cursor()
cur.execute('show databases')

# Store and display databases for users to select
databases = []
print "Select a database to export:"

i = 1;

for x in cur:
	databases.append(x[0])
	print str(i) + ". " + x[0]
	i += 1

# Get user's database selection
selection = int(raw_input("Enter your selection: ")) - 1

if selection >= len(databases):
	print "Invalid selection!"
	quit()

# Set database for session
conn.database = databases[selection]

# Create directory structure to store generated files
if not os.path.exists(databases[selection]):
	os.mkdir(databases[selection])
	os.mkdir(databases[selection] + "/connectors")
	os.mkdir(databases[selection] + "/util")

# Get and store table name list
cur.execute("show tables")

tables = []
for x in cur:
	tables.append(x[0])

# Process tables
for t in tables:
	print "Processing table " + t
	
	# Get and store structure of table
	cur.execute("describe " + t)
	
	columns = []
	for x in cur:
		columns.append(x)
	
	# Pass table details to PHP generator
	d = PHPDocument(t, columns)
	
	# Write generated document to file
	connectorName = t.title() + "Connector"
	d.save(open(databases[selection] + '/connectors/' + connectorName + '.php', 'w'))
	
	print "Processed table " + t
