<?php
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