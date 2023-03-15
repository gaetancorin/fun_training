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

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Mini Login PHP</title>
<style>
body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; padding-top: 50px; }
.container { background: white; padding: 20px 30px; border-radius: 10px; box-shadow: 0 0 10px #ccc; width: 400px; text-align: center; }
input { width: 90%; padding: 10px; margin: 5px 0; font-size: 16px; }
button { padding: 10px 20px; margin-top: 10px; font-size: 16px; cursor: pointer; }
.error { color: red; font-weight: bold; margin-top: 10px; }
</style>
</head>
<body>
<div class="container">
    <h2>🔐 Mini Login</h2>

    <?php if (isset($_SESSION['user'])): ?>
        <p>✅ Bonjour, <strong><?= htmlspecialchars($_SESSION['user']) ?></strong> !</p>
        <a href="?logout"><button>Se déconnecter</button></a>
    <?php else: ?>
        <form method="POST">
            <input type="text" name="username" placeholder="Pseudo" required><br>
            <input type="password" name="password" placeholder="Mot de passe" required><br>
            <button type="submit">Se connecter</button>
        </form>
        <?php if ($error) echo "<div class='error'>$error</div>"; ?>
    <?php endif; ?>
</div>
</body>
</html>