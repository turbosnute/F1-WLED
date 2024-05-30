<?php
   // start_process.php
   session_start();
   $_SESSION['process_started'] = "succesful";

   $command = '/app/f1wled.py'; // replace with your command

   shell_exec('nohup python3 /app/f1wled.py > /app/op.txt 2>&1 &');
   header('Location: index.php');
?>