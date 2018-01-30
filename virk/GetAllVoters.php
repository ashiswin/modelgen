<?php
	require_once 'utils/database.php';
	require_once 'connectors/VoterConnector.php';

	$id = $_GET['id'];

	$VoterConnector = new VoterConnector($conn);

	$response['voters'] = $VoterConnector->selectAll();
	$response['success'] = true;
?>