<?php
// Pour lancer : php -S localhost:8000
// Puis aller sur : http://localhost:8000/habit_tracker.php

session_start();

$file = 'habits.json';
$habits = file_exists($file) ? json_decode(file_get_contents($file), true) : [];

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

    if (isset($_POST['check'])) {
        $habit = $_POST['habit'];
        $date = date('Y-m-d');
        $habits[$habit][$date] = true;
        file_put_contents($file, json_encode($habits));
    }

    if (isset($_POST['delete'])) {
        $habit = $_POST['habit'];
        unset($habits[$habit]);
        file_put_contents($file, json_encode($habits));
    }
}

function last7days() {
    $days = [];
    for ($i = 6; $i >= 0; $i--) {
        $days[] = date('Y-m-d', strtotime("-$i days"));
    }
    return $days;
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>📋 Habit Tracker</title>
<style>
body { font-family: Arial; background: #f0f0f0; display:flex; justify-content:center; padding-top:30px;}
.container { background:white; padding:20px 30px; border-radius:10px; box-shadow:0 0 10px #ccc; width:600px;}
h2 { text-align:center; }
form { margin-bottom: 15px; }
input { padding:5px; font-size:16px; width:70%; }
button { padding:5px 10px; font-size:16px; margin-left:5px; cursor:pointer;}
.habit { margin-bottom:20px; background:#f9f9f9; padding:10px; border-radius:5px;}
.habit-header { display:flex; justify-content: space-between; align-items:center; }
.done { color: green; font-weight:bold; }
.message { margin:10px 0; font-weight:bold; color:green;}
.grid { margin-top:5px; display:flex; gap:5px;}
.cell { width:30px; height:30px; display:flex; justify-content:center; align-items:center; border-radius:3px; background:#ddd;}
.cell.done { background: #4caf50; color:white;}
</style>
</head>
<body>
<div class="container">
<h2>📋 Habit Tracker</h2>

<?php if($message !== ''): ?>
<div class="message"><?= $message ?></div>
<?php endif; ?>

<form method="POST">
    <input type="text" name="habit_name" placeholder="Nouvelle habitude" required>
    <button type="submit" name="add_habit">➕ Ajouter</button>
</form>

<?php if(!empty($habits)): ?>
    <?php foreach($habits as $habit => $days): ?>
        <div class="habit">
            <div class="habit-header">
                <div>
                    <strong><?= htmlspecialchars($habit) ?></strong>
                    (<?= count($days) ?> jour<?= count($days) > 1 ? 's' : '' ?>)
                </div>
                <div>
                    <?php if(!isset($days[date('Y-m-d')])): ?>
                        <form method="POST" style="display:inline;">
                            <input type="hidden" name="habit" value="<?= htmlspecialchars($habit) ?>">
                            <button type="submit" name="check">✅ Aujourd'hui</button>
                        </form>
                    <?php else: ?>
                        <span class="done">✔ Fait aujourd'hui</span>
                    <?php endif; ?>
                    <form method="POST" style="display:inline;">
                        <input type="hidden" name="habit" value="<?= htmlspecialchars($habit) ?>">
                        <button type="submit" name="delete">🗑️ Supprimer</button>
                    </form>
                </div>
            </div>

            <div class="grid">
                <?php foreach(last7days() as $day): ?>
                    <div class="cell <?= isset($days[$day]) ? 'done' : '' ?>" title="<?= $day ?>">
                        <?= date('d', strtotime($day)) ?>
                    </div>
                <?php endforeach; ?>
            </div>
        </div>
    <?php endforeach; ?>
<?php else: ?>
<p>Aucune habitude pour l'instant. Ajoutez-en une !</p>
<?php endif; ?>
</div>
</body>
</html>
