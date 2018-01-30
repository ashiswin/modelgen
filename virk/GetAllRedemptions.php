<?php
	require_once 'utils/database.php';
	require_once 'connectors/RedemptionConnector.php';

	$id = $_GET['id'];

	$RedemptionConnector = new RedemptionConnector($conn);

	$response['redemptions'] = $RedemptionConnector->selectAll();
	$response['success'] = true;
?>