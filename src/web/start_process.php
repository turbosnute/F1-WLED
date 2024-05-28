<?php
// start_process.php
$command = '/app/f1wled.py'; // replace with your command
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("file", "/app/log.txt", "w") // stdout is a file to write to
);
$process = proc_open($command) //, $descriptorspec, $pipes);
?>