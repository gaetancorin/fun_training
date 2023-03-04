<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur:
// http://localhost:8000/loto.php

session_start();

$tirage = [];
$resultat = '';
$userNumbers = [];
$file = 'tirages.json';

// Historique
$historique = [];
if (file_exists($file)) {
    $historique = json_decode(file_get_contents($file), true);
}

// Initialiser l'argent si pas déjà fait
if (!isset($_SESSION['argent'])) {
    $_SESSION['argent'] = 100;
}

// Gains selon nombre de bons numéros
$gains = [
    0 => 0,
    1 => 1,
    2 => 3,
    3 => 5,
    4 => 20,
    5 => 100,
    6 => 1000
];

// Fonction pour jouer un tirage
function playLoto(&$argent, &$historique, $userNumbers, $gains, $file) {
    $tirage = [];
    while (count($tirage) < 6) {
        $num = random_int(1, 49);
        if (!in_array($num, $tirage)) $tirage[] = $num;
    }

    $userNumbers = array_map('intval', $userNumbers);
    $userNumbers = array_unique($userNumbers);

    $correct = array_intersect($tirage, $userNumbers);
    $countCorrect = count($correct);

    $gain = $gains[$countCorrect] ?? 0;
    $argent -= 1; // coût du ticket
    $argent += $gain;

    $historique[] = [
        'user' => $userNumbers,
        'tirage' => $tirage,
        'correct' => $countCorrect,
        'gain' => $gain,
        'argent' => $argent,
        'date' => date('Y-m-d H:i:s')
    ];

    file_put_contents($file, json_encode($historique));

    return "Tirage : " . implode(', ', $tirage) . " | Corrects : $countCorrect | Gain : $gain € | Argent : $argent €";
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $userNumbers = $_POST['numbers'] ?? [1,2,3,4,5,6];

    // Si autoplay
    if (isset($_POST['autoplay'])) {
        // On va utiliser un refresh automatique via JS
        $_SESSION['autoplay'] = true;
    } else {
        $_SESSION['autoplay'] = false;
        $resultat = playLoto($_SESSION['argent'], $historique, $userNumbers, $gains, $file);
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Loto PHP Autoplay</title>
<style>
body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; padding-top: 30px; }
.container { background: white; padding: 20px 30px; border-radius: 10px; box-shadow: 0 0 10px #ccc; width: 500px; text-align: center; }
input { width: 50px; padding: 5px; margin: 5px; text-align: center; font-size: 16px; }
button { padding: 10px 20px; margin-top: 10px; font-size: 16px; cursor: pointer; }
.result { margin-top: 15px; font-weight: bold; }
.history { margin-top: 20px; text-align: left; max-height: 200px; overflow-y: auto; background: #f9f9f9; padding: 10px; border-radius: 5px; }
.argent { font-weight: bold; margin-bottom: 15px; }
</style>
<?php if ($_SESSION['autoplay'] && $_SESSION['argent'] > 0): ?>
<meta http-equiv="refresh" content="1">
<?php endif; ?>
</head>
<body>
<div class="container">
    <h2>🎲 Loto Autoplay</h2>

    <div class="argent">💰 Argent : <?= $_SESSION['argent'] ?> €</div>

    <form method="POST">
        <p>Choisissez 6 numéros entre 1 et 49 :</p>
        <?php for ($i = 0; $i < 6; $i++): ?>
            <input type="number" name="numbers[]" min="1" max="49" required value="<?= $userNumbers[$i] ?? ($i+1) ?>">
        <?php endfor; ?>
        <br>
        <button type="submit" name="play">Tirer les numéros</button>
        <button type="submit" name="autoplay">▶ Autoplay</button>
    </form>

    <?php if ($resultat !== ''): ?>
        <div class="result"><?= $resultat ?></div>
    <?php endif; ?>

    <div class="history">
        <h3>📜 Historique des tirages</h3>
        <?php if (!empty($historique)): ?>
            <?php foreach (array_reverse($historique) as $entry): ?>
                <p>
                    <strong><?= $entry['date'] ?></strong> - Vos numéros : <?= implode(', ', $entry['user']) ?> | Tirage : <?= implode(', ', $entry['tirage']) ?> | Corrects : <?= $entry['correct'] ?> | Gain : <?= $entry['gain'] ?> € | Argent : <?= $entry['argent'] ?> €
                </p>
            <?php endforeach; ?>
        <?php else: ?>
            <p>Aucun tirage pour l'instant.</p>
        <?php endif; ?>
    </div>

    <?php if ($_SESSION['autoplay'] && $_SESSION['argent'] <= 0): ?>
        <div class="result" style="color:red; margin-top:15px;">💸 Plus d'argent ! Autoplay arrêté.</div>
        <?php $_SESSION['autoplay'] = false; ?>
    <?php endif; ?>
</div>
</body>
</html>