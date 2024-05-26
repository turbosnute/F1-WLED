<?php
    // check_process.php
    $processName = '^python3 \./f1wled\.py'; // the process name
    $output = array();
    exec("pgrep -f '$processName'", $output); // execute the pgrep command
    
    // if the output is not empty, the process is running
    if (!empty($output)) {
        echo "Running";
    } else {
        echo "Not running";
    }
?>