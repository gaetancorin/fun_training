<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur
// http://localhost:8000/money_swap.php

$devises = [
    'EUR' => 1,
    'USD' => 1.1,
    'GBP' => 0.85,
    'JPY' => 145
];

$resultat = '';

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $montant = (float) $_POST['montant'];
    $from = $_POST['from'];
    $to = $_POST['to'];

    if (isset($devises[$from]) && isset($devises[$to])) {
        $resultat = $montant * ($devises[$to] / $devises[$from]);
        $resultat = number_format($resultat, 2);
    } else {
        $resultat = "Erreur : devise inconnue";
    }
}
?>