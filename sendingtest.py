import paho.mqtt.client as mqtt #import the client1
import json
broker_address="192.168.178.15" 
client = mqtt.Client("P2") #create new instance
client.connect(broker_address) #connect to broker

dictionary = ["Module1", "D"]
temp1 = json.dumps(dictionary)
client.publish("main_channel",temp1)#publish