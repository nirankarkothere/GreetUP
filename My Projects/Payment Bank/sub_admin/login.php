<?php
session_start();
include '../php/db_connect.php';

// 1. If already logged in, skip the login page and go to dashboard
if (isset($_SESSION['subadmin_id'])) {
    header("Location: dashboard.php");
    exit();
}

$error = "";

// 2. Only run this if the form was actually submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $user = $_POST['username'] ?? '';
    $pass = $_POST['password'] ?? '';

    $stmt = $conn->prepare("SELECT subadmin_id, password FROM sub_admins WHERE username=?");
    $stmt->bind_param("s", $user);
    $stmt->execute();
    $stmt->bind_result($id, $hash);
    
    $found = $stmt->fetch();
    $stmt->close();

    if ($found && password_verify($pass, $hash)) {
        $_SESSION['subadmin_id'] = $id;
        header("Location: dashboard.php");
        exit();
    } else {
        $error = "Invalid username or password!";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sub Admin Login</title>
    <style>
        * { box-sizing: border-box; font-family: "Segoe UI", Tahoma, sans-serif; }
        body { margin: 0; height: 100vh; background: linear-gradient(135deg, #1d2671, #c33764); display: flex; justify-content: center; align-items: center; }
        .login-card { background: #fff; width: 350px; padding: 35px; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); animation: pop 0.6s ease; }
        @keyframes pop { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        .login-card h2 { text-align: center; margin-bottom: 25px; color: #333; letter-spacing: 1px; }
        .login-card input { width: 100%; padding: 12px; margin-bottom: 18px; border-radius: 8px; border: 1px solid #ddd; font-size: 14px; transition: 0.3s; }
        .login-card input:focus { border-color: #c33764; outline: none; box-shadow: 0 0 5px rgba(195,55,100,0.4); }
        .login-card button { width: 100%; padding: 12px; border: none; border-radius: 8px; background: linear-gradient(135deg, #c33764, #1d2671); color: #fff; font-size: 15px; cursor: pointer; transition: 0.3s; }
        .login-card button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,0,0,0.2); }
        .footer-text { text-align: center; margin-top: 15px; font-size: 12px; color: #777; }
        .error-msg { color: #c33764; text-align: center; font-size: 13px; margin-bottom: 15px; font-weight: bold; }
    </style>
</head>
<body>

<div class="login-card">
    <h2>Sub Admin Login</h2>

    <?php if ($error): ?>
        <div class="error-msg"><?php echo $error; ?></div>
    <?php endif; ?>

    <form action="login.php" method="POST">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>

    <div class="footer-text">
        Secure Banking Access 🔐
    </div>
</div>

</body>
</html>