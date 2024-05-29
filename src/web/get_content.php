<?php
// get_content.php
$filename = "/app/op.txt";
if (file_exists($filename)) {
    $content = file_get_contents($filename);
    //echo nl2br($content); // convert newlines to <br> for HTML display
    echo $content;
} else {
    echo "File not found.";
}
?>