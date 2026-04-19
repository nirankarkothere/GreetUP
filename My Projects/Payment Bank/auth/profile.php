<?php
session_start();
include '../php/db_connect.php';
// include '../php/session_check.php';

$bank_id = $_SESSION['bank_id'];

/* 1️⃣ AUTO-FORWARD USER INTO user_profile (first login only) */
$check = $conn->prepare("SELECT bank_id FROM user_profile WHERE bank_id=?");
$check->bind_param("i", $bank_id);
$check->execute();
$check->store_result();

if ($check->num_rows == 0) {

    $create = $conn->prepare("
        INSERT INTO user_profile
        (bank_id,username,aadhar,pan,mobile,age,address,pin_code,profile_photo,transaction_pin)
        SELECT bank_id,'','','','',0,'','', 'default.png',''
        FROM users WHERE bank_id=?
    ");
    $create->bind_param("i", $bank_id);
    $create->execute();
    $create->close();
}
$check->close();

/* 2️⃣ FETCH PROFILE DATA */
$stmt = $conn->prepare("
    SELECT bank_id,username,aadhar,pan,mobile,age,address,pin_code,profile_photo,transaction_pin,updated_at
    FROM user_profile WHERE bank_id=?
");
$stmt->bind_param("i", $bank_id);
$stmt->execute();
$result = $stmt->get_result();
$row = ($result->num_rows > 0) ? $result->fetch_assoc() : null;
$stmt->close();
$conn->close();
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>My Profile</title>
<style>
body{
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg,#e0f2ff,#f8fbff);
    margin:0;
    padding:0;
}
.profile-card{
    max-width:520px;
    margin:60px auto;
    background:#fff;
    border-radius:18px;
    box-shadow:0 15px 35px rgba(0,0,0,0.15);
    padding:25px;
    text-align:center;
}
.profile-photo{
    width:130px;
    height:130px;
    border-radius:50%;
    border:4px solid #1d7af3;
    object-fit:cover;
    margin-top:-80px;
    background:#fff;
}
h2{
    margin-top:10px;
    color:#1d7af3;
}
.info{
    text-align:left;
    margin-top:20px;
}
.info div{
    padding:10px;
    border-bottom:1px dashed #ddd;
    display:flex;
    justify-content:space-between;
}
.info label{
    font-weight:600;
    color:#444;
}
button{
    background:#1d7af3;
    color:white;
    border:none;
    padding:12px 25px;
    border-radius:25px;
    font-size:16px;
    cursor:pointer;
    margin-top:20px;
}
button:hover{background:#125ecf;}
.empty{
    color:#ff3b3b;
    margin:30px 0;
}
</style>
</head>
<body>

<div class="profile-card">

<?php if($row): ?>
<img src="<?= $row['profile_photo'] ?: 'default.png' ?>" class="profile-photo">

<h2>My Bank Profile</h2>

<div class="info">
    <div><label>Bank ID</label><span><?= $row['bank_id'] ?></span></div>
    <div><label>User Name</label><span><?= $row['username'] ?></span></div>
    <div><label>Aadhaar</label><span><?= $row['aadhar'] ?></span></div>
    <div><label>PAN</label><span><?= $row['pan'] ?></span></div>
    <div><label>Mobile</label><span><?= $row['mobile'] ?></span></div>
    <div><label>Age</label><span><?= $row['age'] ?></span></div>
    <div><label>Address</label><span><?= $row['address'] ?></span></div>
    <div><label>Pin Code</label><span><?= $row['pin_code'] ?></span></div>
    <div><label>Transaction PIN</label><span><?= $row['transaction_pin'] ?></span></div>
    <div><label>Last Updated</label><span><?= $row['updated_at'] ?></span></div>
</div>

<a href="updateProfile.php"><button>✏️ Edit My Profile</button></a>

<?php else: ?>
<p class="empty">⚠ Your profile is not completed yet.</p>
<a href="updateProfile.php"><button>Complete My Profile</button></a>
<?php endif; ?>

</div>
</body>
</html>
