<?php
session_start();
include '../php/db_connect.php';

if($_SERVER['REQUEST_METHOD']=="POST"){
    $u = $_POST['username'];
    $p = password_hash($_POST['password'],PASSWORD_DEFAULT);

    $stmt=$conn->prepare("INSERT INTO sub_admins(username,password) VALUES(?,?)");
    $stmt->bind_param("ss",$u,$p);
    $stmt->execute();

    echo "<p class='success'>✅ Sub Admin Added</p>";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Add Sub Admin</title>
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(to right, #6a11cb, #2575fc);
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        color: #333;
    }

    .container {
        background: #fff;
        padding: 40px 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        width: 350px;
        text-align: center;
        animation: fadeIn 1s ease-in-out;
    }

    h3 {
        margin-bottom: 25px;
        color: #2575fc;
    }

    input {
        width: 100%;
        padding: 12px 15px;
        margin: 10px 0;
        border: 1px solid #ccc;
        border-radius: 8px;
        font-size: 16px;
        transition: all 0.3s;
    }

    input:focus {
        border-color: #2575fc;
        box-shadow: 0 0 8px rgba(37,117,252,0.4);
        outline: none;
    }

    button {
        width: 100%;
        padding: 12px;
        background: #2575fc;
        color: #fff;
        font-size: 16px;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        margin-top: 15px;
        transition: all 0.3s;
    }

    button:hover {
        background: #6a11cb;
        transform: translateY(-2px);
    }

    .success {
        background: #d4edda;
        color: #155724;
        padding: 10px;
        margin-top: 15px;
        border-radius: 8px;
        font-weight: bold;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(-20px);}
        to {opacity: 1; transform: translateY(0);}
    }
</style>
</head>
<body>
    <div class="container">
        <form method="POST">
            <h3>Add Sub Admin</h3>
            <input name="username" required placeholder="Username">
            <input name="password" type="password" required placeholder="Password">
            <button>Add</button>
        </form>
    </div>
</body>
</html>
