<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur http://localhost:8000/loto.php

$tirage = [];
$resultat = '';
$userNumbers = [];
$file = 'tirages.json';

// Charger l'historique
$historique = [];
if (file_exists($file)) {
    $historique = json_decode(file_get_contents($file), true);
}

// Tirage et vérification
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Tirage aléatoire 6 numéros uniques
    $tirage = [];
    while (count($tirage) < 6) {
        $num = random_int(1, 49);
        if (!in_array($num, $tirage)) {
            $tirage[] = $num;
        }
    }

    // Numéros choisis par l'utilisateur
    $userNumbers = array_map('intval', $_POST['numbers']);
    $userNumbers = array_unique($userNumbers);

    // Vérification
    $correct = array_intersect($tirage, $userNumbers);
    $countCorrect = count($correct);

    if ($countCorrect === 6) {
        $resultat = "🎉 Jackpot ! Tous les numéros sont corrects : " . implode(', ', $tirage);
    } else {
        $resultat = "Vous avez trouvé $countCorrect numéro(s) : " . implode(', ', $correct);
        $resultat .= "<br>Numéros tirés : " . implode(', ', $tirage);
    }

    // Ajouter au fichier historique
    $historique[] = [
        'user' => $userNumbers,
        'tirage' => $tirage,
        'correct' => $countCorrect,
        'date' => date('Y-m-d H:i:s')
    ];
    file_put_contents($file, json_encode($historique));
}
?>