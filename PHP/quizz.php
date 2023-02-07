<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur http://localhost:8000/mini_quiz.php

session_start();

$questions = [
    [
        'question' => 'Quelle est la capitale de la France ?',
        'options' => ['Paris', 'Madrid', 'Berlin', 'Rome'],
        'answer' => 0
    ],
    [
        'question' => 'Combien de continents y a-t-il ?',
        'options' => ['5', '6', '7', '8'],
        'answer' => 2
    ],
    [
        'question' => 'Quel langage est utilisé côté serveur pour ce projet ?',
        'options' => ['PHP', 'Python', 'JavaScript', 'Java'],
        'answer' => 0
    ]
];

if (!isset($_SESSION['score'])) {
    $_SESSION['score'] = 0;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $q = (int)$_POST['question'];
    $choice = (int)$_POST['choice'];

    if ($choice === $questions[$q]['answer']) {
        $_SESSION['score']++;
        $feedback = "✅ Correct !";
    } else {
        $feedback = "❌ Incorrect ! La bonne réponse était : " . $questions[$q]['options'][$questions[$q]['answer']];
    }

    $nextQuestion = $q + 1;
    if ($nextQuestion >= count($questions)) {
        $finished = true;
        $score = $_SESSION['score'];
        session_destroy();
    }
}
?>

