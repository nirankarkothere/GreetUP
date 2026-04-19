<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Enter PIN</title>
<style>
body{font-family:Arial;background:#eef2f7}
.box{
    max-width:350px;
    margin:80px auto;
    background:#fff;
    padding:25px;
    border-radius:14px;
    text-align:center;
}
input{
    width:100%;
    padding:12px;
    font-size:20px;
    text-align:center;
    letter-spacing:8px;
}
button{
    width:100%;
    margin-top:15px;
    padding:12px;
    background:#1d7af3;
    color:#fff;
    border:none;
    border-radius:8px;
}
</style>
</head>
<body>

<div class="box">
    <h2>🔐 Enter PIN</h2>

    <form action="../php/process_transaction.php" method="POST">
        <input type="password" name="pin" maxlength="4" required>
        
        <!-- Hidden data from transaction -->
        <input type="hidden" name="service" value="<?= $_GET['service'] ?? '' ?>">
        <input type="hidden" name="reference" value="<?= $_GET['ref'] ?? '' ?>">
        <input type="hidden" name="amount" value="<?= $_GET['amount'] ?? '' ?>">

        <button type="submit">Confirm</button>
    </form>
</div>

</body>
</html>
