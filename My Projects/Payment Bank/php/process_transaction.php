<?php
session_start();
include 'db_connect.php';

$bank_id = $_SESSION['bank_id'] ?? null;
$pin     = $_POST['pin'] ?? null;
$amount  = floatval($_POST['amount'] ?? 0);
$desc    = $_POST['description'] ?? 'Transaction';

if (!$bank_id || !$pin || $amount <= 0) {
    $error = "Invalid request";
    goto OUTPUT;
}

/* 🔐 VERIFY TRANSACTION PIN */
$stmt = $conn->prepare(
    "SELECT transaction_pin FROM user_profile WHERE bank_id=?"
);
$stmt->bind_param("i", $bank_id);
$stmt->execute();
$stmt->bind_result($stored_pin);
$stmt->fetch();
$stmt->close();

if (!$stored_pin || $stored_pin !== $pin) {
    $error = "❌ Wrong Transaction PIN";
    goto OUTPUT;
}

/* 💰 FETCH BALANCE */
$stmt = $conn->prepare(
    "SELECT balance FROM user_balance WHERE bank_id=?"
);
$stmt->bind_param("i", $bank_id);
$stmt->execute();
$stmt->bind_result($balance);
$stmt->fetch();
$stmt->close();

if ($balance < $amount) {
    $error = "❌ Insufficient Balance";
    goto OUTPUT;
}

/* ➖ UPDATE BALANCE */
$new_balance = $balance - $amount;

$upd = $conn->prepare(
    "UPDATE user_balance SET balance=? WHERE bank_id=?"
);
$upd->bind_param("di", $new_balance, $bank_id);
$upd->execute();
$upd->close();

/* 🧾 INSERT TRANSACTION HISTORY */
$type = "debit";

$txn = $conn->prepare(
    "INSERT INTO transactions
    (bank_id,type,amount,balance_after,description)
    VALUES (?,?,?,?,?)"
);
$txn->bind_param(
    "isdds",
    $bank_id,
    $type,
    $amount,
    $new_balance,
    $desc
);
$txn->execute();
$txn->close();

$success = true;

OUTPUT:
$conn->close();
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Transaction Status</title>

<?php if(isset($success)): ?>
<meta http-equiv="refresh" content="3;url=../usr/index.html">
<?php endif; ?>

<style>
body{
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    font-family:Arial;
    background:#f2f4f8;
}
.card{
    background:#fff;
    padding:35px;
    border-radius:16px;
    text-align:center;
    box-shadow:0 10px 25px rgba(0,0,0,0.15);
}
.success{color:#1db954}
.error{color:#e53935}
</style>
</head>
<body>

<div class="card">
<?php if(isset($success)): ?>
    <h1 class="success">✅ Payment Successful</h1>
    <p>Amount: ₹<?= htmlspecialchars($amount) ?></p>
    <p>Remaining Balance: ₹<?= htmlspecialchars($new_balance) ?></p>
    <p>Redirecting to dashboard…</p>
<?php else: ?>
    <h1 class="error"><?= htmlspecialchars($error) ?></h1>
    <br>
    <a href="javascript:history.back()">⬅ Go Back</a>
<?php endif; ?>
</div>

</body>
</html>
