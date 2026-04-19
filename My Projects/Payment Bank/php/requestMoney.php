<?php
session_start();
include 'db_connect.php';
// include 'session_check.php';

$sender_id = $_SESSION['bank_id'] ?? null; // logged-in user
$message = "";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $receiver_id = intval($_POST['receiver_id'] ?? 0); // jisse paisa chahiye
    $amount      = floatval($_POST['amount'] ?? 0);

    if (!$sender_id || !$receiver_id || $amount <= 0) {
        $message = "❌ Invalid request data";
    } elseif ($sender_id == $receiver_id) {
        $message = "❌ You cannot request money from yourself";
    } else {

        // Check receiver exists
        $check = $conn->prepare(
            "SELECT bank_id FROM user_profile WHERE bank_id=?"
        );
        $check->bind_param("i", $receiver_id);
        $check->execute();
        $check->store_result();

        if ($check->num_rows === 0) {
            $message = "❌ Bank ID not found";
        } else {

            // Insert money request (CORRECT DIRECTION)
            $stmt = $conn->prepare(
                "INSERT INTO money_requests (sender_id, receiver_id, amount)
                 VALUES (?, ?, ?)"
            );
            $stmt->bind_param("iid", $sender_id, $receiver_id, $amount);

            if ($stmt->execute()) {
                $message = "✅ Money request sent successfully";
            } else {
                $message = "❌ Failed to send request";
            }

            $stmt->close();
        }

        $check->close();
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Request Money</title>
<style>
body{
    font-family:Arial;
    background:#f2f4f8;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    margin:0;
}
.card{
    background:#fff;
    padding:30px;
    border-radius:14px;
    width:360px;
    box-shadow:0 10px 25px rgba(0,0,0,0.15);
    text-align:center;
}
input,button{
    width:100%;
    padding:12px;
    margin-top:12px;
    font-size:16px;
}
button{
    background:#1d7af3;
    color:#fff;
    border:none;
    border-radius:8px;
    cursor:pointer;
}
button:hover{ background:#155db2; }
.success{ color:#1db954; }
.error{ color:#e53935; }
a{
    text-decoration:none;
    color:#1d7af3;
}
a:hover{ text-decoration:underline; }
</style>
</head>
<body>

<div class="card">
    <h2>📥 Request Money</h2>

    <?php if($message): ?>
        <p class="<?= str_contains($message,'✅') ? 'success' : 'error' ?>">
            <?= htmlspecialchars($message) ?>
        </p>
    <?php endif; ?>

    <form method="POST">
        <input type="number" name="receiver_id" placeholder="Receiver Bank ID" required>
        <input type="number" name="amount" placeholder="Amount ₹" required>
        <button type="submit">Request</button>
    </form>

    <br>
    <a href="../index.html">⬅ Back to Dashboard</a>
</div>

</body>
</html>