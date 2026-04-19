<?php
function generateBankID($conn) {
    do {
        $bank_id = mt_rand(100000, 999999); // Random 6-digit number
        $check = $conn->query("SELECT bank_id FROM users WHERE bank_id='$bank_id'");
    } while($check->num_rows > 0); // ensure uniqueness
    return $bank_id;
}
?>
