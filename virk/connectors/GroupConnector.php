<?php
	class GroupConnector {
		private $mysqli = NULL;

		public static $TABLE_NAME = "groups";
		public static $COLUMN_GROUPID = "groupid";
		public static $COLUMN_NAME = "name";
		public static $COLUMN_MEMBERS = "members";
		public static $COLUMN_VOTES = "votes";
		public static $COLUMN_REGISTERED = "registered";
		public static $COLUMN_PASSWORD = "password";
		public static $COLUMN_EVENTID = "eventid";


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

			$this->createStatement = $mysqli->prepare("INSERT INTO " . GroupConnector::$TABLE_NAME . "(`" . GroupConnector::$COLUMN_GROUPID . "`,`" . GroupConnector::$COLUMN_NAME . "`,`" . GroupConnector::$COLUMN_MEMBERS . "`,`" . GroupConnector::$COLUMN_VOTES . "`,`" . GroupConnector::$COLUMN_REGISTERED . "`,`" . GroupConnector::$COLUMN_PASSWORD . "`,`" . GroupConnector::$COLUMN_EVENTID . "`) VALUES(?,?,?,?,?,?,?)");
			$this->selectStatement = $mysqli->prepare("SELECT * FROM " . GroupConnector::$TABLE_NAME . " WHERE `" . GroupConnector::$COLUMN_ID . "` = ?");
			$this->selectAllStatement = $mysqli->prepare("SELECT * FROM " . GroupConnector::$TABLE_NAME);
			$this->deleteStatement = $mysqli->prepare("DELETE FROM " . GroupConnector::$TABLE_NAME . " WHERE `" . GroupConnector::$COLUMN_ID . "` = ?");
		}

		public function create($groupid, $name, $members, $votes, $registered, $password, $eventid) {
			$this->createStatement->bind_param("isssisi", $groupid, $name, $members, $votes, $registered, $password, $eventid);
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