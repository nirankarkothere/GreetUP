<?php
session_start();
include 'db_connect.php';

if(isset($_POST['login'])) {

    $email = trim($_POST['email']);
    $password = $_POST['password'];

    $stmt = $conn->prepare("SELECT bank_id, username, password FROM users WHERE email=?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->store_result();

    if($stmt->num_rows == 1) {
        $stmt->bind_result($bank_id, $username, $hash);
        $stmt->fetch();

        if(password_verify($password, $hash)) {
            $_SESSION['bank_id'] = $bank_id;
            $_SESSION['username'] = $username;
            header("Location: ../usr/index.html");
            exit();
        } else {
            echo "<script>alert('Wrong password');history.back();</script>";
        }
    } else {
        echo "<script>alert('Account not found');history.back();</script>";
    }
}
?>
