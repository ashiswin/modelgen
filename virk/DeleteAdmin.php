<?php
	require_once 'utils/database.php';
	require_once 'connectors/AdminConnector.php';

	$id = $_POST['id'];

	$AdminConnector = new AdminConnector($conn);

	$response['admin'] = $AdminConnector->delete($id);
	$response['success'] = true;
?>