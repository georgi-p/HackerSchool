<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
</head>
<body>

<!-- Create the search form -->
<form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">
	<fieldset>
	<input type="text" name="selishte" value="" placeholder="Search&hellip;" maxlength="70" required="required" />
	<button type="submit">Search</button>
	</fieldset>
</form>

<br>

<div id="result">

<?php

$servername = "localhost";
$username = "root";
$password = "password";
$dbname = "ekattedb";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Adjust the charset
$result = $conn->query("SET NAMES UTF8");

// If there is a word to search for, do the search
if (isset($_POST['selishte'])) {


$selishte = $_POST['selishte'];
echo "Резултати от търсене на \"".$selishte."\": ";
echo "<br>"; echo "<br>";

// Send the query to the database, use pattern matching
$sql = "SELECT t_v_m, name, kmetstvo, obstina FROM selishta WHERE name LIKE \"%".$selishte."%\"";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {

		// Get information from the query result
		$selishte_t_v_m = $row["t_v_m"];
		$selishte_name = $row["name"];
		$kmetstvo = $row["kmetstvo"];
		$obstina = $row["obstina"];

		$sql = "SELECT name, oblast FROM obstini WHERE obstina=\"".$obstina."\"";
		$pair = $conn->query($sql)->fetch_assoc();
		$obstina_name = $pair["name"];
		$oblast = $pair["oblast"];

		$sql = "SELECT name, region FROM oblasti WHERE oblast=\"".$oblast."\"";

		$pair = $conn->query($sql)->fetch_assoc();
		$oblast_name = $pair["name"];
		$region = $pair["region"];

		$sql = "SELECT name FROM regioni WHERE region=\"".$region."\"";
		$pair = $conn->query($sql)->fetch_assoc();
		$region_name = $pair["name"];

		if ($kmetstvo == NULL) {
			echo $selishte_t_v_m." ".$selishte_name.", община ".$obstina_name.", област ".$oblast_name.", регион ".$region_name."<br>";
		}
		else {
			$sql = "SELECT name FROM kmetstva WHERE kmetstvo=\"".$kmetstvo."\"";
			$pair = $conn->query($sql)->fetch_assoc();
			$kmetstvo_name = $pair["name"];
			echo $selishte_t_v_m." ".$selishte_name.", кметство ".$kmetstvo_name.", община ".$obstina_name.", област ".$oblast_name.", регион ".$region_name."<br>";
		}
	}
}

}

// Close the connection
$conn->close();
?>

</div>

</body>
</html>
