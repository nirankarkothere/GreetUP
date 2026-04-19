<?php
// Start session safely
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Always return JSON
header('Content-Type: application/json');

// If logged in
if (isset($_SESSION['bank_id'])) {
    echo json_encode([
        "logged_in" => true,
        "username"  => $_SESSION['username'] ?? "",
        "bank_id"   => $_SESSION['bank_id']
    ]);
} else {
    echo json_encode([
        "logged_in" => false
    ]);
}

exit;
?>