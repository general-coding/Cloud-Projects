<html>
<head><title>Message Board</title></head>
<body>
<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors','On');

echo "<div style='width:400px; margin-right:auto; margin-left:auto; border:1px solid #000; font-family:Lucida Console; font-size:20px'>";
echo "<form action='login.php' method='post'>
<label>UserName : <input type='text' name='username'></label>
<br>
<label>Password : <input type='password' name='password'></label>
<br>
<input type='submit' value='Login'>
<input type='reset' value='Reset'>";
echo "</form>";

if(isset($_SESSION)&&isset($_SESSION['username'])&&isset($_SESSION['password'])){
$username=$_SESSION['username'];
$password=$_SESSION['password'];
try {
  $dbh = new PDO("mysql:host=localhost;dbname=cloud4","root","root",array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
  $dbh->beginTransaction();
  $stmt = $dbh->prepare("select * from users where username= :name and password= :password") or die(print_r($db->errorInfo(), true));;
  $stmt->bindParam(':name',$username);
  $stmt->bindParam(':password',$password);
  $stmt->execute();
  if($stmt->fetch()){
  header("location:sellsure.php");
  }else{
  echo "Wrong password or Username.Please verify your username and password!!";
 }
} catch (PDOException $e) {
  print "Error!: " . $e->getMessage() . "<br/>";
  die();
}

}else{

if(isset($_POST['username'])&&isset($_POST['password'])){
$username=$_POST['username'];
$password=md5($_POST['password']);
try {
  $dbh = new PDO("mysql:host=localhost;dbname=cloud4","root","root",array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
  $dbh->beginTransaction();
  $stmt = $dbh->prepare("select * from users where username= :name and password= :password") or die(print_r($db->errorInfo(), true));
  $stmt->bindParam(':name',$username);
  $stmt->bindParam(':password',$password);
  #$stmt->debugDumpParams();
  $stmt->execute();
  if($stmt->fetch()){
  $_SESSION['username']=$username;
  $_SESSION['password']=$password;
  header("location:sellsure.php");
  }else{
  echo "Wrong password or Username.Please verify your username and password!!";
 }
} catch (PDOException $e) {
  print "Error!: " . $e->getMessage() . "<br/>";
  die();
}
}
}

echo "<form action='registration.php' method='post'>";
echo "<input type='submit' value='New users must register here'>";
echo "</form>";
echo "</div>";
?>
</body>
</html>
