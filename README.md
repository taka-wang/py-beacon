# py-beacon

BLE beacon scanner in python.

## Message Flow

![alt text](https://github.com/taka-wang/py-beacon/blob/34705ac28654d8b2f5a9edf296ea152fa04c183f/flow.png "Flow Chart")

## Scripts

#### Modules

- blescan.py   => bluez libs
- proximity.py => main module

#### Executable

- collector.py => scan beacon and publish via mqtt 
- emitter.py   => calculate nearest beacon and publish via mqtt

#### Test Scripts

- test.py => main module test
- test_parser.py => ConfigParser test

## Test

```bash
mosquitto -c /etc/mosquitto/mosquitto.conf -d # start broker

sudo python test.py
sudo python collector.py # scan BLE 
python emitter.py # calculate nearest beacon
```

## Installation

```bash
sudo apt-get install bluez python-bluez python-numpy
sudo pip install -r requirements.txt
```

## Miscs

- [Setup Environment on BBB](https://gist.github.com/taka-wang/29433180cc8affcde3b2)
- [Install mosquitto 1.4 on raspberry pi](https://gist.github.com/taka-wang/1c47cde3e4c9c2d83156)

## MIT License

blescan.py source from [here](https://github.com/switchdoclabs/iBeacon-Scanner-.git)
