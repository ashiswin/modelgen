import os
import mysql.connector
from phpdocument import PHPConnectorDocument, PHPDatabaseDocument, PHPGetterDocument, PHPAllGetterDocument, PHPDeleterDocument, PHPCreatorDocument
from pattern.text.en import singularize

# Request for MySQL authentication details
user = raw_input('Enter MySQL username: ')
password = raw_input('Enter MySQL password: ')
host = raw_input('Enter host URL/IP Address: ')
directory = raw_input('Folder to save the generated files: ')

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
if not os.path.exists(directory + "/connectors"):
	os.mkdir(directory)
	os.mkdir(directory + "/connectors")
	os.mkdir(directory + "/utils")

# Get and store table name list
cur.execute("show tables")

tables = []
for x in cur:
	tables.append(x[0])

dbDoc = PHPDatabaseDocument(host, user, password, databases[selection])
dbDoc.save(open(directory + '/utils/database.php', 'w'))

print "Wrote database configuration file"

# Process tables
for t in tables:
	print "Processing table " + t
	
	# Get and store structure of table
	cur.execute("describe " + t)
	
	columns = []
	for x in cur:
		columns.append(x)
	
	# Pass table details to PHP generator
	d = PHPConnectorDocument(t, columns)
	getter = PHPGetterDocument(t)
	allgetter = PHPAllGetterDocument(t)
	deleter = PHPDeleterDocument(t)
	creator = PHPCreatorDocument(t, columns)
	
	# Write generated document to file
	connectorName = singularize(t.title()) + "Connector"
	d.save(open(directory + '/connectors/' + connectorName + '.php', 'w'))
	print "\tWrote connector to " + directory + '/connectors/' + connectorName + '.php'
	getter.save(open(directory + '/Get' + singularize(t.title()) + '.php', 'w'))
	print "\tWrote getter to " + directory + '/Get' + singularize(t.title()) + '.php'
	allgetter.save(open(directory + '/GetAll' + t.title() + '.php', 'w'))
	print "\tWrote allgetter to " + directory + '/GetAll' + t.title() + '.php'
	deleter.save(open(directory + '/Delete' + singularize(t.title()) + '.php', 'w'))
	print "\tWrote deleter to " + directory + '/Delete' + t.title() + '.php'
	creator.save(open(directory + '/Create' + singularize(t.title()) + '.php', 'w'))
	print "\tWrote creator to " + directory + '/Create' + singularize(t.title()) + '.php'
	
	print "Processed table " + t
