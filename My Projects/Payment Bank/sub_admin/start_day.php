<?php
session_start();
include '../php/db_connect.php';

$sid = $_SESSION['subadmin_id'];
$cash = $_POST['cash'];
$today = date('Y-m-d');

$stmt = $conn->prepare(
 "INSERT INTO daily_cash (subadmin_id, cash_date, opening_cash, closing_cash)
  VALUES (?,?,?,?)"
);
$stmt->bind_param("isdd", $sid, $today, $cash, $cash);
$stmt->execute();

header("Location: dashboard.php");

?>