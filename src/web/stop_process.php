<?php
    session_start();
    $_SESSION['process_killed'] = "succesful";
    shell_exec("pkill -f f1wled.py");
    header('Location: index.php');
?>