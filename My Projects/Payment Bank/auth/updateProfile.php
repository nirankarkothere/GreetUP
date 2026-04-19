<?php
session_start();
include '../php/db_connect.php';
// include '../php/session_check.php';

$bank_id = $_SESSION['bank_id'] ?? 0;

// === Handle form submission ===
if($_SERVER['REQUEST_METHOD'] === 'POST') {

    // Sanitize input
    $username = trim($_POST['username']);
    $aadhar = trim($_POST['aadhar']);
    $pan = trim($_POST['pan']);
    $mobile = trim($_POST['mobile']);
    $age = (int)$_POST['age'];
    $address = trim($_POST['address']);
    $pin_code = trim($_POST['pin_code']);
    $transaction_pin = trim($_POST['transaction_pin']);

    // Handle profile photo upload
    $profile_photo = '';
    if(isset($_FILES['profile_photo']) && $_FILES['profile_photo']['error'] === 0){
        $ext = pathinfo($_FILES['profile_photo']['name'], PATHINFO_EXTENSION);
        $allowed = ['jpg','jpeg','png','webp'];
        if(in_array(strtolower($ext), $allowed)){
            $newName = 'uploads/'.$bank_id.'_'.time().'.'.$ext;
            move_uploaded_file($_FILES['profile_photo']['tmp_name'], '../'.$newName);
            $profile_photo = $newName;
        }
    }

    // Build SQL dynamically (update photo only if uploaded)
    if($profile_photo){
        $sql = "UPDATE user_profile SET username=?, aadhar=?, pan=?, mobile=?, age=?, address=?, pin_code=?, profile_photo=?,transaction_pin=?, updated_at=NOW() WHERE bank_id=?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ssssssssi",$username,$aadhar,$pan,$mobile,$age,$address,$pin_code,$profile_photo,$transaction_pin,$bank_id);
    } else {
        $sql = "UPDATE user_profile SET username=?, aadhar=?, pan=?, mobile=?, age=?, address=?, pin_code=?, transaction_pin=?, updated_at=NOW() WHERE bank_id=?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("sssssssii",$username,$aadhar,$pan,$mobile,$age,$address,$pin_code,$transaction_pin,$bank_id);
    }

    $stmt->execute();
    $stmt->close();

    // Redirect to profile page after update
    header("Location: profile.php");
    exit;
}

// === Fetch existing profile data to prefill form ===
$stmt = $conn->prepare("SELECT * FROM user_profile WHERE bank_id=?");
$stmt->bind_param("i",$bank_id);
$stmt->execute();
$result = $stmt->get_result();
$row = $result->fetch_assoc() ?: [];
$stmt->close();
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Update Profile</title>
<style>
body{font-family:'Segoe UI',sans-serif;background:#f0f4f8;margin:0;padding:0;}
.container{max-width:600px;margin:50px auto;background:#fff;padding:25px;border-radius:12px;box-shadow:0 15px 35px rgba(0,0,0,0.15);}
h2{color:#1d7af3;text-align:center;}
form{margin-top:20px;}
label{display:block;font-weight:600;margin:10px 0 5px;}
input[type=text], input[type=number], textarea{width:100%;padding:10px;border-radius:6px;border:1px solid #ccc;box-sizing:border-box;}
input[type=file]{margin-top:5px;}
button{margin-top:20px;background:#1d7af3;color:#fff;border:none;padding:12px 20px;border-radius:25px;font-size:16px;cursor:pointer;}
button:hover{background:#125ecf;}
img{max-width:120px;border-radius:50%;margin-top:10px;}
</style>
</head>
<body>

<div class="container">
<h2>✏️ Update My Profile</h2>

<form method="post" enctype="multipart/form-data">
    <label>User Name</label>
    <input type="text" name="username" value="<?= htmlspecialchars($row['username'] ?? '') ?>" required>
    <label>Aadhaar</label>
    <input type="text" name="aadhar" value="<?= htmlspecialchars($row['aadhar'] ?? '') ?>" required>

    <label>PAN</label>
    <input type="text" name="pan" value="<?= htmlspecialchars($row['pan'] ?? '') ?>" required>

    <label>Mobile</label>
    <input type="text" name="mobile" value="<?= htmlspecialchars($row['mobile'] ?? '') ?>" required>

    <label>Age</label>
    <input type="number" name="age" value="<?= htmlspecialchars($row['age'] ?? '') ?>" required>

    <label>Address</label>
    <textarea name="address" rows="3" required><?= htmlspecialchars($row['address'] ?? '') ?></textarea>

    <label>Pin Code</label>
    <input type="text" name="pin_code" value="<?= htmlspecialchars($row['pin_code'] ?? '') ?>" required>

    <label>transaction pin</label>
    <input type="text" name="transaction_pin" value="<?= htmlspecialchars($row['transaction_pin'] ?? '') ?>" required>

    <label>Profile Photo</label>
    <input type="file" name="profile_photo">
    <?php if(!empty($row['profile_photo'])): ?>
        <img src="<?= htmlspecialchars($row['profile_photo']) ?>" alt="Profile Photo">
    <?php endif; ?>

    <button type="submit">Update Profile</button>
</form>
</div>

</body>
</html>
