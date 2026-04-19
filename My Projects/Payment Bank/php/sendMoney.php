<?php
session_start();
include 'db_connect.php'; // Your DB connection
include 'session_check.php';

// Get POST data
$sender_id = $_SESSION['bank_id'] ?? null; // Logged-in user
$receiver_id = $_POST['receiver_id'] ?? null;
$amount = $_POST['amount'] ?? 0;

header('Content-Type: application/json');

if (!$sender_id || !$receiver_id || $amount <= 0) {
    echo json_encode(["success" => false, "message" => "Invalid data"]);
    exit;
}

// Start transaction
$conn->begin_transaction();

try {
    // 1️⃣ Get sender balance
    $stmt = $conn->prepare("SELECT balance FROM user_profile WHERE bank_id=? FOR UPDATE");
    $stmt->bind_param("i", $sender_id);
    $stmt->execute();
    $stmt->bind_result($sender_balance);
    $stmt->fetch();
    $stmt->close();

    if ($sender_balance < $amount) {
        throw new Exception("Insufficient balance");
    }

    // 2️⃣ Deduct from sender
    $new_sender_balance = $sender_balance - $amount;
    $stmt = $conn->prepare("UPDATE user_profile SET balance=? WHERE bank_id=?");
    $stmt->bind_param("di", $new_sender_balance, $sender_id);
    $stmt->execute();
    $stmt->close();

    // 3️⃣ Add to receiver
    $stmt = $conn->prepare("SELECT balance FROM user_profile WHERE bank_id=? FOR UPDATE");
    $stmt->bind_param("i", $receiver_id);
    $stmt->execute();
    $stmt->bind_result($receiver_balance);
    $stmt->fetch();
    $stmt->close();

    $new_receiver_balance = $receiver_balance + $amount;
    $stmt = $conn->prepare("UPDATE user_profile SET balance=? WHERE bank_id=?");
    $stmt->bind_param("di", $new_receiver_balance, $receiver_id);
    $stmt->execute();
    $stmt->close();

    // 4️⃣ Record transactions
    $stmt = $conn->prepare("INSERT INTO transactions (bank_id, type, amount, balance_after, description) VALUES (?, ?, ?, ?, ?)");
    
    // Sender debit
    $desc = "Sent money to bank ID $receiver_id";
    $stmt->bind_param("isdss", $sender_id, $type, $amount, $new_sender_balance, $desc);
    $type = 'debit';
    $stmt->execute();

    // Receiver credit
    $desc = "Received money from bank ID $sender_id";
    $stmt->bind_param("isdss", $receiver_id, $type, $amount, $new_receiver_balance, $desc);
    $type = 'credit';
    $stmt->execute();
    $stmt->close();

    // Commit transaction
    $conn->commit();

    echo json_encode(["success" => true, "message" => "Transfer successful"]);

} catch (Exception $e) {
    $conn->rollback();
    echo json_encode(["success" => false, "message" => $e->getMessage()]);
}

$conn->close();
?>
