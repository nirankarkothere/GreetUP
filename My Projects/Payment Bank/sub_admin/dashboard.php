<?php
session_start();
include '../php/db_connect.php';

// Check sub-admin login
$sid = $_SESSION['subadmin_id'] ?? null;
if (!$sid) {
    header("Location: login.php");
    exit();
}

$today = date('Y-m-d');
$messages = [];

// --- Handle Start Day ---
if (isset($_POST['start_day'])) {
    $cash = $_POST['cash'];
    
    $stmt = $conn->prepare(
        "INSERT INTO daily_cash (subadmin_id, cash_date, opening_cash, closing_cash)
        VALUES (?, ?, ?, ?)"
    );
    $stmt->bind_param("isdd", $sid, $today, $cash, $cash);
    
    if ($stmt->execute()) {
        $messages[] = ["type"=>"success","text"=>"🌅 Day started with opening cash ₹$cash"];
    } else {
        $messages[] = ["type"=>"error","text"=>"❌ Error starting day: " . $stmt->error];
    }
}

// --- Handle Cash Transaction ---
if (isset($_POST['transaction'])) {
    $uid = $_POST['bank_id'];
    $type = $_POST['type'];
    $amt  = $_POST['amount'];
    $reason = $_POST['reason'] ?? '';

    $conn->begin_transaction();
    try {
        // Get user balance with lock
        $q = $conn->prepare("SELECT balance FROM user_balance WHERE bank_id=? FOR UPDATE");
        $q->bind_param("i", $uid);
        $q->execute();
        $q->bind_result($bal);
        if (!$q->fetch()) throw new Exception("User not found");
        $q->close();

        if ($type == 'debit' && $bal < $amt) throw new Exception("Insufficient balance");

        $newBal = ($type == 'credit') ? $bal + $amt : $bal - $amt;

        $u = $conn->prepare("UPDATE user_balance SET balance=? WHERE bank_id=?");
        $u->bind_param("di", $newBal, $uid);
        $u->execute();

        $t = $conn->prepare(
            "INSERT INTO transactions (bank_id, type, amount, balance_after, description)
             VALUES (?, ?, ?, ?, ?)"
        );
        $t->bind_param("isdds", $uid, $type, $amt, $newBal, $reason);
        $t->execute();

        $b = $conn->prepare(
    "INSERT INTO bank_daily_transactions (subadmin_id, user_bank_id, type, amount, reason)
     VALUES (?, ?, ?, ?, ?)"
);

// i = subadmin_id (int)
// i = user_bank_id (int) <--- Changed from 's' to 'i'
// s = type (string/enum)
// d = amount (decimal)
// s = reason (string)
$b->bind_param("iisds", $sid, $uid, $type, $amt, $reason); 
$b->execute();

        // --- UPDATE DAILY CASH LOGIC ---
        // Logic: If user gets Credit, Sub-admin's cash drawer DECREASES. If Debit, Sub-admin's drawer INCREASES.
        $cashAdjustment = ($type == 'credit') ? -$amt : $amt;
        
        $c = $conn->prepare(
            "UPDATE daily_cash
             SET closing_cash = closing_cash + ?
             WHERE subadmin_id=? AND cash_date=?"
        );
        $c->bind_param("dis", $cashAdjustment, $sid, $today);
        $c->execute();

        $conn->commit();
        $messages[] = ["type"=>"success","text"=>"✅ $type ₹$amt for User $uid completed"];
    } catch (Exception $e) {
        $conn->rollback();
        $messages[] = ["type"=>"error","text"=>"❌ Transaction failed: " . $e->getMessage()];
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sub-Admin Dashboard</title>
<style>
*{box-sizing:border-box;font-family:'Segoe UI', Tahoma, sans-serif;}
body{margin:0; background:linear-gradient(135deg,#0f2027,#203a43,#2c5364); min-height:100vh; display:flex; justify-content:center; align-items:flex-start; padding:40px;}
.container{width:400px;}
.card{background:#fff;padding:25px 30px;border-radius:16px;box-shadow:0 20px 40px rgba(0,0,0,0.25);margin-bottom:25px; animation:fadeUp .6s ease;}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px);}to{opacity:1;transform:translateY(0);}}
h2{text-align:center;margin-bottom:20px;color:#2c5364;letter-spacing:1px;}
input, select{width:100%;padding:12px;margin-bottom:15px;border-radius:8px;border:1px solid #ddd;font-size:14px;transition:.3s;}
input:focus, select:focus{outline:none;border-color:#2c5364;box-shadow:0 0 6px rgba(44,83,100,0.4);}
button{width:100%;padding:12px;border:none;border-radius:8px;background:linear-gradient(135deg,#2c5364,#0f2027);color:#fff;font-size:15px;cursor:pointer;transition:.3s;}
button:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(0,0,0,0.3);}
.note{text-align:center;font-size:12px;margin-top:12px;color:#666;}
.messages{margin-bottom:15px;}
.messages p{padding:10px;border-radius:8px;font-size:14px;}
.messages p.success{background:#e0f7fa;color:#00796b;}
.messages p.error{background:#ffebee;color:#c62828;}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;}
.header h2{color:#fff;margin:0;}
.header a{padding:8px 15px;background:#ff4b5c;color:#fff;border-radius:8px;text-decoration:none;font-weight:bold;transition:.3s;}
.header a:hover{background:#ff1e2b;}
</style>
</head>
<body>

<div class="container">

    <!-- Header with Logout -->
    <div class="header">
        <h2>Sub-Admin Dashboard</h2>
        <a href="logout.php">Logout</a>
    </div>

    <!-- Messages -->
    <?php if(!empty($messages)): ?>
        <div class="messages">
            <?php foreach($messages as $msg): ?>
                <p class="<?= $msg['type'] ?>"><?= $msg['text'] ?></p>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>

    <!-- Start Day Form -->
    <div class="card">
        <h2>🌅 Start Day</h2>
        <form method="POST">
            <input type="number" name="cash" placeholder="Opening Cash Amount" required>
            <button type="submit" name="start_day">Start Day</button>
        </form>
        <div class="note">Sub-Admin Authorized 🔐</div>
    </div>

    <!-- Cash Transaction Form -->
    <div class="card">
        <h2>💰 Cash Transaction</h2>
        <form method="POST">
            <input type="text" name="bank_id" placeholder="User Bank ID" required>
            <select name="type" required>
                <option value="">Select Transaction Type</option>
                <option value="credit">Credit (Add Money)</option>
                <option value="debit">Debit (Withdraw Money)</option>
            </select>
            <input type="number" name="amount" placeholder="Amount" required>
            <input type="text" name="reason" placeholder="Reason (optional)">
            <button type="submit" name="transaction">Submit Transaction</button>
        </form>
        <div class="note">Authorized Sub-Admin Access 🔐</div>
    </div>

</div>

</body>
</html>
