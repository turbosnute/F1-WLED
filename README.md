# F1-WLED

## DISCLAIMER
```diff
- This is just a personal little project, do not expect it to work
```

## Requirements
- WLED lamp/panel/something with API and presets for Green, yellow, red, chequered flag + safetycar.

## Build
```
sudo docker build -t f1-wled .
```

## Run
```
sudo docker run -it -v "$PWD/src/web":/var/www/html/ -v f1wled:/config/  -p 8800:80 f1-wled bash
```

- Then run "apache2-foreground"
- navigate to "http:<dockerhost>:8800" with a browser to set the config
- ctrl+c to kill apache in side the container
- run "./f1wled" from bash inside the container

## Configure
...

## TO-DO
- Apache should always run in background.
- How should the script start? And should it automatically be reloaded when new config is saved?
