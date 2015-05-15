html>
<head>
<h2>Add s to your basket</h2>

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
				<form class="form-signin" method='post' action='add.php'
					enctype='multipart/form-data'>
					<label> Name : <input type='text' name='name'></label><br>
					<label> Description: <input type='text' name='desc'>
					</label><br> <label>Category : <select name='category'>
							<optgroup label='Electronic Appliances'>
								<option value='mobile'>Mobile</option>
								<option value='laptops'>Laptops</option>
								<option value='camera'>Camera</option>
							</optgroup>
							<optgroup label='Automobiles'>
								<option value='bike'>Bikes</option>
								<option value='car'>Cars</option>
							</optgroup>
							<optgroup label='Study materails'>
								<option value='books'>Books</option>
								<option value='pdf materials'>PDF Materials</option>
							</optgroup>
					</select></label></br> <label>Upload Image:</label> <input
						type='file' name='image'><br> <input type='submit'
						value='Add to basket'>
				</form>
			</div>
		</div>
	</div>
	
<?php
session_start ();
error_reporting ( E_ALL );
ini_set ( 'display_errors', 'On' );
$userid = @$_SESSION ['username'];

require 'aws-autoloader.php';
use Aws\DynamoDb\DynamoDbClient;
use Aws\Common\Enum\Region;
use Aws\DynamoDb\Enum\Type;
use Aws\S3\S3Client;
$client = DynamoDbClient::factory ( array (
		'credentials' => array (
				'key' => 'awskey',
				'secret' => 'awssecret' 
		),
		'region' => 'us-east-1' 
) );

if ((isset ( $_POST ['name'] )) && (isset ( $_POST ['desc'] ))) {
	
	$category = @$_POST ['category'];
	$id = uniqid ();
	$name = $_POST ['name'];
	$description = $_POST ['desc'];
	$name = @$_FILES ['image'] ['name'];
	$temp = @$_FILES ['image'] ['tmp_name'];
	$type = pathinfo ( $name, PATHINFO_EXTENSION );
	$size = @$_FILES ['image'] ['size'];
		
	if ($size > 20000 || $size == 0) {
		echo $size, ",";
		$errmsg = "Please provide file size between 1 and 20kb";
	}
	
	if ((isset ( $errmsg ))) {
		echo $errmsg;
	} else {
		echo $size;
		$response = $client->put ( array (
				"TableName" => 'cloud4',
				"" => (array (
						"userid" => array (
								'S' => "$userid" 
						),
						"id" => array (
								'S' => "$id" 
						),
						"desc" => array (
								'S' => "$description" 
						),
						"name" => array (
								'S' => "$name" 
						),
						"image" => array (
								'S' => "$name" 
						),
						"category" => array (
								'S' => "$category" 
						) 
				)) 
		) );
		
		$bucket = 's3bucket';
		$s3 = S3Client::factory ( array (
				'key' => 'awskey',
				'secret' => 'awssecret',
				'region' => 'us-east-1' 
		) );
		
		$result = $s3->upload ( $bucket, $name, fopen ( $temp, 'rb' ), 'public-read' );
	}
}

?>
</body>
</html>
