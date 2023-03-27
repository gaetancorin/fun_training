<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/survey/create_survey.php

session_start();

$file = 'current_survey.json';
$message = '';

// Si formulaire soumis
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $title = trim($_POST['title'] ?? '');
    $options = trim($_POST['options'] ?? '');

    if ($title === '' || $options === '') {
        $message = "⚠ Veuillez remplir le titre et les options.";
    } else {
        $optionsArray = array_map('trim', explode(',', $options));
        $survey = [
            'title' => $title,
            'options' => $optionsArray,
            'votes' => array_fill_keys($optionsArray, 0)
        ];
        file_put_contents($file, json_encode($survey));
        $message = "✅ Sondage créé avec succès !";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>📝 Créer un sondage</title>
<style>
body { font-family: Arial; background: #f0f0f0; display:flex; justify-content:center; padding-top:50px; }
.container { background:white; padding:20px 30px; border-radius:10px; box-shadow:0 0 10px #ccc; width:500px; text-align:center;}
input, textarea { padding:10px; margin:5px 0; width:90%; font-size:16px;}
button { padding:10px 20px; margin:5px; font-size:16px; cursor:pointer;}
.message { margin:10px 0; font-weight:bold; color:green;}
</style>
</head>
<body>
<div class="container">
<h2>📝 Créer un nouveau sondage</h2>

<?php if($message !== ''): ?>
<div class="message"><?= $message ?></div>
<?php endif; ?>

<form method="POST">
    <input type="text" name="title" placeholder="Titre du sondage" required>
    <br>
    <textarea name="options" placeholder="Options séparées par des virgules (ex: PHP,Python,JavaScript)" required></textarea>
    <br>
    <button type="submit">Créer le sondage</button>
</form>

<!-- Bouton pour aller vers survey.php -->
<form method="GET" action="survey.php">
    <button type="submit">📊 Aller voter sur le sondage</button>
</form>

<?php if(file_exists($file)):
    $survey = json_decode(file_get_contents($file), true); ?>
    <h3>Sondage actuel :</h3>
    <p><strong><?= htmlspecialchars($survey['title']) ?></strong></p>
    <ul>
    <?php foreach ($survey['options'] as $opt): ?>
        <li><?= htmlspecialchars($opt) ?> (<?= $survey['votes'][$opt] ?? 0 ?> votes)</li>
    <?php endforeach; ?>
    </ul>
<?php endif; ?>
</div>
</body>
</html>
