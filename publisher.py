# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 14:42:40 2022

@author: Kellen Cheng
"""

import time
import numpy as np
import paho.mqtt.client as mqtt
# %% Publisher Code
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))

def on_disconnect(client, userdata, rc):
    if (rc != 0):
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

def on_message(client, userdata, message):
    print("Received message: " + str(message.payload) + " on topic " +
          message.topic + " with QoS " + str(message.qos))

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async("test.mosquitto.org")
client.loop_start()
print("Subscribing...")
client.subscribe("team5", qos=1)
time.sleep(2)
print("Publishing...")
client.publish("team5", "Yeehaw :D", qos=1)
time.sleep(4)

client.disconnect()
client.loop_stop()
