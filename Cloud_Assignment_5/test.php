<html>
<body>
<div style='width:400px; margin-right:auto; margin-left:auto; border:1px solid'>
<p>
<form method="post" action="test.php" enctype="multipart/form-data">
<br><br> 
   File to Display:<input type='file' name='infile'>
<br><br> 
   Numbe of Clusters:<input type='text' name='cluster'>
<br><br> 
	<input type='submit' value='Visualize'>
   </p>
</form>
<?php
error_reporting(E_ALL);
if((isset($_POST["cluster"]))){
	$file_name = @$_FILES['infile']['name'];
	$file_temp = @$_FILES['infile']['tmp_name'];
	$file_path = $file_temp.'/'.$file_name;
	$file_type = pathinfo($file_name,PATHINFO_EXTENSION);
	$target_dir = "/var/www/html/";
	#$target_file = $target_dir . basename($_FILES['infile']['name']);
	$target_file = $target_dir . "input.arff";	
	$wekaout_file = $target_dir . "wekaout.csv";
	#$out = shell_exec("bash /var/www/html/new.sh");
	#echo $out;
	echo $_POST["cluster"];
	$cluster = $_POST["cluster"];
	//move_uploaded_file($file_path,$target_file);
	if(move_uploaded_file($file_temp,$target_file)){
		echo "The file ". basename( $_FILES["infile"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
	if($file_type == "csv"){
		$out = shell_exec("javac -cp /var/www/html/weka.jar /var/www/html/weka.java");
		$out = shell_exec("java -cp .:/var/www/html/weka.jar weka ".$target_file." "."/var/www/html/input.arff");
	}
	chmod($target_file,0777);
	echo "<br><br>";
	#echo "out".$out;
	echo "<br><br>";
	echo $str;
	$out = shell_exec("javac -cp /var/www/html/weka.jar /var/www/html/wekatest.java");
	$out = shell_exec("java -cp .:/var/www/html/weka.jar wekatest /var/www/html/input.arff ".$cluster);
	chmod($wekaout_file,0777);
	header("Location:scatterplot.php");
}
else {echo "nope";}
?>

</body>
</html>
