<?php
    // Get the current time
    $now = new DateTime();

    // Get the number of minutes and seconds since the latest full hour
    $minutes = $now->format('i');
    $seconds = $now->format('s');

    // Calculate the total number of seconds since the latest full hour
    $totalSeconds = $minutes * 60 + $seconds;

    // Calculate the number of seconds since the last half hour
    $secondsSinceLastHalfHour = $totalSeconds % 1800;

    $wled_delay = $secondsSinceLastHalfHour;

    $client_config_path = "/config/config.json";
    $config_data = file_get_contents($client_config_path);
    $config = json_decode($config_data);

    // Update the config object
    $config->wled_delay = $wled_delay;

    // Convert the updated config object back to JSON
    $config_data = json_encode($config);

    // Save the updated config data to the config file
    file_put_contents($client_config_path, $config_data);

    header('Location: index.php');
?>