<html>
<head>
<title>Message Board</title>

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
				<form class="form-signin" action='index.php' method='post'>
					<label>UserName : <input type='text' name='username'></label> <br>
					<label>Password : <input type='password' name='password'></label> <br>
					<input type='submit' value='Login'> <input type='reset'
						value='Reset'>
				</form>
			</div>
		</div>
	</div>
				
<?php
session_start ();
error_reporting ( E_ALL );
ini_set ( 'display_errors', 'On' );

if (isset ( $_SESSION ) && isset ( $_SESSION ['username'] ) && isset ( $_SESSION ['password'] )) {
	$username = $_SESSION ['username'];
	$password = $_SESSION ['password'];
	try {
		$dbh = new PDO ( "mysql:host=rdsendpoint;dbname=dbname", "username", "password", array (
				PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION 
		) );
		$dbh->beginTransaction ();
		$stmt = $dbh->prepare ( "select * from users where username= :name and password= :password" ) or die ( print_r ( $db->errorInfo (), true ) );
		;
		$stmt->bindParam ( ':name', $username );
		$stmt->bindParam ( ':password', $password );
		$stmt->execute ();
		if ($stmt->fetch ()) {
			header ( "location:sellsure.php" );
		} else {
			echo "Wrong password or Username.Please verify your username and password!!";
		}
	} catch ( PDOException $e ) {
		print "Error!: " . $e->getMessage () . "<br/>";
		die ();
	}
} else {
	
	if (isset ( $_POST ['username'] ) && isset ( $_POST ['password'] )) {
		$username = $_POST ['username'];
		$password = $_POST ['password'];
		try {
			$dbh = new PDO ( "mysql:host=rdsendpoint;dbname=dbname", "username", "password", array (
					PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION 
			) );
			$dbh->beginTransaction ();
			$stmt = $dbh->prepare ( "select * from users where username= :name and password= :password" ) or die ( print_r ( $db->errorInfo (), true ) );
			$stmt->bindParam ( ':name', $username );
			$stmt->bindParam ( ':password', $password );
			// $stmt->debugDumpParams();
			$stmt->execute ();
			if ($stmt->fetch ()) {
				$_SESSION ['username'] = $username;
				$_SESSION ['password'] = $password;
				echo $username;
				echo $password;
				header ( "location:sellsure.php" );
			} else {
				echo "Wrong password or Username.Please verify your username and password!!";
			}
		} catch ( PDOException $e ) {
			print "Error!: " . $e->getMessage () . "<br/>";
			die ();
		}
	}
}
?>
<div class='container'>
	<div class="row">
		<div class="col-sm-6 col-md-4 col-md-offset-4">
			<form action='registration.php' method='post'>
				<input type='submit' value='New users must register here'>
			</form>
		</div>
	</div>
</div>

</body>
</html>
