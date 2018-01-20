class PHPDocument:
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
		className = self.table.title()
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
		connectorName = self.table.title() + "Connector"
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
		for i in range(len(self.columns)):
			self.document += "?"
			if i < len(self.columns) - 1:
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
			elif "varchar" in c[1] or "text" in c[1]:
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
	
	
