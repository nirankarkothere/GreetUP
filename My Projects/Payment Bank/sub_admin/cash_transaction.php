<?php
session_start();
include '../php/db_connect.php';

$sid = $_SESSION['subadmin_id'];
$uid = $_POST['bank_id'];
$type = $_POST['type'];
$amt  = $_POST['amount'];
$reason = $_POST['reason'];

$conn->begin_transaction();

/* Get user balance */
$q = $conn->prepare(
 "SELECT balance FROM user_balance WHERE bank_id=? FOR UPDATE"
);
$q->bind_param("i", $uid);
$q->execute();
$q->bind_result($bal);
$q->fetch();
$q->close();

/* Debit check */
if ($type=='debit' && $bal < $amt) {
    $conn->rollback();
    die("Insufficient user balance");
}

/* Update user balance */
$newBal = ($type=='credit') ? $bal+$amt : $bal-$amt;

$u = $conn->prepare(
 "UPDATE user_balance SET balance=? WHERE bank_id=?"
);
$u->bind_param("di", $newBal, $uid);
$u->execute();

/* Insert user transaction */
$t = $conn->prepare(
 "INSERT INTO transactions
 (bank_id,type,amount,balance_after,description)
 VALUES (?,?,?,?,?)"
);
$t->bind_param("isdds", $uid, $type, $amt, $newBal, $reason);
$t->execute();

/* Insert bank ledger */
$b = $conn->prepare(
 "INSERT INTO bank_daily_transactions
 (subadmin_id,user_bank_id,type,amount,reason)
 VALUES (?,?,?,?,?)"
);
$b->bind_param("iids", $sid, $uid, $type, $amt, $reason);
$b->execute();

/* Update cash */
$c = $conn->prepare(
 "UPDATE daily_cash
 SET closing_cash = closing_cash " .
 ($type=='credit' ? "-?" : "+?") .
 " WHERE subadmin_id=? AND cash_date=CURDATE()"
);
$c->bind_param("di", $amt, $sid);
$c->execute();

$conn->commit();

echo "Transaction successful";
?>