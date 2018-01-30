<?php
	require_once 'utils/database.php';
	require_once 'connectors/RedemptionConnector.php';

	$id = $_POST['id'];

	$RedemptionConnector = new RedemptionConnector($conn);

	$response['redemption'] = $RedemptionConnector->delete($id);
	$response['success'] = true;
?>