<p>Bonjour !</p>

<p>Je sais comment tu t'appelles, hé hé. Tu t'appelles !</p>

<?php

$fp = fopen('results.json', 'a');
fwrite($fp, json_encode($_POST, JSON_PRETTY_PRINT));   // here it will print the array pretty
fclose($fp);
?>
