# F1-WLED

## DISCLAIMER
```
- This is just a personal little project, do not expect it to work
```

## Requirements
- WLED lamp/panel/something with API and presets for Green, yellow, red, chequered flag + safetycar.

## Build
```
sudo docker build -t f1-wled .
```

## Environment Variables
- WLED_HOST (String)
- WLED_YELLOW (integer)
- WLED_RED (integer)
- WLED_GREEN (integer)
- WLED_SC (integer)
- WLED_CHEQUERED (integer)
- WLED_TRACKCLEAR (integer)

## Run
```
sudo docker run -it -e WLED_GREEN=4 -e WLED_TRACKCLEAR=7 -e WLED_RED=3 -e WLED_YELLOW=2 -e WLED_SC=5 -e WLED_CHEQUERED=6 -e WLED_HOST="192.168.1.144" f1-wled /app/f1wled.py
```

## TO-DO
- wrapper script should be automatically ran when container starts.
