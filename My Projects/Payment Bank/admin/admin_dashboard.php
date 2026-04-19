<?php
session_start();
include '../php/db_connect.php';

if(!isset($_SESSION['admin_id'])){
    header("Location: login.html");
    exit;
}

/* DATA */
$totalUsers = $conn->query("SELECT COUNT(*) c FROM user_profile")->fetch_assoc()['c'];
$totalSubAdmins = $conn->query("SELECT COUNT(*) c FROM sub_admins")->fetch_assoc()['c'];
$totalBalance = $conn->query("SELECT IFNULL(SUM(balance),0) s FROM user_balance")->fetch_assoc()['s'];
$totalTransactions = $conn->query("SELECT COUNT(*) c FROM transactions")->fetch_assoc()['c'];
?>
<!DOCTYPE html>
<html>
<head>
<title>Admin Dashboard</title>
<style>
body{
    margin:0;
    font-family:Arial;
    background:#f4f6fb;
}
.header{
    background:#1d2671;
    color:#fff;
    padding:20px;
    text-align:center;
}
.dashboard{
    padding:30px;
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:20px;
}
.card{
    background:#fff;
    padding:25px;
    border-radius:16px;
    box-shadow:0 10px 25px rgba(0,0,0,0.1);
}
.card h3{
    margin:0;
    color:#555;
}
.card p{
    font-size:28px;
    margin:10px 0 0;
    font-weight:bold;
}
.nav{
    margin:20px;
    display:flex;
    gap:15px;
}
.nav a{
    padding:10px 16px;
    background:#1d7af3;
    color:#fff;
    text-decoration:none;
    border-radius:8px;
}
</style>
</head>
<body>

<div class="header">
    <h1>🏦 Admin Dashboard</h1>
</div>

<div class="dashboard">
    <div class="card"><h3>Total Users</h3><p><?= $totalUsers ?></p></div>
    <div class="card"><h3>Sub Admins</h3><p><?= $totalSubAdmins ?></p></div>
    <div class="card"><h3>Total Bank Balance</h3><p>₹<?= number_format($totalBalance,2) ?></p></div>
    <div class="card"><h3>Total Transactions</h3><p><?= $totalTransactions ?></p></div>
</div>

<div class="nav">
    <a href="add_subadmin.php">Manage Sub-Admins</a>
    <a href="reports.php">Reports</a>
    <a href="logout.php">Logout</a>
</div>

</body>
</html>
