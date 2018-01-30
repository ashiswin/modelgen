<?php
	require_once 'utils/database.php';
	require_once 'connectors/VoterConnector.php';

	$id = $_GET['id'];

	$VoterConnector = new VoterConnector($conn);

	$response['voter'] = $VoterConnector->select($id);
	$response['success'] = true;
?>