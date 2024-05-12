# F1-WLED

## Requirements
- WLED lamp/panel/something with API and presets for Green, yellow, red flag + safetycar.

## Build
```
sudo docker build -t f1-wled .
```

## Environment Variables
- YELLOW (integer)
- RED (integer)
- GREEN (integer)
- SC (integer)

## Run
```
sudo docker run -it f1-wled bash
```

## TO-DO
- Run deploy.py in dockerfile
- Add environment variables with default values.
- Decode data from livetiming signalr?
- Write function in clientmod.py that calls the WLED API instead of writing to a file.
- wrapper script should be automatically ran when container starts.
