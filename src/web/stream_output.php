<?php
// stream_output.php
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');

$filename = "/app/op.txt";
$lastmodif    = 0;
$currentmodif = 0;

ob_start(); // start output buffering

while (true) {
    clearstatcache();
    $currentmodif = filemtime($filename);

    if ($currentmodif !== $lastmodif) {
        $lastmodif = $currentmodif;
        $output = file_get_contents($filename);
        echo "data: $output\n\n";
        ob_flush();
        flush();
    }

    sleep(1);
}
?>