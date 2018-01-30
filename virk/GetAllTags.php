<?php
	require_once 'utils/database.php';
	require_once 'connectors/TagConnector.php';

	$id = $_GET['id'];

	$TagConnector = new TagConnector($conn);

	$response['tags'] = $TagConnector->selectAll();
	$response['success'] = true;
?>