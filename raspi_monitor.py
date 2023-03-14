
# [How to build a Raspberry Pi Kubernetes Cluster with k3s | by Alex Ortner | Thinkport Technology Blog | Medium](https://medium.com/thinkport/how-to-build-a-raspberry-pi-kubernetes-cluster-with-k3s-76224788576c)

import pyembedded
from pyembedded.raspberry_pi_tools.raspberrypi import PI
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import time
import json
import os

# get node name this script runs on
hostname = os.getenv('NODE_NAME', None)   # from kubernetes env
if not hostname:
    hostname = os.uname().nodename

config_file = 'config.secrets.json'

DEFAULT_MQTT_BROKER=b"mosquitto.mqtt.svc.cluster.local"
DEFAULT_MQTT_PORT=1883
DEFAULT_MQTT_KEEPALIVE=60
DEFAULT_MQTT_TOPIC_ROOT="raspi"
DEFAULT_READ_INTERVAL_SECONDS = 15

CONFIG = {}

try:
    with open(config_file, 'r') as jsonfile:
        CONFIG = json.loads(jsonfile.read())
        print (CONFIG)
except OSError as ose:
    if ose.errno not in (errno.ENOENT,):
        # this re-raises the same error object. 
        raise
    pass # ENOENT.

# subtrees of the config file
MQTT_CONF = CONFIG.get("mqtt", {})
GLOBAL_CONF = CONFIG.get("global", {})

MQTT_BROKER = bytes(MQTT_CONF.get('broker', DEFAULT_MQTT_BROKER), 'utf-8')
MQTT_PORT = MQTT_CONF.get('port', DEFAULT_MQTT_PORT)
MQTT_KEEPALIVE = MQTT_CONF.get('keepalive', DEFAULT_MQTT_KEEPALIVE)
MQTT_TOPIC_ROOT = MQTT_CONF.get('topic_root', DEFAULT_MQTT_TOPIC_ROOT)

read_interval = GLOBAL_CONF.get('read_interval_seconds', DEFAULT_READ_INTERVAL_SECONDS)

pi = PI()

def get_data():

  # get parameters via pymbedded
  ram_raw = pi.get_ram_info()
  disk_raw = pi.get_disk_space()
  cpu_raw = pi.get_cpu_usage()
  temperatur_raw=pi.get_cpu_temp()
  # create dicts/json objects
  temperature = {
      "name": "temperature",
      "value": temperatur_raw,
      "unit": "°C",
      "node": hostname
  }
  ram = {
      "name": "ram",
      "value": {
          "total": round(int(ram_raw[0])/1000000,1),
          "used": round(int(ram_raw[1])/1000000,1),
          "free": round(int(ram_raw[2])/1000000,1),
      },
      "unit": "GB",
      "node": hostname
  }
  disk = {
      "name": "disk",
      "value": {
          "total": disk_raw[0],
          "used": disk_raw[1],
          "free": disk_raw[2],
      },
      "unit": "GB",
      "node": hostname
  }
  cpu = {
      "name": "cpu",
      "value": cpu_raw,
      "unit": "Percent",
      "node": hostname
  }
  return temperature, ram, disk, cpu

mqttc = mqtt.Client("k3s-fixme")
mqttc.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
mqttc.loop_start()

while True:
    temperature, ram, disk, cpu = get_data()
    print(temperature, ram, disk, cpu)
    mqttc.publish("test","Hello from " + hostname)
    mqttc.publish(MQTT_TOPIC_ROOT+"/"+hostname+"/temperature",str(temperature))
    mqttc.publish(MQTT_TOPIC_ROOT+"/"+hostname+"/"+"ram",json.dumps(ram))
    mqttc.publish(MQTT_TOPIC_ROOT+"/"+hostname+"/"+"disk",json.dumps(disk))
    mqttc.publish(MQTT_TOPIC_ROOT+"/"+hostname+"/"+"cpu",json.dumps(cpu))
    time.sleep(read_interval) 
