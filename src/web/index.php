<?php
    session_start();
    /* Check if config is available (in config file). */
    $config_path = "/config/config.json";
    
    /*
    $config_file_content = "{
        \"wled_green\": 4,
        \"wled_yellow\": 2,
        \"wled_red\": 3,
        \"wled_sc\": 5,
        \"wled_checkered\": 7,
        \"wled_clear\": 6,
        \"wled_host\": \"192.168.1.144\",
        \"wled_delay\": 45
    }";
    */
    if (!file_exists($config_path)) {
        file_put_contents($config_path, '');
    }
    $file = fopen($config_path, "r") or die("Unable to open or create config file! ($config_path)");
    $filesize = filesize($config_path);

    if ($filesize > 0) {
        $config_data = fread($file,$filesize);
        $config = json_decode($config_data, true);
    } else {
        // probably no config
        $config = null;
    }
    fclose($file);

    // Initialize the variables
    $wled_green = "";
    $wled_yellow = "";
    $wled_red = "";
    $wled_sc = "";
    $wled_checkered = "";
    $wled_clear = "";
    $wled_host = "";
    $wled_delay = 45; # Default

    // Get the values from the config file
    if (isset($config['wled_green'])) {
        $wled_green = $config['wled_green'];
    }

    if (isset($config['wled_yellow'])) {
        $wled_yellow = $config['wled_yellow'];
    }

    if (isset($config['wled_red'])) {
        $wled_red = $config['wled_red'];
    }

    if (isset($config['wled_sc'])) {
        $wled_sc = $config['wled_sc'];
    }

    if (isset($config['wled_checkered'])) {
        $wled_checkered = $config['wled_checkered'];
    }

    if (isset($config['wled_trackclear'])) {
        $wled_clear = $config['wled_trackclear'];
    }

    if (isset($config['wled_host'])) {
        $wled_host = $config['wled_host'];
    }

    if (isset($config['wled_delay'])) {
        $wled_delay = $config['wled_delay'];
    }

?>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>F1-WLED</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <link href="custom.css" rel="stylesheet">
</head>
  <body class="bg-body-tertiary">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
    <script>
        var slider = document.getElementById("delay");
        var output = document.getElementById("delayvalue");
        output.innerHTML = slider.value;

        slider.oninput = function() {
            output.innerHTML = this.value;
        }
    </script>
    <div class="container">
        <section>
            <h1>F1-WLED</h1>
            <?php if (isset($_SESSION['saved'])) { $_SESSION['saved'] = NULL; ?>
            <div class="flash_message alert alert-success" role="alert">
                Configuration saved.
            </div>
            <?php } elseif (isset($_SESSION['process_started'])) { ?>
            <div class="flash_message alert alert-success" style="z-index:5;position:absolute;top:0;right:0;" role="alert">
                F1-WLED Started.
            </div>
            <?php } elseif (isset($_SESSION['process_killed'])) { $_SESSION['process_killed'] = NULL; ?>
            <div class="flash_message alert alert-danger" style="z-index:5;position:absolute;top:0;right:0;" role="alert">
                F1-WLED Stopped.
            </div>
            <?php } ?>
        </section>
        <section>
            <p class="d-inline-flex gap-1">
                <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseExample" aria-expanded="false" aria-controls="collapseExample">
                    Show Config
                </button><span id="status">We are checking...</span>
            </p>
            <div class="collapse" id="collapseExample">
                <div class="card card-body">
                    <form action="save-config.php" method="post">
                        <input type="hidden" id="confdelay" name="confdelay" value="<?php echo $wled_delay; ?>">
                        <!-- Slider to speficy delay. Between 0 and 80 seconds -->
                        <div class="mb-3">
                            <label for="wled_delay" class="form-label"><strong>Delay</strong> (F1TV typically have a 45-60 sec. delay)</label>
                            <input type="range" class="form-range" value="<?php echo $wled_delay; ?>" min="0" max="80" id="delay" name="wled_delay" id="wled_delay" oninput="this.nextElementSibling.value = this.value"><output><?php echo $wled_delay; ?></output> seconds
                        </div>
                        <!-- Text boxes for environment variables -->
                        <div class="mb-3">
                            <label for="wled_host" class="form-label"><strong>WLED Host</strong> (ip or dns)</label>
                            <input type="text" class="form-control" id="wled_host" name="wled_host" value="<?php echo $wled_host; ?>" required>
                        </div>
                        <div class="mb-3">
                            <label for="wled_yellow" class="form-label"><strong>WLED Yellow Flag Preset</strong> (number)</label>
                            <input type="text" class="form-control" id="wled_yellow" name="wled_yellow" value="<?php echo $wled_yellow; ?>" required>
                        </div>
                        <div class="mb-3">
                            <label for="wled_red" class="form-label"><strong>WLED Red Flag Preset</strong> (number)</label>
                            <input type="text" class="form-control" id="wled_red" name="wled_red" value="<?php echo $wled_red; ?>" required>
                        </div>
                        <div class="mb-3">
                            <label for="wled_green" class="form-label"><strong>WLED Green Flag Preset</strong> (number)</label>
                            <input type="text" class="form-control" id="wled_green" name="wled_green" value="<?php echo $wled_green; ?>" required>
                        </div>
                        <div class="mb-3">
                            <label for="wled_sc" class="form-label"><strong>WLED Safety Car Preset</strong> (number)</label>
                            <input type="text" class="form-control" id="wled_sc" name="wled_sc" value="<?php echo $wled_sc; ?>" required>
                        </div>
                        <div class="mb-3">
                            <label for="wled_checkered" class="form-label"><strong>WLED Checkered Flag Preset</strong> (number)</label>
                            <input type="text" class="form-control" id="wled_checkered" name="wled_checkered" value="<?php echo $wled_checkered; ?>" required>
                        </div>
                        <div class="mb-3">
                            <label for="wled_trackclear" class="form-label"><strong>WLED Track Clear Flag Preset</strong> (number)</label>
                            <input type="text" class="form-control" id="wled_trackclear" name="wled_trackclear" value="<?php echo $wled_clear; ?>" required>
                        </div>

                        <button type="submit" class="btn btn-primary">Save Config</button> <a class="btn btn-default mybtn" href="rolex.php">Rolex</a>
                    </form>
                </div><!-- card-body -->
            </div><!-- collapse -->
        </section>
        <section>
            <p><strong>Output: </strong></p>
            <textarea id="content" class="form-control" rows="20" style="font-size: smaller;"></textarea>
        </section>
        <!--
        <section>
            <textarea id="output" rows="30" cols="200"></textarea>
        </section>
        -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script>
        $(document).ready(function(){
            setInterval(function(){
                $.get("check_process.php", function(data, status){
                    $("#status").html(data);
                });
            }, 2000); // check every 2 seconds
        });
        </script>
        <?php
            if(isset($_SESSION['process_started'])) {
        ?>
        <script>
            $(document).ready(function(){
                setInterval(function(){
                    $.get("get_content.php", function(data){
                        $("#content").html(data);
                        $("#content").scrollTop($("#content")[0].scrollHeight);
                    });
                }, 1000); // update every second
            });
        </script>
    <?php
                $_SESSION['process_started'] = NULL;
            }
    ?>

        </div>
    </div>
  </body>
</html>