<?php
    $wled_green = (int)$_POST['wled_green'];
    $wled_yellow = (int)$_POST['wled_yellow'];
    $wled_red = (int)$_POST['wled_red'];
    $wled_sc = (int)$_POST['wled_sc'];
    $wled_checkered = (int)$_POST['wled_checkered'];
    $wled_trackclear = (int)$_POST['wled_trackclear'];
    $wled_host = $_POST['wled_host'];
    $wled_delay = (int)$_POST['wled_delay'];
    
    // Check if variables is numeric:
    if (!is_numeric($wled_green) || !is_numeric($wled_yellow) || !is_numeric($wled_red) || !is_numeric($wled_sc) || !is_numeric($wled_checkered) || !is_numeric($wled_trackclear) || !is_numeric($wled_delay)) {
        die("Invalid input! Please enter a number for the delay and the colors.");
    }

    $config_file_content = "{
        \"wled_green\": $wled_green,
        \"wled_yellow\": $wled_yellow,
        \"wled_red\": $wled_red,
        \"wled_sc\": $wled_sc,
        \"wled_checkered\": $wled_checkered,
        \"wled_trackclear\": $wled_trackclear,
        \"wled_host\": \"$wled_host\",
        \"wled_delay\": $wled_delay
    }";

    $client_config_path = "/config/config.json";
    $file = fopen($client_config_path, "w") or die("Unable to open or create config file! ($client_config_path)");
    fwrite($file, $config_file_content);
    fclose($file);

    
    header('Location: index.php?saved=succesful');
?>