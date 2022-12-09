<?php
// Pour lancer, dans le terminal: php -S localhost:8000
// Puis aller sur http://localhost:8000/calculatrice.php
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
        default:
            $resultat = "Opération invalide";
    }
}
?>

