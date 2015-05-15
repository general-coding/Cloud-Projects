<html>
<head>
<h2>Sell Sure</h2>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="bootstrap.min.css" type="text/css">

<!-- Optional theme -->
<link rel="stylesheet" href="bootstrap-theme.min.css" type="text/css">

<!-- Latest compiled and minified JavaScript -->
<script src="bootstrap.min.js">
	
</script>
<script>
  function toggleVisibility(id) {
   var el = document.getElementById(id);

   if (el.style.visibility=="visible") {
          el.style.visibility="hidden";
     }
     else {
          el.style.visibility="visible";
     }
 }
</script>
</head>
<body>

	<div class='container'>
		<div class="row">
			<div class="col-sm-6 col-md-4 col-md-offset-4">
				<form class="form-signin" action='sellsure.php' method='get'>
					<input type='hidden' name='logout' value='logout'> <input
						type='submit' value='Logout'>
				</form>
			</div>
		</div>
	</div>

	<div class='container'>
		<div class="row">
			<div class="col-sm-6 col-md-4 col-md-offset-4">
				<form class="form-signin" action='sellsure.php' method='get'>
					<input type='text' name='search'> <input type='submit'
						value='Search for items'>
				</form>
			</div>
		</div>
	</div>

	<div class='container'>
		<div class="row">
			<div class="col-sm-6 col-md-4 col-md-offset-4">
				<form class="form-signin" action='sellsure.php' method='get'>
					<input type='text' name='searchcat'> <input type='submit'
						value='Search Via Category'>
				</form>
			</div>
		</div>
	</div>

	<div class='container'>
		<div class="row">
			<div class="col-sm-6 col-md-4 col-md-offset-4">
				<form class="form-signin" action='additem.php' method='post'>
					<h2>Add items to your basket</h2>
					<input type='submit' value='Add to basket'>
				</form>
			</div>
		</div>
	</div>
<?php
error_reporting ( E_ALL );
ini_set ( 'display_errors', 'On' );
session_start ();

require 'aws-autoloader.php';
use Aws\DynamoDb\DynamoDbClient;
use Aws\DynamoDb\Enum\Type;
$client = DynamoDbClient::factory ( array (
		'credentials' => array (
				'key' => 'awskey',
				'secret' => 'awssecret' 
		),
		'region' => 'us-east-1' 
) );

if (isset ( $_GET ['searchcat'] )) {
	$searchcat = $_GET ['searchcat'];
	
	$response = $client->scan ( array (
			'TableName' => 'cloud4',
			'ProjectionExpression' => 'itemname,itemid,category,image,itemdesc,userid',
			'ExpressionAttributeValues' => array (
					':a1' => array (
							'S' => $searchcat 
					) 
			),
			'FilterExpression' => 'category = :a1' 
	) );
	
	echo "<h2>Search Results via category</h2>";
	foreach ( $response ['Items'] as $key => $value ) {
		if (@$value ['userid'] ['S'] != $_SESSION ['username']) {
			echo "<div style='border:1px solid'>";
			// echo '<label>Item Name: '.@$value['itemname']['S'].'</label></br>';
			echo '<label>Item Description: ' . @$value ['itemdesc'] ['S'] . '</label></br>';
			// echo '<label>Item Id: '.@$value['itemid']['S'].'</label></br>';
			// echo '<label>Category: '.@$value['category']['S'].'</label></br>';
			echo '<label>User Id: ' . @$value ['userid'] ['S'] . '</label></br>';
			echo '<label><img src="https://s3.amazonaws.com/s3bucket/' . @$value ['image'] ['S'] . '" height="150" width="150"></label></br>';
			echo '</div>';
		}
	}
}

if (isset ( $_GET ['search'] )) {
	
	$search = $_GET ['search'];
	
	$response = $client->scan ( array (
			'TableName' => 'cloud4',
			'ProjectionExpression' => 'itemname,itemid,category,image,itemdesc,userid',
			'ExpressionAttributeValues' => array (
					':a1' => array (
							'S' => $search 
					) 
			),
			'FilterExpression' => 'itemname = :a1' 
	) );
	
	foreach ( $response ['Items'] as $key => $value ) {
		if (@$value ['userid'] ['S'] != $_SESSION ['username']) {
			echo "<div style='border:1px solid'>";
			echo '<label>Item Name: ' . @$value ['itemname'] ['S'] . '</label></br>';
			echo '<label>Item Description: ' . @$value ['itemdesc'] ['S'] . '</label></br>';
			echo '<label>Item Id: ' . @$value ['itemid'] ['S'] . '</label></br>';
			echo '<label>Category: ' . @$value ['category'] ['S'] . '</label></br>';
			echo '<label>User Id: ' . @$value ['userid'] ['S'] . '</label></br>';
			echo '<label><img src="https://s3.amazonaws.com/s3bucket/' . @$value ['image'] ['S'] . '" height="150" width="150"></label></br>';
			echo '</div>';
		}
	}
}

$userid = @$_SESSION ['username'];

$response = $client->scan ( array (
		'TableName' => 'cloud4',
		'ProjectionExpression' => 'itemname,itemid,category,image,itemdesc,userid',
		'ExpressionAttributeValues' => array (
				':a1' => array (
						'S' => $userid 
				) 
		),
		'FilterExpression' => 'userid = :a1' 
) );

foreach ( $response ['Items'] as $key => $value ) {
	echo "<div style='border:1px solid'>";
	echo "<form action='sellsure.php' method='get'>";
	echo '<label>Item Name: ' . @$value ['itemname'] ['S'] . '</label></br>';
	echo '<label for="' . @$a . '">Item Description: ' . @$value ['itemdesc'] ['S'] . '</label></br>';
	echo '<label>Item Id: ' . @$value ['itemid'] ['S'] . '</label></br>';
	echo '<label>Category: ' . @$value ['category'] ['S'] . '</label></br>';
	echo '<label>User Id: ' . @$value ['userid'] ['S'] . '</label></br>';
	echo '<label><img id=\'imgvis\' src="https://s3.amazonaws.com/s3bucket/' . @$value ['image'] ['S'] . '" style="visibility:hidden"/></br>';
	//echo '<input type="checkbox" id="' . @$a . '" onChange="toggleVisibility(\'imgvis\');" /><br/>';
	echo '<input type="hidden" name="delete" value="' . @$value ['itemid'] ['S'] . '">';
	echo '</br><label><input type="submit" name="deleteitem" value="Delete the Item"></label>';
	echo '</form>';
	echo '</div>';
}

if (isset ( $_GET ['deleteitem'] )) {
	
	$delete = @$_GET ['delete'];
	
	$scan = $client->getIterator ( 'scan', array (
			'TableName' => 'cloud4' 
	) );
	foreach ( $scan as $item ) {
		$client->deleteItem ( array (
				'TableName' => 'cloud4',
				'Key' => array (
						'itemid' => array (
								'S' => $delete 
						) 
				) 
		) );
	}
	header ( 'location:sellsure.php' );
}

if (isset ( $_GET ['logout'] )) {
	session_destroy ();
	echo "session destroyed";
	header ( "location:index.php" );
}

?>
</body>
</html>
