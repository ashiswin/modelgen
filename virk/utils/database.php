<?php
	$conn = new mysqli("devostrum.no-ip.info", "ashiswin", "terror56", "virk");
	if($conn->connect_error) {
		$response["success"] = false;
		$response["message"] = "Connection failed: " . $conn->connect_error;
	}
?>
