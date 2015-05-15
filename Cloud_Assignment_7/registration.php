<html>
<head>
<h2>Registration Page</h2>

<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="bootstrap.min.css" type="text/css">

<!-- Optional theme -->
<link rel="stylesheet" href="bootstrap-theme.min.css" type="text/css">

<!-- Latest compiled and minified JavaScript -->
<script src="bootstrap.min.js">
	
</script>
</head>
<body>
	<div class='container'>
		<div class="row">
			<div class="col-sm-6 col-md-4 col-md-offset-4">
				<form class="form-signin" action='registration.php' method='post'>
					<label>Username : <input type='text' name='username'></label> <br>
					<label>Password : <input type='password' name='password'>
					</label> <br> <label>Fullname : <input type='text' name='fullname'></label>
					<br> <label>Email ID : <input type='text' name='emailid'></label> <br>
					<input type='submit' value='Register'> <input type='reset'
						value='Reset'>
				</form>
			</div>
		</div>
	</div>

<?php
session_start ();
if (isset ( $_POST ['username'] ) && isset ( $_POST ['password'] ) && isset ( $_POST ['fullname'] ) && isset ( $_POST ['emailid'] )) {
	$username = $_POST ['username'];
	$password = $_POST ['password'];
	$fullname = $_POST ['fullname'];
	$emailid = $_POST ['emailid'];
	try {
		$dbh = new PDO ( "mysql:host=rdsendpoint;dbname=dbname", "username", "password", array (
				PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION 
		) );
		$dbh->exec ( 'insert into users values("' . $username . '","' . $password . '","' . $fullname . '","' . $emailid . '")' );
		header ( "location:index.php" );
		echo $username;
		echo $password;
		echo "Inserted into DB";
	} catch ( PDOException $e ) {
		print "Error:! " . $e->getMessage () . "</br>";
		if ($e->getCode () == 23000) {
			echo "<br>";
			echo "<br>";
			echo "User Name already exists. Please try another one";
		}
		die ();
	}
}
?>
</body>
</html>
