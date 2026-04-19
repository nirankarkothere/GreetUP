<?php
session_start();
include 'db_connect.php';
include 'session_check.php';

$receiver_id = $_SESSION['bank_id'] ?? null;
$request_id  = $_POST['request_id'] ?? null;
$pin         = $_POST['pin'] ?? null;

if (!$receiver_id || !$request_id || !$pin) {
    die("Invalid request");
}

/* 1️⃣ Get request details */
$stmt = $conn->prepare(
    "SELECT sender_id, amount FROM money_requests WHERE request_id=? AND receiver_id=? AND status='pending'"
);
$stmt->bind_param("ii", $request_id, $receiver_id);
$stmt->execute();
$stmt->store_result();
$stmt->bind_result($sender_id, $amount);

if ($stmt->num_rows === 0) {
    die("Request not found or already processed");
}
$stmt->fetch();
$stmt->close();

/* 2️⃣ Verify receiver PIN */
$stmt = $conn->prepare("SELECT transaction_pin FROM user_profile WHERE bank_id=?");
$stmt->bind_param("i", $receiver_id);
$stmt->execute();
$stmt->bind_result($stored_pin);
$stmt->fetch();
$stmt->close();

if ($pin !== $stored_pin) {
    die("❌ Wrong PIN");
}

/* 3️⃣ Check receiver balance */
$stmt = $conn->prepare("SELECT balance FROM user_balance WHERE bank_id=?");
$stmt->bind_param("i", $receiver_id);
$stmt->execute();
$stmt->bind_result($receiver_balance);
$stmt->fetch();
$stmt->close();

if ($receiver_balance < $amount) {
    die("❌ Insufficient balance");
}

/* 4️⃣ Deduct from receiver, add to sender */
$new_receiver_balance = $receiver_balance - $amount;

// Receiver debit
$upd = $conn->prepare("UPDATE user_balance SET balance=? WHERE bank_id=?");
$upd->bind_param("di", $new_receiver_balance, $receiver_id);
$upd->execute();
$upd->close();

// Sender credit
$stmt = $conn->prepare("SELECT balance FROM user_balance WHERE bank_id=?");
$stmt->bind_param("i", $sender_id);
$stmt->execute();
$stmt->bind_result($sender_balance);
$stmt->fetch();
$stmt->close();

$new_sender_balance = $sender_balance + $amount;

$upd = $conn->prepare("UPDATE user_balance SET balance=? WHERE bank_id=?");
$upd->bind_param("di", $new_sender_balance, $sender_id);
$upd->execute();
$upd->close();

/* 5️⃣ Insert transactions */
$txn = $conn->prepare(
    "INSERT INTO transactions (bank_id,type,amount,balance_after,description)
     VALUES (?,?,?,?,?)"
);
$desc_receiver = "Sent to Bank ID $sender_id";
$desc_sender   = "Received from Bank ID $receiver_id";

$type = "debit";
$txn->bind_param("isdds", $receiver_id, $type, $amount, $new_receiver_balance, $desc_receiver);
$txn->execute();

$type = "credit";
$txn->bind_param("isdds", $sender_id, $type, $amount, $new_sender_balance, $desc_sender);
$txn->execute();
$txn->close();

/* 6️⃣ Update request status */
$stmt = $conn->prepare("UPDATE money_requests SET status='approved', created_at=NOW() WHERE request_id=?");
$stmt->bind_param("i", $request_id);
$stmt->execute();
$stmt->close();

$conn->close();
?>
<!DOCTYPE html>
<html>
<head>
<title>Request Approved</title>
<meta http-equiv="refresh" content="3;url=notification.php">
</head>
<body>
<h2>✅ Request Approved Successfully</h2>
<p>₹<?= htmlspecialchars($amount) ?> sent to sender ID <?= htmlspecialchars($sender_id) ?></p>
<p>Redirecting...</p>
</body>
</html>
