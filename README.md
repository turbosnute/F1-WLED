# F1-WLED

## DISCLAIMER
```diff
- This is just a personal little project, do not expect it to work
```

## Requirements
- WLED lamp/panel/something with API and presets for Green, red, chequered flag + safetycar.

## Build
```
cd f1-wled/
sudo docker build -t f1-wled .
```

## Run
```
sudo docker run -it -v "$PWD/src/web":/var/www/html/ -v f1wled:/config/ -p 8800:80 f1-wled
```

- navigate to `http://dockerhost:8800` with a browser to set and save the config. Then start F1-wled from the same web interface. 

## To-Do
- Implement yellow flags?