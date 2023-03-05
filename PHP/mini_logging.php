<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur:
// http://localhost:8000/mini_login.php

session_start();

$users = [
    'alice' => 'password123',
    'bob' => 'secure456',
    'charlie' => 'mypassword'
];

$error = '';

if (isset($_GET['logout'])) {
    session_destroy();
    header('Location: mini_login.php');
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    if (isset($users[$username]) && $users[$username] === $password) {
        $_SESSION['user'] = $username;
        header('Location: mini_login.php');
        exit;
    } else {
        $error = '❌ Identifiants incorrects';
    }
}
?>