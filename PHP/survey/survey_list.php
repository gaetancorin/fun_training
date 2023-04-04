<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/survey_list.php

session_start();

$dir = __DIR__ . '/surveys';
if (!is_dir($dir)) mkdir($dir);

$files = array_diff(scandir($dir), ['.','..']);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>📋 Liste des sondages</title>
<style>
body { font-family: Arial; background:#f0f0f0; display:flex; justify-content:center; padding-top:50px;}
.container { background:white; padding:20px 30px; border-radius:10px; box-shadow:0 0 10px #ccc; width:500px; text-align:center;}
button { padding:10px 20px; margin:5px; font-size:16px; cursor:pointer;}
</style>
</head>
<body>
<div class="container">
<h2>📋 Liste des sondages</h2>

<?php if(empty($files)): ?>
    <p>Aucun sondage disponible. <a href="create_survey.php">Créer un sondage</a></p>
<?php else: ?>
    <?php foreach($files as $file): ?>
        <form method="GET" action="survey.php">
            <input type="hidden" name="file" value="<?= htmlspecialchars($file) ?>">
            <button type="submit"><?= htmlspecialchars(pathinfo($file, PATHINFO_FILENAME)) ?></button>
        </form>
    <?php endforeach; ?>
<?php endif; ?>

<br>
<form method="GET" action="create_survey.php">
    <button type="submit">📝 Créer un nouveau sondage</button>
</form>
</div>
</body>
</html>
