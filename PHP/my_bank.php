<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/my_bank.php

session_start();

// Initialiser le solde et l'historique si ce n'est pas déjà fait
if (!isset($_SESSION['solde'])) $_SESSION['solde'] = 100;
if (!isset($_SESSION['historique'])) $_SESSION['historique'] = [];

// Gestion du POST pour dépôt ou retrait
$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $montant = (float) ($_POST['montant'] ?? 0);
    $action = $_POST['action'] ?? '';

    if ($montant <= 0) {
        $message = "⚠ Montant invalide.";
    } else {
        if ($action === 'depot') {
            $_SESSION['solde'] += $montant;
            $_SESSION['historique'][] = [
                'type' => 'Dépôt',
                'montant' => $montant,
                'date' => date('Y-m-d H:i:s')
            ];
            $message = "✅ Vous avez déposé $montant €.";
        } elseif ($action === 'retrait') {
            if ($montant > $_SESSION['solde']) {
                $message = "⚠ Solde insuffisant pour retirer $montant €.";
            } else {
                $_SESSION['solde'] -= $montant;
                $_SESSION['historique'][] = [
                    'type' => 'Retrait',
                    'montant' => $montant,
                    'date' => date('Y-m-d H:i:s')
                ];
                $message = "✅ Vous avez retiré $montant €.";
            }
        }
    }
}
?>

