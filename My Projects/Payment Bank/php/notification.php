<?php
session_start();
include 'db_connect.php';

$bank_id = $_SESSION['bank_id'];

$stmt = $conn->prepare(
    "SELECT request_id, sender_id, amount, created_at
     FROM money_requests
     WHERE receiver_id=? AND status='pending'
     ORDER BY created_at DESC"
);
$stmt->bind_param("i", $bank_id);
$stmt->execute();
$result = $stmt->get_result();
?>
<!DOCTYPE html>
<html>
<head>
<title>Notifications</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body{
    margin:0;
    font-family: 'Segoe UI', Arial;
    background:linear-gradient(135deg,#eef2f7,#dfe7f2);
}
.container{
    max-width:420px;
    margin:auto;
    padding:20px;
}
h2{
    text-align:center;
    margin-bottom:20px;
}
.card{
    background:#fff;
    border-radius:16px;
    padding:18px;
    margin-bottom:18px;
    box-shadow:0 12px 30px rgba(0,0,0,.12);
    animation:fadeIn .4s ease;
}
@keyframes fadeIn{
    from{opacity:0;transform:translateY(10px)}
    to{opacity:1;transform:translateY(0)}
}
.row{
    display:flex;
    justify-content:space-between;
    margin-bottom:6px;
}
.amount{
    font-size:22px;
    font-weight:700;
    color:#1d7af3;
}
.time{
    font-size:12px;
    color:#777;
}
.pin{
    width:100%;
    padding:10px;
    margin:10px 0;
    border-radius:8px;
    border:1px solid #ccc;
}
.actions{
    display:flex;
    gap:10px;
}
button{
    flex:1;
    padding:12px;
    border:none;
    border-radius:10px;
    font-weight:600;
    cursor:pointer;
}
.approve{
    background:#1db954;
    color:#fff;
}
.reject{
    background:#e53935;
    color:#fff;
}
.empty{
    text-align:center;
    color:#555;
    margin-top:60px;
}
</style>
</head>

<body>

<div class="container">
    <h2>🔔 Money Requests</h2>

    <?php if($result->num_rows === 0): ?>
        <div class="empty">
            💤 No pending requests<br>
            Enjoy the silence.
        </div>
    <?php endif; ?>

    <?php while($row = $result->fetch_assoc()): ?>
    <div class="card">
        <div class="row">
            <div>
                <b>From</b><br>
                #<?= htmlspecialchars($row['sender_id']) ?>
            </div>
            <div class="amount">
                ₹<?= number_format($row['amount'],2) ?>
            </div>
        </div>

        <div class="time">
            ⏱ <?= date("d M Y, h:i A", strtotime($row['created_at'])) ?>
        </div>

        <!-- APPROVE -->
        <form action="process_request.php" method="POST">
            <input type="hidden" name="request_id" value="<?= $row['request_id'] ?>">
            <input type="password" name="pin" class="pin" placeholder="🔐 Transaction PIN" required>

            <div class="actions">
                <button type="submit" name="action" value="approve" class="approve">
                    ✅ Approve
                </button>
        </form>

        <!-- REJECT -->
        <form action="process_request.php" method="POST">
            <input type="hidden" name="request_id" value="<?= $row['request_id'] ?>">
                <button type="submit" name="action" value="reject" class="reject">
                    ❌ Reject
                </button>
            </div>
        </form>
    </div>
    <?php endwhile; ?>
</div>

</body>
</html>
