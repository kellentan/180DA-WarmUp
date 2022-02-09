# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 14:18:27 2022

@author: Kellen Cheng
"""

import time
import numpy as np
import paho.mqtt.client as mqtt
# %% Subscriber Code
def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    
    # client.subscribe("ece180d/test", qos=1)
    client.subscribe("team5", qos=1)
    
def on_disconnect(client, userdata, rc):
    if (rc != 0):
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

def on_message(client, userdata, message):
    print("Received message: " + str(message.payload) + " on topic " +
          message.topic + " with QoS " + str(message.qos))
    
    return message.payload

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async("test.mosquitto.org")
client.loop_start()
print("Subscribing...")
client.subscribe("team5", qos=1)
time.sleep(2)

count = 0
while True:
    count += 1
    if (count > 100000): break
    pass
client.loop_stop()
client.disconnect()

print("Here is our message: ", str(on_message))
    
    
    
    
    
    
    
    