#TODO:
# Make a better wire_process.py
# Implement in timer_process.py that the function will send the message to start blinken from anywhere without repeating and taking to long
#

import paho.mqtt.client as mqtt #import the client1
from time import sleep
import json
########################################

amount_mistakes = 0
active_Modules = 0
status = "Sleeping"
time_up = 0

def on_message(client, userdata, message):
    global amount_mistakes, active_Modules, status, time_up
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print(type(message))
    new_message = json.loads(str(message.payload.decode("utf-8")))
    print(type(new_message))
    print(new_message)
    print(new_message[1])
    if new_message[1] == "R": #Register
        active_Modules += 1
        if status == "Sleeping":
            status = "Active"
    elif new_message[1] == "D": #Done
        active_Modules -= 1
    elif new_message[1] == "T": #Time up
        time_up = 1
    elif new_message[1] == "F": #Fault +1
        amount_mistakes += 1
    
    
########################################
def main_process():
    global amount_mistakes, active_Modules, status, time_up
    broker_address="192.168.178.15"
    print("creating new instance")
    client = mqtt.Client("P1") #create new instance
    client.on_message=on_message #attach function to callback
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    client.loop_start() #start the loop
    print("Subscribing to topic","main_channel")
    client.subscribe("main_channel")
    while True:
        sleep(0.5)
        print("amount_mistakes={}".format(amount_mistakes))
        print("active_module={}".format(active_Modules))
        print("status={}".format(status))
        print("time_up={}".format(time_up))
        print("")
        print("")
        print("")
        if status == "Active" and active_Modules < 1:
            while True:
                print("CLEARED")
                print("CLEARED")
                print("CLEARED")
                sleep(0.1)
                print("amount_mistakes={}".format(amount_mistakes))
                print("active_module={}".format(active_Modules))
                print("status={}".format(status))
                print("time_up={}".format(time_up))
                print("")
                print("")
                print("")
                sleep(0.5)
        pass
        if amount_mistakes > 2 or time_up == 1:
            while True:
                print("BOOM!")
                print("BOOM!")
                print("BOOM!")
                sleep(0.1)
                print("amount_mistakes={}".format(amount_mistakes))
                print("active_module={}".format(active_Modules))
                print("status={}".format(status))
                print("time_up={}".format(time_up))
                print("")
                print("")
                print("")
                sleep(0.5)
    client.loop_stop() #stop the loop