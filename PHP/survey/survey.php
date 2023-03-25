<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/survey.php

session_start();

$file = 'current_survey.json';
$message = '';

// Lire le sondage existant
if (!file_exists($file)) {
    die("⚠ Aucun sondage n'est disponible. Créez-en un via create_survey.php.");
}
$survey = json_decode(file_get_contents($file), true);

// Si vote soumis
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $vote = $_POST['vote'] ?? '';
    if ($vote !== '' && in_array($vote, $survey['options'])) {
        $survey['votes'][$vote]++;
        file_put_contents($file, json_encode($survey));
        $message = "✅ Merci pour votre vote pour \"$vote\" !";
    } else {
        $message = "⚠ Option invalide.";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>🗳️ Sondage</title>
<style>
body { font-family: Arial; background: #f0f0f0; display:flex; justify-content:center; padding-top:50px; }
.container { background:white; padding:20px 30px; border-radius:10px; box-shadow:0 0 10px #ccc; width:500px; text-align:center;}
button { padding:10px 20px; margin:5px; font-size:16px; cursor:pointer;}
.message { margin:10px 0; font-weight:bold; color:green;}
.results { margin-top:20px; text-align:left; max-height:200px; overflow-y:auto; background:#f9f9f9; padding:10px; border-radius:5px;}
</style>
</head>
<body>
<div class="container">
<h2>🗳️ <?= htmlspecialchars($survey['title']) ?></h2>

<?php if($message !== ''): ?>
<div class="message"><?= $message ?></div>
<?php endif; ?>

<form method="POST">
    <?php foreach($survey['options'] as $option): ?>
        <button type="submit" name="vote" value="<?= htmlspecialchars($option) ?>"><?= htmlspecialchars($option) ?></button>
    <?php endforeach; ?>
</form>

<div class="results">
<h3>📊 Résultats actuels :</h3>
<ul>
    <?php foreach($survey['votes'] as $opt => $count): ?>
        <li><?= htmlspecialchars($opt) ?> : <?= $count ?> vote<?= $count > 1 ? 's' : '' ?></li>
    <?php endforeach; ?>
</ul>
</div>
</div>
</body>
</html>
