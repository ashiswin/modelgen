<?php
	require_once 'utils/database.php';
	require_once 'connectors/AdminConnector.php';

	$id = $_GET['id'];

	$AdminConnector = new AdminConnector($conn);

	$response['admins'] = $AdminConnector->selectAll();
	$response['success'] = true;
?>