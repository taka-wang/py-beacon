#
# by Taka Wang
#

import ConfigParser
import paho.mqtt.client as mqtt
from proximity import *

DEBUG = True

def onConnect(client, userdata, rc):
    """MQTT onConnect handler"""
    print("Connected to broker: " + str(rc))

def initMQTT(url = "localhost", port = 1883, keepalive = 60):
    """Init MQTT connection"""
    client = mqtt.Client()
    client.on_connect = onConnect
    try:
        client.connect(url, port, keepalive)
        client.loop_start()
        return client
    except Exception, e:
        print(e)
        return None

def startScan(mqttclnt, filter="", topic="/ble/rssi/"):
    """Scan BLE beacon and publish to MQTT broker"""
    if mqttclnt:
        scanner = Scanner()
        while True:
            for beacon in scanner.scan():
                fields = beacon.split(",")
                if fields[1].startswith(filter):
                    mqttclnt.publish(topic, '{"id":"%s","val":"%s"}' % (fields[0], fields[5]))
                    if DEBUG: print(fields[0], fields[5])

def init():
    """Read config file"""
    ret = {}
    config = ConfigParser.ConfigParser()
    config.read("config")
    global DEBUG
    DEBUG = True if int(config.get('Collector', 'debug')) == 1 else False
    ret["url"]       = config.get('MQTT', 'url')
    ret["port"]      = int(config.get('MQTT', 'port'))
    ret["keepalive"] = int(config.get('MQTT', 'keepalive'))
    ret["filter"]    = config.get('Scanner', 'filter')
    ret["topic_id"]  = config.get('Scanner', 'topic_id')
    return ret

if __name__ == '__main__':
    conf = init()
    clnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])
    startScan(clnt, conf["filter"], conf["topic_id"])
