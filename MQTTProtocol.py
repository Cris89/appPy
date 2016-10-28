'''
Created on Oct 26, 2016

@author: cris
'''

import paho.mqtt.client as paho

class Protocol():
    '''
    classdocs
    '''

    client = paho.Client(client_id="AppPy")

    def __init__(self):
        '''
        Constructor
        '''
    
    def on_connect(self, host):
        print("Client ID: " + self.client._client_id + " connected at " + host + ":8883")

    def connect(self, host):
        self.client.on_connect = self.on_connect(host)
        self.client.connect(host, port=8883)      

    def on_subscribe(self, topic):
        print("Subscribed to topic: " + topic)

    def on_message(self, client, userdata, msg):
        learner = open("Learner.txt", "a")
        learner.write(msg.payload)
        learner.write("\n")
        learner.close()
        print ("Received " + msg.payload + ": written on Learner.txt")
    
    def subscribe(self, topic):
        self.client.on_subscribe = self.on_subscribe(topic)
        self.client.on_message = self.on_message
        self.client.subscribe(topic)
    
    def on_publish(self, client, userdata, mid):
        print("mid: " + str(mid))
        
    def publish(self, topic, string):
        self.client.on_publish = self.on_publish
        (rc, mid) = self.client.publish(topic, string, qos=1)
