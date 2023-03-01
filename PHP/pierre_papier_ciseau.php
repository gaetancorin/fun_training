<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur:
// http://localhost:8000/pierre_papier_ciseau.php


session_start();

$resultat = "";
$choix = ['Pierre', 'Papier', 'Ciseaux'];

if (!isset($_SESSION['score'])) {
    $_SESSION['score'] = ['victoires' => 0, 'defaites' => 0, 'egalites' => 0];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['player'])) {
    $player = $_POST['player'];
    $computer = $choix[array_rand($choix)];

    if ($player === $computer) {
        $resultat = "🤝 Égalité ! Ordinateur : $computer";
        $_SESSION['score']['egalites']++;
    } elseif (
        ($player === 'Pierre' && $computer === 'Ciseaux') ||
        ($player === 'Papier' && $computer === 'Pierre') ||
        ($player === 'Ciseaux' && $computer === 'Papier')
    ) {
        $resultat = "✅ Vous gagnez ! Ordinateur : $computer";
        $_SESSION['score']['victoires']++;
    } else {
        $resultat = "❌ Vous perdez ! Ordinateur : $computer";
        $_SESSION['score']['defaites']++;
    }
}

if (isset($_POST['reset'])) {
    $_SESSION['score'] = ['victoires' => 0, 'defaites' => 0, 'egalites' => 0];
    $resultat = "🔄 Score réinitialisé.";
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Pierre-Papier-Ciseaux PHP</title>
<style>
body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; padding-top: 50px; }
.game { background: white; padding: 20px 30px; border-radius: 10px; box-shadow: 0 0 10px #ccc; width: 400px; text-align: center; }
button { padding: 10px 20px; margin: 5px; font-size: 16px; cursor: pointer; }
.result { margin-top: 15px; font-weight: bold; }
.score { margin-top: 20px; }
</style>
</head>
<body>
<div class="game">
    <h2>✊ Pierre-Papier-Ciseaux</h2>

    <form method="POST">
        <button name="player" value="Pierre">✊ Pierre</button>
        <button name="player" value="Papier">📄 Papier</button>
        <button name="player" value="Ciseaux">✂️ Ciseaux</button>
    </form>

    <?php if ($resultat !== ""): ?>
        <div class="result"><?= $resultat ?></div>
    <?php endif; ?>

    <div class="score">
        <h3>Score</h3>
        <p>✅ Victoires : <?= $_SESSION['score']['victoires'] ?></p>
        <p>❌ Défaites : <?= $_SESSION['score']['defaites'] ?></p>
        <p>🤝 Égalités : <?= $_SESSION['score']['egalites'] ?></p>

        <form method="POST">
            <button name="reset">🔄 Réinitialiser le score</button>
        </form>
    </div>
</div>
</body>
</html>
