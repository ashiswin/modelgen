<?php
	require_once 'utils/database.php';
	require_once 'connectors/EventConnector.php';

	$id = $_POST['id'];

	$EventConnector = new EventConnector($conn);

	$response['event'] = $EventConnector->delete($id);
	$response['success'] = true;
?>