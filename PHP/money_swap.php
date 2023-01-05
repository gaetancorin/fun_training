<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur
// http://localhost:8000/money_swap.php

$devises = [
    'EUR' => 1,
    'USD' => 1.1,
    'GBP' => 0.85,
    'JPY' => 145
];

$resultat = '';

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $montant = (float) $_POST['montant'];
    $from = $_POST['from'];
    $to = $_POST['to'];

    if (isset($devises[$from]) && isset($devises[$to])) {
        $resultat = $montant * ($devises[$to] / $devises[$from]);
        $resultat = number_format($resultat, 2);
    } else {
        $resultat = "Erreur : devise inconnue";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>💱 MoneySwap - Convertisseur de devises</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: #e0f7fa;
    display: flex;
    justify-content: center;
    padding-top: 50px;
}
.money-swap {
    background: white;
    padding: 25px 35px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    width: 400px;
}
h2 {
    text-align: center;
    margin-bottom: 20px;
}
input, select, button {
    width: 100%;
    padding: 12px;
    margin: 6px 0;
    font-size: 16px;
    border-radius: 6px;
    border: 1px solid #ccc;
}
button {
    background: #00796b;
    color: white;
    border: none;
    cursor: pointer;
    font-weight: bold;
}
button:hover {
    background: #004d40;
}
.resultat {
    margin-top: 20px;
    font-weight: bold;
    font-size: 18px;
    text-align: center;
}
</style>
</head>
<body>
<div class="money-swap">
    <h2>💱 MoneySwap</h2>
    <form method="POST">
        <input type="number" step="any" name="montant" placeholder="Montant" required>
        <select name="from" required>
            <?php foreach ($devises as $dev => $rate) echo "<option value='$dev'>$dev</option>"; ?>
        </select>
        <select name="to" required>
            <?php foreach ($devises as $dev => $rate) echo "<option value='$dev'>$dev</option>"; ?>
        </select>
        <button type="submit">Convertir</button>
    </form>

    <?php if ($resultat !== ''): ?>
        <div class="resultat">
            <?= htmlspecialchars($montant) ?> <?= $_POST['from'] ?> = <?= $resultat ?> <?= $_POST['to'] ?>
        </div>
    <?php endif; ?>
</div>
</body>
</html>