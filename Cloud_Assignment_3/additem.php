html>
<head>
<h2>Add items to your basket</h2>
</head>
<body>
<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors','On');
$userid = @$_SESSION['username'];
echo "<form method='post' action='additem.php' enctype='multipart/form-data'>";
echo "<label>Item Name       : <input type='text' name='itemname'></label><br>";
echo "<label>Item Description: <input type='text' name='itemdesc'></label><br>";
echo "<label>Category :";
echo "<select name='category'>";
echo "<optgroup label='Electronic Appliances'>";
echo "<option value='mobile'>Mobile</option>";
echo "<option value='laptops'>Laptops</option>";
echo "<option value='camera'>Camera</option>";
echo "</optgroup>";
echo "<optgroup label='Automobiles'>";
echo "<option value='bike'>Bikes</option>";
echo "<option value='car'>Cars</option>";
echo "</optgroup>";
echo "<optgroup label='Study materails'>";
echo "<option value='books'>Books</option>";
echo "<option value='pdf materials'>PDF Materials</option>";
echo "</optgroup>";
echo "</select></label></br>";
echo "<label>Upload Image:</label>";
echo "<input type='file' name='image'><br>";
echo "<input type='submit' value='Add to basket'>";
echo "</form>";
echo "<form action='sellsure.php' method='post'>";
echo "<input type='submit' value='Go back to search page'>";
echo "</form>";

require 'aws-autoloader.php';
use Aws\DynamoDb\DynamoDbClient;
use Aws\Common\Enum\Region;
use Aws\DynamoDb\Enum\Type;
use Aws\S3\S3Client;
$client = DynamoDbClient::factory(array(
   'credentials' => array(
        'key'    => 'key',
        'secret' => 'secret'
    ),
         'region' => 'us-east-1'
));


if((isset($_POST['itemname']))&&(isset($_POST['itemdesc']))){

$category = @$_POST['category'];
$itemid = uniqid();
$itemname = $_POST['itemname'];
$itemdescription = $_POST['itemdesc'];
$image_name = @$_FILES['image']['name'];
$image_temp = @$_FILES['image']['tmp_name'];
$image_type = pathinfo($image_name,PATHINFO_EXTENSION);
$size = @$_FILES['image']['size'];

/*echo $userid;
echo "<br>";
echo $itemid;
echo "<br>";
echo $itemdescription;
echo "<br>";
echo $itemname;
echo "<br>";
echo $image_name;
echo "<br>";
echo "$category";
echo "<br>";
*/

if($size > 60000 || $size == 0){
echo $size, ",";
$errmsg = "Please provide file size between 1 and 60kb";
}

if((isset($errmsg))){
echo $errmsg;
}
else{
echo $size;
$response = $client->putItem(array(
                               "TableName" => 'cloud4',
		"Item" => (array(
				     "userid"=> array('S'=> "$userid"),
                     "itemid" => array('S' => "$itemid"),
				     "itemdesc" => array('S' => "$itemdescription"),
				     "itemname" => array('S' => "$itemname"),
				     "image" => array('S' => "$image_name"),
				     "category"=> array('S' => "$category")               
                              )
)
)
);

$bucket='bucket';
$s3 = S3Client::factory(array(
	'key'    => 'key',
    'secret' => 'secret',
	'region' => 'us-east-1'
	));

$result= $s3->upload(
	$bucket,
	$image_name,
	fopen($image_temp,'rb'),'public-read'
);
}}

?>
</body>
</html>
