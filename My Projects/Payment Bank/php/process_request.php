<?php
session_start();
include 'db_connect.php';

$receiver_id = $_SESSION['bank_id'] ?? null;
$request_id  = $_POST['request_id'] ?? null;
$action      = $_POST['action'] ?? null;
$pin         = $_POST['pin'] ?? null;

$status  = "failed";
$message = "❌ Payment Failed";

if (!$receiver_id || !$request_id || !$action) {
    goto OUTPUT;
}

/* ================== APPROVE ================== */
if ($action === 'approve') {

    /* 🔐 VERIFY PIN */
    $stmt = $conn->prepare(
        "SELECT transaction_pin FROM user_profile WHERE bank_id=?"
    );
    $stmt->bind_param("i", $receiver_id);
    $stmt->execute();
    $stmt->bind_result($stored_pin);
    $stmt->fetch();
    $stmt->close();

    if (!$stored_pin || $stored_pin != $pin) {
        $message = "❌ Wrong Transaction PIN";
        goto OUTPUT;
    }

    /* 🔄 START DB TRANSACTION */
    $conn->begin_transaction();

    try {
        /* 📥 GET REQUEST */
        $stmt = $conn->prepare(
            "SELECT sender_id, amount FROM money_requests
             WHERE request_id=? AND receiver_id=? AND status='pending'
             FOR UPDATE"
        );
        $stmt->bind_param("ii", $request_id, $receiver_id);
        $stmt->execute();
        $stmt->bind_result($sender_id, $amount);
        $stmt->fetch();
        $stmt->close();

        if (!$sender_id || $amount <= 0) {
            throw new Exception("Invalid request");
        }

        /* 🧱 ENSURE BALANCE ROWS EXIST */
        $conn->query(
            "INSERT IGNORE INTO user_balance (bank_id,balance)
             VALUES ($receiver_id,0), ($sender_id,0)"
        );

        /* 💰 LOCK RECEIVER BALANCE */
        $stmt = $conn->prepare(
            "SELECT balance FROM user_balance WHERE bank_id=? FOR UPDATE"
        );
        $stmt->bind_param("i", $receiver_id);
        $stmt->execute();
        $stmt->bind_result($receiver_balance);
        $stmt->fetch();
        $stmt->close();

        if ($receiver_balance < $amount) {
            throw new Exception("Insufficient balance");
        }

        /* 💰 LOCK SENDER BALANCE */
        $stmt = $conn->prepare(
            "SELECT balance FROM user_balance WHERE bank_id=? FOR UPDATE"
        );
        $stmt->bind_param("i", $sender_id);
        $stmt->execute();
        $stmt->bind_result($sender_balance);
        $stmt->fetch();
        $stmt->close();

        /* 🧮 CALCULATE */
        $receiver_new = $receiver_balance - $amount;
        $sender_new   = $sender_balance + $amount;

        /* 🔄 UPDATE BALANCES */
        $stmt = $conn->prepare(
            "UPDATE user_balance SET balance=? WHERE bank_id=?"
        );
        $stmt->bind_param("di", $receiver_new, $receiver_id);
        $stmt->execute();

        $stmt->bind_param("di", $sender_new, $sender_id);
        $stmt->execute();
        $stmt->close();

        /* 🧾 TRANSACTION LOGS */
        $stmt = $conn->prepare(
            "INSERT INTO transactions
            (bank_id,type,amount,balance_after,description)
            VALUES (?,?,?,?,?)"
        );

        $type = 'debit';
        $desc = 'Money sent (request approved)';
        $stmt->bind_param("isdds", $receiver_id, $type, $amount, $receiver_new, $desc);
        $stmt->execute();

        $type = 'credit';
        $desc = 'Money received (request approved)';
        $stmt->bind_param("isdds", $sender_id, $type, $amount, $sender_new, $desc);
        $stmt->execute();

        $stmt->close();

        /* ✅ UPDATE REQUEST */
        $stmt = $conn->prepare(
            "UPDATE money_requests SET status='approved' WHERE request_id=?"
        );
        $stmt->bind_param("i", $request_id);
        $stmt->execute();
        $stmt->close();

        $conn->commit();

        $status  = "success";
        $message = "✅ Payment Successful";

    } catch (Exception $e) {
        $conn->rollback();
        $message = "❌ " . $e->getMessage();
    }
}

/* ================== REJECT ================== */
if ($action === 'reject') {

    $stmt = $conn->prepare(
        "UPDATE money_requests
         SET status='rejected'
         WHERE request_id=? AND receiver_id=?"
    );
    $stmt->bind_param("ii", $request_id, $receiver_id);
    $stmt->execute();
    $stmt->close();

    $status  = "failed";
    $message = "❌ Request Rejected";
}

OUTPUT:
$conn->close();
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Payment Status</title>
<meta http-equiv="refresh" content="3;url=../usr/index.html">

<style>
body{
    font-family:Arial;
    background:#f2f4f8;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}
.card{
    background:#fff;
    padding:35px;
    border-radius:16px;
    text-align:center;
    box-shadow:0 10px 25px rgba(0,0,0,0.15);
}
.success{color:#1db954}
.failed{color:#e53935}
</style>
</head>
<body>

<div class="card">
    <h1 class="<?= $status ?>">
        <?= htmlspecialchars($message) ?>
    </h1>
    <p>Redirecting to dashboard…</p>
</div>

</body>
</html>
