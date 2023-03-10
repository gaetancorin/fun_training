<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/my_bank.php

session_start();

// Initialiser le solde, l'historique et les emprunts
if (!isset($_SESSION['solde'])) $_SESSION['solde'] = 100;
if (!isset($_SESSION['historique'])) $_SESSION['historique'] = [];
if (!isset($_SESSION['emprunts'])) $_SESSION['emprunts'] = []; // tableau des emprunts en cours
$taux_interet = 0.08; // 8% par jour

$message = '';

// Fonction pour calculer les intérêts
function calculerInterets(&$emprunts, $taux) {
    foreach ($emprunts as &$emprunt) {
        $emprunt['jours'] += 1;
        $emprunt['montant_du'] = round($emprunt['montant_initial'] * pow(1 + $taux, $emprunt['jours']), 2);
    }
}

// Gestion du POST
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $montant = (float) ($_POST['montant'] ?? 0);
    $action = $_POST['action'] ?? '';

    switch($action) {
        case 'jour':
            calculerInterets($_SESSION['emprunts'], $taux_interet);
            $message = "📆 Un jour a passé, intérêts appliqués sur tous les emprunts.";
            break;
        case 'depot':
            if ($montant <= 0) { $message = "⚠ Montant invalide."; break; }
            $_SESSION['solde'] += $montant;
            $_SESSION['historique'][] = ['type'=>'Dépôt','montant'=>$montant,'date'=>date('Y-m-d H:i:s')];
            $message = "✅ Vous avez déposé $montant €.";
            break;
        case 'retrait':
            if ($montant <= 0) { $message = "⚠ Montant invalide."; break; }
            if ($montant > $_SESSION['solde']) { $message = "⚠ Solde insuffisant pour retirer $montant €."; break; }
            $_SESSION['solde'] -= $montant;
            $_SESSION['historique'][] = ['type'=>'Retrait','montant'=>$montant,'date'=>date('Y-m-d H:i:s')];
            $message = "✅ Vous avez retiré $montant €.";
            break;
        case 'emprunt':
            if ($montant <= 0) { $message = "⚠ Montant invalide."; break; }
            $_SESSION['solde'] += $montant;
            $_SESSION['emprunts'][] = ['montant_initial'=>$montant,'montant_du'=>$montant,'jours'=>0,'date'=>date('Y-m-d H:i:s')];
            $_SESSION['historique'][] = ['type'=>'Emprunt','montant'=>$montant,'date'=>date('Y-m-d H:i:s')];
            $message = "💵 Vous avez emprunté $montant €.";
            break;
        case 'rembourser':
            if ($montant <= 0) { $message = "⚠ Montant invalide."; break; }
            if ($montant > $_SESSION['solde']) { $message = "⚠ Vous n'avez pas assez d'argent pour rembourser $montant €."; break; }

            // Remboursement sur les emprunts les plus anciens en premier
            foreach ($_SESSION['emprunts'] as $key => &$emprunt) {
                if ($montant <= 0) break;
                if ($emprunt['montant_du'] <= $montant) {
                    $montant -= $emprunt['montant_du'];
                    $_SESSION['solde'] -= $emprunt['montant_du'];
                    $_SESSION['historique'][] = ['type'=>'Remboursement','montant'=>$emprunt['montant_du'],'date'=>date('Y-m-d H:i:s')];
                    unset($_SESSION['emprunts'][$key]);
                } else {
                    $emprunt['montant_du'] -= $montant;
                    $_SESSION['solde'] -= $montant;
                    $_SESSION['historique'][] = ['type'=>'Remboursement','montant'=>$montant,'date'=>date('Y-m-d H:i:s')];
                    $montant = 0;
                }
            }
            // Réindexer le tableau
            $_SESSION['emprunts'] = array_values($_SESSION['emprunts']);
            $message = "💸 Remboursement effectué.";
            break;
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>💰 My Bank avec Emprunts</title>
<style>
body { font-family: Arial; background: #f0f0f0; display:flex; justify-content:center; padding-top:50px;}
.container { background:white; padding:20px 30px; border-radius:10px; box-shadow:0 0 10px #ccc; width:500px; text-align:center;}
input { padding:10px; margin:5px 0; width:80%; font-size:16px;}
button { padding:10px 20px; margin:5px; font-size:16px; cursor:pointer;}
.solde { font-weight:bold; margin-bottom:15px; font-size:18px;}
.message { margin-top:10px; font-weight:bold; color:green;}
.history { margin-top:20px; text-align:left; max-height:200px; overflow-y:auto; background:#f9f9f9; padding:10px; border-radius:5px;}
.emprunts { margin-top:20px; text-align:left; max-height:150px; overflow-y:auto; background:#fff3cd; padding:10px; border-radius:5px;}
</style>
</head>
<body>
<div class="container">
<h2>💰 My Bank avec Emprunts</h2>
<div class="solde">Solde actuel : <?= $_SESSION['solde'] ?> €</div>

<form method="POST">
    <input type="number" step="0.01" name="montant" placeholder="Montant">
    <br>
    <button type="submit" name="action" value="depot">Déposer</button>
    <button type="submit" name="action" value="retrait">Retirer</button>
    <button type="submit" name="action" value="emprunt">💵 Emprunter</button>
    <button type="submit" name="action" value="rembourser">💸 Rembourser</button>
    <button type="submit" name="action" value="jour">⏭ Passer un jour</button>
</form>

<?php if($message !== ''): ?>
<div class="message"><?= $message ?></div>
<?php endif; ?>

<div class="emprunts">
<h3>📌 Emprunts en cours</h3>
<?php if(!empty($_SESSION['emprunts'])): ?>
    <?php foreach($_SESSION['emprunts'] as $e): ?>
        <p>Montant initial : <?= $e['montant_initial'] ?> € | À rembourser : <?= $e['montant_du'] ?> € | Jours : <?= $e['jours'] ?></p>
    <?php endforeach; ?>
<?php else: ?>
<p>Aucun emprunt en cours.</p>
<?php endif; ?>
</div>

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
