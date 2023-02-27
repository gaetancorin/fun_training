<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur http://localhost:8000/loto.php

$tirage = [];
$resultat = '';
$userNumbers = [];
$file = 'tirages.json';

// Charger l'historique
$historique = [];
if (file_exists($file)) {
    $historique = json_decode(file_get_contents($file), true);
}

// Tirage et vérification
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Tirage aléatoire 6 numéros uniques
    $tirage = [];
    while (count($tirage) < 6) {
        $num = random_int(1, 49);
        if (!in_array($num, $tirage)) {
            $tirage[] = $num;
        }
    }

    // Numéros choisis par l'utilisateur
    $userNumbers = array_map('intval', $_POST['numbers']);
    $userNumbers = array_unique($userNumbers);

    // Vérification
    $correct = array_intersect($tirage, $userNumbers);
    $countCorrect = count($correct);

    if ($countCorrect === 6) {
        $resultat = "🎉 Jackpot ! Tous les numéros sont corrects : " . implode(', ', $tirage);
    } else {
        $resultat = "Vous avez trouvé $countCorrect numéro(s) : " . implode(', ', $correct);
        $resultat .= "<br>Numéros tirés : " . implode(', ', $tirage);
    }

    // Ajouter au fichier historique
    $historique[] = [
        'user' => $userNumbers,
        'tirage' => $tirage,
        'correct' => $countCorrect,
        'date' => date('Y-m-d H:i:s')
    ];
    file_put_contents($file, json_encode($historique));
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Loto PHP</title>
<style>
body { font-family: Arial; background: #f0f0f0; display: flex; justify-content: center; padding-top: 30px; }
.container { background: white; padding: 20px 30px; border-radius: 10px; box-shadow: 0 0 10px #ccc; width: 500px; text-align: center; }
input { width: 50px; padding: 5px; margin: 5px; text-align: center; font-size: 16px; }
button { padding: 10px 20px; margin-top: 10px; font-size: 16px; cursor: pointer; }
.result { margin-top: 15px; font-weight: bold; }
.history { margin-top: 20px; text-align: left; max-height: 200px; overflow-y: auto; background: #f9f9f9; padding: 10px; border-radius: 5px; }
</style>
</head>
<body>
<div class="container">
    <h2>🎲 Loto</h2>

    <form method="POST">
        <p>Choisissez 6 numéros entre 1 et 49 :</p>
        <?php for ($i = 0; $i < 6; $i++): ?>
            <input type="number" name="numbers[]" min="1" max="49" required value="<?= $userNumbers[$i] ?? '' ?>">
        <?php endfor; ?>
        <br>
        <button type="submit">Tirer les numéros</button>
    </form>

    <?php if ($resultat !== ''): ?>
        <div class="result"><?= $resultat ?></div>
    <?php endif; ?>

    <div class="history">
        <h3>📜 Historique des tirages</h3>
        <?php if (!empty($historique)): ?>
            <?php foreach (array_reverse($historique) as $entry): ?>
                <p>
                    <strong><?= $entry['date'] ?></strong> - Vos numéros : <?= implode(', ', $entry['user']) ?> | Tirage : <?= implode(', ', $entry['tirage']) ?> | Corrects : <?= $entry['correct'] ?>
                </p>
            <?php endforeach; ?>
        <?php else: ?>
            <p>Aucun tirage pour l'instant.</p>
        <?php endif; ?>
    </div>
</div>
</body>
</html>