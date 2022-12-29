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
        'date' => date('H:i:s')
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
?>