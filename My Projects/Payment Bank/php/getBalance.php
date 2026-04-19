<?php
session_start();
include 'db_connect.php';

header('Content-Type: application/json');

$bank_id = $_SESSION['bank_id'] ?? null;

if (!$bank_id) {
    echo json_encode(["success" => false, "message" => "User not logged in"]);
    exit;
}

// Get PIN from POST or GET
$pin = $_POST['pin'] ?? $_GET['pin'] ?? '';

if (empty($pin)) {
    echo json_encode(["success" => false, "message" => "PIN required"]);
    exit;
}

// Verify PIN
$stmt = $conn->prepare("SELECT transaction_pin FROM user_profile WHERE bank_id=?");
$stmt->bind_param("i", $bank_id);
$stmt->execute();
$stmt->bind_result($stored_pin);
$stmt->fetch();
$stmt->close();

if (!$stored_pin || $stored_pin != $pin) {
    echo json_encode(["success" => false, "message" => "❌ Wrong Transaction PIN"]);
    exit;
}

// PIN correct - get balance
$check = $conn->prepare("SELECT bank_id FROM user_balance WHERE bank_id=?");
$check->bind_param("i", $bank_id);
$check->execute();
$check->store_result();

if ($check->num_rows === 0) {
    $insert = $conn->prepare("INSERT INTO user_balance (bank_id, balance) VALUES (?, 0)");
    $insert->bind_param("i", $bank_id);
    $insert->execute();
    $insert->close();
}
$check->close();

$stmt = $conn->prepare("SELECT balance FROM user_balance WHERE bank_id=?");
$stmt->bind_param("i", $bank_id);
$stmt->execute();
$stmt->bind_result($balance);

if ($stmt->fetch()) {
    echo json_encode(["success" => true, "balance" => $balance]);
} else {
    echo json_encode(["success" => false, "message" => "Balance not found"]);
}
$stmt->close();
$conn->close();
?>