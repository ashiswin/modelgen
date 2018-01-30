<?php
	require_once 'utils/database.php';
	require_once 'connectors/AdminConnector.php';

	$id = $_GET['id'];

	$AdminConnector = new AdminConnector($conn);

	$response['admin'] = $AdminConnector->select($id);
	$response['success'] = true;
?>