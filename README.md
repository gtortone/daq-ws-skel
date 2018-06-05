
## DAQ with websockets
A simple application developed with Flask-SocketIO for DAQ run control and acquisition

### Usage
```
gunicorn daq-ws:app -b 0.0.0.0 --threads 16
```


