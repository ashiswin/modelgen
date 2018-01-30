<?php
	require_once 'utils/database.php';
	require_once 'connectors/EventConnector.php';

	$id = $_GET['id'];

	$EventConnector = new EventConnector($conn);

	$response['event'] = $EventConnector->select($id);
	$response['success'] = true;
?>