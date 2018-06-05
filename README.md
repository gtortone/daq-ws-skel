
## DAQ with websockets
A simple application developed with Flask-SocketIO for DAQ run control and acquisition

### Requirements
* Prepare a virtual environment for Python3
```
virtualenv -p python3 venv
```
* Activate virtual environment
```
source venv/bin/activate
```
* Install packages
```
pip install -r requirements.txt
```

### Usage
```
gunicorn daq-ws:app -b 0.0.0.0 --threads 16
```


