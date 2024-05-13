# F1-WLED

## THIS THING IS NOT YET WORKING

## Requirements
- WLED lamp/panel/something with API and presets for Green, yellow, red, chequered flag + safetycar.

## Build
```
sudo docker build -t f1-wled .
```

## Environment Variables
- WLED_SERVER (String)
- YELLOW (integer)
- RED (integer)
- GREEN (integer)
- SC (integer)
- CHEQUERED (integer)

## Run
```
sudo docker run -it f1-wled bash
```

## TO-DO
- Script should look for "TRACK CLEAR" message to turn off SC light.
- Write function in clientmod.py that calls the WLED API instead of writing to a file.
- wrapper script should be automatically ran when container starts.
