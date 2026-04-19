<?php
session_start();
if(!isset($_SESSION['bank_id'])) {
    header("Location: ../auth/account.html");
    exit();
}
?>
