<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/my_bank.php

session_start();

// Initialiser le solde et l'historique si ce n'est pas déjà fait
if (!isset($_SESSION['solde'])) $_SESSION['solde'] = 100;
if (!isset($_SESSION['historique'])) $_SESSION['historique'] = [];

// Gestion du POST pour dépôt, retrait ou emprunt
$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $montant = (float) ($_POST['montant'] ?? 0);
    $action = $_POST['action'] ?? '';

    if ($montant <= 0) {
        $message = "⚠ Montant invalide.";
    } else {
        switch($action) {
            case 'depot':
                $_SESSION['solde'] += $montant;
                $_SESSION['historique'][] = [
                    'type' => 'Dépôt',
                    'montant' => $montant,
                    'date' => date('Y-m-d H:i:s')
                ];
                $message = "✅ Vous avez déposé $montant €.";
                break;
            case 'retrait':
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
                break;
            case 'emprunt':
                $_SESSION['solde'] += $montant;
                $_SESSION['historique'][] = [
                    'type' => 'Emprunt',
                    'montant' => $montant,
                    'date' => date('Y-m-d H:i:s')
                ];
                $message = "💵 Vous avez emprunté $montant €.";
                break;
        }
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>💰 My Bank</title>
<style>
body { font-family: Arial; background: #f0f0f0; display:flex; justify-content:center; padding-top:50px;}
.container { background:white; padding:20px 30px; border-radius:10px; box-shadow:0 0 10px #ccc; width:400px; text-align:center;}
input { padding:10px; margin:5px 0; width:80%; font-size:16px;}
button { padding:10px 20px; margin:5px; font-size:16px; cursor:pointer;}
.solde { font-weight:bold; margin-bottom:15px; font-size:18px;}
.message { margin-top:10px; font-weight:bold; color:green;}
.history { margin-top:20px; text-align:left; max-height:200px; overflow-y:auto; background:#f9f9f9; padding:10px; border-radius:5px;}
</style>
</head>
<body>
<div class="container">
<h2>💰 My Bank</h2>
<div class="solde">Solde actuel : <?= $_SESSION['solde'] ?> €</div>

<form method="POST">
    <input type="number" step="0.01" name="montant" placeholder="Montant" required>
    <br>
    <button type="submit" name="action" value="depot">Déposer</button>
    <button type="submit" name="action" value="retrait">Retirer</button>
    <button type="submit" name="action" value="emprunt">💵 Emprunter</button>
</form>

<?php if($message !== ''): ?>
<div class="message"><?= $message ?></div>
<?php endif; ?>

<div class="history">
<h3>📜 Historique des transactions</h3>
<?php if(!empty($_SESSION['historique'])): ?>
    <?php foreach(array_reverse($_SESSION['historique']) as $entry): ?>
        <p><strong><?= $entry['date'] ?></strong> - <?= $entry['type'] ?> : <?= $entry['montant'] ?> €</p>
    <?php endforeach; ?>
<?php else: ?>
<p>Aucune transaction pour l'instant.</p>
<?php endif; ?>
</div>
</div>
</body>
</html>
