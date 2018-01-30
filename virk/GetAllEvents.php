<?php
	require_once 'utils/database.php';
	require_once 'connectors/EventConnector.php';

	$id = $_GET['id'];

	$EventConnector = new EventConnector($conn);

	$response['events'] = $EventConnector->selectAll();
	$response['success'] = true;
?>