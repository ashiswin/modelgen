from pattern.text.en import singularize

class PHPConnectorDocument:
	def __init__(self, t, c):
		self.table = t
		self.columns = c
		
		self.document = "<?php\n"
		
		self.header()
		self.columnVariables()
		self.defineStatements()
		self.constructor()
		self.defineCreate()
		self.defineSelect()
		self.defineSelectAll()
		self.defineUpdate()
		self.defineDelete()
		self.footer()
		
	def header(self):
		className = singularize(self.table.title())
		self.document += "\tclass " + className + "Connector {\n"
		self.document += "\t\tprivate $mysqli = NULL;\n\n"
		self.document += "\t\tpublic static $TABLE_NAME = \"" + self.table + "\";\n"
	
	def columnVariables(self):
		for c in self.columns:
			self.document += "\t\tpublic static $COLUMN_" + c[0].upper() + " = \"" + c[0] + "\";\n"
		self.document += "\n\n"
		
	def defineStatements(self):
		self.document += "\t\tprivate $createStatement = NULL;\n"
		self.document += "\t\tprivate $selectStatement = NULL;\n"
		self.document += "\t\tprivate $selectAllStatement = NULL;\n"
		self.document += "\t\tprivate $updateStatement = NULL;\n"
		self.document += "\t\tprivate $deleteStatement = NULL;\n"
	
	def constructor(self):
		connectorName = singularize(self.table.title()) + "Connector"
		self.document += "\t\tfunction __construct($mysqli) {\n"
		self.document += "\t\t\tif($mysqli->connect_errno > 0){\n"
		self.document += "\t\t\t\tdie('Unable to connect to database [' . $mysqli->connect_error . ']');\n"
		self.document += "\t\t\t}\n\n"
		self.document += "\t\t\t$this->mysqli = $mysqli;\n\n"
		
		# Define create statement
		self.document += "\t\t\t$this->createStatement = $mysqli->prepare(\"INSERT INTO \" . " + connectorName + "::$TABLE_NAME . \"("
		
		for i in range(len(self.columns)):
			c = self.columns[i]
			
			if c[0] == "id":
				continue
			
			self.document += "`\" . " + connectorName + "::$COLUMN_" + c[0].upper() + " . \"`"
			if i < len(self.columns) - 1:
				self.document += ","
		self.document += ") VALUES("
		for i in range(len(self.columns) - 1):
			self.document += "?"
			if i < len(self.columns) - 2:
				self.document += ","
		
		self.document += ")\");\n"
		
		# Define select statement
		self.document += "\t\t\t$this->selectStatement = $mysqli->prepare(\"SELECT * FROM \" . " + connectorName + "::$TABLE_NAME . \" WHERE `\" . " + connectorName + "::$COLUMN_ID . \"` = ?\");\n"
		
		# Define selectAll statement
		self.document += "\t\t\t$this->selectAllStatement = $mysqli->prepare(\"SELECT * FROM \" . " + connectorName + "::$TABLE_NAME);\n"
		
		# TODO: Define update statement
		
		# Define delete statement
		self.document += "\t\t\t$this->deleteStatement = $mysqli->prepare(\"DELETE FROM \" . " + connectorName + "::$TABLE_NAME . \" WHERE `\" . " + connectorName + "::$COLUMN_ID . \"` = ?\");\n"
		
		self.document += "\t\t}\n\n"
	
	def defineCreate(self):
		self.document += "\t\tpublic function create("
		for i in range(len(self.columns)):
			c = self.columns[i]
			if c[0] == "id":
				continue
			
			self.document += "$" + c[0]
			if i < len(self.columns) - 1:
				self.document += ", "
		self.document += ") {\n"
		
		self.document += "\t\t\t$this->createStatement->bind_param(\""
		types = ""
		
		for i in range(len(self.columns)):
			c = self.columns[i]
			
			if c[0] == "id":
				continue
			if "int" in c[1]:
				types += "i"
			elif "varchar" in c[1] or "text" in c[1] or "date" in c[1]:
				types += "s"
			else:
				types += "?"
		self.document += types + "\", "
		for i in range(len(self.columns)):
			c = self.columns[i]
			if c[0] == "id":
				continue
			
			self.document += "$" + c[0]
			if i < len(self.columns) - 1:
				self.document += ", "
		self.document += ");\n"
		self.document += "\t\t\treturn $this->createStatement->execute();\n";
		self.document += "\t\t}\n\n"
	
	def defineSelect(self):
		self.document += "\t\tpublic function select($id) {\n"
		self.document += "\t\t\t$this->selectStatement->bind_param(\"i\", $id);\n"
		self.document += "\t\t\tif(!$this->selectStatement->execute()) return false;\n\n"
		self.document += "\t\t\treturn true;\n"
		self.document += "\t\t}\n"
		
	def defineSelectAll(self):
		self.document += "\t\tpublic function selectAll() {\n"
		self.document += "\t\t\tif(!$this->selectAllStatement->execute()) return false;\n"
		self.document += "\t\t\t$result = $this->selectAllStatement->get_result();\n"
		self.document += "\t\t\t$resultArray = $result->fetch_all(MYSQLI_ASSOC);\n"
		self.document += "\t\t\treturn $resultArray;\n"
		self.document += "\t\t}\n\n"
	
	def defineUpdate(self):
		pass
		# TODO: Define update
	
	def defineDelete(self):
		self.document += "\t\tpublic function delete($id) {\n"
		self.document += "\t\t\t$this->deleteStatement->bind_param(\"i\", $id);\n"
		self.document += "\t\t\tif(!$this->deleteStatement->execute()) return false;\n\n"
		self.document += "\t\t\treturn true;\n"
		self.document += "\t\t}\n"
	
	def footer(self):
		self.document += "\t}\n"
		self.document += "?>"
	def display(self):
		print self.document
	
	def save(self, file):
		file.write(self.document)
		file.close()

