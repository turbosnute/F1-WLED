<?php
    // check_process.php
    session_start();

    $processName = 'f1wled\.py'; // the process name
    $output = array();
    exec("pgrep -f '$processName'", $output); // execute the pgrep command
    
    // if the output is not empty, the process is running
    if (!empty($output)) {
        echo "<a type='button' href='stop_process.php' class='btn btn-danger'>Stop F1-WLED</a>"; #<p><span style='color:green; font-weight:bold;'>Running</span></p>";
    } else {
        echo "<a type='button' href='start_process.php' class='btn btn-success'>Start F1-WLED</a>"; #<p><span style='color:red;'>Not Running</span></p>";
    }
?>