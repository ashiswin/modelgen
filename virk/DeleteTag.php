<?php
	require_once 'utils/database.php';
	require_once 'connectors/TagConnector.php';

	$id = $_POST['id'];

	$TagConnector = new TagConnector($conn);

	$response['tag'] = $TagConnector->delete($id);
	$response['success'] = true;
?>