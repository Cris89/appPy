'''
Created on Oct 26, 2016

@author: cris
'''

import os
import paho.mqtt.client as paho
import random

class Protocol():
    '''
    classdocs
    '''

    client = paho.Client(client_id="AppPy")
    counter = 0
    randomCheck = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def __init__(self):
        '''
        Constructor
        '''
    
    def on_connect(self, host):
        print("Client ID: " + self.client._client_id + " connected at " + host + ":8883")

    def connect(self, host):
        self.client.connect(host, port=8883)
        self.client.on_connect = self.on_connect(host)      

    def on_subscribe(self, topic):
        print("Subscribed to topic: " + topic)

    def on_message(self, client, userdata, msg):
        data = open("data.txt", "a")
        data.write(msg.payload)
        data.write("\n")
        data.close()
        print ("Received " + msg.payload + ": written on data.txt")
        self.counter += 1
        if self.counter == self.randomCheck:
            os.system("/home/cris/spark-2.0.1-bin-hadoop2.7/bin/spark-submit spark.py")
            count = open("count.txt", "r")
            count.seek(-2,2)
            while (count.read(1) != '\n'):
                    count.seek(-2, 1)
            self.publish("CountsAppPy", count.readline())
            count.close()
            self.counter = 0
            self.randomCheck = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])   
    
    def subscribe(self, topic):
        self.client.subscribe(topic)
        self.client.on_subscribe = self.on_subscribe(topic)
        self.client.on_message = self.on_message
    
    def on_publish(self, topic):
        print("\nNumber of strings so far published on " + topic + "\n")
        
    def publish(self, topic, string):
        self.client.on_publish = self.on_publish(topic)
        self.client.publish(topic, string, qos=1)
