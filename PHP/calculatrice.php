<?php
// Pour lancer, ecrire dans le terminal: php -S localhost:8000
// Puis aller sur:
// http://localhost:8000/calculatrice.php
$resultat = "";
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $a = (float) $_POST["a"];
    $b = (float) $_POST["b"];
    $op = $_POST["op"];

    switch ($op) {
        case '+':
            $resultat = $a + $b;
            break;
        case '-':
            $resultat = $a - $b;
            break;
        case '*':
            $resultat = $a * $b;
            break;
        case '/':
            $resultat = $b != 0 ? $a / $b : "Erreur : division par 0";
            break;
        case '%':
            $resultat = $a * $b / 100;
            break;
        case '√':
            $resultat = $a >= 0 ? sqrt($a) : "Erreur : nombre négatif";
            break;
        case '^':
            $resultat = pow($a, $b);
            break;
        default:
            $resultat = "Opération invalide";
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Mini Calculatrice PHP</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        form {
            background: white;
            padding: 20px 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px #ccc;
            text-align: center;
        }
        input, select, button {
            margin: 5px;
            padding: 10px;
            font-size: 16px;
        }
        .resultat {
            margin-top: 15px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<form method="POST">
    <h2>🧮 Mini Calculatrice</h2>

    <input type="number" step="any" name="a" required placeholder="Nombre 1">
    <select name="op">
        <option value="+">+</option>
        <option value="-">−</option>
        <option value="*">×</option>
        <option value="/">÷</option>
        <option value="%">%</option>
        <option value="√">√</option>
        <option value="^">^</option>
    </select>
    <input type="number" step="any" name="b" placeholder="Nombre 2 (ignoré pour √)">
    <br>
    <button type="submit">Calculer</button>

    <?php if ($resultat !== ""): ?>
        <div class="resultat">
            ✅ Résultat : <strong><?= htmlspecialchars($resultat) ?></strong>
        </div>
    <?php endif; ?>
</form>

</body>
</html>
