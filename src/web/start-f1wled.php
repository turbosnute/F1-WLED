<?php



    // set all the variables to the environment variables using shell_exec(). This is vunerable for injection and should be washed first
    $command = "export WLED_GREEN=$wled_green; export WLED_YELLOW=$wled_yellow; export WLED_RED=$wled_red; export WLED_SC=$wled_sc; export WLED_CHECKERED=$wled_checkered; export WLED_CLEAR=$wled_clear; export WLED_HOST=$wled_host; export WLED_DELAY=$wled_delay";
    #shell_exec($command);

    #$command = "export VAR1=value1; export VAR2=value2; export VAR3=value3; python3 my_script.py";
    #shell_exec($command);


?>