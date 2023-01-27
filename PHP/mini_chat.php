<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur
// http://localhost:8000/mini_chat.php

$file = 'messages_chat.json';

// Charger les messages existants
$messages = [];
if (file_exists($file)) {
    $messages = json_decode(file_get_contents($file), true);
}

// Ajouter un nouveau message
if (isset($_POST['pseudo'], $_POST['message']) && $_POST['message'] !== '') {
    $messages[] = [
        'pseudo' => htmlspecialchars($_POST['pseudo']),
        'message' => htmlspecialchars($_POST['message']),
        'date' => date('H:i:s'),
        'likes' => 0 // nouveau champ pour les likes
    ];
    file_put_contents($file, json_encode($messages));
}

// Supprimer un message (optionnel)
if (isset($_GET['supprimer'])) {
    $index = (int)$_GET['supprimer'];
    if (isset($messages[$index])) {
        array_splice($messages, 1, $index);
        file_put_contents($file, json_encode($messages));
    }
}

// Ajouter un like
if (isset($_GET['like'])) {
    $index = (int)$_GET['like'];
    if (isset($messages[$index])) {
        $messages[$index]['likes']++;
        file_put_contents($file, json_encode($messages));
    }
}

// Fonction pour générer une couleur à partir du pseudo
function pseudoColor($pseudo) {
    $hash = md5($pseudo);
    return '#' . substr($hash, 0, 6);
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Mini Chat PHP</title>
<style>
body {
    font-family: Arial;
    background: #f0f0f0;
    display: flex;
    justify-content: center;
    padding-top: 50px;
}
.chat {
    background: white;
    padding: 20px 30px;
    border-radius: 10px;
    box-shadow: 0 0 10px #ccc;
    width: 500px;
}
input, textarea, button {
    width: 100%;
    padding: 10px;
    margin: 5px 0;
    font-size: 16px;
}
.message {
    border-bottom: 1px solid #ddd;
    padding: 10px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.message span {
    display: block;
    font-size: 14px;
    color: gray;
}
.message div.likes {
    display: flex;
    align-items: center;
    gap: 5px;
}
a {
    text-decoration: none;
    color: #00796b;
    font-weight: bold;
}
a:hover {
    color: #004d40;
}
</style>
</head>
<body>
<div class="chat">
    <h2>💬 Mini Chat</h2>
    <form method="POST">
        <input type="text" name="pseudo" placeholder="Votre pseudo" required>
        <textarea name="message" placeholder="Votre message" rows="3" required></textarea>
        <button type="submit">Envoyer</button>
    </form>

    <h3>Messages :</h3>
    <?php if (empty($messages)): ?>
        <p>Aucun message pour l'instant.</p>
    <?php else: ?>
        <?php foreach ($messages as $index => $msg): ?>
            <div class="message">
                <div>
                    <strong style="color: <?= pseudoColor($msg['pseudo']) ?>"><?= $msg['pseudo'] ?></strong>
                    <span><?= $msg['date'] ?></span>
                    <p><?= $msg['message'] ?></p>
                </div>
                <div class="likes">
                    <a href="?like=<?= $index ?>">❤️</a> <?= $msg['likes'] ?>
                </div>
            </div>
        <?php endforeach; ?>
    <?php endif; ?>
</div>
</body>
</html>
