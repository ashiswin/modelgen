<?php
	require_once 'utils/database.php';
	require_once 'connectors/GroupConnector.php';

	$id = $_POST['id'];

	$GroupConnector = new GroupConnector($conn);

	$response['group'] = $GroupConnector->delete($id);
	$response['success'] = true;
?>