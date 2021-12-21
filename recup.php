<?php

$fp = fopen('results2.json', 'a');
fwrite($fp, json_encode($_POST, JSON_PRETTY_PRINT));   // here it will print the array pretty
fclose($fp);
?>
