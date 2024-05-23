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
sudo docker run -it -v f1wled:/config -p 8800:80 f1-wled /app/f1wled.py

```

## Configure
...

## TO-DO
- wrapper script should be automatically ran when container starts.
- Document how to do config.
- f1wled should run as www-data so it can access the environment variables set by php