class PHPDatabaseDocument:
	def __init__(self, host, user, pwd, db):
		self.document = "<?php\n"
		self.document += "\t$conn = new mysqli(\"" + host + "\", \"" + user + "\", \"" + pwd + "\", \"" + db + "\");\n"
		self.document += "\tif($conn->connect_error) {\n"
		self.document += "\t\t$response[\"success\"] = false;\n"
		self.document += "\t\t$response[\"message\"] = \"Connection failed: \" . $conn->connect_error;\n"
		self.document += "\t}\n"
		self.document += "?>\n"
	
	def display(self):
		print self.document
	
	def save(self, file):
		file.write(self.document)
		file.close()

class PHPGetterDocument:
	def __init__(self, t):
		self.connectorName = singularize(t.title()) + "Connector"
		self.table = t
		
		self.document = "<?php\n"
		
		self.includes()
		self.body()
		
	def includes(self):
		self.document += "\trequire_once 'utils/database.php';\n"
		self.document += "\trequire_once 'connectors/" + self.connectorName + ".php';\n\n"
	
	def body(self):
		self.document += "\t$id = $_GET['id'];\n\n"
		self.document += "\t$" + self.connectorName + " = new " + self.connectorName + "($conn);\n\n"
		self.document += "\t$response['" + singularize(self.table) + "'] = $" + self.connectorName + "->select($id);\n"
		self.document += "\t$response['success'] = true;\n\n"
		self.document += "\techo(json_encode($response));\n"
		self.document += "?>"
	
	def display(self):
		print self.document
	
	def save(self, file):
		file.write(self.document)
		file.close()

class PHPAllGetterDocument:
	def __init__(self, t):
		self.connectorName = singularize(t.title()) + "Connector"
		self.table = t
		
		self.document = "<?php\n"
		
		self.includes()
		self.body()
		
	def includes(self):
		self.document += "\trequire_once 'utils/database.php';\n"
		self.document += "\trequire_once 'connectors/" + self.connectorName + ".php';\n\n"
	
	def body(self):
		self.document += "\t$" + self.connectorName + " = new " + self.connectorName + "($conn);\n\n"
		self.document += "\t$response['" + self.table + "'] = $" + self.connectorName + "->selectAll();\n"
		self.document += "\t$response['success'] = true;\n\n"
		self.document += "\techo(json_encode($response));\n"
		self.document += "?>"
	
	def display(self):
		print self.document
	
	def save(self, file):
		file.write(self.document)
		file.close()

class PHPDeleterDocument:
	def __init__(self, t):
		self.connectorName = singularize(t.title()) + "Connector"
		self.table = t
		
		self.document = "<?php\n"
		
		self.includes()
		self.body()
		
	def includes(self):
		self.document += "\trequire_once 'utils/database.php';\n"
		self.document += "\trequire_once 'connectors/" + self.connectorName + ".php';\n\n"
	
	def body(self):
		self.document += "\t$id = $_POST['id'];\n\n"
		self.document += "\t$" + self.connectorName + " = new " + self.connectorName + "($conn);\n\n"
		self.document += "\t$response['" + singularize(self.table) + "'] = $" + self.connectorName + "->delete($id);\n"
		self.document += "\t$response['success'] = true;\n\n"
		self.document += "\techo(json_encode($response));\n"
		self.document += "?>"
	
	def display(self):
		print self.document
	
	def save(self, file):
		file.write(self.document)
		file.close()

class PHPCreatorDocument:
	def __init__(self, t, c):
		self.connectorName = singularize(t.title()) + "Connector"
		self.table = t
		self.columns = c
		
		self.document = "<?php\n"
		
		self.includes()
		self.body()
	
	def includes(self):
		self.document += "\trequire_once 'utils/database.php';\n"
		self.document += "\trequire_once 'connectors/" + self.connectorName + ".php';\n\n"
	
	def body(self):
		for c in self.columns:
			if c[0] == 'id':
				continue
			self.document += "\t$" + c[0] + " = $_POST['" + c[0] + "'];\n"
		self.document += "\n"
		self.document += "\t$" + self.connectorName + " = new " + self.connectorName + "($conn);\n\n"
		self.document += "\tif(!$" + self.connectorName + "->create("
		first = True
		for c in self.columns:
			if c[0] == 'id':
				continue
			
			if not first:
				self.document += ", "
			
			first = False
			self.document += "$" + c[0]
		self.document += ")) {\n"
		self.document += "\t\t$response['success'] = false;\n"
		self.document += "\t\t$response['message'] = \"Failed to create " + singularize(self.table) + "!\";\n"
		self.document += "\t}\n"
		self.document += "\telse {\n"
		self.document += "\t\t$response['success'] = true;\n"
		self.document += "\t}\n\n"
		self.document += "\techo(json_encode($response));\n"
		self.document += "?>"
	
	def display(self):
		print self.document
	
	def save(self, file):
		file.write(self.document)
		file.close()
