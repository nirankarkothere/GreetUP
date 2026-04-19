<?php
session_start();
include '../php/db_connect.php';

$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

$stmt = $conn->prepare("SELECT admin_id, password FROM admins WHERE username=?");
$stmt->bind_param("s", $username);
$stmt->execute();
$result = $stmt->get_result();

if($result->num_rows === 1){
    $row = $result->fetch_assoc();
    if(password_verify($password, $row['password'])){
        $_SESSION['admin_id'] = $row['admin_id'];
        header("Location: admin_dashboard.php");
        exit;
    }
}

echo "❌ Invalid Admin Credentials";
