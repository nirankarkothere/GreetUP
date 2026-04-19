<?php
include 'db_connect.php';

$username = 'admin';
$password = password_hash('admin', PASSWORD_DEFAULT);

$stmt = $conn->prepare("INSERT INTO admins (username,password) VALUES (?,?)");
$stmt->bind_param("ss",$username,$password);
$stmt->execute();

echo "✅ Admin created successfully";
?>