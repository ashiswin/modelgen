<?php
	class AdminsConnector {
		private $mysqli = NULL;

		public static $TABLE_NAME = "admins";
		public static $COLUMN_ID = "id";
		public static $COLUMN_USERNAME = "username";
		public static $COLUMN_PASSWORD = "password";
		public static $COLUMN_SALT = "salt";
		public static $COLUMN_NAME = "name";


		private $createStatement = NULL;
		private $selectStatement = NULL;
		private $selectAllStatement = NULL;
		private $updateStatement = NULL;
		private $deleteStatement = NULL;
		function __construct($mysqli) {
			if($mysqli->connect_errno > 0){
				die('Unable to connect to database [' . $mysqli->connect_error . ']');
			}

			$this->mysqli = $mysqli;

			$this->createStatement = $mysqli->prepare("INSERT INTO " . AdminsConnector::$TABLE_NAME . "(`" . AdminsConnector::$COLUMN_USERNAME . "`,`" . AdminsConnector::$COLUMN_PASSWORD . "`,`" . AdminsConnector::$COLUMN_SALT . "`,`" . AdminsConnector::$COLUMN_NAME . "`) VALUES(?,?,?,?,?)");
			$this->selectStatement = $mysqli->prepare("SELECT * FROM " . AdminsConnector::$TABLE_NAME . " WHERE `" . AdminsConnector::$COLUMN_ID . "` = ?");
			$this->selectAllStatement = $mysqli->prepare("SELECT * FROM " . AdminsConnector::$TABLE_NAME);
			$this->deleteStatement = $mysqli->prepare("DELETE FROM " . AdminsConnector::$TABLE_NAME . " WHERE `" . AdminsConnector::$COLUMN_ID . "` = ?");
		}

		public function create($username, $password, $salt, $name) {
			$this->createStatement->bind_param("ssss", $username, $password, $salt, $name);
			return $this->createStatement->execute();
		}

		public function select($id) {
			$this->selectStatement->bind_param("i", $id);
			if(!$this->selectStatement->execute()) return false;

			return true;
		}
		public function selectAll() {
			if(!$this->selectAllStatement->execute()) return false;
			$result = $this->selectAllStatement->get_result();
			$resultArray = $result->fetch_all(MYSQLI_ASSOC);
			return $resultArray;
		}

		public function delete($id) {
			$this->deleteStatement->bind_param("i", $id);
			if(!$this->deleteStatement->execute()) return false;

			return true;
		}
	}
?>