<?php
// Pour lancer, ecrire dans le terminal:
// php -S localhost:8000
// Puis aller sur
// http://localhost:8000/todolist.php
$file = 'taches.json';

$taches = [];
if (file_exists($file)) {
    $taches = json_decode(file_get_contents($file), true);
}

if (isset($_POST['nouvelle_tache']) && $_POST['nouvelle_tache'] !== '') {
    $taches[] = [
        'texte' => $_POST['nouvelle_tache'],
        'faite' => false
    ];
    file_put_contents($file, json_encode($taches));
}

if (isset($_GET['supprimer'])) {
    $index = (int)$_GET['supprimer'];
    if (isset($taches[$index])) {
        array_splice($taches, $index, 1);
        file_put_contents($file, json_encode($taches));
    }
}

if (isset($_GET['toggle'])) {
    $index = (int)$_GET['toggle'];
    if (isset($taches[$index])) {
        $taches[$index]['faite'] = !$taches[$index]['faite'];
        file_put_contents($file, json_encode($taches));
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Mini To-Do List PHP</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            display: flex;
            justify-content: center;
            padding-top: 50px;
        }
        .todolist {
            background: white;
            padding: 20px 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px #ccc;
            width: 400px;
        }
        input, button {
            padding: 10px;
            margin: 5px 0;
            font-size: 16px;
        }
        ul {
            list-style: none;
            padding-left: 0;
        }
        li {
            margin: 8px 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        li.fait {
            text-decoration: line-through;
            color: gray;
        }
        a {
            margin-left: 10px;
            text-decoration: none;
            color: red;
        }
    </style>
</head>
<body>
<div class="todolist">
    <h2>📝 Mini To-Do List</h2>
    <form method="POST">
        <input type="text" name="nouvelle_tache" placeholder="Nouvelle tâche" required>
        <button type="submit">Ajouter</button>
    </form>

    <ul>
        <?php foreach ($taches as $index => $tache): ?>
            <li class="<?= $tache['faite'] ? 'fait' : '' ?>">
                <span><?= htmlspecialchars($tache['texte']) ?></span>
                <div>
                    <a href="?toggle=<?= $index ?>">✔️</a>
                    <a href="?supprimer=<?= $index ?>">❌</a>
                </div>
            </li>
        <?php endforeach; ?>
    </ul>
</div>
</body>
</html>