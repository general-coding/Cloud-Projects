<html>
<head>
<h2>Sell Sure</h2>
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
<?php
error_reporting(E_ALL);
ini_set('display_errors', 'On');
session_start();
echo "<form action='sellsure.php' method='get'>";
echo "<input type='hidden' name='logout' value='logout'>";
echo "<input type='submit' value='Logout'>";
echo "</form>";

echo "<form action='sellsure.php' method='get'>";
echo "<input type='text' name='search'>";
echo "<input type='submit' value='Search for items'>";
echo "</form>";
echo "<br><br>";
echo "<div>";
echo "<form action='sellsure.php' method='get'>";
echo "<input type='text' name='searchcat'>";
echo "<input type='submit' value='Search Via Category'>";
echo "</form>";
echo "</div>";
echo "<div style='border:1px solid'>";
echo "<form action='additem.php' method='post'>";
echo "<h2>Add items to your basket</h2>";
echo "<input type='submit' value='Add to basket'>";
echo "</form>";
echo "</div>";


require 'aws-autoloader.php';
use  Aws\DynamoDb\DynamoDbClient;
use Aws\DynamoDb\Enum\Type;
$client = DynamoDbClient::factory(array(
   'credentials' => array(
        'key'    => 'key',
        'secret' => 'secret',
    ),
         'region' => 'us-east-1'
));

if(isset($_GET['searchcat'])){
$searchcat = $_GET['searchcat'];

$response = $client->scan(array(
        'TableName' => 'cloud4',
        'ProjectionExpression' => 'itemname,itemid,category,image,itemdesc,userid',
        'ExpressionAttributeValues' =>  array (
            ':a1' => array('S' => $searchcat )) ,
        'FilterExpression' => 'category = :a1' ,
));

echo "<h2>Search Results via category</h2>";
foreach($response['Items'] as $key=>$value){
	if(@$value['userid']['S']!=$_SESSION['username']){
	echo "<div style='border:1px solid'>";
//	echo '<label>Item Name: '.@$value['itemname']['S'].'</label></br>';
	echo '<label>Item Description: '.@$value['itemdesc']['S'].'</label></br>';
//	echo '<label>Item Id: '.@$value['itemid']['S'].'</label></br>';
//	echo '<label>Category: '.@$value['category']['S'].'</label></br>';
	echo '<label>User Id: '.@$value['userid']['S'].'</label></br>';
	echo '<label><img src="https://s3.amazonaws.com/puneethbharadwajcloudprj/'.@$value['image']['S'].'" height="150" width="150"></label></br>';
	echo '</div>';
}
}

}

if(isset($_GET['search'])){

$search = $_GET['search'];

$response = $client->scan(array(
        'TableName' => 'cloud4',
        'ProjectionExpression' => 'itemname,itemid,category,image,itemdesc,userid',
        'ExpressionAttributeValues' =>  array (
            ':a1' => array('S' => $search )) ,
        'FilterExpression' => 'itemname = :a1' ,
));


foreach($response['Items'] as $key=>$value){
	if(@$value['userid']['S']!=$_SESSION['username']){
	echo "<div style='border:1px solid'>";
	echo '<label>Item Name: '.@$value['itemname']['S'].'</label></br>';
	echo '<label>Item Description: '.@$value['itemdesc']['S'].'</label></br>';
	echo '<label>Item Id: '.@$value['itemid']['S'].'</label></br>';
	echo '<label>Category: '.@$value['category']['S'].'</label></br>';
	echo '<label>User Id: '.@$value['userid']['S'].'</label></br>';
	echo '<label><img src="https://s3.amazonaws.com/bucket/'.@$value['image']['S'].'" height="150" width="150"></label></br>';
	echo '</div>';
}
}
}

$userid = @$_SESSION['username'];

$response = $client->scan(array(
        'TableName' => 'cloud4',
        'ProjectionExpression' => 'itemname,itemid,category,image,itemdesc,userid',
        'ExpressionAttributeValues' =>  array (
            ':a1' => array('S' => $userid )) ,
        'FilterExpression' => 'userid = :a1' ,
));

//print_r($response);
foreach($response['Items'] as $key=>$value){
	$a = "chk".($count + 1);
	echo "<div style='border:1px solid'>";
	echo "<form action='sellsure.php' method='get'>";
	echo '<label>Item Name: '.@$value['itemname']['S'].'</label></br>';
	echo '<label for="'.@$a.'">Item Description: '.@$value['itemdesc']['S'].'</label></br>';
	echo '<label>Item Id: '.@$value['itemid']['S'].'</label></br>';
	echo '<label>Category: '.@$value['category']['S'].'</label></br>';
	echo '<label>User Id: '.@$value['userid']['S'].'</label></br>';
	echo '<label><img id=\'imgvis\' src="https://s3.amazonaws.com/bucket/'.@$value['image']['S'].'" style="visibility:hidden"/></br>';
	echo '<input type="checkbox" id="'.@$a.'" onChange="toggleVisibility(\'imgvis\');" /><br/>';
	echo '<input type="hidden" name="delete" value="'.@$value['itemid']['S'].'">';
	echo '</br><label><input type="submit" name="deleteitem" value="Delete the Item"></label>';
	echo '</form>';
	echo '</div>';
	$count++;
}

if(isset($_GET['deleteitem'])){

$delete = @$_GET['delete'];

$scan = $client->getIterator('scan',array('TableName' => 'cloud4'));
foreach($scan as $item){
	$client->deleteItem(array(
	'TableName' => 'cloud4',
	'Key' => array(
	'itemid' => array('S' => $delete)
	)
));
}
header('location:sellsure.php');
}

if(isset($_GET['logout'])){
  session_destroy();
  echo "session destroyed";
  header("location:login.php");
 }


?>
</body>
</html>
