<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/habit_tracker.php

session_start();

// Fichier pour stocker les habitudes
$file = 'habits.json';
$habits = file_exists($file) ? json_decode(file_get_contents($file), true) : [];

// Ajouter une nouvelle habitude
$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['add_habit'])) {
        $name = trim($_POST['habit_name'] ?? '');
        if ($name === '') {
            $message = "⚠ Veuillez entrer un nom d'habitude.";
        } else {
            $habits[$name] = $habits[$name] ?? [];
            file_put_contents($file, json_encode($habits));
            $message = "✅ Habitude '$name' ajoutée !";
        }
    }

    // Marquer un jour comme accompli
    if (isset($_POST['check'])) {
        $habit = $_POST['habit'];
        $date = date('Y-m-d');
        $habits[$habit][$date] = true;
        file_put_contents($file, json_encode($habits));
    }

    // Supprimer une habitude
    if (isset($_POST['delete'])) {
        $habit = $_POST['habit'];
        unset($habits[$habit]);
        file_put_contents($file, json_encode($habits));
    }
}
?>


