<?php
	class EventConnector {
		private $mysqli = NULL;

		public static $TABLE_NAME = "events";
		public static $COLUMN_ID = "id";
		public static $COLUMN_NAME = "name";
		public static $COLUMN_DATE = "date";
		public static $COLUMN_START = "start";
		public static $COLUMN_END = "end";
		public static $COLUMN_MIN = "min";
		public static $COLUMN_MAX = "max";
		public static $COLUMN_REWARD = "reward";
		public static $COLUMN_LOGOUTPASS = "logoutpass";
		public static $COLUMN_ADMINID = "adminid";
		public static $COLUMN_CREATED = "created";


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

			$this->createStatement = $mysqli->prepare("INSERT INTO " . EventConnector::$TABLE_NAME . "(`" . EventConnector::$COLUMN_NAME . "`,`" . EventConnector::$COLUMN_DATE . "`,`" . EventConnector::$COLUMN_START . "`,`" . EventConnector::$COLUMN_END . "`,`" . EventConnector::$COLUMN_MIN . "`,`" . EventConnector::$COLUMN_MAX . "`,`" . EventConnector::$COLUMN_REWARD . "`,`" . EventConnector::$COLUMN_LOGOUTPASS . "`,`" . EventConnector::$COLUMN_ADMINID . "`,`" . EventConnector::$COLUMN_CREATED . "`) VALUES(?,?,?,?,?,?,?,?,?,?,?)");
			$this->selectStatement = $mysqli->prepare("SELECT * FROM " . EventConnector::$TABLE_NAME . " WHERE `" . EventConnector::$COLUMN_ID . "` = ?");
			$this->selectAllStatement = $mysqli->prepare("SELECT * FROM " . EventConnector::$TABLE_NAME);
			$this->deleteStatement = $mysqli->prepare("DELETE FROM " . EventConnector::$TABLE_NAME . " WHERE `" . EventConnector::$COLUMN_ID . "` = ?");
		}

		public function create($name, $date, $start, $end, $min, $max, $reward, $logoutpass, $adminid, $created) {
			$this->createStatement->bind_param("s???iissi?", $name, $date, $start, $end, $min, $max, $reward, $logoutpass, $adminid, $created);
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