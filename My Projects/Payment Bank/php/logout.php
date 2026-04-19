<?php
session_start();
$_SESSION = [];
session_destroy();
header("Location: ../usr/index.html");
exit();
?>
