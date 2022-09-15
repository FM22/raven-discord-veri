<html lang="en-UK">
<head>
	<title>Part III Verification</title>

	<link rel="stylesheet" href="../css/2021jan23.css">
</head>
<body>
<h1 style="text-align: center;">Part III Discord Verification</h1>
<?php
if ($db = pg_connect("dbname=dra user=dra connect_timeout=5")) {
	//Check if there is an account associated to the given crsID
	$crsid =  $_SERVER['AAPRINCIPAL'];
	$query = "SELECT userid FROM partIII.members WHERE crsid='$crsid'";
	$results = pg_query($db, $query);
	
	if ($row = pg_fetch_row($results)) {
		echo "Account $row[0] already associated with crsid $crsid. If you want to manually verify a second account, please contact your server admins.";
	}
	elseif (pg_last_error($db)) {
		echo "Database error checking against crsID.";
	}
	
	else {
		//Check for verification ID in the database
		$id = $_GET['id'];
		if (ctype_digit($id)) { //Excludes empty string, and checks for numeric strings to prevent code injection
			$query = "SELECT userid FROM partIII.members WHERE verifyd = '$id'";
			$results = pg_query($db, $query);
		
			if ($user = pg_fetch_row($results)) { //Set user to verified in the database
				$query = "UPDATE partIII.members SET verified = true, verifyd = '', manualverif = false, crsid = '$crsid' WHERE userid = '$user[0]'";
				if (pg_query($db, $query)) {
					echo "You have been successfully verified.";
					shell_exec("curl -G '131.111.179.83:8080' -d userid='$user[0]'");
				}
				else {
					echo "Database error";
				}
			}
			else {
				echo "No users found with verification ID $id; please check you have copied the link correctly.<br>If you just successfully verified and refreshed, you need not worry.";
			}
		}
		
		else {
			echo "Invalid user ID format; please check you have copied the link correctly.";
		}
	}
	
}
else {
	echo "Failed to connect to verification database. Please try again later.";
	echo pg_last_error($db);
}
?>
</body>
</html>
