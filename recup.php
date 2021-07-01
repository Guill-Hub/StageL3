<p>Bonjour !</p>

<p>Je sais comment tu t'appelles, hé hé. Tu t'appelles <?php echo $_POST['json']; ?> !</p>

<?php

file_put_contents('donnees.json', $_POST['json']);

?>
