<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/survey.php

session_start();

// Fichier pour sauvegarder les votes
$file = 'survey_votes.json';
$votes = file_exists($file) ? json_decode(file_get_contents($file), true) : [];

// Si formulaire soumis
$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['choix'])) {
    $choix = $_POST['choix'];

    // Initialiser le vote pour ce choix si inexistant
    if (!isset($votes[$choix])) $votes[$choix] = 0;

    // Vérifier si utilisateur a déjà voté
    if (isset($_SESSION['a_vote']) && $_SESSION['a_vote'] === true) {
        $message = "⚠ Vous avez déjà voté !";
    } else {
        $votes[$choix]++;
        $_SESSION['a_vote'] = true;
        file_put_contents($file, json_encode($votes));
        $message = "✅ Merci pour votre vote !";
    }
}

// Calcul du total pour le pourcentage
$totalVotes = array_sum($votes);
?>

