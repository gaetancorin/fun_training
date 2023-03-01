<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur:
// http://localhost:8000/password_generator.php

function generatePassword($length = 12, $uppercase = true, $numbers = true, $symbols = true) {
    $chars = 'abcdefghijklmnopqrstuvwxyz';
    if ($uppercase) $chars .= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    if ($numbers) $chars .= '0123456789';
    if ($symbols) $chars .= '!@#$%^&*()-_=+[]{};:,.<>?';

    $password = '';
    for ($i = 0; $i < $length; $i++) {
        $password .= $chars[random_int(0, strlen($chars) - 1)];
    }
    return $password;
}

$password = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $length = (int)$_POST['length'];
    $uppercase = isset($_POST['uppercase']);
    $numbers = isset($_POST['numbers']);
    $symbols = isset($_POST['symbols']);
    $password = generatePassword($length, $uppercase, $numbers, $symbols);
}
?>