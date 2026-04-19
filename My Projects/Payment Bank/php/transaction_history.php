<?php
session_start();
include '../php/db_connect.php';
// include '../php/session_check.php';

$bank_id = $_SESSION['bank_id'];

/* 📅 Current month range */
$monthStart = date('Y-m-01 00:00:00');
$monthEnd   = date('Y-m-t 23:59:59');

/* 💸 TOTAL MONTHLY SPENDING (DEBIT) */
$totalStmt = $conn->prepare(
    "SELECT IFNULL(SUM(amount),0)
     FROM transactions
     WHERE bank_id=?
     AND type='debit'
     AND created_at BETWEEN ? AND ?"
);
$totalStmt->bind_param("iss", $bank_id, $monthStart, $monthEnd);
$totalStmt->execute();
$totalStmt->bind_result($totalSpending);
$totalStmt->fetch();
$totalStmt->close();

/* 📜 TRANSACTION HISTORY */
$txnStmt = $conn->prepare(
    "SELECT type, amount, balance_after, description, created_at
     FROM transactions
     WHERE bank_id=?
     ORDER BY created_at DESC"
);
$txnStmt->bind_param("i", $bank_id);
$txnStmt->execute();
$result = $txnStmt->get_result();
?>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Transaction History</title>
<style>
body{
    font-family:Arial;
    background:#f2f4f8;
    margin:0;
    padding:20px;
}
.container{
    max-width:900px;
    margin:auto;
}
.card{
    background:#fff;
    padding:20px;
    border-radius:14px;
    margin-bottom:20px;
    box-shadow:0 8px 20px rgba(0,0,0,0.1);
}
h2{margin-top:0}
.spending{
    font-size:26px;
    color:#e53935;
    font-weight:bold;
}
table{
    width:100%;
    border-collapse:collapse;
}
th,td{
    padding:12px;
    border-bottom:1px solid #eee;
    text-align:left;
}
th{background:#fafafa}
.credit{color:#1db954;font-weight:bold}
.debit{color:#e53935;font-weight:bold}
.small{color:#777;font-size:14px}
</style>
</head>
<body>

<div class="container">

<!-- 📊 MONTHLY SPENDING -->
<div class="card">
    <h2>📊 This Month Spending</h2>
    <div class="spending">₹<?= number_format($totalSpending,2) ?></div>
</div>

<!-- 📜 TRANSACTION HISTORY -->
<div class="card">
    <h2>📜 Transaction History</h2>

    <?php if($result->num_rows > 0): ?>
    <table>
        <tr>
            <th>Type</th>
            <th>Amount</th>
            <th>Balance After</th>
            <th>Description</th>
            <th>Date</th>
        </tr>

        <?php while($row = $result->fetch_assoc()): ?>
        <tr>
            <td class="<?= $row['type'] ?>">
                <?= strtoupper($row['type']) ?>
            </td>
            <td>₹<?= number_format($row['amount'],2) ?></td>
            <td>₹<?= number_format($row['balance_after'],2) ?></td>
            <td><?= htmlspecialchars($row['description']) ?></td>
            <td class="small"><?= $row['created_at'] ?></td>
        </tr>
        <?php endwhile; ?>

    </table>
    <?php else: ?>
        <p>No transactions found.</p>
    <?php endif; ?>

</div>

</div>
</body>
</html>

<?php
$txnStmt->close();
$conn->close();
?>