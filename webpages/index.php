<html lang="en-UK">
<head>
	<title>Part III Verification</title>

	<link rel="stylesheet" href="../css/2021jan23.css">
</head>
<body>
<h1 style="text-align: center;">Part III Discord Verification</h1>
<?php
$id = $_GET['id'];
if (ctype_digit($id)) { //Excludes empty string
	if ($db = pg_connect("dbname=dra")) {
		$query = "SELECT userid FROM partIII.members WHERE verifyd = '$id'";
		$results = pg_query($db, $query);
		
		if ($user = pg_fetch_row($results)) {
			$query = "UPDATE partIII.members SET verified = true, verifyd = '', manualverif = false WHERE userid = '$user[0]'";
			pg_query($db, $query);
			
			echo "You have been successfully verified.";
		}
		else {
			echo "No users found with verification ID $id; please check you have copied the link correctly.<br>If you just successfully verified and refreshed, you need not worry.";
		}
	}
	else {
		echo "Failed to connect to verification database. Please try again later.";
	}
	
}
else {
	echo "Invalid user ID format; please check you have copied the link correctly.";
}
?>

</body>
</html>
