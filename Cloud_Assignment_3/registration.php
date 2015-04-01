<html>
<head>
<h2>Registration Page</h2>
</head>
<body>
<?php
session_start();
echo "<form action='registration.php' method='post'>
<label>Username : <input type='text' name='username'></label>
<br>
<label>Password : <input type='password' name='password'></label>
<br>
<label>Fullname : <input type='text' name='fullname'></label>
<br>
<label>Email ID : <input type='text' name='emailid'></label>
<br>
<input type='submit' value='Register'>
<input type='reset' value='Reset'>";

if(isset($_POST['username'])&&isset($_POST['password'])&&isset($_POST['fullname'])&&isset($_POST['emailid'])){
$username= $_POST['username'];
$password= $_POST['password'];
$fullname= $_POST['fullname'];
$emailid =$_POST['emailid'];
try{
$dbh = new PDO("mysql:host=localhost;dbname=cloud4","root","root",array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
$dbh->exec('insert into users values("'.$username.'","' . md5("$password") . '","'.$fullname.'","'.$emailid.'")');
header("location:login.php");
echo "Inserted into DB";
}catch(PDOException $e){
print "Error:! ".$e->getMessage()."</br>";
if($e->getCode()==23000){
    echo "<br>";
    echo "<br>";
    echo "User Name already exists. Please try another one";
}
die();
}
}
?>
</body>
</html>
