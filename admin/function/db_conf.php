<?php
$dbServername = "192.168.1.111";
$dbUsername = "root";
$dbPassword = "1";
$dbName = "stockdata";
$conn = new mysqli($dbServername, $dbUsername, $dbPassword , $dbName);
mysqli_set_charset($conn,"utf8");
?>