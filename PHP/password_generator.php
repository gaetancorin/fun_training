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

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Password Generator</title>
<style>
body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; padding-top: 50px; }
.container { background: white; padding: 20px 30px; border-radius: 10px; box-shadow: 0 0 10px #ccc; width: 400px; text-align: center; }
input[type=number] { width: 60px; }
button { padding: 10px 20px; margin-top: 10px; font-size: 16px; cursor: pointer; }
.password { margin-top: 15px; font-weight: bold; word-break: break-all; }
</style>
</head>
<body>
<div class="container">
    <h2>🔑 Password Generator</h2>

    <form method="POST">
        <label>Length: <input type="number" name="length" value="12" min="4" max="20"></label><br>
        <label><input type="checkbox" name="uppercase" checked> Uppercase</label><br>
        <label><input type="checkbox" name="numbers" checked> Numbers</label><br>
        <label><input type="checkbox" name="symbols" checked> Symbols</label><br>
        <button type="submit">Generate</button>
    </form>

    <?php if ($password !== ''): ?>
        <div class="password">💻 <?= htmlspecialchars($password) ?></div>
    <?php endif; ?>
</div>
</body>
</html>