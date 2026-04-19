<?php
include 'db_connect.php';
include 'bank_id_generator.php';

if(isset($_POST['signup'])) {
    $username = $conn->real_escape_string($_POST['username']);
    $email = $conn->real_escape_string($_POST['email']);
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

    $bank_id = generateBankID($conn);

    $sql = "INSERT INTO users (bank_id, username, email, password)
            VALUES ('$bank_id', '$username', '$email', '$password')";

    if($conn->query($sql) === TRUE) {
        echo "<script>alert('Signup successful! Your Bank ID: $bank_id'); window.location.href='../auth/account.html';</script>";
    } else {
        echo "<script>alert('Error: ".$conn->error."'); window.history.back();</script>";
    }
}
$conn->close();
?>
