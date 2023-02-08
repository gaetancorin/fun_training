<?php
// Pour lancer, écrire dans le terminal :
// php -S localhost:8000
// Puis aller sur:
// http://localhost:8000/quizz.php

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


<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Mini Quiz PHP</title>
<style>
body { font-family: Arial; display: flex; justify-content: center; padding-top: 50px; background: #f0f0f0; }
.quiz { background: white; padding: 20px 30px; border-radius: 10px; box-shadow: 0 0 10px #ccc; width: 500px; }
button { padding: 10px 20px; margin-top: 10px; font-size: 16px; }
</style>
</head>
<body>
<div class="quiz">
    <h2>📝 Mini Quiz</h2>

    <?php if (!isset($finished) || !$finished): ?>
        <?php $current = isset($nextQuestion) ? $nextQuestion : 0; ?>
        <form method="POST">
            <p><strong>Question <?= $current + 1 ?>:</strong> <?= $questions[$current]['question'] ?></p>
            <?php foreach ($questions[$current]['options'] as $i => $opt): ?>
                <label>
                    <input type="radio" name="choice" value="<?= $i ?>" required>
                    <?= $opt ?>
                </label><br>
            <?php endforeach; ?>
            <input type="hidden" name="question" value="<?= $current ?>">
            <button type="submit">Valider</button>
        </form>
        <?php if (isset($feedback)) echo "<p>$feedback</p>"; ?>
    <?php else: ?>
        <h3>🎉 Quiz terminé !</h3>
        <p>Votre score : <?= $score ?> / <?= count($questions) ?></p>
        <a href="quizz.php"><button>Recommencer</button></a>
    <?php endif; ?>
</div>
</body>
</html>
