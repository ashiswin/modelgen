<?php
	require_once 'utils/database.php';
	require_once 'connectors/VoterConnector.php';

	$id = $_POST['id'];

	$VoterConnector = new VoterConnector($conn);

	$response['voter'] = $VoterConnector->delete($id);
	$response['success'] = true;
?>