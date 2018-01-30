<?php
	require_once 'utils/database.php';
	require_once 'connectors/GroupConnector.php';

	$id = $_GET['id'];

	$GroupConnector = new GroupConnector($conn);

	$response['group'] = $GroupConnector->select($id);
	$response['success'] = true;
?>