<?php
	class TagConnector {
		private $mysqli = NULL;

		public static $TABLE_NAME = "tags";
		public static $COLUMN_TAGID = "tagid";
		public static $COLUMN_STUDENTID = "studentid";
		public static $COLUMN_LASTUPDATE = "lastupdate";


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

			$this->createStatement = $mysqli->prepare("INSERT INTO " . TagConnector::$TABLE_NAME . "(`" . TagConnector::$COLUMN_TAGID . "`,`" . TagConnector::$COLUMN_STUDENTID . "`,`" . TagConnector::$COLUMN_LASTUPDATE . "`) VALUES(?,?,?)");
			$this->selectStatement = $mysqli->prepare("SELECT * FROM " . TagConnector::$TABLE_NAME . " WHERE `" . TagConnector::$COLUMN_ID . "` = ?");
			$this->selectAllStatement = $mysqli->prepare("SELECT * FROM " . TagConnector::$TABLE_NAME);
			$this->deleteStatement = $mysqli->prepare("DELETE FROM " . TagConnector::$TABLE_NAME . " WHERE `" . TagConnector::$COLUMN_ID . "` = ?");
		}

		public function create($tagid, $studentid, $lastupdate) {
			$this->createStatement->bind_param("ss?", $tagid, $studentid, $lastupdate);
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