<?php
	class RedemptionConnector {
		private $mysqli = NULL;

		public static $TABLE_NAME = "redemptions";
		public static $COLUMN_ID = "id";
		public static $COLUMN_STUDENTID = "studentid";
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

			$this->createStatement = $mysqli->prepare("INSERT INTO " . RedemptionConnector::$TABLE_NAME . "(`" . RedemptionConnector::$COLUMN_STUDENTID . "`,`" . RedemptionConnector::$COLUMN_EVENTID . "`) VALUES(?,?,?)");
			$this->selectStatement = $mysqli->prepare("SELECT * FROM " . RedemptionConnector::$TABLE_NAME . " WHERE `" . RedemptionConnector::$COLUMN_ID . "` = ?");
			$this->selectAllStatement = $mysqli->prepare("SELECT * FROM " . RedemptionConnector::$TABLE_NAME);
			$this->deleteStatement = $mysqli->prepare("DELETE FROM " . RedemptionConnector::$TABLE_NAME . " WHERE `" . RedemptionConnector::$COLUMN_ID . "` = ?");
		}

		public function create($studentid, $eventid) {
			$this->createStatement->bind_param("si", $studentid, $eventid);
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