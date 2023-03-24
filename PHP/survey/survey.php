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

    $votes[$choix]++;
    file_put_contents($file, json_encode($votes));
    $message = "✅ Merci pour votre vote !";
}

// Calcul du total pour le pourcentage
$totalVotes = array_sum($votes);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>📊 Survey PHP</title>
<style>
body { font-family: Arial; background: #f0f0f0; display:flex; justify-content:center; padding-top:50px; }
.container { background:white; padding:20px 30px; border-radius:10px; box-shadow:0 0 10px #ccc; width:500px; text-align:center;}
button { padding:10px 20px; margin:5px; font-size:16px; cursor:pointer;}
.message { margin:10px 0; font-weight:bold; color:green;}
.bar { height:20px; background:#00796b; margin:5px 0; color:white; text-align:center; line-height:20px; border-radius:5px;}
</style>
</head>
<body>
<div class="container">
<h2>📊 Survey : Quel est ton langage préféré ?</h2>

<?php if($message !== ''): ?>
<div class="message"><?= $message ?></div>
<?php endif; ?>

<form method="POST">
    <button type="submit" name="choix" value="PHP">PHP</button>
    <button type="submit" name="choix" value="Python">Python</button>
    <button type="submit" name="choix" value="JavaScript">JavaScript</button>
    <button type="submit" name="choix" value="Autre">Autre</button>
</form>

<h3>📊 Résultats :</h3>
<?php foreach ($votes as $option => $count):
    $percent = $totalVotes > 0 ? round($count / $totalVotes * 100) : 0;
?>
<div><?= $option ?> : <?= $count ?> vote<?= $count>1?'s':'' ?> (<?= $percent ?>%)</div>
<div class="bar" style="width:<?= $percent ?>%"><?= $percent ?>%</div>
<?php endforeach; ?>

<p>Total votes : <?= $totalVotes ?></p>
</div>
</body>
</html>
